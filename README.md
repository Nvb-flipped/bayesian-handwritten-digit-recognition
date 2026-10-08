# Bayesian handwritten digit recognition

CISC3024 — Pattern Recognition, AI Assignment #2  
Paco, Sou Chak Tong

An independently implemented **last-layer Laplace classifier**, motivated by [Laplace Redux (NeurIPS 2021)](https://papers.nips.cc/paper/2021/hash/a7c9585703d275249f30a088cebba0ad-Abstract.html). A Gaussian weight prior, exact conditional softmax Hessian and posterior predictive averaging make Bayesian inference substantive. This is a small educational adaptation, not the paper's benchmark reproduction.

## Measured results

The 1,797-image scikit-learn digits subset is split into **1,077 train / 360 validation / 360 test** images, stratified with split seed 3024. Neural initialization seeds: 11, 22, 33. Selection uses validation NLL.

| Method | Accuracy (%) | Macro-F1 | NLL (nats) | Brier |
|---|---:|---:|---:|---:|
| Gaussian naïve Bayes | 91.94 | 0.920 | 0.630 | 0.134 |
| MAP | 97.78 ± 0.28 | 0.978 ± 0.003 | 0.099 ± 0.003 | 0.040 ± 0.002 |
| Full Laplace | 97.69 ± 0.16 | 0.977 ± 0.002 | 0.151 ± 0.003 | 0.055 ± 0.001 |

Variation is sample SD across three initialization seeds on **the same** 360 test images. NB is deterministic and evaluated once. Brier sums over classes. Laplace retains strong recognition accuracy but has worse probability quality than MAP. [Detailed results and ablations](docs/wiki/Experiments-and-Results.md).

[Compiled report](report/main.pdf). Its only intentionally incomplete section is **STUDENT REFLECTION REQUIRED**. Public repository/wiki publication is deliberately deferred to Prompt 03; no Assignment 2 public URL exists yet.

## Reproduce

Python 3.12 was used. Create an independent environment:

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

The executed local venv reuses existing Assignment 1 PyTorch/scientific packages **read-only** through a path file; missing scikit-learn dependencies were installed into Assignment 2. The standalone setup above does not require Assignment 1. GPU is optional; the recorded run uses CPU and four PyTorch threads.

Small pipeline check:

~~~powershell
.\.venv\Scripts\python.exe -m bayes_digits.experiment --config configs/smoke.json
~~~

The smoke run selects its own model before its test stage. Smoke and full configurations were written before either run; smoke test outcomes were not used to change the full configuration. [scripts/reproduce.ps1](scripts/reproduce.ps1) runs tests, experiment, figures and quantitative tables.

## Compile

With Tectonic installed, run:

~~~powershell
Push-Location report
tectonic -X compile --untrusted main.tex
Pop-Location
~~~

Exact local Codex command (project root):

~~~powershell
& "C:/Users/csmen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" "C:/Users/csmen/.codex/plugins/cache/openai-bundled/latex/0.2.8/scripts/compile_latex.py" report/main.tex --compiler tectonic --json
~~~

First use may download the public TeX bundle. Compilation uses no shell escape. Generate quantitative tables after changing results. The PDF embeds vector figures from results/figures/.

## Evidence

~~~text
src/bayes_digits/    Data, features, posterior, metrics, experiment, plots
configs/            Full and smoke settings
scripts/            Reproduction, report assets and evidence audit
tests/              Mathematical/data/model checks
results/            Metrics, splits, probabilities, models, figures, logs
report/             LaTeX, generated tables and PDF
docs/               Research, AI workflow and wiki sources
~~~

- [Method](docs/wiki/Method-and-Mathematics.md)
- [Dataset/protocol](docs/wiki/Dataset-and-Protocol.md)
- [Research and verified references](docs/research.md)
- [Actual AI workflow](docs/ai_usage.md)
- [Reproducibility audit](results/audit.json)
- [Full-precision results](results/summary.json)
- [Figure provenance](results/figure_manifest.json)
- [Acceptance record](docs/acceptance.md)

The nine numbered figures and one tested covariance-example diagram are generated reproducibly in PDF/SVG/PNG, with 300-DPI PNG exports and vector analytical plots. The raw NPZ holds test indices, labels, probabilities and mutual information. Reloads and a fresh full run reproduce all 18 arrays exactly in the recorded environment.

Prompt 02 corrected training-loss logging to use the same completed epoch as validation. All 18 primary arrays remain bitwise identical to the original Git snapshot a28a563. Nine tests pass, including a verified covariance example. The post hoc fixed-model diagnostic runs eight independent sampling repetitions at each of 128/512/2048 draws for all three fitted models (72 predictions), without retuning. At 512 draws, NLL repeat SD is 0.0013–0.0019 nats; at 2048, the mean NLL penalty against matched MAP remains 0.0511–0.0555 nats. Sampling noise alone does not explain the primary negative probability-quality finding. [Initial review record](docs/review_02.md). The [final refinement](docs/refinement_02.md) enlarges digit examples, improves labels, replaces F1 SD bars with all raw seed values and observed ranges, adds explicit calibration-bin counts and a tested covariance diagram, and strengthens the literature rationale. All 25 executed evidence files remain byte-identical to Prompt 02 commit 93b625e; no model was retuned.

This is UCI optdigits' **original test subset**, repartitioned, not the complete dataset or original benchmark protocol. [UCI provenance and CC BY 4.0 terms](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits). Writer independence is not established. One split and three seeds do not justify broad deployment claims.

The materially used skill guidance is acknowledged in the report: [Scientific Agent Skills, Kassis et al. (2026)](https://arxiv.org/abs/2609.00065).
