# 简单数据预览脚本
# 用途：快速检查合成样本的字段、行数与基本分布（跑 demo 前先看一眼更稳）。

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'data' / 'sample' / 'policy_texts.csv'
FIN = ROOT / 'data' / 'sample' / 'financial_reports.csv'


def preview_policy(n=5):
    df = pd.read_csv(POLICY, parse_dates=['date'])
    print('\n== 政策文本样本（前 {} 条） =='.format(n))
    print(df.head(n)[['id', 'date', 'source', 'title']].to_string(index=False))
    # 简单统计
    print('\n政策文本总量：', len(df))
    print('按来源计数：')
    print(df['source'].value_counts().to_string())


def preview_financial(n=5):
    df = pd.read_csv(FIN)
    print('\n== 财报样本（前 {} 条） =='.format(n))
    print(df.head(n)[['id', 'firm_id', 'year', 'revenue', 'profit']].to_string(index=False))
    print('\n财报记录总量：', len(df))
    print('年份分布：')
    print(df['year'].value_counts().sort_index().to_string())


if __name__ == '__main__':
    # 先查看样本，再按需要扩展或替换为真实数据
    preview_policy(6)
    preview_financial(6)
    print('\n提示：如果你换成真实数据，注意同步更新字段名与时间口径。')
