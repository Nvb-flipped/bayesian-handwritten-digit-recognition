# Actual skill documentation and consultation status

This index accompanies Section 1 of the report. Status is taken from the recorded [AI-use history](ai_usage.md), not inferred from installation alone. Guidance is distinct from executed scripts or experiment evidence.

The linked snapshots preserve the complete installed `SKILL.md` documents byte-for-byte, including their original metadata, attribution and licensing declarations where supplied. They use `.txt` to distinguish archived instructions from executable project skills. Referenced helper scripts/assets are part of the original packages, not asserted to have been executed or fully vendored here. [Manifest](skill_documents/manifest.json) records original document locators, actual available upstream metadata and SHA-256 hashes; no upstream commit is invented.

| Skill | Recorded consultation | Actual contribution | Complete instruction document |
|---|---|---|---|
| `literature-review` | Prompt 01; materially applied | Primary-source provenance and bounded literature review | [Full installed instruction document](skill_documents/literature-review/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `experimental-design` | Prompt 01; materially applied | Matched controls and seed replication | [Full installed instruction document](skill_documents/experimental-design/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `scikit-learn` | Prompt 01; materially applied | Splits, baselines and metric conventions | [Full installed instruction document](skill_documents/scikit-learn/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `scientific-visualization` | Prompts 01/02 and refinement; applied | Honest encodings, vector export and final-size inspection | [Full installed instruction document](skill_documents/scientific-visualization/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `scientific-writing` | Inspected in 01; applied in 02 | Evidence-bound prose and claim limitations; no external review service | [Full installed instruction document](skill_documents/scientific-writing/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `statistical-analysis` | Prompt 02; materially applied | Replication units, seed spread and integration variability | [Full installed instruction document](skill_documents/statistical-analysis/SKILL.md.txt) ([upstream package](https://github.com/k-dense-ai/scientific-agent-skills)) |
| `latex-paper-en` | Inspected in 01; applied in 02/refinement | Mathematical exposition, captions and section review; external services unused | [Full installed instruction document](skill_documents/latex-paper-en/SKILL.md.txt) ([upstream package](https://github.com/bahayonghang/academic-writing-skills)) |
| `machine-learning` | Prompt 01; materially applied | Deterministic training and model-evaluation guidance | [Full installed instruction document](skill_documents/machine-learning/SKILL.md.txt) |
| `pytorch-patterns` | Prompt 01; materially applied | Training, device handling and checkpoint checks | [Full installed instruction document](skill_documents/pytorch-patterns/SKILL.md.txt) |
| `pytorch-training-recipe` | Prompt 01; materially applied | Reproducible training and small end-to-end checks | [Full installed instruction document](skill_documents/pytorch-training-recipe/SKILL.md.txt) |
| `pdf` | Prompts 01/02 and refinement; applied | Extraction, Poppler rendering and page inspection | [Full installed instruction document](skill_documents/pdf/SKILL.md.txt) |
| `latex-compile` | Prompts 01/02 and refinement; applied | Compiler detection and actual project compilation | [Full installed instruction document](skill_documents/latex-compile/SKILL.md.txt) |

The installed `pymc`, `exploratory-data-analysis`, `analytical-method-validation` and `markdown-mermaid-writing` have no recorded material role. Installation does not establish use. No mathematical software skill or independent reviewer is credited merely because it was available; mathematical identities were verified using the implemented numerical/autograd tests.

Prompt 01 inspected `scientific-writing` and `latex-paper-en` but did not invoke their review services/scripts. Prompt 02 materially applied their procedural guidance. No paid image generation, subagent or external manuscript-review service was used. Current section refinement applies LaTeX section-writing, scientific-visualization and PDF-verification guidance; the existing skills acknowledgment is retained.

The original task instructions remain in [Prompt 01](../prompts/01_RESEARCH_IMPLEMENT_REPORT.md), [Prompt 02](../prompts/02_CRITICAL_REVIEW_AND_FIGURES.md), [Prompt 03](../prompts/03_PUBLISH_GITHUB_AND_WIKI.md) and [Prompt 04](../prompts/04_FINAL_SUBMISSION_AUDIT.md). [Verbatim-excerpt ledger](prompt_excerpts.json) records exact text, source headings, line numbers and file hashes. The [workflow diagram source](../report/instruction_workflow.tex) distinguishes verified repository publication from the pending wiki pages and Prompt 04 audit.

This index, snapshots and original prompt records are available in the public topic-named repository linked in the report. Prompt 03 published the audited history on 9 October 2026; the report contains its verified URL. Six separate wiki pages are published and synchronized from the main repository. Prompt 04 remains pending.
