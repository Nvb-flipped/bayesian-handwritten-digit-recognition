# Codex Prompt 01 — Research, implement, experiment, and draft the report

Work inside the **current project folder**. Execute this task autonomously, not merely as a plan.

## Source of truth

1. Read `AIassign2.pdf` completely and preserve its requirements.
2. Read `AGENTS.md` completely.
3. Discover the skills actually available to this Codex environment (project-local and/or global). Inspect the instructions for useful skills before the corresponding work. Prefer research, Bayesian/statistical ML, symbolic mathematics, dataset analysis, experimental design, scientific visualization, LaTeX, PDF verification, and Git/GitHub workflows when available.
4. Inspect the existing files, Python/GPU environment, tools, Git status, and authentication state. Do not assume specific hardware or authentication.

## Goal and scope

Implement a well-grounded **recent probability- or Bayes-based classification/recognition algorithm for computer vision or pattern recognition**, including all technical deliverables and a rigorous LaTeX report compiled to PDF. The assignment explicitly permits AI to write all code and asks for the AI workflow to be documented. The student's learning reflection must remain student-authored.

### Phase A — literature and method choice

- Search verified **primary papers**. Develop at least **three substantive candidate methods**, when suitable candidates exist, and compare: publication/year, mathematical basis, relevance to the course, reproducibility, compute/data requirements, evaluation protocol, and risk.
- Prefer genuinely recent publications (approximately 2021–2026) while citing older foundational Bayesian/probabilistic work when appropriate. If a simpler or older method is selected, do not falsely represent it as recent; explain the justification and assignment-fit issue explicitly.
- The selected method must rely substantially on probability or Bayesian inference, not merely a neural classifier ending in softmax.
- Choose an accessible image or recognition dataset with documented provenance. Avoid an unjustifiably large or expensive study. Define research questions/hypotheses that tests can actually answer.
- Write a truthful record of AI literature-search queries, candidates, verified references, model choice, project decisions, and consulted skills. Cite the real source URLs/DOIs. Do not invent search history.
- Produce an in-depth mathematical exposition: notation, prior/likelihood/posterior if applicable, assumptions, inference/estimation process, prediction rule, objective, derivation steps, a small illustrative example when useful, and complexity/limitations. Verify important symbolic or numerical identities against the implementation.

### Phase B — software implementation

- Organize modular Python code and CLI scripts suited to the **actual selected algorithm**; create `src/`, `configs/`, `scripts/`, `tests/`, `results/`, `docs/`, `report/`, and supporting files as needed. Avoid a monolithic script.
- Dataset acquisition/preprocessing: record source and terms where relevant, apply reproducible splits, fit preprocessing on training only, document class balance, prevent leakage, and save split seeds/indices when practical.
- Implement the target method and **at least one scientifically meaningful baseline**; prefer two complementary baselines when feasible (e.g. simple statistical/probabilistic and common discriminative baseline). Match preprocessing/splits and tune fairly.
- Implement appropriate deterministic seeding, device support, config capture, evaluation, and model serialization as applicable.
- Before full experiments, verify imports, data shapes, split isolation, inference/probability normalization when applicable, mathematical formulas, checkpoints, and one small end-to-end run. Add meaningful automated tests.

### Phase C — actual experiments and figures

- Execute experiments, not just write scripts. Use a proper train/validation/test strategy; select models with validation only. Prefer at least **three independent seeds** for stochastic training if feasible; otherwise explain the computational/algorithmic reason.
- Report suitable aggregate and per-class classification metrics (accuracy, macro-F1, precision, recall, confusion matrix). If calibrated/probabilistic outputs are available, evaluate appropriate negative log-likelihood, Brier score, calibration/reliability and uncertainty; avoid invalid comparisons.
- Consider a small controlled ablation or sensitivity analysis tied to the probability/Bayes mechanism (prior choice, parameter estimation, sample size, posterior approximation, etc.) if relevant, with a stated hypothesis. Never create meaningless plot quantity simply to increase the figure count.
- Preserve raw or per-example results when feasible. Make every published figure, table, and scalar traceable to saved outputs.
- Create figures appropriate for the actual method, with publication-quality styling: data/class distribution; method/inference flow; baseline comparison with variation where available; a readable normalized confusion matrix; class-level results; probability calibration/uncertainty and convergence plots when methodologically valid; failure cases where image-based visualization helps.
- Every figure must have a purpose and be **legible in the final compiled PDF**, not just when opened alone. Provide informative captions and analyze results rather than merely describe numbers.

### Phase D — report and documentation

- Produce a comprehensive undergraduate technical report in LaTeX, compiled to `report/main.pdf` (or a clearly documented equivalent path). If no page limit is specified, aim for the technical depth of approximately **9–14 well-used pages**, not artificial filler.
- Cover exactly the instructor's six required items, including detailed and truthful AI use: how AI was instructed to research, how `AGENTS.md` established consistent constraints, how engineered prompts decomposed the work, what installed skills actually contributed, how the method was implemented, experiment settings and measured results, and public code link once available.
- Include mathematics, step-by-step derivations, algorithm pseudocode, architecture/inference diagram where useful, dataset and baseline justifications, full parameter table, experiment protocol, meaningful graphs/tables, evidence-driven discussion, and limitations.
- Use only verified citations. Make the technical description agree with real code, configs, logs, and generated metrics.
- In Section 5 or the relevant reflection section, insert exactly an explicit **STUDENT REFLECTION REQUIRED** placeholder. Do not invent the student's thoughts/learning experiences. Do not mislabel that placeholder as complete.
- Include the course/title/student metadata from `AGENTS.md` in the LaTeX title area.
- Create a reproducible README and detailed reference documentation in GitHub Flavored Markdown, with **GitHub-safe math**: `$...$` inline, standalone `$$...$$` blocks, or fenced `math` blocks. Use fenced `mermaid` code blocks for diagrams if applicable. Create a factual AI-use log and bibliography/provenance record.
- Prepare `docs/wiki/` Markdown sources for a useful GitHub wiki (Home, Method-and-Mathematics, Dataset-and-Protocol, Experiments-and-Results, Reproduction, AI-Workflow), with working links and no contradictory figures. Wiki will be published separately in Prompt 03.

## Local acceptance

Do not stop at code creation. Execute the entire local training/evaluation pipeline, run tests, generate and inspect figures, compile the report, inspect every PDF page, and fix errors. Do not fabricate successful runs. Do not publish to GitHub yet; publication is deliberately handled in Prompt 03 after quality review and student reflection.

Your completion report must state: selected paper/method and URLs; justification; dataset/splits; configuration; actual baselines and measured results; test status; PDF path; exact remaining work; and any blockers. Update truthful logs/README with real execution results.
