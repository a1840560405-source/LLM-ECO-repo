# 从工具到范式：大语言模型与计量经济学的融合演进

作者：钟廷杰  |  仓库：https://github.com/a1840560405-source/LLM-ECO-repo

这不是“论文仓库”，更像一个可复用的项目骨架：把白皮书、样例数据和一套能跑通的 demo 放在一起，方便你把想法落到可复现的流程里（也便于后续交付/协作）。

主要内容：

- `whitepaper/` — 白皮书与执行摘要
- `data/sample/` — 合成示例数据（用于 demo 与可复现测试）
- `scripts/` — 可脚本化运行的 demo pipeline
- `notebooks/` — 演示用 Notebook
- `CONTRIBUTING.md`、`CITATION.md`、`metadata.json`、`LICENSE` — 协作与引用说明
- `.github/workflows/` — CI 示例（Markdown → PDF；Python demo + tests）

你可以从两份短文开始：

- `docs/case-study-1pager.md` — 1 页案例：这个 demo 到底在跑什么、为什么这么设计
- `docs/faq.md` — 常见疑问：中文文本、时间泄漏、EV 校正、DID 可信度等

这个仓库主要想展示两件事：

1) 如何把“文本信号 → 指标 → 回归/评估”串成一个最小可复现闭环；
2) 在 demo 级别也尽量把常见坑提前处理掉（中文 tokenization、泄漏、校正不稳定等）。

环境建议

- 推荐 Python 3.11（有官方预编译轮子，免编译）。如果本机是 3.14 且没有编译链，请先安装 3.11 再创建虚拟环境。
- 依赖见 `requirements.txt`，请使用 `python -m pip` 安装。

快速开始

1. 先看执行摘要 `whitepaper/executive_summary.md`，评估方法论是否匹配你的研究/咨询问题；
2. 用合成数据快速跑一遍 demo（见 `data/sample/`），确认变量构建与量化流程；
3. 若满意，可替换为真实数据并沿用同样的流程做可重复性验证。

本地生成 PDF（需 Pandoc 与 LaTeX）：

```powershell
cd d:\LLM-eco-repo
pandoc whitepaper/paper.md -o whitepaper/paper.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

本地运行 demo 与测试（推荐 Python 3.11）：

```powershell
cd d:\LLM-eco-repo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts\demo_pipeline.py
python -m unittest discover -s tests -p "test_*.py" -v
```

许可与引用

本项目采用 MIT 许可（见 `LICENSE`）。引用请参考 `CITATION.md`，并在使用真实数据时注明数据来源与许可。

交流与合作

欢迎在 Issues 里提问或讨论（最好顺手说明：你手头的数据范围/许可、期望的评估口径、以及最终交付形式）。如果你希望把它做成“能交付”的版本，也可以在此基础上继续扩展：更稳健的评估、更多审计与质量检查、以及面向生产的运行方式。