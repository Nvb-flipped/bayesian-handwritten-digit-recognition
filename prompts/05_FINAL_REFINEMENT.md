# Prompt 05 — Final Comprehensive Refinement and Publication-Quality Audit

## Objective

Conduct a comprehensive, independent, instructor-level review and refinement of the existing **CISC3024 AI Assignment #2 — Bayesian Handwritten Digit Recognition** project.

**Repository:** https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition

**Primary goal:** Maximize the submission's quality toward **100/100 (Excellent) in every assessment criterion**, while preserving mathematical correctness, scientific integrity, genuine experimental evidence, reproducibility, and compliance with the original assignment instructions.

**Figure quality target:** Professional, publication-ready scientific figures inspired by the design and production standards of *Nature* and *Science*, including the experimental figures, model-inference diagram, and AI-workflow diagram.

Implement improvements; do not merely provide recommendations.

Read the complete repository and relevant instructions before modifying anything.

---

## 1. Authoritative Instructions and Constraints

Read and respect, in priority order:

1. `AIassign2.pdf` — original instructor requirements.
2. `AGENTS.md` — persistent project instructions.
3. Existing executed prompt files, research/evidence records, and current report.
4. Applicable installed project skills.

The report must comprehensively cover:

1. How AI found the algorithm.
2. Algorithm description.
3. How AI implemented the algorithm.
4. Experiment settings and results.
5. What the student learned.
6. A public webpage link to the source code.

**Non-negotiable constraints:**

- All technical code must be written or modified by the AI agent, consistent with the assignment.
- Preserve the genuine student-authored reflection. Do not fabricate or rewrite personal experiences.
- Preserve original datasets, splits, raw predictions, selected models, original hyperparameters, and primary experimental results unless a verified mathematical/implementation defect requires correction.
- Never fabricate experimental results, citations, prompts, skill usage, human actions, statistical significance, or independent reviews.
- Do not change figures to make results appear more favorable.
- Do not use final-test outcomes to retune model selection or hyperparameters.
- Do not replace the chosen algorithm merely to improve measured accuracy.
- If the 2021 method's recency presents a genuine assignment-compliance risk, clearly identify it and strengthen the defensible justification; request a decision before undertaking a major algorithm replacement.
- Distinguish existing confirmatory results from new post hoc exploratory analyses.
- Do not force-push, rewrite public Git history, delete meaningful evidence, or expose credentials.

Aim for verifiable excellence, not an unsupported guarantee of full marks.

---

## 2. Skills: Mandatory Inspection and Selective Application

Inspect the relevant installed `SKILL.md` files under `.agents/skills/` and follow their applicable procedures, including supporting instructions where required.

Prioritize these figure-related skills:

| Skill | Intended purpose |
|---|---|
| `nature-figure` | Journal-grade visual standards and figure production |
| `scientific-visualization` | Honest statistical encodings, readability and accessibility |
| `scientific-figure-making` | Multi-panel scientific figure composition |
| `plot-from-data` | Rebuilding figures directly from original numerical evidence |
| `agent-figure-gallery` | Reference layouts and visual-design patterns |
| `scipilot-figure-skill` | Scientific diagram design and refinement |
| `markdown-mermaid-writing` | Workflow architecture and diagram planning, where appropriate |

Also use the relevant methodological skills:

- `analytical-method-validation`
- `experimental-design`
- `statistical-analysis`
- `exploratory-data-analysis`
- `literature-review`
- `scientific-writing`
- `latex-paper-en`
- `scikit-learn`

Do not invoke every skill indiscriminately. Select the most appropriate guidance for each task and document material usage accurately.

Use `plot-from-data` rather than `plot-from-image` wherever original numerical results exist. Never reconstruct approximate numerical results from figure pixels when exact source data are available.

**Figure generation must remain reproducible from project code and actual saved evidence.** Do not use generative imagery for quantitative plots, data-based panels, or mathematical diagrams where precision is essential.

---

## 3. Repository Cleanup, Privacy and Portability

Perform a comprehensive audit of public-facing files, logs, metadata, generated artifacts, and tracked history.

### 3.1 Remove machine-specific information

Known affected files include:

- `README.md`
- `results/environment.json`
- `results/publication_relocation.json`
- `results/logs/compile.json`
- `results/logs/publication_compile_initial_failure.json`

Search for additional local paths, usernames, internal cache paths, absolute working directories, environment-specific commands, credentials, and unnecessary personal metadata.

The current README contains an absolute Codex runtime command under a Windows user directory. Replace it with portable instructions.

Use relative paths and portable commands wherever possible.

**Preserve provenance integrity:** distinguish redacted public metadata from immutable original measurement evidence. If removing paths affects hashes or historical audit assertions, update the audit architecture transparently rather than silently changing original measurements.

Do not claim that a normal commit removes information from previous public commits. Report historical exposure separately; do not rewrite published history without explicit approval.

### 3.2 Improve reproducibility

- Make the README independently usable after a clean clone.
- Provide tested Windows PowerShell instructions and, where feasible, Linux/macOS instructions.
- Remove unnecessary dependencies on the Codex runtime, Assignment 1, or private plugin directories.
- Verify pinned dependencies and Python-version compatibility.
- Document Tectonic compilation with a portable workflow.
- Ensure figures, tables, tests, and the report can be regenerated.
- Verify historical-commit-dependent audits on a full clone, or provide an alternative current-state verification procedure.
- Add an appropriate GitHub Actions workflow for automated tests and smoke checks, subject to practical runtime limits.
- Perform a clean-environment reproduction rather than relying exclusively on existing local caches.

Inspect the redistribution licenses of archived third-party skill documents. Preserve attribution and licenses where redistribution is permitted; otherwise replace public copies with suitable source links and hashes.

Consider adding an appropriate license for original project code, but do not apply a license to third-party material without authorization.

---

## 4. Scientific and Mathematical Audit

Independently verify:

- Likelihood and prior definitions.
- MAP objective and gradient.
- Exact conditional softmax Hessian.
- Hessian matrix layout and indexing.
- Positive definiteness and numerical conditioning.
- Laplace posterior construction.
- Cholesky-based posterior sampling.
- Predictive probability integration.
- Calibration, entropy and mutual information.
- Probability normalization and metric definitions.
- Dataset splitting and absence of selection leakage.
- The interpretation of all ablations.

Check all important equations against the source implementation and existing automated tests.

Add targeted tests only where meaningful deficiencies are found.

Explicitly distinguish:

1. Exact conditional Hessian computation.
2. Approximate Gaussian posterior inference.
3. Point-estimated feature representation.
4. Uncertainty that is and is not represented by the model.

Correct any discovered technical defect and regenerate dependent evidence, while keeping a traceable before/after record.

Do not characterize the original implementation as defective without reproducible evidence.

---

## 5. Improve Experimental Analysis and Statistical Rigor

Inspect the existing results, including:

- Gaussian naïve Bayes.
- Separately selected MAP.
- Matched-prior MAP.
- Full Laplace.
- Diagonal Laplace.
- Per-class results.
- Calibration and uncertainty.
- Prior sensitivity.
- Monte Carlo integration diagnostics.

### Required refinements

**A. Quantify paired differences**

Use existing per-example predictions to quantify differences between matched MAP and Laplace, particularly:

- Accuracy/error rate.
- NLL.
- Brier score.
- Calibration, with suitable caveats.

Use paired estimands and appropriate statistical procedures. Where valid, consider paired bootstrap intervals over held-out images.

Do not treat the three training seeds as independent test datasets. Describe separately the variation associated with initialization, finite Monte Carlo integration, and finite test-set sampling.

Do not invent significance or population-level certainty.

**B. Improve calibration interpretation**

Address sparse confidence-bin populations, actual bin support, and uncertainty in estimated bin accuracy.

The interpretation must not imply that tiny bins provide reliable calibration evidence.

**C. Explain the unfavorable Bayesian results**

Retain the measured finding that Laplace has worse probability-quality scores than MAP in this experiment.

Provide a rigorous, evidence-bounded interpretation of potential causes, including approximation assumptions, prior effects, representation uncertainty and posterior predictive averaging.

Distinguish hypotheses from demonstrated mechanisms.

**D. Evaluate additional robustness only when scientifically justified**

Optionally add clearly labeled exploratory experiments involving input corruption or distribution shift if feasible without compromising the original held-out protocol.

Do not tune original models using these outcomes or replace primary results.

Preserve original experimental settings and add any supplementary analysis in separate files.

---

## 6. Comprehensive Nature/Science-Inspired Figure Redesign

Review **every existing figure**, including the AI-workflow diagram and the model-inference diagram.

Use the applicable official publisher specifications and inspected figure skills as design references. Do not invent submission requirements or claim journal certification.

### Universal standards

- Consistent typography, visual hierarchy, line weights, colors and panel labels.
- Colorblind-safe palettes with grayscale-readable encodings.
- Correct axes, baselines, units, denominators and transformations.
- Explicitly identified sample sizes and variability definitions.
- Readable text at the intended final PDF figure size.
- Clean alignment, balanced spacing and restrained visual decoration.
- Meaningful multi-panel arrangements rather than arbitrary panel collections.
- Vector PDF/SVG exports plus high-resolution raster exports where appropriate.
- Consistent panel lettering and concise scientifically informative titles.
- Captions that independently explain what is shown, its source, and the defensible conclusion.
- No distorted axes, clipped uncertainty intervals, unsupported smoothing, or misleading normalization.
- No unnecessary duplication of legends, text, or figures.

Prefer professional and restrained journal-style design over decorative graphics.

Keep digit images true to their native pixel values; do not smooth or enhance examples in a way that changes the evidence.

### Figure-specific requirements

**1. Dataset overview**

Improve class-distribution readability and compactness. Preserve exact split counts and deterministic sample selection.

**2. Model inference workflow**

Redesign into a high-quality scientific architecture diagram that clearly separates:

- Dataset and feature learning.
- Frozen feature extraction.
- MAP head estimation.
- Exact conditional Hessian.
- Gaussian posterior approximation.
- Monte Carlo predictive integration.
- Validation-based selection.
- Final held-out evaluation.

Accurately represent the actual implemented sequence and distinguish training from inference.

**3. Covariance geometry**

Retain mathematically validated geometry, consistent coordinate scales, and correct variance interpretation. Improve typography, labeling, and composition.

**4. Classifier comparison**

Make recognition and probabilistic-score differences immediately interpretable.

Preserve individual seed observations. Prefer direct, scientifically meaningful comparisons; avoid excessive empty space or heavy legends.

**5. Confusion matrix and class-level performance**

Improve the crowded F1-deficit presentation.

Evaluate whether a paired per-digit difference plot,

`F1(Laplace) − F1(MAP)`,

communicates the findings more clearly.

Use exact saved observations and clearly distinguish per-seed values from descriptive summary markers.

**6. Calibration and uncertainty**

Treat this as a highest-priority redesign.

Improve confidence-bin support representation, avoid overinterpreting sparse bins, preserve appropriate reliability comparisons, and clearly identify the very small misclassification group in the mutual-information panel.

**7. Training curves**

Improve consistency, reduce unnecessary repetition, and retain genuine train/validation loss data and truthful scaling.

**8. Prior sensitivity and ablations**

Make discrete grid evaluation and validation-only selection explicit.

Ensure the visualization cannot be interpreted as showing a continuous, precisely estimated prior optimum.

**9. Failure cases**

Improve the image-label layout and make true label, predicted label, confidence and relevant probability information understandable.

Do not cherry-pick examples. Retain the original deterministic selection rule.

**10. Monte Carlo diagnostics**

Improve clarity of the sample-count experiment and numerical integration variability.

Distinguish Monte Carlo repetition SD from dataset uncertainty and initialization variability.

### Deliverables for every redesigned figure

- Regenerated PDF.
- Regenerated SVG.
- Appropriate high-resolution PNG.
- Exact numerical source references.
- Updated provenance/manifest.
- An individually reviewed rendering.
- A short scientific rationale for the plot design.

Inspect both individual figure exports and their actual appearance in the compiled report. A figure that looks good enlarged is not automatically readable at final page size.

Do not introduce text overlap, clipped annotations, misleading colors, or unnecessary blank report pages.

---

## 7. AI-Workflow Diagram: Major Redesign

The existing six-box workflow is functional but needs a more sophisticated and concise visual architecture.

Redesign it as an editable vector diagram, preferably integrated into the LaTeX report.

A compact horizontal swimlane or similarly clear scientific-process design is preferred.

Show three distinct conceptual layers:

1. **Human direction:** original assignment, `AGENTS.md`, engineered prompts and genuine human decisions.
2. **AI execution:** literature research, algorithm selection, implementation, verification, experiments, figure/report creation and refinement.
3. **Verified evidence:** source files, tests, recorded results, report, repository, wiki and final audit.

Represent Prompts 01–04 accurately and show their actual contribution to the workflow.

Include genuine review/repair feedback loops and distinguish executed stages from optional or unexecuted possibilities.

Avoid long sentences inside boxes. Move detailed descriptions into the caption and accompanying report text.

The diagram must demonstrate **how engineered prompts and relevant skills materially changed the work**, not just a generic AI-project lifecycle.

Do not invent human reviews, approval stages, agent roles or evidence.

Maintain vector quality and readability in the final PDF.

---

## 8. Report and Literature Refinement

Review the complete LaTeX report critically as if grading it against the instructor's stated requirements.

### Algorithm discovery

Strengthen the self-contained explanation of:

- The student's instruction strategy.
- Genuine literature-search queries.
- Comparison of candidate algorithms.
- Verified primary sources.
- Selection criteria and trade-offs.
- Why the chosen method is appropriate for the assignment.
- How persistent instructions, task prompts and skills influenced actual decisions.

Address the 2021 publication date honestly. Do not describe classical Laplace theory as newly invented in 2021.

### Algorithm and implementation

Ensure every important mathematical mechanism is explained clearly and connected to its implementation.

Improve equation-to-code-to-test traceability where useful.

### Experimental results

Lead with meaningful findings rather than only displaying figures or large amounts of raw numbers.

Explain relevant negative findings, controlled ablations, statistical limitations and the scope of the conclusions.

### Student reflection

Preserve the authentic student-written content and factual meaning. Do not create fictional learning experiences or rewrite it into an AI-authored personal reflection.

### Citations and formatting

- Verify bibliographic claims against authentic sources.
- Maintain consistent mathematical notation.
- Resolve cross-reference, typography and layout problems.
- Ensure all six mandatory report sections are present and sufficiently detailed.
- Keep the complete report self-contained while using the repository/wiki for supplementary evidence.

Do not maximize page count for its own sake.

---

## 9. GitHub README, Wiki and Documentation

Refine the public repository so an instructor can easily identify:

- The project objective and selected algorithm.
- The connection to Bayesian classification.
- Key experimental settings.
- Principal measured results and limitations.
- How AI performed the assignment.
- How to reproduce results.
- Where to find the compiled report.
- Where to inspect source code, raw evidence, prompts and skill records.

Remove local usernames and private machine-specific compilation instructions.

Synchronize relevant wiki content with verified updates.

Check public links, mathematics rendering, images, internal navigation and consistency with the report.

Avoid conflicting versions of results or descriptions.

Retain provenance and historical audit documents without falsely presenting outdated records as the current project state.

---

## 10. Verification and Acceptance Criteria

Do not declare completion unless all applicable checks actually pass.

### Technical verification

- All existing unit tests pass.
- Added tests pass.
- Smoke experiments execute successfully.
- Model checkpoints can be loaded.
- Saved primary results remain consistent, except for explicitly documented and justified corrections.
- Numerical tables agree with recorded data.
- Reproducibility scripts and relevant audits pass.
- Dependency checks pass.
- New supplementary statistical calculations are independently validated where feasible.

### Figure verification

- Every figure regenerated from exact source data.
- PDF/SVG exports are valid.
- Raster exports meet the selected production specification.
- Captions, panel labels and legends are accurate.
- Fonts, figure colors, axes and uncertainty indicators are consistent.
- No clipping, overlap or unreadable text at final size.
- Every report page visually inspected after the final build.

### Report verification

- LaTeX compilation succeeds.
- No unresolved references or material layout defects.
- Every table and figure matches evidence.
- All required instructor sections are present.
- The genuine student reflection is preserved.
- Public source links are correct.
- References and scientific claims have been checked.

### Privacy and publication verification

- No unnecessary machine-specific paths remain in current public-facing content.
- Remaining historical exposure is explicitly documented.
- Third-party skill redistribution and attribution are checked.
- Git working-tree changes are reviewed.
- No unrelated files, credentials, environment caches or secrets are committed.
- The published repository and wiki can be accessed as intended.

Existing provenance audits may rely on historical file hashes and commits. Reconcile changes without silently weakening test coverage.

---

## 11. Execution and Delivery

Work autonomously through the necessary inspection, implementation, testing, figure generation, report compilation and documentation updates.

Use the following process:

**Phase A — Baseline audit**

Identify the actual issues, proposed fixes, affected files and scientific risks. Record the current Git commit and preserve a reproducible baseline.

**Phase B — Technical and privacy improvements**

Implement necessary repository cleanup, mathematical/statistical improvements and reproduction enhancements.

**Phase C — Figure redesign**

Apply relevant figure skills and regenerate all appropriate scientific figures and workflow diagrams.

**Phase D — Report refinement**

Integrate verified analysis, redesigned figures and precise explanations into the final PDF.

**Phase E — Adversarial quality review**

Review the result from the perspective of a demanding university instructor and scientific journal graphics reviewer. Resolve material shortcomings and repeat verification.

**Phase F — Final acceptance audit**

Run applicable tests, builds, reproducibility checks, full PDF rendering, link checks and public-documentation validation.

Create a concise audit record under `docs/` containing:

1. Issues discovered.
2. Exact changes made.
3. Evidence supporting each correction.
4. Verification commands and observed outcomes.
5. Original versus final figure assessment.
6. Remaining scientific limitations and unresolved risks.
7. Final submission readiness by each of the six instructor criteria.

Do not repeatedly retrain or alter the existing model unless technically necessary. Prefer verified improvements built on existing evidence.

Create a descriptive local Git commit for completed and verified changes. **Do not force-push or rewrite Git history.** Ask for approval before pushing changes to the public repository, unless publication has been separately authorized.

### Final response required

When finished, report:

- What was fixed or refined.
- Which scientific figures and diagrams were redesigned.
- Whether all tests, reproduction checks and PDF compilation passed.
- Whether any original experimental results changed, and why.
- The resulting PDF and repository artifact locations.
- Any remaining blockers or limitations.
- An evidence-based assessment of readiness for Excellent-level coursework submission.

**Completion standard:** The project should meet every explicit instructor requirement, withstand a rigorous technical and reproducibility audit, and present scientifically honest results with polished, consistently designed, publication-grade figures.

Do not declare that it will receive 100/100 or has passed independent peer review unless those claims have external evidence.