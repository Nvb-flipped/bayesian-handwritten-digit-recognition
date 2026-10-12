# Reproduction

[Home](Home.md) · [Method](Algorithm-and-Mathematics.md) · [Results](Results-and-Visualization.md)

The [current README](../../README.md) provides complete clean-clone Windows and POSIX instructions, pinned requirements and portable Tectonic compilation. Python 3.12 is verified; CPU computation is sufficient. No private Codex runtime or other assignment is required.

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-review.txt
.\.venv\Scripts\python.exe scripts/reproduce.py
Push-Location report
tectonic -X compile --untrusted main.tex
Pop-Location
~~~

The runner checks dependencies, all 13 tests, smoke execution, checkpoint reloads, a full rerun in ignored tmp/reproduction, saved numerical equality, paired analysis, figures/tables and historical audits. It retains primary measurements. Clone complete Git history for audits against a28a563, 93b625e and 43b8acd; shallow clones need `git fetch --unshallow`.

A fresh independent Windows CPU-wheel environment reproduced all 18 arrays bitwise. Cross-platform bitwise equality is not guaranteed; CI runs tests and smoke on Ubuntu and Windows. macOS instructions are provided but not executed here. Repeated fixed-model Monte Carlo diagnostics remain in results/review_diagnostics and can be regenerated with scripts/review_diagnostics.py. They do not select new models.

The [Prompt 05 audit](../refinement_05.md) records current checks and limitations. Earlier dated records remain historical. [Metadata redactions](../../results/refinement_05/metadata_redactions.json) change current command/path strings only; earlier public commits still expose them. [Skill provenance/licensing](../skill_sources.md) preserves hashes and attribution without asserting redistribution rights for undocumented copies.
