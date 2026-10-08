# Codex Prompt 03 — Public GitHub publication and optional wiki

Read `AGENTS.md`, `AIassign2.pdf`, and actual local project status. This prompt authorizes publishing the completed **Assignment #2 project as a new PUBLIC GitHub repository**, and publishing its wiki if supported. Do not overwrite another repository or leak secrets.

## Preconditions and local review

1. Confirm the student's authentic reflection has been provided and inserted into the report. If not, stop publication and ask for that content; never invent the reflection.
2. Verify actual code, configs, figures, data provenance, tests, reproducibility instructions, report/PDF and citation links. The selected target is a new project repo, with proposed name `cisc3024-ai-assignment-2`; if that name is unavailable, propose a non-destructive alternative rather than overwriting anything.
3. Audit tracked/staged files and Git history for secrets, tokens, passwords, personally sensitive unrelated files, dataset caches, model blobs, local environments, and large unnecessary assets. Be mindful the report title page intentionally includes the student ID, so the user should understand it will be public.
4. Ensure `.gitignore`, public README, report and documentation are accurate. Treat wiki pages as technical documentation, not a substitute for the assignment PDF.

## Create and publish repository

- Check existing Git remotes/repo names first. If no GitHub CLI is available, first check whether a connected GitHub integration or other authorized method can perform publication. Do not assume authentication.
- Prefer `gh` using an authenticated account when available. For a new local Git repository that already has commits, a typical supported command is:

  ```powershell
  gh repo create cisc3024-ai-assignment-2 --public --source=. --remote=origin --push
  ```

  Adapt to observed state and existing remotes. If the repository is already created, push safely without creating a duplicate. Never force-push unrelated history.
- Verify visibility is **public** and README/source/PDF files are accessible using the actual repository URL. Capture the exact URL and commit hash.
- Insert the **real** public source URL into README and the LaTeX report (required by the instructor), recompile the PDF, inspect it, commit and push the update, and verify the final public files. If updating README/report changes tracked results, reconcile links/metadata coherently.

## Wiki — desired if technically possible

GitHub's wiki is a **separate Git repository**, not merely a `docs/wiki/` directory. Prefer `docs/wiki/` as version-controlled source in the main repository, with a synchronized published wiki.

1. Enable the repository wiki using either GitHub repository Settings → General → Features → Wikis or:

   ```powershell
   gh repo edit --enable-wiki
   ```

2. Ensure the wiki exists with an initial **Home** page. If a Git wiki cannot be cloned until an initial page is created, create the first page through the GitHub **Wiki** web UI (using any available authorized browser capability). If only the user can complete this UI action, give precise one-time steps and continue after they do so.
3. Clone from the actual GitHub owner/repo URL using the verified pattern:

   ```powershell
   git clone https://github.com/OWNER/REPO.wiki.git
   ```

   Replace `OWNER/REPO` with the actual repo. Do not try this URL before the wiki is initialized. Keep wiki clone **outside** the main repository's tracked tree or in a Git-ignored staging path.
4. Synchronize the factual pages from `docs/wiki/` (create/edit as needed). At minimum include:
   - `Home.md`: purpose, navigation, report/source links;
   - `Algorithm-and-Mathematics.md`: probability model, notation, verifiable derivations;
   - `Dataset-and-Experiment-Protocol.md`: provenance, preprocessing, splits and settings;
   - `Results-and-Visualization.md`: actual measured results, analyses, linked figures;
   - `Reproduction.md`: tested setup and execution instructions;
   - `AI-Workflow.md`: `AGENTS.md`, prompts, actually used skills, scope and limitations.
5. Write valid **GitHub Flavored Markdown**, particularly for mathematical expressions: `$...$` inline, standalone `$$...$$` display, or fenced `math` blocks. Link visuals using URLs/paths that work **from the wiki**, not relative paths that only work inside the main repo. Use fenced `mermaid` for supported process diagrams if useful.
6. Commit and push the wiki pages to the wiki's own default branch; verify public wiki Home and at least two substantive content pages in the browser or via available read-only checks. Verify linked equations, figures, tables and navigation.
7. Add the actual wiki URL to README. Keep the main repository's documentation and wiki logically consistent.

## Handle blockers precisely

- If `gh` is absent, explain how to install/login and, where permitted, use a connected GitHub integration. Never pretend to publish.
- If browser login or authorization is required, ask the user only for the authentication action; never request a password or token in chat.
- If the GitHub wiki feature is inaccessible, permission-restricted, or uninitialized and can't be edited, **still finish public repository publication** where possible, preserve `docs/wiki/`, and report exact manual steps for wiki activation.
- Do not claim the wiki is published merely because files exist under `docs/wiki/`.

## Final verification and summary

Provide verified items only:

- GitHub public repository URL and visibility;
- final commit SHA;
- report path and GitHub link;
- all required project content publicly available;
- wiki enabled and public wiki URL, with pages verified (or exact blocker);
- public README and wiki GitHub math rendered correctly where inspection is available;
- remaining actionable issues, if any.
