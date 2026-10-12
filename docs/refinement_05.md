# Prompt 05 — Comprehensive final refinement

## Baseline and analysis plan

Baseline: `11fe6ceb1b2f85bf04b281e273bb73ad38657105` (Prompt 04). The original measurement files, model choices, split and student reflection are frozen. Prompt 05 is an explicitly post hoc refinement, not a new confirmatory study or independent human review.

Issues confirmed before editing: current machine paths in README and four metadata/log files; reproduction verified only in a reused environment; archived skill documents lack a complete redistribution-license record; crowded class-deficit marks; reliability points do not display bin-accuracy uncertainty; discrete prior samples joined into apparent curves; generic model and AI diagrams; no paired finite-image analysis.

The supplementary estimand is the mean, across the three fixed fitted models, of Laplace minus matched-MAP scores. Resample the same 360 image positions jointly for every method and seed, with replacement, 5,000 times using seed 20261012. Report percentile 95% intervals for error rate, NLL, class-summed Brier and recomputed ten-bin ECE. No seed resampling, significance tests, model selection or exclusions. Intervals are conditional on fixed models and an exchangeable-image assumption; unknown writer dependence, one split and post hoc choice prevent population-level guarantees. Record per-seed estimates separately. Wilson 95% binomial intervals illustrate reliability-bin precision; mark bins with fewer than 20 images as sparse. Empty bins remain empty.

## Figure contract

Coursework is the destination; Nature/Science guidance is a design reference, not a journal submission or certification. Preserve exact native pixels, all measured seed values and all eight prespecified errors. Python/Matplotlib is the established backend. Use editable vector PDF/SVG plus 300-DPI PNG, approximately 170 mm wide, sans-serif labels and redundant marker/line encodings. Core font size is 9 pt at final width, with every rendered glyph at least 5 pt. Inspect exports and every final report page.

| Figure | Scientific question and implemented encoding |
|---|---|
| Dataset | Is split support balanced? Exact count heatmap and deterministic native-pixel examples. |
| Inference | Where does Bayesian inference enter? Nine numbered train/validation/lock/test stages, distinguishing exact curvature from approximate posterior. |
| Covariance | Why are marginal and contrast variances different? Tested full/diagonal contours and exact densities on common geometry. |
| Comparison | Is accuracy sufficient? All seed errors, NLL and Brier, with descriptive means and seed SD. |
| Classes | Which labels fail, and which method changes F1? Row-normalized confusion plus signed paired F1 differences, all seeds. |
| Calibration | How precise are the reliability observations? Three separate reliability panels, Wilson intervals, exact bin counts, sparse-bin markers; MI ECDF for 352 correct/8 errors. |
| Training | Did losses improve within the budget? Matched post-update curves, shared log limits and compact common legend. |
| Prior/ablation | What was actually searched? Discrete validation-only grid points and fixed-prior test controls. |
| Errors | What do all prespecified mistakes look like? Native pixels, true/predicted digits, confidence and probability of truth. |
| Monte Carlo | Is the NLL penalty sampling noise? Fixed-model mean penalties and repetition SD, eight repetitions, no dataset-CI interpretation. |
| AI workflow | How did engineered instructions affect work? Human, AI and evidence swimlanes; authentic P01–P04 and current P05 refinement; review/repair feedback. |

## Verification and completed changes

All changes below were performed by the same AI agent. This is an adversarial self-audit with independent numerical formulations, not external peer review. Primary training/inference modules, the selected models, the raw predictions and the student's five reflection paragraphs are unchanged.

- Added `src/bayes_digits/paired.py`, a separate paired-analysis entry point, a SciPy-based independent audit and four meaningful tests. They check elementwise Hessian indexing/common-logit prior curvature, predictive MI against direct entropy, paired-score identities and sparse/empty Wilson boundaries. The original nine tests remain intact.
- Added a portable Python reproduction runner, pinned optional PDF-review dependencies and a Python 3.12 GitHub Actions matrix for Ubuntu/Windows tests and smoke execution. A new isolated environment used freshly installed CPU PyTorch/scientific packages without the old Assignment 1 package path.
- Redacted the command/path strings in four public metadata/log records. The ledger preserves baseline and public SHA-256 values. The frozen-evidence audit now proves **24 byte-identical measurement files plus one environment record with exactly one command-string change**; every other environment field remains identical. It still verifies all 18 arrays, original table values, class data and toy geometry.
- Audited 12 archived skill records: five verified MIT documents retain their complete upstream copyright/license; seven current full copies with unverified redistribution rights were replaced by links/hash provenance. Their historical hashes remain verifiable from the baseline commit. No new blanket license is imposed.
- Regenerated all ten scientific figures directly from exact saved files, with embedded fonts, vector PDF/SVG and 300-DPI PNG. Added cropped PDF/SVG/PNG exports of the editable TikZ instruction workflow. The manifests bind numerical inputs and supporting/generator source hashes.
- Reworked Section 1's workflow and staged-review explanation while retaining seven authentic prompt excerpts, original candidate comparison/selection justification, all original displayed equations and eight original references. Added the separate paired table, calibration-interval caveats, a bounded explanation of unfavorable Bayesian scores, and an honest 2021-recency boundary. Added the verified SciPy bootstrap documentation reference.
- Improved float placement, common figure widths, panel alignment and captions. The final 19-page report has eleven numbered tables, nine numbered experimental diagrams/figures, the unnumbered tested covariance illustration and the independently numbered AI workflow. Every page was rendered and inspected, including the unchanged student reflection on page 18.

## Executed verification

Run commands from the project root with the independent environment's Python; use `python` after activating an equivalent installed environment. Exact logs and machine-readable outcomes are under [results/refinement_05](../results/refinement_05/).

| Command/check | Observed outcome |
|---|---|
| `python -m pip check` | No broken requirements. |
| `python -m pytest -q` | All 13 tests passed. |
| `python -m bayes_digits.experiment --config configs/smoke.json` | Small complete training/validation/locked-test run succeeded. |
| `python scripts/reproduce.py` | Dependencies, tests, smoke, checkpoint reload, independent full protocol, paired calculations, figures/tables and numerical/history audits passed. |
| `python scripts/audit_results.py` | All 18 primary saved arrays and reported summary reproduced bitwise; every selected checkpoint reload passed. |
| `python scripts/audit_review.py` | Original prediction evidence, 72 fixed-model diagnostics, checkpoint provenance, references and reflection passed. |
| `python scripts/audit_refinement.py` | Frozen measurements, command-only exception, numerical tables, exact class observations and covariance geometry passed. |
| `python scripts/audit_instruction_section.py` | Seven quotations, 12 current/historical skill hashes, original prompts, reflection, equations, eight references and selection rationale passed. |
| `python scripts/audit_paired.py` | Additive-score intervals matched independently formulated SciPy percentile bootstraps; count-weighted ECE and all 19 occupied-bin Wilson intervals matched independent calculations. |
| Saved posterior audit | All three 330-dimensional precision matrices are positive definite; eigenspectra, Cholesky reconstruction and prior-only common-logit directions verified in `conditioning.json`. |
| Nature Figure PDF geometry checks | All ten scientific PDFs passed without text collisions or clipping; all nine multi-panel alignment checks passed. The single-axis inference diagram has no panel grid. |
| `python scripts/validate_submission.py` and `python scripts/check_artifacts.py` | PDF/section/table/quote/reflection checks, embedded fonts, SVG/XML validity, PNG size/DPI, source/export hashes, GFM structure, local links and current English/privacy checks passed. |
| Tectonic build | Main report and standalone TikZ workflow compiled successfully. Main final pass: no unresolved references, overfull/underfull boxes or duplicate destinations. Tectonic emits a nonfatal default-Fontconfig configuration diagnostic; embedded-font and visual checks pass. |
| Final visual inspection | All 19 report pages and every scientific/workflow export inspected at the intended size; no clipping, overlap or unreadable labels observed. See `visual_review.json`. |

The exact paired NLL penalty is **0.0538895 nats**, conditional 95% percentile interval **[0.0399442, 0.0661221]**. Error-count differences are zero for each fixed model; the conditional error-rate interval is **[-0.277778, +0.277778] percentage points**, which does not prove equivalence. The Brier/ECE evidence and analysis assumptions are preserved in [paired.json](../results/refinement_05/paired.json). Original accuracy and probability-quality results were not changed or retuned.

## Figure review: before and after

The figure-contract table above gives the scientific rationale for each export. The original readable but crowded panels were replaced by consistent 9-point sans-serif typography, restrained accessible colors, explicit units and redundant shapes/line styles. Confusion proportions retain their denominator and per-seed observations. The former bounded F1 deficit is now a symmetric signed **F1(Laplace) - F1(separately selected MAP)** comparison, preserving both unfavorable and favorable measured differences. This class display uses a different comparator from the matched-prior bootstrap, explicitly named in each caption.

Calibration received the largest change: separate method panels, unconnected occupied-bin points, exact support tables, marginal Wilson intervals and open markers for fewer than 20 images. No bin was deleted. The MI distributions are independently normalized over 352 correct versus eight erroneous predictions. Prior candidates are unconnected discrete observations; neither an interpolated optimum nor test-based tuning is implied. Monte Carlo axes use the actual powers of two and repetition SD is clearly distinguished from image uncertainty. All eight prespecified mistakes retain their native pixels and deterministic original-index order.

The model diagram separates feature learning/freezing, candidate MAP heads, exact training curvature, Gaussian approximation, validation selection, selection lock and final integration. The AI diagram distinguishes actual human directions, Codex/skill activities and verified evidence across Prompts 01-05, including same-agent repair loops. It does not invent human peer review or external gallery generation.

The export checks initially found real annotation collisions/clipping and unequal panel spacing; these were fixed before final delivery. The generic collision tool also returned 26 false positives for the TikZ export because its text-trace grouping merged several separate lines into one bounding box. The original failed diagnostic is retained in `collisions/instruction_workflow.json`; a per-line span check using the same collision thresholds found no collisions (`workflow_geometry.json`), and the exported and report diagrams were visually checked. This is a documented validator limitation, not a hidden successful run.

The plotting-source validator has **17 PASS, four WARN and zero FAIL**. Its strict Nature defaults prefer TIFF, 600 DPI and Nature column widths; this English course report intentionally uses 300-DPI PNG and approximately 170-mm vector figures. The remaining logarithmic-guard heuristic is checked against the actual positive NLL data/explicit log axes. These advisories are retained in `figure_source_validation.json`; no strict journal certification is claimed.

## Sources, privacy and scope

Official [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/) and [panel export guidance](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/) were consulted for legibility, vector text, restrained formatting and final-size inspection. The official Science author page returned HTTP 403, so live verification of its current specifications was unavailable. Source metadata for Laplace Redux, NatPN, VBLL, MacKay, UCI, scikit-learn, Guo and Scientific Agent Skills was checked against primary publisher/manuscript/documentation records; the added [SciPy bootstrap documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) supports the paired percentile procedure. The MacKay DOI resolver failed in this browser, but [the MIT Press article record](https://direct.mit.edu/neco/article/4/3/415/5639/Bayesian-Interpolation) verified its author, year, volume, pages and DOI. Access failures do not justify invented sources.

The current public deliverables contain English text and no unnecessary absolute user-home paths. Current metadata has documented redactions; **earlier public commits still expose the old machine paths and removed third-party skill copies**. Normal commits do not remove historical exposure. History was not rewritten or force-pushed. The student's authorized course identity/reflection remain public. Secret-pattern and excluded-cache inventory checks are bounded audits, not guarantees against every possible secret format.

Remaining scientific limitations are one small repartitioned dataset, one split, three fitted models, unknown writer dependence, a coarse validation grid, conditional fixed-feature Gaussian inference, finite posterior integration and post hoc image-bootstrap assumptions. Sparse bin intervals are marginal, conditional and based on a binomial approximation; no simultaneous calibration band or population guarantee is claimed. Corruption/OOD, new-writer generalization and representation uncertainty remain untested. The optional additional robustness experiment was not performed because it was unnecessary for these scoped refinements. macOS instructions are documented but unexecuted; cross-platform bitwise equality is not promised. Laplace Redux's 2021 publication is at the old end of Prompt 01's range, and an examiner could apply a stricter interpretation of recency.

## Readiness against the six instructor criteria

| Instructor criterion | Evidence-based assessment |
|---|---|
| How AI found the algorithm | Self-contained three-page instruction/search/candidate section; authentic prompt excerpts, primary-source records, selective actual skill contributions and editable executed workflow. |
| Algorithm description | Explicit prior/likelihood/MAP, exact conditional Hessian, Gaussian approximation, correct triangular sampling, prediction/MI and tested covariance example; approximation limits are explicit. |
| How AI implemented it | Modular AI-written code, equation/code mapping, executed pseudocode, meaningful tests and honest repair records. |
| Experiment settings/results | Locked validation-based protocol, unchanged genuine primary results, controlled ablations/MC diagnostics, transparent supplementary paired statistics and ten reproducible scientific figures. |
| What the student learned | All five student-authored paragraphs and both canonical source files preserved without alteration. |
| Source-code webpage | Public repository and six-page wiki exist; current publication/tree/PDF/wiki checks are recorded separately after synchronization. |

The evidence supports readiness for an Excellent-level coursework submission, subject to the disclosed recency and scientific limitations. It does not guarantee a mark or claim independent peer review. The report should be submitted through the instructor's specified Moodle route; publication is supplementary evidence.

## Publication verification

Local content is verified. Current normal Git push, six-page wiki synchronization, fresh full-clone checks and Ubuntu/Windows CI outcomes are recorded after execution in the final publication evidence. Earlier publication records remain historical.
