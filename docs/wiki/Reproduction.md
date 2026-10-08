# Reproduction

[Home](Home.md) · [Method](Method-and-Mathematics.md) · [Results](Experiments-and-Results.md)

Python 3.12; install pinned requirements. GPU optional; actual run used CPU.

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m bayes_digits.experiment --config configs/default.json
.\.venv\Scripts\python.exe scripts/review_diagnostics.py
.\.venv\Scripts\python.exe -m bayes_digits.figures --results results
.\.venv\Scripts\python.exe scripts/build_report.py
.\.venv\Scripts\python.exe scripts/audit_results.py
.\.venv\Scripts\python.exe scripts/audit_review.py
~~~

The existing local venv reuses Assignment 1 dependencies read-only. Fresh requirements installation is independent of that optimization. Compile with Tectonic from report/:

~~~powershell
tectonic -X compile --untrusted main.tex
~~~

The first build may download its TeX bundle. Figures/tables must exist. Nine tests check math/data/models. The audit regenerates metrics, reloads models and reruns the full study; all 18 arrays matched exactly in the recorded environment. Source hashes identify the executed modules. Bitwise cross-platform portability is not promised.

The review diagnostic adds 72 fixed-model sampling repetitions, with settings and raw probabilities preserved in results/review_diagnostics/. Run it before figures to reproduce the ninth figure and generated diagnostic text. The review audit compares primary arrays against the original Git commit a28a563 and checks all diagnostic metrics. It requires that commit in local history; a shallow clone must fetch it first.

Preserved evidence: config, dataset hash, splits, histories, prior scores, selection lock, metrics, predictions, summary, environment, audit and figure manifest. Public clone URL will be verified during Prompt 03.
