# Reproduction

[Home](Home.md) · [Method](Algorithm-and-Mathematics.md) · [Results](Results-and-Visualization.md)

Python 3.12; install pinned requirements. GPU optional; actual run used CPU.

~~~powershell
git clone https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition.git
Set-Location bayesian-handwritten-digit-recognition
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

The review diagnostic adds 72 fixed-model sampling repetitions, with settings and raw probabilities preserved in results/review_diagnostics/. Run it before figures to reproduce the Monte Carlo diagnostic figure and generated diagnostic text. The review audit compares primary arrays against the original Git commit a28a563 and checks all diagnostic metrics. It requires that commit in local history; a shallow clone must fetch it first. Final presentation invariance is checked with `python scripts/audit_refinement.py` against Prompt 02 commit `93b625e`; that commit is also required. The original environment hashes describe the executed experiment; current plotting hashes are verified separately in figure_manifest.json.

Preserved evidence: config, dataset hash, splits, histories, prior scores, selection lock, metrics, predictions, summary, environment, audit and figure manifest. The public clone URL above was verified in Prompt 03; clone the complete history for the historical evidence audits.
