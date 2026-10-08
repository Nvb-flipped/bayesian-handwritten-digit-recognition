# AGENTS.md

## Project identity

- **Course:** CISC3024 — Pattern Recognition
- **Assignment:** AI Assignment #2 (October 2026)
- **Student:** Paco, Sou Chak Tong
- **Student ID:** U-C3-2652-3
- **Problem:** Research, implement, and evaluate a **recent classification/recognition algorithm based substantively on probability or Bayesian theory**, applied to computer vision or pattern recognition.
- **Deliverables:** Executed, reproducible code; verified experimental evidence; an academically rigorous LaTeX report compiled to PDF; public GitHub source repository; and, when technically possible, a populated GitHub wiki.

The original `AIassign2.pdf` takes precedence over any paraphrase of the coursework requirements. All technical code is to be written by the AI agent, not the student. The section **"What I Have Learnt from This AI Assignment"** is the student's own reflection and must not be fabricated.

## Permanent project rules

### Research and algorithm suitability

- Research and verify a defensible **recent** method in primary literature before committing to the implementation. Distinguish its original contribution from older foundational probability/Bayes concepts.
- The proposed classifier must actually use probability or Bayesian theory in its defining algorithm or inference mechanism. Merely outputting softmax probabilities does not satisfy this requirement by itself.
- Identify and justify the dataset, baselines, comparisons, assumptions, parameter estimation/inference process, and metrics **after** literature review; do not hardcode an arbitrary algorithm or dataset prematurely.
- Verify bibliographic metadata; never invent sources, quotes, results, citations, or algorithm claims.

### Scientific correctness and reproducibility

- Maintain isolated training/validation/final test sets or a defensible equivalent protocol; avoid any data leakage, including preprocessing fitted on held-out data.
- Choose hyperparameters using only training/validation data. Do not tune using the final test results.
- Record dataset origin, license/usage conditions if relevant, versions, splits, seeds, configurations, hardware, runtimes, and executed commands.
- Save raw/machine-readable experiment results and scripts capable of regenerating plots and tables.
- Include mathematically meaningful derivations, definitions of symbols, assumptions, limitations, and explanations of the connection from equations to implemented code. Check nontrivial formulas symbolically, numerically, or with unit tests when possible.
- Evaluate accuracy and error patterns; for genuine probabilistic predictions also evaluate suitable **probability-quality measures** (such as log loss, Brier score, calibration) when valid. Do not require inappropriate metrics for a method that cannot meaningfully supply them.
- Use meaningful baseline(s), controlled comparisons and repeated runs where computationally feasible; label any single-run results and limitations clearly.

### Code, testing, and documentation

- Prefer maintainable, modular Python code, configuration-driven experiments, automated tests, and non-interactive entry points. Choose scikit-learn, PyTorch, PyMC, or other justified libraries based on the selected method rather than forcing a framework.
- Implement smoke tests, mathematical/numerical checks, model/data tests, and end-to-end reproduction checks. Fix underlying errors, not symptoms.
- Document the actual AI workflow and skill usage. Do not reconstruct fictional prompts or interventions.
- Keep `README.md` accessible, concise, and complete. Put detailed algorithmic documentation in `docs/` and, when available, the wiki.
- Never assert that code was run, tests passed, a PDF compiled, or GitHub publication succeeded unless actually verified.

### Figure and report quality

- Use publication-quality **evidence-driven** plots: correct scales, units, captions, readable labels at final PDF size, consistent typography and colors, appropriately marked sample sizes and uncertainty, and no cherry-picked cases.
- Prefer PDF/SVG vector plots for line art/charts; use suitably high-resolution raster images when necessary. Do not use AI-generated or decorative figures as replacements for actual measured data.
- Inspect the compiled report **page by page**, not merely the LaTeX logs; fix crowded/tiny figures, awkward page breaks, unused whitespace, broken symbols, captions, and unreadable tables. Repeat compilation and inspection as needed.
- The report must cover all six instructor requirements: (1) how AI found the algorithm, (2) description, (3) AI implementation, (4) settings/results, (5) student's learning reflection, (6) public code URL. Explain the actual roles of persistent instructions (`AGENTS.md`), engineered prompts, and installed skills.
- Reserve a clear placeholder for the student's **own** reflection; after the student supplies text, insert it faithfully rather than inventing personal experiences.
- Include course, assignment, student name, and student ID on the report title page. Avoid unnecessarily duplicating student ID throughout public README/wiki pages.
- Do not pad the report to meet an arbitrary page count. Seek technical depth, informative figures, mathematical clarity, and rigorous interpretation.

### GitHub Markdown and wiki

- Write repository and wiki Markdown in **GitHub Flavored Markdown (GFM)**. For inline math use `$...$`; for block math use separate `$$` lines or a fenced `math` block. Do **not** assume LaTeX `\(...\)` or `\[...\]` will render consistently in GitHub Markdown.
- Use Markdown headings, relative links (where applicable), fenced code blocks with languages, Markdown tables only where readable, and `mermaid` fences for supported diagrams. Check rendering on GitHub where accessible.
- LaTeX `.tex` sources use normal LaTeX math environments; do not mechanically copy Markdown delimiters into `.tex` files.
- If the wiki is available, maintain its documentation source in the main repository (for example, `docs/wiki/`), then publish to the **separate wiki Git repository** and verify the public pages. Avoid leaving two contradictory versions.
- The public repo must contain sufficient source, configuration, tests, and report material to reproduce the project. Exclude credentials, environment files, private data, large caches, raw datasets, and unnecessary checkpoints.

### Agent skills and scope

- Inspect actual installed skills before relying on them. Relevant candidates include `literature-review`, `machine-learning`, `scikit-learn`, `sympy`, `statistical-analysis`, `scientific-visualization`, `exploratory-data-analysis`, `experimental-design`, `scientific-writing`, `latex-paper-en`, `latex:latex-compile`, and `pdf:pdf`. Some may be absent; use only those actually available and do not invent their effects.
- If relevant skills require extra packages, tools, accounts, or secrets, check availability and proceed with a scientifically valid alternative where possible. Never echo credentials into files, reports, logs, or Git commits.
- Course instructions > this `AGENTS.md` > the current task prompt > optional skill suggestions. When a task-specific user instruction conflicts, ask before violating the course requirements or scientific integrity.

### Completion and external actions

- Perform all feasible technical work autonomously. Stop and ask only for necessary user-only input, such as authentication, permission prompts, or the student's personal reflection.
- Before calling any phase complete, verify the stated acceptance criteria. Report partial progress and genuine blockers explicitly.
- Publishing to GitHub is intended and authorized for this project; use a **new public repository**, never overwrite or force-push unrelated work. Confirm the intended target if an existing repository or ambiguous remote is found.
- A GitHub wiki is desirable, not a reason to block otherwise complete coursework if permissions/tools make wiki creation impossible; record the precise blocker and preserve wiki source pages for later publication.
