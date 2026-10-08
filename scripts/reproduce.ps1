$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
& .venv/Scripts/python.exe -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
& .venv/Scripts/python.exe -m bayes_digits.experiment --config configs/default.json
if ($LASTEXITCODE -ne 0) { throw "Experiment failed" }
& .venv/Scripts/python.exe -m bayes_digits.figures --results results
if ($LASTEXITCODE -ne 0) { throw "Figures failed" }
& .venv/Scripts/python.exe scripts/build_report.py
if ($LASTEXITCODE -ne 0) { throw "Report assets failed" }

