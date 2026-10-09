# Technical acceptance and final submission audit

Updated on 9 October 2026 after Prompt 02, its [final refinement](refinement_02.md), student reflection insertion and [Section 1 refinement](instruction_section_review.md). The original Prompt 01 acceptance snapshot is recoverable in Git a28a563. The student's supplied reflection is included and verified. Prompt 04 repeated tests, full reproduction and final PDF/public-documentation checks. This records technical completion and verified public repository publication; the separate wiki is populated and publicly verified.

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
| Compile and inspect report | Final Tectonic exit code 0; 18 pages, Section 1 on pages 2–4, with all five student-supplied paragraphs verified on page 17. Every final rendered page (1–18) visually inspected for legibility, equations, cropping, captions and layout. |
| Check Markdown | README/six wiki previews parsed as GFM and visually inspected with rendered math/tables. Local links checked; public README and repository Markdown rendering checked in Prompt 03. Public wiki mathematics, matrices, figures, results tables and navigation are verified. |
| Document AI workflow | [Actual AI-use log](ai_usage.md), seven verified prompt excerpts, vector workflow diagram, [twelve skill-document snapshots](skill_sources.md), README and six wiki sources. No invented personal reflection or search history. |
| Version control | Independent Git history uploaded to the new public topic-named repository, remote origin and public main branch; local branch codex/prompt-01 tracks origin/main. |

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

The LaTeX plugin's compile_latex.py built report/main.tex with Tectonic; the exact compiler command and output are in [compile.json](../results/logs/compile.json). Poppler rendered every page, and the AI reviewed the images. Correcting package order (float before hyperref) removed duplicate figure/table PDF destination warnings. There are no overfull/underfull boxes. Initial-pass citation/reference warnings are resolved by the compiler's subsequent pass. Earlier builds recorded a Fontconfig setup diagnostic; the final successful build and page review are authoritative.

The quantitative result is not uniformly favorable to the Bayesian method: Laplace accuracy is 97.69% and NLL 0.151; the selected MAP baseline achieves 97.78% and NLL 0.099. The report retains this negative probability-quality finding. Three seeds share one test split and do not establish general superiority or deployment performance.

## Final submission status

Completed: the student supplied their own reflection; all five paragraphs are preserved in report/student_reflection.txt and included through report/student_reflection.tex. Compilation, extracted-text comparison and visual inspection passed.
Prompt 04 reran all nine tests, metric/checkpoint checks and a fresh full reproduction. It recompiled and inspected every page and rechecked public repository/wiki documentation. The report now shows the small nonzero diagonal NLL SD as 0.0002 instead of rounding it to 0.000. All 25 original experiment evidence files remain unchanged; six numerical includes are byte-identical and the seventh has only that verified precision correction. See [final audit](submission_audit_04.md).

The remaining student action is to submit the final PDF through UMMoodle as required by the assignment. No course-site upload or Turnitin check was performed by the agent.

The student initialized Home through the Codex browser. CLI synchronization then published all six pages to the separate wiki master branch; public Home, mathematical and results pages were verified. GitHub rejected an operator macro and Markdown escaped matrix row separators in the first wiki rendering; supported upright notation and fenced math repaired both without changing the equations.

The public repository and report URL are verified. No local execution or final compilation blocker remains. See [publication record](publication_03.md) for resolved initialization/rendering issues and the retained initial compile failure.
