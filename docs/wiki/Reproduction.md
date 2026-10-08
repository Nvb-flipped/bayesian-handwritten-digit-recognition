# Reproduction

[Home](Home.md) · [Method](Method-and-Mathematics.md) · [Results](Experiments-and-Results.md)

Python 3.12; install pinned requirements. GPU optional; actual run used CPU.

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m bayes_digits.experiment --config configs/default.json
.\.venv\Scripts\python.exe -m bayes_digits.figures --results results
.\.venv\Scripts\python.exe scripts/build_report.py
.\.venv\Scripts\python.exe scripts/audit_results.py
~~~

The existing local venv reuses Assignment 1 dependencies read-only. Fresh requirements installation is independent of that optimization. Compile with Tectonic from report/:

~~~powershell
tectonic -X compile --untrusted main.tex
~~~

The first build may download its TeX bundle. Figures/tables must exist. Seven tests check math/data/models. The audit regenerates metrics, reloads models and reruns the full study; all 18 arrays matched exactly in the recorded environment. Source hashes identify the original modules. Bitwise cross-platform portability is not promised.

Preserved evidence: config, dataset hash, splits, histories, prior scores, selection lock, metrics, predictions, summary, environment, audit and figure manifest. Public clone URL will be verified during Prompt 03.

