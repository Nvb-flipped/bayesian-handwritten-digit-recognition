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
for name,digest in env["source_sha256"].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
for name in ["main.tex","main.pdf","performance.tex","ablation.tex","selection.tex","per_class.tex"]:
    assert (Path("report")/name).exists(),name
manifest=json.loads(Path("results/figure_manifest.json").read_text())
assert len(manifest)==8
for figure in manifest:
    for ext in ["pdf","svg","png"]:
        assert (Path("results/figures")/(figure["name"]+"."+ext)).exists()
for key in ["metrics_regenerated","checkpoint_predictions_bitwise_equal","full_reproduction_bitwise_equal"]:
    assert json.loads(Path("results/audit.json").read_text())[key]
print(f"Artifact audit passed: {links} local links, recorded source hashes, eight figures, report and results.")

