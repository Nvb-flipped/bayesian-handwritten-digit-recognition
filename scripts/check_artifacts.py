"""Check local documentation links, recorded source hashes and evidence completeness."""
import hashlib
import json
from pathlib import Path
import re

root=Path(".")
links=0
for f in [Path("README.md"),*Path("docs").rglob("*.md")]:
    for target in re.findall(r"\]\(([^)]+)\)",f.read_text(encoding="utf8")):
        if "://" in target or target.startswith("#"): continue
        dest=(f.parent/target.split("#")[0]).resolve()
        assert dest.exists(),f"Broken local link: {f} -> {target}"
        links+=1
env=json.loads(Path("results/environment.json").read_text())
manifest=json.loads(Path("results/figure_manifest.json").read_text())
for name,digest in env["source_sha256"].items():
    # Keep the original experiment record immutable. Plotting is regenerated
    # separately and its current code hash is verified by the figure manifest.
    if name==manifest[0]['generator']: continue
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
for name in ["main.tex","main.pdf","performance.tex","ablation.tex","selection.tex","per_class.tex"]:
    assert (Path("report")/name).exists(),name
expected=9+int(Path('results/review_diagnostics/summary.json').exists())
assert len(manifest)==expected
for figure in manifest:
    assert hashlib.sha256(Path(figure['generator']).read_bytes()).hexdigest()==figure['generator_sha256']
    for name,digest in figure['source_sha256'].items():
        assert hashlib.sha256((Path('results')/name).read_bytes()).hexdigest()==digest,name
    for ext in ["pdf","svg","png"]:
        assert (Path("results/figures")/(figure["name"]+"."+ext)).exists()
for name,digest in json.loads(Path('results/markdown_validation.json').read_text())['source_sha256'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
pdf_validation=json.loads(Path('results/report_validation.json').read_text())
assert hashlib.sha256(Path(pdf_validation['pdf']).read_bytes()).hexdigest()==pdf_validation['sha256']
for figure in json.loads(Path('results/figure_export_validation.json').read_text())['figures']:
    for ext,record in figure['files'].items():
        path=Path('results/figures')/(figure['name']+'.'+ext)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],path
for key in ["metrics_regenerated","checkpoint_predictions_bitwise_equal","full_reproduction_bitwise_equal"]:
    assert json.loads(Path("results/audit.json").read_text())[key]
print(f"Artifact audit passed: {links} local links, recorded source hashes, {expected} figures, report and results.")
