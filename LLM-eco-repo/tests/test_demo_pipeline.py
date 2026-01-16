"""
Basic smoke tests for demo_pipeline functions using synthetic data.
中英双语注释，验证核心流程不抛异常且返回关键字段。
"""
import unittest
from pathlib import Path
import pandas as pd

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'scripts'))
import demo_pipeline as dp  # noqa: E402


class DemoPipelineTest(unittest.TestCase):
    def setUp(self):
        self.policy_df, self.fin_df = dp.load_data()

    def test_rag_like_match(self):
        matched, tfidf, p_tfidf, r_tfidf = dp.rag_like_match(self.policy_df, self.fin_df)
        self.assertFalse(matched.empty)
        self.assertIn('policy_sim', matched.columns)
        # Check all reports matched to a policy
        self.assertEqual(len(matched), len(self.fin_df))

    def test_ev_and_did(self):
        matched, tfidf, p_tfidf, r_tfidf = dp.rag_like_match(self.policy_df, self.fin_df)
        policy_df, matched, svd = dp.build_features(self.policy_df, matched, tfidf, p_tfidf, r_tfidf)
        matched = dp.simulate_proxy(matched)
        matched, model, attenuation, manual_idx = dp.ev_correction(matched, sample_frac=0.5)
        self.assertGreater(len(manual_idx), 0)
        self.assertIn('proxy_corrected', matched.columns)
        self.assertIn('ev_warning', matched.columns)
        res, merged = dp.did_regression(matched)
        self.assertIn('treated_post', merged.columns)
        self.assertIn('proxy_corrected', merged.columns)
        # statsmodels result sanity
        self.assertTrue(hasattr(res, 'params'))


if __name__ == '__main__':
    unittest.main()
