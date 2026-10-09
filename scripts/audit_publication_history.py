"""Check publishable Git history without emitting suspected credential contents."""
import hashlib
import json
from pathlib import Path
import re
import subprocess


def audit():
    objects = subprocess.check_output(['git', 'rev-list', '--objects', '--all']).decode().splitlines()
    names = {}
    for row in objects:
        sha, _, name = row.partition(' ')
        names.setdefault(sha, name)
    metadata = subprocess.check_output(['git', 'cat-file', '--batch-check'],
        input=('\n'.join(names)+'\n').encode()).decode().splitlines()
    patterns = [rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'github_pat_[A-Za-z0-9_]{40,}',
        rb'sk-[A-Za-z0-9_-]{30,}', rb'AKIA[0-9A-Z]{16}', rb'xox[baprs]-[A-Za-z0-9-]{20,}',
        rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    findings = []
    blobs = 0
    total = 0
    largest = 0
    for row in metadata:
        sha, kind, size = row.split()
        if kind != 'blob':
            continue
        name = names[sha]
        if any(p in Path(name).parts for p in ['.venv', '.agents', '.codex', 'tmp', 'data', 'checkpoints']):
            findings.append(dict(path=name,reason='Excluded environment/cache directory present in history'))
        size = int(size)
        if size >= 10_000_000:
            findings.append(dict(path=name,reason='Unnecessary-large-file threshold requires review'))
        data = subprocess.check_output(['git', 'cat-file', 'blob', sha])
        if any(re.search(pattern, data) for pattern in patterns):
            findings.append(dict(path=name,reason='Credential/private-key pattern'))
        blobs += 1
        total += size
        largest = max(largest, size)
    assert not findings, 'History findings (values withheld): '+json.dumps(findings)
    tracked = subprocess.check_output(['git','ls-files','-z']).decode().split('\0')[:-1]
    selected = {p.as_posix():p.stat().st_size for p in sorted(Path('results/models').glob('*'))}
    record = dict(review_date='2026-10-09', baseline_commit=subprocess.check_output(
        ['git','rev-parse','HEAD']).decode().strip(),
        commits_checked=int(subprocess.check_output(['git','rev-list','--count','--all'])),
        historical_blobs_checked=blobs, historical_blob_bytes=total, largest_blob_bytes=largest,
        credential_pattern_findings=[], excluded_directory_findings=[], tracked_files=len(tracked),
        selected_checkpoints=selected,
        checkpoint_rationale='Only seven selected small artifacts retained for exact checkpoint reload/reproduction audits; no dataset caches or redundant training checkpoints.',
        intentional_public_course_identity='Report title includes the student name and ID required by the course.',
        scope='Pattern and inventory audit, not a guarantee that every conceivable secret format is detectable.')
    Path('results/publication_history_audit.json').write_text(json.dumps(record,indent=2)+'\n',
        encoding='utf8',newline='\n')
    print(f'History audit passed: {record["commits_checked"]} commits, {blobs} blobs; '
          f'largest {largest:,} bytes; no credential-pattern or excluded-directory findings.')


if __name__ == '__main__':
    audit()
