# Build PDF from whitepaper using pandoc (PowerShell)
# 生成 PDF 前请确保安装了 pandoc 和 LaTeX（或合适的 PDF 引擎）

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "[INFO] Building PDF from whitepaper/paper.md ..." -ForegroundColor Cyan
pandoc "whitepaper/paper.md" -o "whitepaper/paper.pdf" --pdf-engine=xelatex -V geometry:margin=1in
Write-Host "[INFO] PDF generated at whitepaper/paper.pdf" -ForegroundColor Green
