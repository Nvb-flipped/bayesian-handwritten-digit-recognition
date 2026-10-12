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

Variation is sample SD across three initialization seeds on **the same** 360 test images. NB is deterministic and evaluated once. Brier sums over classes. Laplace retains strong recognition accuracy but has worse probability quality than MAP. [Detailed results and ablations](docs/wiki/Results-and-Visualization.md).

[Compiled report](report/main.pdf). [Public source repository](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition). [Public wiki](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/wiki), populated with six technical pages. [Version-controlled wiki sources](docs/wiki/Home.md).

## Clean-clone reproduction

Python **3.12** is validated. The primary study originally used PyTorch 2.11.0+cu128 on CPU; a newly created, independent CPU-wheel environment reproduced all 18 saved arrays bitwise. No Assignment 1 environment, Codex runtime, private plugin or downloaded dataset is required. Bitwise agreement on other operating systems is not promised.

Windows PowerShell:

~~~powershell
git clone https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition.git
Set-Location bayesian-handwritten-digit-recognition
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-review.txt
.\.venv\Scripts\python.exe scripts/reproduce.py
~~~

Linux/macOS shell (CPU wheels are available for supported platforms; macOS can install torch from PyPI):

~~~bash
git clone https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition.git
cd bayesian-handwritten-digit-recognition
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-review.txt
.venv/bin/python scripts/reproduce.py
~~~

The portable runner checks dependencies and 13 tests, executes a smoke experiment, reloads checkpoints, independently trains the unchanged full protocol into **ignored `tmp/reproduction`**, compares saved arrays/summary, computes the separate paired analysis and regenerates figures/tables. It does not overwrite the primary measurements. Historical audits require the complete Git history (the default clone); use `git fetch --unshallow` for a shallow clone. Windows and Ubuntu CI check tests and smoke execution; full bitwise reproduction is an environment-specific check. macOS instructions have not been executed here.

To regenerate the optional, already recorded 72 fixed-model sampling diagnostics:

~~~powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts/review_diagnostics.py
~~~

## Portable LaTeX compilation

Install [Tectonic](https://tectonic-typesetting.github.io/en-US/install/), then run from the repository root:

~~~powershell
Push-Location report
tectonic -X compile --untrusted main.tex
Pop-Location
~~~

For a POSIX shell: `cd report && tectonic -X compile --untrusted main.tex`. Alternatively the reproduction runner accepts `--compile` when Tectonic is on PATH. First use may download the public TeX bundle; no shell escape is needed. Quantitative tables and all ten plot PDFs/SVGs/300-DPI PNGs are generated from exact saved evidence. The AI swimlane diagram has editable TikZ source in `report/instruction_workflow.tex`.

## Findings and limitations

Primary accuracy and probability scores above are unchanged. Matched-prior controls isolate posterior averaging: post hoc paired image bootstrap gives **Laplace − matched MAP NLL = 0.05389**, conditional 95% percentile interval **[0.03994, 0.06612]**; Brier difference **0.01358 [0.00823, 0.01878]**. Error-rate difference is zero, with interval **[−0.278, +0.278] percentage points**. ECE difference is **0.05536 [0.04162, 0.05959]**, with additional binning/bias caveats. These resample 360 shared image positions jointly across three fixed models, never 1,080 independent examples. They are exploratory, conditional on the observed fitted models/draws, and do not account for unknown writer dependence. See [analysis plan, design rationale and final audit](docs/refinement_05.md) and [exact paired evidence](results/refinement_05/paired.json).

Initialization SD, eight-repeat Monte Carlo integration SD and image-bootstrap intervals describe different variation. The 72 fixed-model diagnostic retains an NLL penalty at 2,048 draws. Calibration panels display exact bin support, 95% Wilson bin-accuracy intervals and open markers for bins with fewer than 20 images; these are marginal bin intervals, not simultaneous calibration bands. The class comparison shows exact signed per-seed F1 differences. No test-driven model retuning occurred.

The small study repartitions UCI optdigits' original test subset rather than reproducing its official benchmark. [UCI source and CC BY 4.0 terms](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits). Writer independence, representation uncertainty, corruption and out-of-distribution detection are untested. Laplace Redux (2021) is at the older edge of the engineered prompt's 2021–2026 range; the assignment does not specify a numerical recency cutoff. This is a defensible educational framework choice, not a state-of-the-art claim or a guaranteed grading outcome.

## Evidence and AI instructions

- [LaTeX/PDF report](report/main.pdf), including the unchanged student-authored reflection
- [Original assignment](AIassign2.pdf), [persistent rules](AGENTS.md) and [staged prompts](prompts/05_FINAL_REFINEMENT.md)
- [Research queries and verified primary sources](docs/research.md)
- [AI-use record](docs/ai_usage.md), [skill consultation and licenses](docs/skill_sources.md), [verbatim prompt ledger](docs/prompt_excerpts.json)
- [Full-precision primary metrics](results/summary.json), [checkpoint/reproduction audit](results/audit.json), [current figure provenance](results/figure_manifest.json)
- [Prompt 05 acceptance audit](docs/refinement_05.md), [metadata redaction ledger](results/refinement_05/metadata_redactions.json)
- [Public wiki](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/wiki) and [version-controlled wiki pages](docs/wiki/Home.md)

Prompt 01 researched, implemented and executed the study. Prompt 02 repaired loss logging and strengthened mathematical/visual interpretation while preserving all original arrays. Prompt 03 published after the student's explicit approval; Prompt 04 audited submission. Prompt 05 adds paired analysis, privacy/portability cleanup, complete figure and workflow redesign, and clean-environment verification. Earlier dated audit records describe their historical states; the current acceptance record is Prompt 05.

Current public metadata replaces unnecessary machine paths with portable commands/placeholders; hardware, package versions, timings and measurements remain. **Earlier public commits still contain the paths and removed third-party skill copies.** Normal commits do not erase them; no history rewrite was performed. Five verified MIT skill instruction documents retain the complete copyright/license notice; other installed-copy provenance is represented by links and hashes. No blanket license is imposed on the student's reflection, report or third-party material. [Scientific Agent Skills acknowledgment](https://arxiv.org/abs/2609.00065).
