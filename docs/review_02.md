# Prompt 02 technical and figure review

Historical review snapshot before the student's reflection was supplied. The current report includes the student's five paragraphs and the expanded Section 1; its current pagination and validation record are in results/report_validation.json.

This records the initial Prompt 02 review at commit 93b625e. Figure styles and final layout are superseded by the [final refinement record](refinement_02.md); the original executed diagnostic remains unchanged.

Review date: 8 October 2026. Baseline snapshot: Git a28a563. This is an adversarial AI self-review of the existing work, not independent human peer review. The assignment PDF, AGENTS.md, Prompt 02, code, configs, measured evidence, report and installed guidance were inspected.

## Prioritized initial issues

No critical mathematical or held-out selection error was identified in the initial audit. The following findings require repair or explicit scope limits.

| ID | Priority | Finding | Required action |
|---|---|---|---|
| M1 | Major | Train NLL is logged before the optimizer update while validation NLL is logged after it. | Evaluate both losses at the completed epoch; test checkpoint/history consistency, rerun and compare saved predictions to the original snapshot. |
| M2 | Major | Full-range accuracy/F1 panels hide the few-error differences; overlapping seed points conceal replication. | Plot error counts and F1 deficits from zero; horizontally offset seed markers and label the transformations. |
| M3 | Major | Reliability lines join sparsely occupied and missing bins; raw MI histogram counts obscure the eight errors beside 352 correct cases. | Use unconnected reliability points with bin occupancy, and empirical distributions normalized within correct/error groups; retain denominators. |
| M4 | Major | Posterior sampling variation is unmeasured, limiting interpretation of the finite-sample NLL result. | Execute a separately configured post hoc diagnostic with fixed models/priors and repeated independent draws at 128/512/2048 samples. Do not retune. |
| M5 | Major | Tiny confusion labels, color-only convergence lines, and panel/legend inconsistencies weaken final-size readability. | Enlarge annotations, add redundant shapes/styles and panel labels, inspect all exports and every final page. |
| M6 | Major | Scalar curvature example is evaluated away from a stated optimum; it does not teach class covariance cancellation. | Replace with an exact small conditional MAP/Hessian example, verify it numerically, explain logit contrasts and predictive averaging. |
| M7 | Major, found during final provenance QA | Windows-generated JSON used CRLF while Git records LF, so source-data hashes could fail after a fresh checkout. | Write generated JSON/TeX with explicit LF; retain LF checkout attributes for hash-bound sources; add a byte-level regression test and rerun. |
| m1 | Minor | Source-hash paths use Windows separators; actual device metadata can say auto rather than its resolved device. | Record portable paths and resolved device; retain original commit evidence. |
| m2 | Minor | Figure manifests lack explicit questions, transformation details, source hashes and accessible numeric alternatives. | Expand provenance and provide underlying transformed figure data plus a per-figure review table. |
| m3 | Minor | Captions state displays more often than their bounded conclusions; references need a fresh source check. | Add evidence-bound conclusions, re-open primary sources, check all citation keys/links and final PDF references. |

## Diagnostic plan recorded before execution

Use selected checkpoints for all three feature seeds; hold features, head means, prior precisions, split indices and primary predictions fixed. At each sample count 128, 512 and 2048, run eight independent sampling repetitions per model (72 predictions). Use deterministic sampling seeds specified in configs/review_diagnostics.json. Report per-model NLL means/sample SD across repetitions and matched-MAP NLL on the same 360 images. This measures numerical integration variability conditional on the fitted posterior and test set; it is not a dataset confidence interval or a new model-selection stage. Preserve all repetition probabilities and metrics. No significance tests or superiority claims are added.

## Resolution

All listed issues were addressed. No unresolved critical or major technical/visual defect was found within the inspected environment. This is a bounded self-review, not a guarantee of correctness or independent peer-review certification.

| Finding | Actual resolution and evidence |
|---|---|
| M1 | Both losses now use the completed epoch's weights. The tiny-batch test checks history against checkpoint cross-entropy. Nine tests pass. Reproduction and the original-commit comparison preserve all 18 primary prediction/label/index/MI arrays bitwise. Histories and execution metadata legitimately changed. |
| M2 | Comparison shows integer errors out of 360, alongside NLL and Brier from zero. Seed markers are offset and shaped. Class performance shows explicitly labeled F1 deficits with complete descriptive SD bars and a zero reference; the report retains raw F1. |
| M3 | Reliability uses unconnected occupied bins; marker area increases with occupancy. MI uses separately normalized empirical distributions with 352 correct/eight errors, not unequal raw-count histograms. |
| M4 | All 72 configured repetitions executed. Recorded metrics were regenerated from their saved probabilities, and checkpoint hashes remained fixed. At 512 samples NLL repetition SD is 0.0013–0.0019 nats; at 2048 the mean penalty versus matched MAP is 0.0511–0.0555 nats. These are conditional numerical diagnostics, not confidence intervals or tuning. |
| M5 | Larger confusion labels, coherent method colors, seed styles/shapes, split hatches, panel labels and repositioned legends. All nine exports were inspected individually and on their actual report pages. PDF/SVG are vector analytical outputs; PNG is 300 DPI. |
| M6 | Exact two-class MAP example now derives the full Hessian, inverse and contrast variance, with a numerical unit test. The illustrative sigmoid average is explicitly separate from experiment data. |
| M7 | JSON/figure/TeX writers now specify LF, with corresponding Git attributes and a ninth test checking saved bytes. Configuration/script hashes are verified in the diagnostic audit; figure source hashes and Markdown hashes are checked against both working files and the staged Git blobs. Literal generated SVG bytes are preserved with -text. All 77 recorded hash checks passed; [Git provenance record](../results/git_provenance_validation.json). This ensures preservation through Git, not cross-platform floating-point identity. |
| m1 | Portable source-hash paths and requested/resolved device are saved; CPU usage is distinguished from detected GPU availability. |
| m2 | Manifest now records generator/source hashes, dimensions and DPI. Transformed figure data and a [per-figure review](figure_review_02.md) provide numerical alternatives and scientific questions. |
| m3 | Captions specify transformations, units, denominators, variability and bounded conclusions. All eight references were re-opened in primary sources, and citation keys match the report bibliography. |

## Section-by-section technical assessment

| Report section | Assessment |
|---|---|
| 1. AI research/method choice | Three recent substantive Bayesian candidates are distinguished; 2021 is at the older edge of the prompt's range. Laplace Redux's practical framework is distinguished from classical Laplace theory. Actual prompts, skills and same-agent review are disclosed. |
| 2. Algorithm | Categorical likelihood, isotropic Gaussian prior including biases, summed objective, gradient and class-major Hessian match code. Positive prior yields unique conditional MAP and positive-definite curvature. Exact conditional Hessian is distinguished from an approximate posterior and from full-network curvature. Cholesky transpose and predictive probability averaging are tested. Complexity and conditional uncertainty limits are stated. |
| 3. AI implementation | Module/formula mapping and executable pseudocode are present. Optimizer convergence/gradient checks, serialization, covariance simulation, metrics, split disjointness and the new toy example are tested. The logging repair is disclosed without claiming changed scientific results. |
| 4. Experiments | Explicit 1,077/360/360 split, fixed-range scaling, three seeds and all settings are recorded. All selection is validation-based and precedes test predictions. NB is a simpler statistical comparator; matched MAP and diagonal precision are controlled ablations. Raw predictions regenerate metrics. Post hoc sampling diagnostic is labeled and does not retune. |
| 4. Interpretation | Lower MAP NLL/Brier and higher Laplace ECE remain visible. Covariance intuition is mathematically compatible rather than a measured causal decomposition. All eight representative-seed errors are shown; sparse bins, shared test examples and small seed count constrain conclusions. |
| 5. Student learning | Exactly one explicit student-authored reflection placeholder remains. No learning experiences were generated. |
| 6. Code webpage | Actual local/publication status is disclosed. No invented URL; publication is deferred as Prompt 02 requires. |

## Executed verification

- Nine tests passed; [test log](../results/logs/tests.log). The expanded [reproduction script](../scripts/reproduce.ps1) ran tests, primary experiment, sampling diagnostic, figures and report tables successfully; [log](../results/logs/reproduction.log).
- [Primary audit](../results/audit.json) regenerated metrics, reloaded checkpoints and repeated the full experiment with identical arrays. [Review audit](../results/review_audit.json) compared all 18 arrays to Git a28a563 and regenerated 72 diagnostic records. Original evidence remains in that commit.
- [Sampling evidence](../results/review_diagnostics/provenance.json) preserves configuration, deterministic repetition seeds, actual duration, script/checkpoint hashes and raw probabilities.
- Tectonic exited successfully; every final PDF page (1–15) was rendered with Poppler and visually inspected. No clipping, overlap, unresolved final references, duplicate PDF destinations or overfull/underfull boxes were found. [Compile log](../results/logs/compile.json), [PDF validation](../results/report_validation.json).
- README and six wiki pages were parsed as GFM and rendered in disposable headless Chrome with MathJax 3. All seven screenshots were inspected; 26 math nodes rendered without math errors and all three tables were readable without overflow. [Markdown record](../results/markdown_validation.json). The in-app localhost preview timed out; the separate local renderer succeeded. Public GitHub rendering remains a Prompt 03 check.
- [Palette audit](../results/palette_audit.json) passes graphical contrast against white for all four colors. Four of six gray-separation pairs warrant review, so color is supplemented by labels, hatching, shapes or line styles. This is not a blanket accessibility certification.

## Remaining boundaries

One small dataset subset, one split, three shared-test seeds, unknown writer separation, point-estimated features, local Gaussian approximation, coarse prior grid and reused validation partition limit external validity. Sampling repetitions quantify integration variation only. No OOD, corruption, writer-generalization or significance claim is added. Further experiments are prospective, not implied to have run.

The student must replace the reflection placeholder in their own words before Prompt 03. Publication and insertion of a real public URL are deliberately deferred; earlier CLI authentication was invalid. No source or wiki was published during this review.
