"""Audit quoted instructions, source snapshots and unchanged report evidence."""
import hashlib
import json
from pathlib import Path
import subprocess


def audit():
    baseline = '43b8acd'
    main = Path('report/main.tex').read_text(encoding='utf8')
    original = subprocess.check_output(['git', 'show', f'{baseline}:report/main.tex']).decode('utf8')
    anchor = r'\section{Algorithm Description}'
    end = r'\section{Webpage Link of the Source Codes}'
    assert main.split(anchor, 1)[1].split(end, 1)[0] == original.split(anchor, 1)[1].split(end, 1)[0], 'Sections 2 through 5 changed'
    assert main.split(r'\begin{thebibliography}', 1)[1] == original.split(r'\begin{thebibliography}', 1)[1], 'Bibliography changed'
    start = r'\textbf{Why Laplace Redux rather than a newer method?}'
    rationale = original.split(start, 1)[1].split(r'\subsection{Actual skill contributions}', 1)[0]
    assert start + rationale in main, 'Existing selection justification changed'
    sources = ['AGENTS.md', 'AIassign2.pdf'] + [p.as_posix() for p in sorted(Path('prompts').glob('*.md'))]
    sources += ['report/student_reflection.txt', 'report/student_reflection.tex']
    preserved = {}
    for name in sources:
        data = Path(name).read_bytes()
        assert data == subprocess.check_output(['git', 'show', f'{baseline}:{name}']), name
        preserved[name] = hashlib.sha256(data).hexdigest()
    quotes = json.loads(Path('docs/prompt_excerpts.json').read_text(encoding='utf8'))
    for row in quotes:
        data = Path(row['source']).read_bytes()
        text = data.decode('utf8')
        assert hashlib.sha256(data).hexdigest() == row['source_sha256']
        assert row['quote'] in text
        assert text[:text.index(row['quote'])].count('\n') + 1 == row['line']
        assert row['latex_quote'] in main
    skills = json.loads(Path('docs/skill_documents/manifest.json').read_text())
    for row in skills:
        assert hashlib.sha256(Path(row['snapshot']).read_bytes()).hexdigest() == row['sha256']
    diagram = Path('report/instruction_workflow.tex').read_text()
    assert r'\input{instruction_workflow.tex}' in main
    assert r'\ref{fig:ai-workflow}' in main
    assert all(text in diagram for text in ['HUMAN', 'Codex Desktop', 'Laplace Redux, NatPN, VBLL',
        'Prompt 02', 'Pending:', 'Prompt 03', 'Prompt 04'])
    record = dict(baseline_commit=baseline, source_files_and_reflection_bitwise_unchanged=preserved,
        sections_2_through_5_source_unchanged=True, bibliography_preserved=True, original_selection_justification_preserved=True,
        verified_verbatim_excerpts=len(quotes), skill_document_snapshots_verified=len(skills),
        vector_diagram_source_sha256=hashlib.sha256(diagram.encode('utf8')).hexdigest(),
        github_publication_pending=False, independent_peer_review_claimed=False)
    Path('results/instruction_section_audit.json').write_text(json.dumps(record, indent=2)+'\n',
        encoding='utf8', newline='\n')
    print(f'Instruction audit passed: {len(quotes)} verified excerpts, {len(skills)} skill snapshots; '
          'original prompts, reflection, selection rationale and Sections 2 through 5 and bibliography preserved.')


if __name__ == '__main__':
    audit()
