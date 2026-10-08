# Actual AI workflow

8 October 2026. The user asked the agent to read the assignment PDF, AGENTS.md and Prompt 01 and execute it completely.

## Instructions and location

The initial chat was in Assignment 1. Requested Assignment 2 files were absent there and found in the sibling Assignment 2 directory. All new work was performed in Assignment 2; Assignment 1 source and artifacts were not edited.

The entire course PDF was extracted with pypdf and its page rendered with Poppler and inspected. AGENTS.md supplied persistent rules; Prompt 01 decomposed research, implementation, experiments and reporting and explicitly deferred publication until Prompt 03.

## Consulted skills

Materially applied: literature-review (primary sources/provenance), experimental-design (matched controls/seed replication), scikit-learn (splits/baselines/metrics), scientific-visualization plus publication guidelines (scales, vector output, sample sizes), machine-learning/PyTorch patterns/training recipe (seeding, tiny-batch, checkpoints), PDF (extraction/rendering), LaTeX compile (compiler detection/build).

Latex-paper-en and scientific-writing were inspected as candidates; their review services/scripts were not used. No subagent or paid image generator was used. The Scientific Agent Skills reference is acknowledged in the report, following the materially applied local skills' instructions.

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

## Student authorship

The agent authored all technical code/report prose. The named learning-reflection section contains **STUDENT REFLECTION REQUIRED**. It must be replaced by student-authored text. No personal experiences were invented.
