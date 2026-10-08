# Local technical acceptance through Prompt 02

Updated on 8 October 2026 after Prompt 02 and its [final refinement](refinement_02.md). The original Prompt 01 acceptance snapshot is recoverable in Git a28a563. The student's supplied reflection is now included and verified. This records local technical completion; public publication remains pending.

## Verified deliverables

| Requirement | Actual evidence |
|---|---|
| Read assignment and persistent/task instructions | Entire one-page AIassign2.pdf extracted and visually checked; AGENTS.md and Prompt 01 read. Assignment 2 files were found in the sibling directory. |
| Compare three recent substantive Bayesian methods | [Research record](research.md): Laplace Redux (2021), Natural Posterior Network (2022), Variational Bayesian Last Layers (2024); verified primary sources. |
| Implement selected method | Modular last-layer Laplace code, full conditional Hessian, Gaussian prior, Cholesky posterior sampling; independent project adaptation. |
| Prevent selection leakage | Saved stratified 1,077/360/360 indices, validation checkpoint/prior selection, selection lock before full-run test predictions. |
| Execute meaningful comparisons | Three neural seeds; deterministic Gaussian NB baseline; separately selected MAP baseline; matched-prior MAP and diagonal-precision ablations. |
| Preserve evidence | Configurations, versions, hashes, selections, checkpoints, per-example predictions, classification/probability metrics and figure provenance in results/. |
| Test mathematical/data/model behavior | Nine tests passed, including the exact covariance example and corrected epoch-loss logging; [test log](../results/logs/tests.log). |
| Verify documented execution | scripts/reproduce.ps1 executed successfully; [reproduction log](../results/logs/reproduction.log). |
| Audit reproduction with separate computations | Metrics regenerated, checkpoints reloaded, full run repeated; all 18 arrays bitwise identical in this environment; [audit](../results/audit.json). Same AI agent performed this, not an independent human reviewer. |
| Resolve technical/figure findings | [Prompt 02 record](review_02.md): logging repair, tested math example, 72 executed sampling repetitions and regenerated metrics; primary arrays remain unchanged. |
| Generate meaningful figures | Nine numbered figures plus one tested toy geometry diagram, each PDF/SVG/300-DPI PNG; all inspected alone and in the report. [Per-figure review](figure_review_02.md). |
| Compile and inspect report | Final Tectonic exit code 0; 16 pages, with all five student-supplied paragraphs verified on page 15. Every final rendered page (1–16) visually inspected for legibility, equations, cropping, captions and layout. |
| Check Markdown | README/six wiki previews parsed as GFM and visually inspected with rendered math/tables. Local links checked; public rendering deferred. |
| Document AI workflow | [Actual AI-use log](ai_usage.md), README and six wiki sources. No invented personal reflection or search history. |
| Version control | New independent local Git repository, branch codex/prompt-01. No publication or remote added in this phase. |

## Executed commands and checks

The following were executed from the project root using the recorded local environment. Logs preserve actual outputs, and results/environment.json records library versions and source hashes.

~~~powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m bayes_digits.experiment --config configs/smoke.json
.\scripts\reproduce.ps1
.\.venv\Scripts\python.exe scripts/audit_results.py
.\.venv\Scripts\python.exe -m pip check
~~~

The LaTeX plugin's compile_latex.py built report/main.tex with Tectonic; the exact compiler command and output are in [compile.json](../results/logs/compile.json). Poppler rendered every page, and the AI reviewed the images. Correcting package order (float before hyperref) removed duplicate figure/table PDF destination warnings. There are no overfull/underfull boxes. Initial-pass citation/reference warnings are resolved by the compiler's subsequent pass. A Fontconfig setup diagnostic appears in the log, but compilation succeeds and embedded fonts/text were visually verified.

The quantitative result is not uniformly favorable to the Bayesian method: Laplace accuracy is 97.69% and NLL 0.151; the selected MAP baseline achieves 97.78% and NLL 0.099. The report retains this negative probability-quality finding. Three seeds share one test split and do not establish general superiority or deployment performance.

## Exact remaining work

Completed: the student supplied their own reflection; all five paragraphs are preserved in report/student_reflection.txt and included through report/student_reflection.tex. Compilation, extracted-text comparison and visual inspection passed.
1. In Prompt 03, repair GitHub authentication, create a new public Assignment 2 repository, publish source/report and wiki when available, verify public pages, and insert the real code URL into the report. The inspected GitHub CLI authentication is invalid. Publication was explicitly deferred by Prompts 01 and 02.
2. Perform the final submission audit (Prompt 04) after those changes.

There is no unresolved local execution or compilation blocker. The public code URL remains pending for Prompt 03; the reflection has been supplied and verified. No personal experiences or public URL have been fabricated.
