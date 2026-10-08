"""Check post hoc outputs, primary prediction invariance, and Markdown structure."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import numpy as np
from bayes_digits.metrics import evaluate
from bayes_digits.experiment import save_json

snapshot='a28a563'
original=np.load(io.BytesIO(subprocess.check_output(['git','show',f'{snapshot}:results/predictions.npz'])))
current=np.load('results/predictions.npz')
assert original.files==current.files
assert all(np.array_equal(original[k],current[k]) for k in original.files)
root=Path('results/review_diagnostics')
arrays=np.load(root/'probabilities.npz')
settings=json.loads((root/'config.json').read_text())
records=json.loads((root/'records.json').read_text())
assert len(records)==3*len(settings['sample_counts'])*settings['repetitions']
for row in records:
    key=f'p_{row["feature_seed"]}_{row["samples"]}_{row["repetition"]}'
    metrics=evaluate(arrays['labels'],arrays[key])
    assert all(metrics[k]==v for k,v in row['metrics'].items())
provenance=json.loads((root/'provenance.json').read_text())
assert hashlib.sha256(Path('configs/review_diagnostics.json').read_bytes()).hexdigest()==provenance['config_sha256']
assert hashlib.sha256(Path('scripts/review_diagnostics.py').read_bytes()).hexdigest()==provenance['script_sha256']
for name,digest in provenance['checkpoint_sha256'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest
tex=Path('report/main.tex').read_text()
citations=set(k for group in re.findall(r'\\cite\{([^}]+)\}',tex) for k in group.split(','))
bib=set(re.findall(r'\\bibitem\{([^}]+)\}',tex))
assert citations==bib,(citations-bib,bib-citations)
assert 'STUDENT REFLECTION REQUIRED' not in tex
assert r'\input{student_reflection.tex}' in tex
reflection=Path('report/student_reflection.txt').read_text(encoding='utf8')
reflection_tex=Path('report/student_reflection.tex').read_text(encoding='utf8')
assert reflection_tex.replace(r'\%','%').replace(r'\textquoteright{}','’')==reflection
markdown=list(Path('docs/wiki').glob('*.md'))+[Path('README.md')]
for path in markdown:
    text=path.read_text(encoding='utf8')
    assert not any(token in text for token in [r'\(',r'\)',r'\[',r'\]']),path
    assert sum(line.strip()=='$$' for line in text.splitlines())%2==0,path
    for fence in ['```','~~~']:
        assert sum(line.startswith(fence) for line in text.splitlines())%2==0,path
    assert not any('$$' in line and line.strip()!='$$' for line in text.splitlines()),path
save_json('results/review_audit.json',dict(primary_prediction_arrays_bitwise_unchanged=len(current.files),
    baseline_commit=snapshot,diagnostic_metrics_regenerated=len(records),
    fixed_checkpoint_hashes_verified=True,citation_keys_verified=len(bib),
    markdown_files_checked=len(markdown),reflection_placeholder_preserved=False,
    supplied_student_reflection_preserved=True,
    reflection_source_sha256=hashlib.sha256(reflection.encode('utf8')).hexdigest()))
print(f'Review audit passed: {len(current.files)} unchanged arrays; {len(records)} diagnostic records; '
      f'{len(bib)} citation keys; {len(markdown)} Markdown pages.')
