# 咨询提案一页纸（Proposal One‑Pager）

**客户 / Client**：〈客户名称〉  
**项目 / Project**：AI + 文本信号 → 指标构建与政策/经营影响评估  
**日期 / Date**：2026-01-16  
**联系人 / Contact**：钟廷杰  

---

## 1. 背景与目标（Context & objectives）

**中文**：
- 背景：〈一句话描述当前业务/研究痛点〉
- 目标：把〈文本来源：政策/公告/研报/财报〉变成可量化指标，并回答〈影响什么结果〉。

**English**:
- Context: 〈one sentence on current pain point〉
- Objective: convert 〈policy / filings / reports〉 into measurable signals and evaluate impact on 〈outcomes〉.

---

## 2. 方案概览（Approach at a glance）

1) 文本对齐：检索/匹配政策—主体—时间（避免错配）
2) 指标构建：关键词 + 语义特征 + 质量控制（漂移监测）
3) 偏误与校正：代理变量偏误（EV）、look‑ahead leakage、口径漂移
4) 评估：DID/事件研究/稳健性检验 + 可解释汇报
5) 工程交付：脚本化流水线 + 测试 + CI + 运行手册

---

## 3. 范围与交付物（Scope & deliverables）

**核心交付物**（可勾选）：
- [ ] 数据与口径文档（Data dictionary + definitions）
- [ ] 可复现 PoC（Notebook + pipeline 脚本）
- [ ] 指标解释卡（feature cards）
- [ ] 因果评估报告（含稳健性）
- [ ] 工程化流水线 + CI + 测试
- [ ] 培训与交接（workshop + Q&A）

**范围外**（默认不含）：线上系统开发/前端可视化、大规模分布式训练、客户侧数据采购。

---

## 4. 计划与里程碑（Timeline & milestones）

- M1（第 1–2 周）：诊断与口径对齐 → 需求冻结（baseline）
- M2（第 3–6 周）：PoC 闭环 → 初版结果与复现
- M3（第 6–12 周）：工程化交付 → 上线支持与交接（可选）

---

## 5. 验收标准（Acceptance criteria）

- 可复现：固定环境一键运行得到一致结果
- 可解释：核心指标有定义、直觉、失败模式
- 可审计：数据处理链路、参数、版本可追溯
- 稳健性：关键结论对口径/样本扰动不敏感（或敏感性清楚标注）

---

## 6. 费用（Pricing）

- 快速诊断：¥3–10 万
- PoC：¥12–40 万
- 交付与运维：¥30–120 万

> 说明：最终报价以数据可得性、合规要求与交付深度为准。
