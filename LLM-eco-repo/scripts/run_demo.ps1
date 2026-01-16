# PowerShell script to run the demo pipeline (bilingual prompt)
# 运行演示脚本前请确认已安装 requirements.txt 中的依赖

$ErrorActionPreference = "Stop"

Write-Host "[INFO] Running demo pipeline... / 正在运行演示流程..." -ForegroundColor Cyan
python "$PSScriptRoot\demo_pipeline.py"

Write-Host "[INFO] Done. / 完成。" -ForegroundColor Green
