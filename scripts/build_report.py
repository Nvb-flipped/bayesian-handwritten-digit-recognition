"""Generate quantitative LaTeX tables directly from measured JSON."""
import json
from pathlib import Path
import numpy as np

root=Path("results")
report=Path("report")
report.mkdir(exist_ok=True)
summary=json.loads((root/"summary.json").read_text())
select=json.loads((root/"selection_locked.json").read_text())
env=json.loads((root/"environment.json").read_text())
records=json.loads((root/"metrics.json").read_text())
def cell(method,key,scale=1,digits=3):
    v=summary[method][key]
    m=v["mean"]*scale
    return f"{m:.{digits}f}" if v["sd"] is None else "$"+f"{m:.{digits}f}\\pm {v['sd']*scale:.{digits}f}"+"$"

main=[r"\begin{tabular}{lrrrr}\toprule",
      r"Method & Accuracy (\%) & Macro-F1 & NLL & Brier \\\midrule"]
for method in ["Gaussian NB","MAP","Laplace"]:
    main.append(method+" & "+cell(method,"accuracy",100,2)+" & "+cell(method,"macro_f1")
                +" & "+cell(method,"nll")+" & "+cell(method,"brier")+r"\\")
main.append(r"\bottomrule\end{tabular}")
(report/"performance.tex").write_text("\n".join(main),newline="\n")
more=[r"\begin{tabular}{lrrr}\toprule",
      r"Method & Macro-precision & Macro-recall & ECE \\\midrule"]
for method in ["Gaussian NB","MAP","Laplace"]:
    more.append(method+" & "+" & ".join(cell(method,k) for k in ["macro_precision","macro_recall","ece"])+r"\\")
more.append(r"\bottomrule\end{tabular}")
(report/"probability_metrics.tex").write_text("\n".join(more),newline="\n")
abl=[r"\begin{tabular}{lrrr}\toprule",r"Frozen-prior variant & Accuracy (\%) & NLL & ECE \\\midrule"]
for method in ["Matched MAP","Laplace","Diagonal Laplace"]:
    abl.append(method+" & "+cell(method,"accuracy",100,2)+" & "+cell(method,"nll")+" & "+cell(method,"ece")+r"\\")
abl.append(r"\bottomrule\end{tabular}")
(report/"ablation.tex").write_text("\n".join(abl),newline="\n")
rows=[r"\begin{tabular}{rrrrr}\toprule",
      r"Seed & Feature epoch & MAP $\alpha$ & LA $\alpha$ & LA validation NLL \\\midrule"]
for r in select["selections"]:
    rows.append(f"{r['seed']} & {r['feature_epoch']} & {r['map_alpha']} & {r['laplace_alpha']} & {r['laplace_validation_nll']:.4f}"+r"\\")
rows.append(r"\bottomrule\end{tabular}")
(report/"selection.tex").write_text("\n".join(rows),newline="\n")
rows=[r"\begin{tabular}{rrrrr}\toprule",r"Digit & Test support & Precision & Recall & F1 \\\midrule"]
for k in range(10):
    vals=[r["metrics"]["per_class"][str(k)] for r in records if r["method"]=="Laplace"]
    rows.append(str(k)+f" & {vals[0]['support']:.0f} & "+
                " & ".join(f"{np.mean([v[key] for v in vals]):.3f}" for key in ["precision","recall","f1-score"])+r"\\")
rows.append(r"\bottomrule\end{tabular}")
(report/"per_class.tex").write_text("\n".join(rows),newline="\n")
macros=[r"\newcommand{\RunSeconds}{"+f"{env['seconds']:.2f}"+r"}",
        r"\newcommand{\LaplaceAcc}{"+f"{summary['Laplace']['accuracy']['mean']*100:.2f}"+r"}",
        r"\newcommand{\LaplaceNLL}{"+f"{summary['Laplace']['nll']['mean']:.3f}"+r"}",
        r"\newcommand{\MapNLL}{"+f"{summary['MAP']['nll']['mean']:.3f}"+r"}"]
(report/"results.tex").write_text("\n".join(macros),newline="\n")
diagnostic=root/'review_diagnostics'
if (diagnostic/'summary.json').exists():
    values=json.loads((diagnostic/'summary.json').read_text())
    reference=json.loads((diagnostic/'matched_map.json').read_text())
    at512=[v for v in values if v['samples']==512]
    at2048=[v for v in values if v['samples']==2048]
    penalty=[v['nll']['mean']-next(r['matched_map_nll'] for r in reference
                                 if r['feature_seed']==v['feature_seed']) for v in at2048]
    text=(f"At 512 draws, within-model NLL SD across eight repetitions ranges from "
          f"{min(v['nll']['sd'] for v in at512):.4f} to {max(v['nll']['sd'] for v in at512):.4f} nats. "
          f"At 2048 draws, mean Laplace-minus-matched-MAP NLL remains "
          f"{min(penalty):.4f}--{max(penalty):.4f} nats across the three fitted models. "
          "These descriptive results support a persistent probability-score penalty in this setting, "
          "rather than attributing it solely to the original random draws.\n")
    (report/'diagnostic_text.tex').write_text(text,newline="\n")
print("Report tables generated from recorded results.")
