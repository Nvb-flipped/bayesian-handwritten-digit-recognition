# Section 1 instruction/discovery refinement

9 October 2026. Scope: explain how the student's documented instructions guided Codex, without changing the method, experiment evidence or student reflection. Baseline: local commit `43b8acd`. This is AI self-review, not independent human peer review.

## Section objective and structure

An examiner should understand the instruction hierarchy, authentic research process, selection criteria and effects of staged review from the report alone.

1. Page 2: course requirements, persistent AGENTS rules, executable prompts, skill guidance; vector workflow and actual skill contributions.
2. Page 3: seven verified prompt extracts with file identifiers, purposes and recorded responses; actual algorithm queries and verification fallbacks.
3. Page 4: preserved three-method comparison and Laplace Redux rationale; Prompt 02's technical/figure improvements; complete-record pointers and pending publication.

The TikZ diagram uses distinct human/activity/output categories and labeled arrows. Its dashed feedback loop represents repairs and rechecks. GitHub/wiki publication and the post-publication audit are explicitly pending. A separate workflow caption counter preserves numbered experimental Figures 1–9.

## Claim–evidence map

| Claim | Existing evidence | Status |
|---|---|---|
| Persistent rules and staged prompts guided execution | Original AGENTS.md, course PDF and all four original prompt files; actual AI-use record | Supported; originals preserved byte-for-byte |
| Prompt excerpts are authentic | [Excerpt ledger](prompt_excerpts.json): exact text, heading, line and SHA-256; compiled PDF text checks | Seven supported extracts; explanatory responses explicitly summarized |
| Three candidate methods were compared and primary sources checked | [Research record](research.md), original candidate table and verified bibliography | Supported; bounded narrative review, no exhaustive coverage claim |
| Laplace was selected for mathematical inspectability | Existing substantive selection rationale and pre-execution controls in research/configuration records | Preserved; no measured superiority claim over NatPN/VBLL |
| Skills contributed in distinct stages | [AI-use record](ai_usage.md), [skill index](skill_sources.md), twelve full instruction-document snapshots and hashes | Material use distinguished from inspection/availability; no helper execution inferred |
| Prompt 02 improved mathematics and figures | [Initial review](review_02.md), [refinement record](refinement_02.md), tests/reproduction logs and 72 saved diagnostic records | Supported; same-agent review and post hoc status stated |
| Scientific evidence and student authorship were preserved | [Instruction audit](../results/instruction_section_audit.json), [refinement audit](../results/refinement_audit.json), [report validation](../results/report_validation.json) | Original prompts, reflection, rationale and Sections 2 onward preserved; 25 evidence files and seven numerical table files unchanged |
| GitHub deliverables are not yet public | Existing publication deferral and earlier authentication finding | Pending Prompt 03; no URL invented |

## Verification and repairs

Tectonic compiled the 18-page report successfully. All final pages were rendered with Poppler at scale-to 1400 and individually inspected; Section 1 occupies exactly pages 2–4. The diagram is native vector drawing with readable labels at normal page size; page 2 contains no image/form draw calls. The first preview exposed an overly long horizontal arrow label; shortening it repaired the crowding. There are no overfull/underfull boxes, duplicate destinations or unresolved final-pass references. All seven prompt extracts and all five student-supplied reflection paragraphs were verified in extracted PDF text; the reflection remains on page 17.

The affected instruction, evidence and review audits passed. They verify all 25 saved experiment files, 18 primary arrays, seven numerical table files, 60 raw F1 observations, unchanged confusion proportions, covariance geometry, 72 diagnostic metric records and eight citation keys. The numerical-table audit now lists the generated tables explicitly, so the new non-numerical TikZ include is not mistaken for frozen numerical evidence. No model, split, selection or plotting implementation changed; ML tests/training were not rerun for this prose/TikZ revision. Previously executed tests remain documented as historical evidence.

All 102 recorded hash checks match both working files and staged Git blobs. The staged inventory contains no credential-pattern matches or environment/cache directories. Git's first whitespace check treated preserved CRLF archive endings as trailing whitespace; a scoped `cr-at-eol` attribute recognizes those original endings. The repeated check passes while every archived document retains its original bytes.

One evidence-audit invocation lacked the documented `PYTHONPATH=src` setting and failed on import; rerunning with that setting passed. A literal caption-text check failed on extracted typographic ligatures; using the same Unicode/whitespace normalization as the other PDF text checks verified the caption without changing the report. Initial-pass LaTeX reference warnings resolved on subsequent passes; the Fontconfig setup diagnostic remains non-blocking. No unresolved local verification failure was found.

README, six wiki source pages and the new skill-document index were rendered locally as GFM in headless Chrome with MathJax, visually inspected, and checked for table/document overflow and math errors. This is local preview verification, not verification of unpublished GitHub rendering.

## Remaining limitations

Research/review verification remains agent-conducted; it is neither independent human review nor an exhaustive search. Skill snapshots preserve complete instruction entry documents, not entire external helper packages. The existing single-dataset/split, three-seed, frozen-feature and approximate-posterior limitations remain unchanged. Publication, insertion of a verified repository URL and the post-publication audit remain for Prompts 03/04.
