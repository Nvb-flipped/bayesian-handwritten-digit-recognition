# Prompt 03 publication record

9 October 2026. The student approved uploading the complete audited Git history, including their name, student ID and authentic reflection in the report, and requested topic-based repository and local folder names. The initial automatic approval rejection was resolved by that explicit approval; no public upload occurred before it.

## Verified public repository

- [Public repository](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition), owner `Nvb-flipped`, default branch `main`, API `private=false`.
- [Report](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/blob/main/report/main.pdf).
- Source, configurations, tests, report source/PDF, original prompts, complete consulted skill instructions and experimental evidence are included. Raw dataset caches, environments and temporary files are excluded. Seven small checkpoints are retained because checkpoint reloads and reproduction audits use them.
- Initial published commit: `07c03704b1a95ace8ed8933341f03553655eacbc`. Later commits update publication links and verification records; the current public `main` commit is authoritative.
- Local project folder name: `bayesian-handwritten-digit-recognition` (previously `AI Assignment 2`). The Python package remains `bayes_digits`.

## Executed verification

Prepublication tests: **9 passed**. The full fresh reproduction, checkpoint reloads and independently regenerated metrics passed; all **18 primary arrays** matched bitwise in the recorded environment. All **25 executed evidence files**, seven numerical report includes and the original student reflection are preserved. Section 1's seven prompt excerpts, twelve archived skill documents and original selection rationale remain verified. Publication edits are limited to status/links, wiki documentation and verification/publishing helpers; no model was retuned.

The Git history scanner checks every reachable blob for supported credential patterns, excluded cache/environment paths and assets of at least 10 MB. No findings were reported. This is a scoped pattern audit, not a guarantee that every conceivable secret format is detectable. Final PDF and staged-byte provenance checks are recorded under `results/`.

The first publication compile failed because the sandbox could not fetch Tectonic's official TeX bundle. Compilation succeeded with authorized network access. The long repository URL then triggered an overfull line; separating it into its own paragraph repaired the layout. The final successful build and visual review are recorded separately from the retained initial failure log.

## Wiki: published after web initialization

GitHub's repository API confirms `has_wiki=true`. The signed-out public browser redirects the uninitialized wiki route to the source repository. At the student's request, an authenticated CLI check of the separate wiki Git URL was attempted; `git ls-remote` returned **Repository not found**. No wiki clone or push was performed before the initial Home page existed. Enabling the feature has not created its first page.

[GitHub's documented workflow](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages) creates an initial page on GitHub before cloning its separate Git repository. The available CLI has no working first-page initialization path here. This initially blocked wiki publication. The student subsequently signed in through the Codex browser and created Home, resolving it. The CLI then cloned and published the six pages on the observed wiki default branch, master.

Six canonical source pages are preserved in [docs/wiki](wiki/Home.md): Home, Algorithm-and-Mathematics, Dataset-and-Experiment-Protocol, Results-and-Visualization, Reproduction and AI-Workflow. Mathematics uses GFM `$`/`$$`, scientific figures use public raw PNG URLs, and the publishing helper converts source links into absolute wiki/repository routes.

The completed initialization step was: sign in as the repository owner, open Wiki, create **Home**, and save initial text. For subsequent synchronization, run from the project root:

```powershell
.\.venv\Scripts\python.exe scripts/publish_wiki.py --publish
```

Without `--publish`, the helper only prepares six pages in ignored `tmp/wiki-ready/`. It refuses to clone or push an inaccessible/uninitialized wiki, checks the clone's exact remote and uses normal fast-forward Git operations. Public Home, Algorithm-and-Mathematics and Results-and-Visualization were inspected in the browser. The first rendering rejected the operatorname macro and consumed matrix row separators; upright function names and fenced math repaired both. Final equations, correct 2-by-2 matrices, three figures, tables and navigation are readable. The verified wiki link is now included in README/report. Prompt 04 remains a subsequent submission audit.

[Verified public wiki](https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition/wiki). Wiki content commit: `49cdaf0` (the first six-page upload was `544f19c`). All six public routes were checked without authentication.

## Final public and relocation checks

Anonymous verification matched all 172 blobs of content commit 1618499177e6a530620500bcdff13a067f442ff0, checked required source/report/evidence files, and confirmed the public PDF is byte-identical. All six wiki routes returned HTTP 200 without authentication and all three embedded figure files matched local bytes. The separate wiki content exactly matches the publishing helper's transformed sources. The public README links and measured-result table were inspected on GitHub.

The local folder is now bayesian-handwritten-digit-recognition. Windows initially interrupted the move on hidden directories and ignored test links; 91 remaining regular files were copied and SHA-verified before the obsolete folder was removed. At the new path, all nine tests passed again (4.07 s), pip check found no broken requirements, and the artifact audit passed. Experimental results, original prompts, archived skill documents and student reflection are unchanged. Initial failures are documented and resolved; no publication or relocation blocker remains. Prompt 04 is the remaining requested separate stage.
