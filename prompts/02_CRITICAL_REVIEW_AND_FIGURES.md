# Codex Prompt 02 — Adversarial academic review, improved graphs, and visual QA

Act as a **strict independent reviewer and scientific-figure editor** of the already executed Assignment #2 project. Read `AGENTS.md`, `AIassign2.pdf`, the code, actual configs/metrics, figure-generating scripts, report source and compiled PDF. Inspect the relevant scientific-writing, statistical-analysis, scientific-visualization, LaTeX and PDF skills that are actually available.

The previous assignment scored **93/100**: the reviewer found it correct but wanted **more technical detail and substantially better graphs**. This task is a mandatory quality gate intended to eliminate those weaknesses, not to invent new achievements.

## Review and improve technical depth

Audit the report **section by section** for:

1. **Method choice:** Is the selected algorithm actually recent and substantively probabilistic/Bayesian? Are primary-source citations verified, and is novelty/adaptation represented correctly?
2. **Mathematics:** Are notation, assumptions, priors/likelihoods/posteriors or equivalent probability model, inference, objective, derivations, and prediction rule clear, justified, and consistent with code? Are there skipped steps a Pattern Recognition student would need explained? Include an annotated numerical example or useful conceptual intuition where beneficial.
3. **Implementation:** Does it explain what AI implemented and why, map formulas to source modules, give pseudocode of the key computation, and make reproducibility possible?
4. **Experiments:** Are dataset/splits, preprocessing, random seeds, hyperparameters, baselines, controls, validation/test separation, and metrics fully specified? Are comparisons fair? Are measured results traceable to saved data? Are uncertainty and class-level performance addressed where justified?
5. **Interpretation:** Does it analyze *why* the results behave this way, evidence for claims, failure cases, trade-offs, calibration/uncertainty (where applicable), sensitivity, threats to validity, and limitations?
6. **Assignment compliance:** Are all six required instructor items covered? Is AI usage—including `AGENTS.md`, engineered prompts, and actual installed skills—explained accurately? Is the personal-reflection placeholder preserved without invented text?

Improve weak sections with **substance**, not word-count padding. If a scientifically important claim requires an additional feasible experiment, implement and actually execute it, then propagate the measured results consistently throughout the paper/README/wiki. Never invent data or backfill references.

## Scientific visualization quality gate

For **every** generated chart and figure:

- Identify the exact scientific question and source data.
- Inspect titles, captions, legend location, axis labels/units, uncertainty semantics, sample counts, class ordering, color choices, and density of labels.
- Replace vague/ornamental graphs with appropriate scientific plots. Avoid 3D effects, unjustified smoothing, truncated axes that mislead, unnecessary gradients, clutter and tiny labels.
- Use consistent fonts, a colorblind-considerate palette, distinguish lines with markers/styles as needed, and use adequate contrast in print and screen views.
- Prefer vector PDF/SVG for analytical plots, sufficiently high-resolution raster for photographs, reproducible plot scripts, and consistent output naming.
- Check both the **individual exported figure** and how it appears at normal size on the **actual report page**. Do not accept unreadable confusion-matrix labels, collapsed multi-panel plots, overly small tables, or figures stranded on near-empty pages.
- Captions must state *what is plotted* and *what scientifically relevant conclusion follows*, without overstating evidence.
- Use a controlled layout with informative whitespace; no unnecessary pages or enormous gaps.

## Required QA loop

1. Produce a short internal issue list prioritized as critical / major / minor.
2. Fix all critical issues and as many major/minor issues as defensible.
3. Re-run affected tests, figure generation, experiments where necessary, and bibliography/reference checks.
4. Compile the LaTeX report and render **every PDF page** to images.
5. Inspect each page for legibility, clipping, empty space, bad floats, typography, broken math, citations, and reference consistency.
6. Revise and repeat until there are no material technical, experimental, or visual problems within the available environment.
7. Validate GitHub Markdown in README and wiki source: correct links, `$...$`/`$$...$$` or `math` fences, rendered diagrams, and readable tables.
8. Summarize changes, unresolved issues and real tests performed. Do not claim a flawless or peer-reviewed paper merely because a checklist was completed.

Do **not** publish yet. Preserve the student's reflection placeholder, and finish by asking the student to add the reflection in their own words before running Prompt 03.
