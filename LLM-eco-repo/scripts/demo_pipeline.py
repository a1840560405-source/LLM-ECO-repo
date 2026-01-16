"""Demo pipeline for the synthetic samples in data/sample/.

Notes:
    - Kept intentionally small so it can run in CI and be easy to modify.
    - The text side uses a TF-IDF baseline (no external tokenizers).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data" / "sample" / "policy_texts.csv"
FIN_PATH = ROOT / "data" / "sample" / "financial_reports.csv"

positive_keywords = ['支持','鼓励','补贴','稳定','促进','优惠']
negative_keywords = ['收紧','惩罚','制裁','监管加强','减少','取消']

rng = np.random.RandomState(20260116)


def _mixed_zh_tokenizer(text: str):
    """Tokenize Chinese/English text for TF-IDF without extra dependencies.

    We mix:
      - char-level tokens (works for Chinese, where there are no spaces)
      - whitespace tokens (works for English, numbers, IDs)
    """
    if text is None:
        return []
    s = str(text).strip().lower()
    if not s:
        return []
    # Char tokens help Chinese; whitespace tokens help English/IDs.
    chars = [ch for ch in s if not ch.isspace()]
    words = s.split()
    return chars + words


def sentiment_score(text: str) -> float:
    """Simple keyword sentiment in [-1, 1]."""
    txt = (text or '').lower()
    pos = sum(txt.count(k) for k in positive_keywords)
    neg = sum(txt.count(k) for k in negative_keywords)
    if pos + neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)


def load_data():
    policy_df = pd.read_csv(POLICY_PATH, parse_dates=['date'])
    fin_df = pd.read_csv(FIN_PATH)
    return policy_df, fin_df


def rag_like_match(policy_df: pd.DataFrame, fin_df: pd.DataFrame):
    # TF-IDF baseline with a tokenizer that doesn't fall over on Chinese text.
    tfidf = TfidfVectorizer(
        tokenizer=_mixed_zh_tokenizer,
        token_pattern=None,
        lowercase=True,
        min_df=1,
        max_df=0.9,
        ngram_range=(1, 2),
    )
    policy_tfidf = tfidf.fit_transform(policy_df['text'].fillna(''))
    report_tfidf = tfidf.transform(fin_df['report_excerpt'].fillna(''))
    sims = cosine_similarity(report_tfidf, policy_tfidf)
    best_idx = sims.argmax(axis=1)
    best_scores = sims.max(axis=1)
    matched = policy_df.iloc[best_idx].reset_index(drop=True)
    matched = matched[['id','date','source','title','text']].rename(columns={
        'id':'policy_id','date':'policy_date','source':'policy_source','title':'policy_title','text':'policy_text'
    })
    fin_matched = pd.concat([fin_df.reset_index(drop=True), matched], axis=1)
    fin_matched['policy_sim'] = best_scores
    return fin_matched, tfidf, policy_tfidf, report_tfidf


def build_features(policy_df, fin_matched, tfidf, policy_tfidf, report_tfidf):
    # Sentiment
    policy_df = policy_df.copy()
    fin_matched = fin_matched.copy()
    policy_df['policy_sentiment'] = policy_df['text'].apply(sentiment_score)
    fin_matched['report_sentiment'] = fin_matched['report_excerpt'].apply(sentiment_score)

    # SVD semantic features (adaptive to small feature sizes)
    n_samples, n_features = policy_tfidf.shape
    # TruncatedSVD requires 1 <= n_components < n_features.
    max_components = max(1, min(5, n_features - 1))
    if n_features <= 1:
        # Degenerate case: no usable TF-IDF features
        policy_df['policy_svd0'] = 0.0
        fin_matched['report_svd0'] = 0.0
        svd = None
    else:
        svd = TruncatedSVD(n_components=max_components, random_state=0)
        policy_svd = svd.fit_transform(policy_tfidf)
        report_svd = svd.transform(report_tfidf)
        policy_df['policy_svd0'] = policy_svd[:, 0]
        fin_matched['report_svd0'] = report_svd[:, 0]

    return policy_df, fin_matched, svd


def simulate_proxy(fin_matched):
    fin_matched = fin_matched.copy()
    fin_matched['latent_true'] = (
        0.5 * fin_matched['report_sentiment'].fillna(0) +
        0.4 * fin_matched['report_svd0'].fillna(0) +
        0.1 * fin_matched['policy_sim'].fillna(0)
    )
    fin_matched['proxy_raw'] = fin_matched['latent_true'] + rng.normal(loc=0, scale=0.3, size=len(fin_matched))
    return fin_matched


def ev_correction(fin_matched, sample_frac=0.2):
    fin_matched = fin_matched.copy()
    manual_idx = rng.choice(fin_matched.index, size=max(1, int(len(fin_matched) * sample_frac)), replace=False)
    fin_matched.loc[manual_idx, 'manual_label'] = fin_matched.loc[manual_idx, 'latent_true'] + rng.normal(loc=0, scale=0.05, size=len(manual_idx))
    y = fin_matched.loc[manual_idx, 'manual_label']
    x = fin_matched.loc[manual_idx, 'proxy_raw']
    x_ = sm.add_constant(x)
    model = sm.OLS(y, x_).fit()
    attenuation = model.params['proxy_raw'] if 'proxy_raw' in model.params.index else model.params[1]
    attenuation = float(attenuation)

    # Safety: avoid exploding corrections when attenuation is ~0.
    min_abs_att = 0.10
    if (not np.isfinite(attenuation)) or (abs(attenuation) < min_abs_att):
        fin_matched['proxy_corrected'] = fin_matched['proxy_raw']
        fin_matched['ev_warning'] = f"attenuation_unstable:{attenuation}"
        attenuation_used = np.nan
    else:
        fin_matched['proxy_corrected'] = fin_matched['proxy_raw'] / attenuation
        fin_matched['ev_warning'] = ""
        attenuation_used = attenuation
    return fin_matched, model, attenuation_used, manual_idx


def did_regression(fin_matched):
    merged = fin_matched.copy()
    # Define treated using pre-2020 revenue mean to avoid look-ahead.
    pre = merged[merged['year'] < 2020]
    firm_mean_pre = pre.groupby('firm_id')['revenue'].mean()
    median_pre = firm_mean_pre.median()
    merged['treated'] = merged['firm_id'].map(lambda x: 1 if firm_mean_pre.get(x, 0) > median_pre else 0)
    merged['post'] = (merged['year'].astype(int) >= 2020).astype(int)
    merged['treated_post'] = merged['treated'] * merged['post']
    formula = 'profit ~ treated_post + proxy_corrected + C(firm_id) + C(year)'
    res = smf.ols(formula, data=merged).fit(cov_type='cluster', cov_kwds={'groups': merged['firm_id']})
    return res, merged


def run_demo():
    policy_df, fin_df = load_data()
    fin_matched, tfidf, policy_tfidf, report_tfidf = rag_like_match(policy_df, fin_df)
    policy_df, fin_matched, svd = build_features(policy_df, fin_matched, tfidf, policy_tfidf, report_tfidf)
    fin_matched = simulate_proxy(fin_matched)
    fin_matched, model, attenuation, manual_idx = ev_correction(fin_matched)
    res, merged = did_regression(fin_matched)

    print('\n=== Results ===')
    print('manual sample size:', len(manual_idx))
    print('attenuation used:', attenuation)
    print('DID coef (treated_post):', res.params.get('treated_post', 'NA'))
    print('\nDID table:')
    print(res.summary().tables[1])

    return {
        'fin_matched': fin_matched,
        'attenuation': attenuation,
        'did_result': res,
    }


if __name__ == "__main__":
    run_demo()
