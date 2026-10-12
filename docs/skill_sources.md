# Skill provenance and redistribution

The historical consultation record identifies guidance actually applied in Prompts 01–04. Installation alone is not evidence of use. The [manifest](skill_documents/manifest.json) retains exact installed-document SHA-256 hashes and original source locators. No matching upstream commit is invented.

Five MIT instruction documents remain public with the [complete K-Dense permission/copyright notice](skill_documents/LICENSE-K-Dense.txt). Seven other copies were removed from the current tree because complete permission/notice provenance for the installed copies was not established. The scikit-learn instruction declares BSD-3-Clause; that is not replaced with a blanket MIT license. Upstream links and historical hashes remain; private plugin instructions have no invented public URL. Old commits still contain these copies. This normal commit does not remove historical exposure.

| Skill | Actual historical contribution | Complete documentation / source |
|---|---|---|
| `literature-review` | Prompt 01; materially applied: Primary-source provenance and bounded literature review | [Installed instruction](skill_documents/literature-review/SKILL.md.txt) |
| `experimental-design` | Prompt 01; materially applied: Matched controls and seed replication | [Installed instruction](skill_documents/experimental-design/SKILL.md.txt) |
| `scikit-learn` | Prompt 01; materially applied: Splits, baselines and metric conventions | [Upstream package](https://github.com/k-dense-ai/scientific-agent-skills) (installed-copy hash in manifest) |
| `scientific-visualization` | Prompts 01/02 and refinement; applied: Honest encodings, vector export and final-size inspection | [Installed instruction](skill_documents/scientific-visualization/SKILL.md.txt) |
| `scientific-writing` | Inspected in 01; applied in 02: Evidence-bound prose and claim limitations; no external review service | [Installed instruction](skill_documents/scientific-writing/SKILL.md.txt) |
| `statistical-analysis` | Prompt 02; materially applied: Replication units, seed spread and integration variability | [Installed instruction](skill_documents/statistical-analysis/SKILL.md.txt) |
| `latex-paper-en` | Inspected in 01; applied in 02/refinement: Mathematical exposition, captions and section review; external services unused | [Upstream package](https://github.com/bahayonghang/academic-writing-skills) (installed-copy hash in manifest) |
| `machine-learning` | Prompt 01; materially applied: Deterministic training and model-evaluation guidance | Local installed instruction; hash/provenance retained, no verified public upstream |
| `pytorch-patterns` | Prompt 01; materially applied: Training, device handling and checkpoint checks | Local installed instruction; hash/provenance retained, no verified public upstream |
| `pytorch-training-recipe` | Prompt 01; materially applied: Reproducible training and small end-to-end checks | Local installed instruction; hash/provenance retained, no verified public upstream |
| `pdf` | Prompts 01/02 and refinement; applied: Extraction, Poppler rendering and page inspection | Local installed instruction; hash/provenance retained, no verified public upstream |
| `latex-compile` | Prompts 01/02 and refinement; applied: Compiler detection and actual project compilation | Local installed instruction; hash/provenance retained, no verified public upstream |

## Prompt 05 consultation

Nature Figure, scientific visualization and scientific figure composition guided final-size typography, accessible encodings, exact-data plots, vector export, alignment and collision checks. Plot-from-data reinforced using saved arrays rather than reading pixels. Statistical-analysis and experimental-design guidance informed paired image resampling and separation of seed, integration and image-sampling variability. Literature-review and scientific-writing guided verified sources and bounded interpretations; LaTeX and PDF guidance supported compilation and page inspection. Scikit-learn guidance supported metric/bin conventions.

Agent-figure-gallery was inspected but its external gallery workflow was not run. Scipilot and Markdown/Mermaid guidance were inspected; no external diagram generator or Mermaid renderer was executed (the editable diagram uses TikZ). EDA and analytical-method-validation were inspected; no laboratory-assay validation framework or automated EDA report was applied. PyMC and plot-from-image were not used. No subagent, external manuscript-review service, human peer review or generative quantitative imagery is claimed. New consultation does not retroactively change the historical usage record.

Original task files are under [prompts](../prompts/05_FINAL_REFINEMENT.md); seven [verbatim excerpts](prompt_excerpts.json) remain verified. [AI-use history](ai_usage.md) and [Prompt 05 audit](refinement_05.md) distinguish consultation, execution and evidence.

Original project code has not been relicensed by this refinement. Public visibility is not a blanket license for report, reflection, dataset or third-party documentation. UCI dataset terms remain separately attributed.
