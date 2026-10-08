# Final report and figure refinement

Completed locally on 8 October 2026, following the user's final refinement request and Prompt 02. This is AI self-review, not independent peer review. The comparison baseline is local commit `93b625e`.

## Issues and improvements

| Priority / issue | Final change |
|---|---|
| Major: negative F1-deficit range could imply impossible scores | Figure 4 now plots every seed's actual $1-F_1$ value, arithmetic means and observed min–max spans on a 0–0.12 axis. No SD bars are clipped or relabeled as intervals. All 60 measured values remain in figure_data.json and match metrics.json exactly. |
| Major: small/crowded Figures 2/4/5/6 | Figure 2 enlarges native digit pixels in a labeled 2×5 grid. Figure 4 uses compact integer-percent confusion annotations with an explicit caption and unchanged full-precision proportions. Figure 5 uses larger panels, shared positive NLL limits and seed line/shape encodings. Figure 6 uses equal-size reliability points, all 30 bin counts including zeros, exact proportion axes and separately normalized disagreement ECDFs with group sizes. |
| Major: avoidable whitespace in original pages 9/11/12 | Adjusted float placement, spacing and figure sizes; related plots/tables share pages. Shortened duplicated reproduction/publication text. The stronger literature discussion and useful toy diagram fit within 15 pages, the same total as the reviewed baseline; no global font shrink or page-count padding. Numbered figure identities 1–9 are retained. |
| Major: weak rationale for a 2021 method | Section 1.2 connects Laplace Redux's modular design to the study's auditable 330-parameter head and matched inference controls. VBLL's frozen-feature post-training is explicitly acknowledged as feasible. NatPN's density-driven mechanism is distinguished. Selection reflects mathematical inspectability, not measured superiority over unexecuted newer methods. Paper defaults and project adaptations are separated. |
| Useful mathematical explanation | Added an unnumbered, explicitly labeled toy diagram: full covariance versus diagonal precision, identical centers and equal axis scales, radius-one Mahalanobis contours and exact logit-contrast densities. Marginal variances 3/4 versus 2/3 coexist with contrast variances 1 versus 4/3. These are not 68% joint regions or new ten-class measurements. Contours are numerically verified. |
| Minor: metadata and documentation consistency | README, wiki sources, figure review and AI-use records reflect the actual plots. Original execution/environment evidence remains immutable; new generator hashes live in the figure manifest. The initial Prompt 02 review is explicitly historical. |

## Executed verification

- Nine pytest tests passed in 8.42 seconds; the existing covariance test also verifies the plotted contours. [Log](../results/logs/tests.log).
- Fresh full reproduction into the ignored temporary directory, checkpoint reloads and independent metric regeneration passed: all 18 primary arrays and summary metrics match. [Log](../results/logs/refinement_reproduction_audit.log), [audit](../results/audit.json).
- Review audit regenerated 72 diagnostic metric records, checked checkpoint/configuration hashes, all eight used citation keys and seven Markdown source pages. [Log](../results/logs/refinement_review_audit.log), [audit](../results/review_audit.json).
- The new [refinement audit](../scripts/audit_refinement.py) verifies all 25 executed evidence files and seven numerical table files byte-for-byte against `93b625e`, all 18 arrays, all 60 F1 observations, confusion proportions and toy geometry. [Log](../results/logs/refinement_evidence_audit.log), [machine-readable audit](../results/refinement_audit.json). No model, split, prior selection, result or recorded runtime changed.
- Tectonic compiled the final PDF successfully. All 15 pages were rendered with Poppler and visually inspected; nine tables, nine numbered figures, the extra toy diagram, equations, captions and references were checked. No overfull/underfull boxes, duplicate destinations or unresolved final-pass references. [Compile log](../results/logs/compile.json), [PDF validation](../results/report_validation.json).
- All ten individual PDF/SVG/300-DPI PNG exports were inspected, with embedded PDF fonts and recorded source/export hashes verified. [Export validation](../results/figure_export_validation.json). README and six wiki sources were rendered locally as GFM with math and inspected; public GitHub rendering remains for Prompt 03. [Markdown validation](../results/markdown_validation.json).

The original experiment's plot-module hash describes its earlier plotting code. Artifact checks verify every unchanged training/evaluation module against that historical environment and verify current plotting code against the new figure manifest; they do not rewrite an execution record to imply the revised plots existed during training.

## Findings from verification and remaining limits

The first refinement preview exposed confusion-label crowding and a clipped covariance-panel title. Both were corrected before the final compile. NatPN HTML retrieval returned an internal tool error; the primary PDF was accessible and verified the relevant mechanism. Tectonic emitted a Fontconfig configuration diagnostic, but compilation succeeded and final fonts/text were verified. There is no unresolved verification failure.

The scientific limits remain: one small dataset/split, three shared-test initialization seeds, local Gaussian inference conditional on point-estimated features, sparse reliability bins and only eight representative errors. The toy diagram explains covariance algebra, not an experimentally isolated cause of the ten-class result. Newer methods were reviewed, not benchmarked. The unfavorable Laplace probability scores are preserved.

The student's reflection remains empty by design. GitHub publication and the public source URL remain for Prompt 03; earlier invalid authentication will need attention then. No publication was attempted during this refinement.
