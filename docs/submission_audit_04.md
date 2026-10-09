# Prompt 04 — Final submission audit

Audited 9 October 2026 under `AGENTS.md` and the original `prompts/04_FINAL_SUBMISSION_AUDIT.md`. The one-page course assignment was extracted and visually inspected again. This is final verification of the executed study; no new algorithm search or model selection was performed.

## Submission checklist

| Requirement | Verified final evidence |
|---|---|
| Correct title and student metadata | PDF page 1: Bayesian Handwritten Digit Recognition, AI Assignment #2, CISC3024 Pattern Recognition, Paco, Sou Chak Tong, U-C3-2652-3. |
| How AI found the algorithm | Section 1, pages 2–4: instruction hierarchy, seven authentic excerpts, actual search/candidate comparison, skills and vector workflow. |
| Algorithm description | Section 2, pages 5–7: likelihood/prior, MAP, exact conditional Hessian, Gaussian approximation, sampling and tested covariance example. |
| AI implementation | Section 3, page 8: modular implementation, inference diagram and verification requirements. |
| Experiment settings/results | Section 4, pages 9–17: validation selection, baselines, ablations, diagnostic and limitations. |
| Student learning reflection | Section 5, page 17: all five student-supplied paragraphs preserved without rewriting; source and compiled text checks passed. |
| Public source-code webpage | Section 6, page 17: actual repository and wiki URI annotations; public publication checked separately. |
| Final PDF | [report/main.pdf](../report/main.pdf), 18 pages. Recompiled successfully with Tectonic and every final page rendered with Poppler and visually inspected. |
| Tests/reproducibility | All nine tests passed. Fresh full reproduction matched saved metrics and all 18 prediction arrays exactly; checkpoint reloads also matched. |
| Evidence invariance | 25 saved experiment files unchanged; all 18 primary arrays and 72 diagnostic records verified. Six numerical includes unchanged; the seventh differs only in the verified SD formatting described below. |
| References and figures | Eight citation keys checked; nine numbered figures and ten numbered tables present, plus vector workflow and toy covariance diagrams. Equations, captions, bibliography and all pages checked for readability. |
| Public documentation | README and public wiki Home, mathematics, results and reproduction pages inspected in the GitHub browser. Six wiki pages synchronized via the separate wiki repository. Anonymous HTTP and exact source checks are in the publication audit. |
| Safe version control | Staged-file/provenance and full-history credential-pattern/large-file checks; normal pushes to public `main`, without force-pushing. |

## Corrections

The diagonal-Laplace NLL sample SD is 0.00019644239400501596. Three-decimal formatting previously displayed `0.000`; Table 10 now displays `0.229 ± 0.0002`. Only SD display precision changed. The numerical-table audit requires this exact replacement, derived from the unchanged summary, and byte identity for every other table entry. The public wiki already displayed this nonzero SD and agrees with the final PDF.

Obsolete current-status statements that described Prompt 04 as pending were updated in Section 1, the workflow output stage, README, skill index, acceptance page and wiki workflow. Earlier dated AI-use/publication records remain historical records; this audit supplies the current state. Reproduction documentation now identifies the Monte Carlo diagnostic by content rather than a misleading figure ordinal. No scientific figure data, selected model, test outcome or student reflection changed.

## Verification records

- [Final tests](../results/logs/submission_tests.log) and [fresh full reproduction](../results/logs/submission_reproduction.log).
- [Compile output](../results/logs/compile.json) and [PDF/text/visual checks](../results/report_validation.json).
- [Submission requirement audit](../results/submission_audit.json), [refinement/evidence audit](../results/refinement_audit.json), [instruction audit](../results/instruction_section_audit.json) and [diagnostic/citation audit](../results/review_audit.json).
- [Markdown checks](../results/markdown_validation.json), [staged provenance](../results/git_provenance_validation.json), [public-source/wiki verification](../results/publication_audit.json) and [history scan](../results/publication_history_audit.json).

The tracked publication record identifies the verified content commit before the final verification-record commit, avoiding a self-referential commit hash. The final pushed HEAD is checked again after that commit and reported to the student.

## Results and remaining limits

Laplace: 97.69% ± 0.16% accuracy and NLL 0.151 ± 0.003. Separately selected MAP: 97.78% ± 0.28% and NLL 0.099 ± 0.003. Gaussian NB: 91.94% and NLL 0.630. SD describes three initialization seeds on one fixed 360-image test set, not a confidence interval. The unfavorable probability-quality result remains in the report.

This is one small dataset/split with three neural initializations, a local Gaussian posterior over a frozen head, coarse prior choices and finite Monte Carlo integration. Representation uncertainty, writer separation and OOD performance were not evaluated. Reproduction was verified in the recorded local environment, not across all platforms. These checks are AI self-review, not independent human peer review.

No unresolved mandatory technical verification failure remains. Initial-pass reference warnings resolved during recompilation; no final unresolved references or layout-box warnings were found. Earlier publication/compile/wiki failures and their repairs remain documented in the historical records.

Public [source repository](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition), [PDF](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/blob/main/report/main.pdf) and [wiki](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/wiki) are real publication destinations. The student's remaining action is to submit the final PDF through UMMoodle under the course instructions. No UMMoodle upload or Turnitin check was performed by the agent.
