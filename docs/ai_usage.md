# Actual AI workflow

8 October 2026. The user asked the agent to read the assignment PDF, AGENTS.md and Prompt 01 and execute it completely.

## Instructions and location

The initial chat was in Assignment 1. Requested Assignment 2 files were absent there and found in the sibling Assignment 2 directory. All new work was performed in Assignment 2; Assignment 1 source and artifacts were not edited.

The entire course PDF was extracted with pypdf and its page rendered with Poppler and inspected. AGENTS.md supplied persistent rules; Prompt 01 decomposed research, implementation, experiments and reporting and explicitly deferred publication until Prompt 03.

## Consulted skills

Materially applied: literature-review (primary sources/provenance), experimental-design (matched controls/seed replication), scikit-learn (splits/baselines/metrics), scientific-visualization plus publication guidelines (scales, vector output, sample sizes), machine-learning/PyTorch patterns/training recipe (seeding, tiny-batch, checkpoints), PDF (extraction/rendering), LaTeX compile (compiler detection/build).

During Prompt 01, latex-paper-en and scientific-writing were inspected as candidates; their review services/scripts were not used. Prompt 02 materially applied scientific-writing (evidence-bound revisions), statistical-analysis (dependence and variability units), latex-paper-en caption/experiment/reviewer guidance, scientific-visualization, PDF and the LaTeX compile plugin. No subagent or paid image generator was used. The Scientific Agent Skills reference is acknowledged in the report, following the materially applied local skills' instructions.

## Actual sequence

1. Inspect files, environment, GPU, Git and authentication.
2. Search primary literature; compare three candidates and choose conditional Laplace.
3. Write modular code, full/smoke configurations and meaningful tests.
4. Verify formulas against autograd, covariance simulation, probability normalization, split isolation, serialization and tiny-batch reproduction.
5. Repair pytest's Windows system temporary-directory access issue by selecting a project-local directory. All seven tests then pass.
6. Execute a three-epoch small pipeline with validation selection before its test stage. Its test outputs were not used to change the already specified full configuration.
7. Execute all full neural seeds and NB; preserve candidate settings, selections, models, raw predictions and metrics.
8. Regenerate metrics, reload checkpoints and repeat the full run. All 18 arrays match exactly.
9. Generate and inspect eight evidence figures; fix flow arrows.
10. Generate LaTeX tables from JSON, write the technical report and six wiki source pages.
11. Compile and inspect the report. Final outcomes are recorded in acceptance.md.
12. Correct LaTeX package order to remove duplicate table/figure hyperlink destinations, rebuild, and inspect all 14 final pages again. Initialize a separate local Git repository for Assignment 2; publication remains deferred.

## Environment and repairs

Observed: Python 3.12.14, PyTorch 2.11.0+cu128, RTX 5060 Ti available. Actual experiments used CPU and four PyTorch threads. The new local venv reuses existing scientific dependencies through a read-only path file; missing sklearn dependencies were installed locally.

Initial ensurepip initialization returned nonzero; the environment interpreter and inherited pip subsequently worked and imports were verified. Sandboxed package download failed DNS resolution; authorized network escalation succeeded. Pip dependency check passed.

Initial Tectonic compile could not retrieve an uncached TeX bundle under sandbox restrictions; the build was retried with network access. Outcomes are supported by the actual compiler log, not invocation alone.

GitHub CLI reported invalid authentication. No token was displayed or saved. Publication is deferred and no repository URL is fabricated.

## Prompt 02 review

The user subsequently requested full technical review and figure improvement. The agent reread AGENTS.md, Prompt 02 and the course PDF, audited code/configs/evidence and opened all eight primary reference records again. Bibliographic metadata and the selected paper's inference description agree with the cited sources. Verification is by the AI, not an independent human verifier.

The initial prioritized issue list is in review_02.md. The review corrected pre-update training versus post-update validation loss logging, added a verified two-class covariance example, enlarged confusion annotations, separated seed points, changed near-perfect accuracy/F1 plots to error counts/F1 deficits, replaced joined reliability lines with occupied-bin scatter, and replaced imbalanced count histograms with within-group empirical MI distributions. The selected models and all 18 primary saved arrays remain unchanged against the original commit.

A post hoc diagnostic plan/config was recorded before executing 72 fixed-model predictions at 128/512/2048 samples with eight independent repetitions per fitted model/count. It quantified integration variability without retuning. Nine tests passed; full reproduction, reload and metric audits were run. Nine figures were inspected individually and in the compiled report, which is rendered page by page again after final revisions. The reference acknowledgment remains; no independent peer-review certification is claimed.

## Student authorship

The agent authored all technical code/report prose. The named learning-reflection section contains **STUDENT REFLECTION REQUIRED**. It must be replaced by student-authored text. No personal experiences were invented.

## Final publication-quality refinement

The user requested another visual and technical pass focused on Figures 2/4/5/6, bounded F1 variation, whitespace and the rationale for the 2021 method. The agent revised plotting and LaTeX layout, added numerically tested toy covariance geometry, rechecked relevant primary sources and retained the Scientific Agent Skills acknowledgment. It did not retune or modify the saved experiment evidence. New audits compare against commit 93b625e; the final 15-page PDF and all ten individual exports were inspected. The initial refinement preview exposed crowded confusion annotations and a clipped toy-panel title; both were corrected before delivery. This remains AI self-review, not external peer review. The student reflection and Prompt 03 publication remain pending.

## Student reflection insertion

The student supplied five paragraphs in the conversation and explicitly asked that their meaning and content be preserved. The agent copied them without rewriting into report/student_reflection.txt and generated the LaTeX inclusion with percent-sign escaping and explicit curly-apostrophe encoding. The first PDF text comparison caught omitted Unicode apostrophes; explicit LaTeX encoding fixed the issue. All five paragraphs were compared with extracted PDF text on page 15 and visually checked. The final report has 16 pages, all rendered and inspected. Reflection checks now verify the supplied text rather than requiring the former placeholder. No experiment or figure was regenerated, and GitHub publication remains deferred to Prompt 03.

## Instruction/discovery section refinement — 9 October 2026

The user requested a self-contained account of instruction hierarchy, actual prompt excerpts, recorded discovery and skill contributions, plus a mandatory vector workflow diagram. The agent reread AGENTS.md, all four original task prompts, research/AI-use/review records, the course PDF and current LaTeX. It did not treat reading Prompts 03/04 as authorization to execute publication.

Section 1 now occupies pages 2–4, with seven extracts verified against the original files and recorded in [the excerpt ledger](prompt_excerpts.json). It explains prompt purposes and recorded responses, all three actual algorithm queries, primary-source verification failures/fallbacks, candidate criteria and staged review. The existing substantive candidate comparison and selection justification are preserved. A TikZ diagram distinguishes human instructions, AI activities and local outputs, includes the repair/recheck loop, and marks GitHub/wiki publication and the post-publication audit pending. The first diagram preview revealed a horizontal arrow-label crowding issue; shortening that label repaired it.

The [skill-document index](skill_sources.md) preserves twelve complete installed instruction-document snapshots with actual source metadata and hashes. It identifies material use separately from inspection and availability. The current revision applied LaTeX section-writing, scientific-visualization and PDF-verification guidance. No new literature search, model selection, training, test-set tuning or numerical result was added. No independent reviewer, subagent or external manuscript-review service was used.

The final report has 18 pages. All pages were rendered and individually inspected; Section 1 occupies pages 2–4 and the unchanged reflection is on page 17. Source/PDF excerpt checks, reflection checks, numerical-evidence and citation audits passed. An audit import failure caused by an omitted `PYTHONPATH=src` setting was corrected. README, six wiki pages and the skill index passed local rendered GFM checks. The [scoped refinement review](instruction_section_review.md) records evidence, repairs and remaining limits.

## Prompt 03: public publication (9 October 2026)

The student explicitly approved full public history upload, including title-page identifiers and their reflection, and requested a topic-based repository and local folder name. Authenticated GitHub CLI access created https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition and pushed the audited history to public main. The report and README received the real URL. Nine tests, a fresh full reproduction, immutable-evidence checks and the history scan passed before upload. The initial automatic-review refusal was resolved by student approval.

GitHub confirms Wikis enabled. Public browser access redirects the empty wiki; the browser is signed out. At the student's request, authenticated git ls-remote checked the wiki URL and returned Repository not found. Six canonical source pages and scripts/publish_wiki.py are prepared; no wiki publication is claimed. The first publication compile failed on a blocked official bundle fetch and succeeded after authorized network access; a long-URL overflow was repaired. Subsequent final PDF and public-file verification are recorded in results and docs/publication_03.md. Prompt 04 remains a separate subsequent audit.

The student then created Home in the Codex browser. The CLI cloned the initialized wiki, observed its master default branch and published all six pages (544f19c). Browser inspection found rejected operatorname macros and incorrectly escaped matrix rows; upright notation and fenced math repaired the same equations in 49cdaf0. Public wiki Home, mathematical derivations, matrices, measured-result tables, three figures and navigation were checked. README/report now contain both verified public URLs.
