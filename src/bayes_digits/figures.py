"""Regenerate all vector/raster figures exclusively from recorded evidence."""
import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from .data import load_data

COLORS=["#0072B2","#D55E00","#009E73"]
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                     "pdf.fonttype":42,"svg.fonttype":"none","savefig.facecolor":"white"})


def generate(root):
    root=Path(root)
    out=root/"figures"
    out.mkdir(exist_ok=True)
    records=json.loads((root/"metrics.json").read_text())
    config=json.loads((root/"config.json").read_text())
    summary=json.loads((root/"summary.json").read_text())
    split=np.load(root/"splits.npz")
    preds=np.load(root/"predictions.npz")
    x,y,_,_=load_data(config["split_seed"])
    seed=config["seeds"][0]  # Predeclared representative seed, not the best run.
    manifest=[]
    def save(fig,name,sources,description):
        for suffix in ["pdf","svg","png"]:
            fig.savefig(out/f"{name}.{suffix}",dpi=180)
        manifest.append(dict(name=name,sources=sources,description=description,
                             inches=fig.get_size_inches().tolist()))
        plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(7,2.8),layout="constrained")
    for i,k in enumerate(["train","validation","test"]):
        axes[0].bar(np.arange(10)+(i-1)*.25,np.bincount(y[split[k]],minlength=10),
                    width=.25,label=f"{k} (n={len(split[k])})",color=COLORS[i])
    axes[0].set(xlabel="Digit",ylabel="Images",xticks=np.arange(10))
    axes[0].legend(fontsize=7)
    examples=np.concatenate([x[split["train"][np.flatnonzero(y[split["train"]]==k)[0]]].reshape(8,8)
        for k in range(10)],axis=1)
    axes[1].imshow(examples,cmap="gray",vmin=0,vmax=1,interpolation="nearest")
    axes[1].set(yticks=[],xticks=np.arange(10)*8+3.5,xticklabels=np.arange(10),
                title="First training image per class")
    save(fig,"dataset",["splits.npz","sklearn.load_digits"],"Split balance and deterministic digit examples.")

    fig,ax=plt.subplots(figsize=(7,2.6),layout="constrained")
    ax.axis("off")
    dimension=10*(config["hidden"]+1)
    labels=["1. Train images\n64 scaled pixels",f"2. Feature learning\n{config['hidden']} tanh units","3. Freeze features\nfit MAP head",
            f"4. Training curvature\n{dimension} x {dimension} Hessian",f"5. Gaussian posterior\n{config['posterior_samples']} weight samples","6. Average probabilities\nclass + uncertainty"]
    for i,text in enumerate(labels):
        row=i//3
        col=i%3 if row==0 else 2-i%3
        xpos=.03+col*.33; ypos=.57-row*.45
        ax.add_patch(FancyBboxPatch((xpos,ypos),.27,.32,boxstyle="round,pad=0.01",
                     transform=ax.transAxes,edgecolor=COLORS[0],facecolor="#EFF6FA"))
        ax.text(xpos+.135,ypos+.16,text,ha="center",va="center",transform=ax.transAxes,fontsize=9)
        if row==0 and col<2:
            ax.annotate("",xy=(xpos+.32,ypos+.16),xytext=(xpos+.28,ypos+.16),
                        xycoords="axes fraction",arrowprops=dict(arrowstyle="->"))
        if row==1 and col>0:
            ax.annotate("",xy=(xpos-.04,ypos+.16),xytext=(xpos-.01,ypos+.16),
                        xycoords="axes fraction",arrowprops=dict(arrowstyle="->"))
    ax.annotate("",xy=(.825,.44),xytext=(.825,.55),xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->"))
    ax.text(.5,.98,"Validation selects epoch and prior; test predictions follow selection lock",
            ha="center",va="top",transform=ax.transAxes,fontsize=9)
    save(fig,"inference",["src/bayes_digits"],"Project inference stages, with training and validation roles.")

    fig,axes=plt.subplots(1,3,figsize=(7,2.6),layout="constrained")
    methods=["Gaussian NB","MAP","Laplace"]
    for ax,key,label in zip(axes,["accuracy","nll","brier"],["Accuracy","NLL (nats)","Brier (sum over classes)"]):
        for j,method in enumerate(methods):
            vals=[r["metrics"][key] for r in records if r["method"]==method]
            ax.scatter(np.full(len(vals),j),vals,color=COLORS[j],s=25,zorder=3)
            m=summary[method][key]
            if m["sd"] is not None:
                ax.errorbar(j,m["mean"],yerr=m["sd"],color=COLORS[j],capsize=5,fmt="_")
        ax.set(xticks=np.arange(3),xticklabels=["GNB","MAP","LA"],ylabel=label,xlim=(-.5,2.5))
        ax.set_ylim(bottom=0)
        if key=="accuracy": ax.set_ylim(0,1.03)
    save(fig,"comparison",["metrics.json","summary.json"],"Raw seed results and sample SD; GNB evaluated once.")

    fig,axes=plt.subplots(1,2,figsize=(7,3.4),layout="constrained")
    selected=[r for r in records if r["method"]=="Laplace"]
    counts=np.array([r["metrics"]["confusion"] for r in selected])
    norm=(counts/counts.sum(2,keepdims=True)).mean(0)
    im=axes[0].imshow(norm,vmin=0,vmax=1,cmap="Blues")
    for i in range(10):
        for j in range(10):
            if norm[i,j]>.005:
                axes[0].text(j,i,f"{norm[i,j]:.2f}",ha="center",va="center",fontsize=6,
                             color="white" if norm[i,j]>.55 else "black")
    axes[0].set(xlabel="Predicted digit",ylabel="True digit",xticks=range(10),yticks=range(10))
    fig.colorbar(im,ax=axes[0],fraction=.046,label="Mean row proportion")
    for method,color,marker in zip(["MAP","Laplace"],COLORS[:2],["o","s"]):
        members=[r for r in records if r["method"]==method]
        vals=np.array([[r["metrics"]["per_class"][str(k)]["f1-score"] for k in range(10)] for r in members])
        axes[1].errorbar(range(10),vals.mean(0),yerr=vals.std(0,ddof=1),label=method,
                         marker=marker,color=color,capsize=3,markersize=4)
    axes[1].set(xlabel="Digit",ylabel="Per-class F1",xticks=range(10),ylim=(0,1.02))
    axes[1].legend()
    save(fig,"classes",["metrics.json"],"Row-normalized confusion and class F1, 3 seeds on the same test set.")

    fig,axes=plt.subplots(1,2,figsize=(7,2.9),layout="constrained")
    for method,color,marker in zip(methods,COLORS,["^","o","s"]):
        r=next(r for r in records if r["method"]==method and (r["seed"]==seed or r["seed"] is None))
        bins=[b for b in r["metrics"]["reliability"] if b["count"]]
        axes[0].plot([b["confidence"] for b in bins],[b["accuracy"] for b in bins],
                     marker=marker,color=color,label=method)
    axes[0].plot([0,1],[0,1],"k--",linewidth=1)
    axes[0].set(xlabel="Mean confidence",ylabel="Observed accuracy",xlim=(0,1),ylim=(0,1.03))
    axes[0].legend(fontsize=8)
    p=preds[f"Laplace_{seed}"]
    good=p.argmax(1)==preds["labels"]
    mi=preds[f"MI_{seed}"]
    edges=np.linspace(0,max(mi.max(),.001),16)
    for mask,label,color in [(good,"Correct",COLORS[0]),(~good,"Errors",COLORS[1])]:
        axes[1].hist(mi[mask],bins=edges,histtype="step",linewidth=1.5,color=color,
                     label=f"{label} (n={mask.sum()})")
    axes[1].set(xlabel="Posterior mutual information (nats)",ylabel="Images")
    axes[1].legend(fontsize=8)
    save(fig,"calibration",["metrics.json","predictions.npz"],f"Reliability and posterior disagreement, prespecified seed {seed}.")

    fig,axes=plt.subplots(1,2,figsize=(7,2.7),layout="constrained")
    for s,color in zip(config["seeds"],COLORS):
        h=json.loads((root/f"history_{s}.json").read_text())
        axes[0].plot([v["epoch"] for v in h],[v["train_nll"] for v in h],color=color,label=f"seed {s}")
        axes[1].plot([v["epoch"] for v in h],[v["validation_nll"] for v in h],color=color)
    for ax in axes: ax.set(xlabel="Epoch",ylabel="NLL (nats)",yscale="log")
    axes[0].set_title("Training"); axes[1].set_title("Validation")
    axes[0].legend(fontsize=8)
    save(fig,"convergence",[f"history_{s}.json" for s in config["seeds"]],"Feature network NLL, before convex last-layer refitting.")

    fig,axes=plt.subplots(1,2,figsize=(7,2.9),layout="constrained")
    sens=json.loads((root/"sensitivity.json").read_text())
    for s,color in zip(config["seeds"],COLORS):
        v=[r for r in sens if r["seed"]==s]
        axes[0].plot([r["alpha"] for r in v],[r["laplace_validation_nll"] for r in v],
                     marker="o",color=color,label=f"seed {s}")
    axes[0].set(xlabel="Prior precision alpha",ylabel="Validation NLL (nats)",xscale="log")
    axes[0].legend(fontsize=8)
    for j,method in enumerate(["Matched MAP","Laplace","Diagonal Laplace"]):
        vals=[r["metrics"]["nll"] for r in records if r["method"]==method]
        axes[1].scatter(np.full(len(vals),j),vals,color=COLORS[j],s=25)
        axes[1].errorbar(j,np.mean(vals),yerr=np.std(vals,ddof=1),fmt="_",capsize=4,color=COLORS[j])
    axes[1].set(xticks=range(3),xticklabels=["Matched\nMAP","Full\nLaplace","Diagonal\nLaplace"],
                ylabel="Test NLL (nats)",ylim=(0,None))
    save(fig,"sensitivity",["sensitivity.json","metrics.json"],"Prior selection uses validation; frozen-prior ablations use test.")

    bad=np.flatnonzero(p.argmax(1)!=preds["labels"])
    bad=bad[np.argsort(preds["indices"][bad])][:8]
    fig,axes=plt.subplots(2,4,figsize=(7,3.5),layout="constrained")
    for ax in axes.ravel(): ax.axis("off")
    for ax,j in zip(axes.ravel(),bad):
        ax.imshow(x[preds["indices"][j]].reshape(8,8),cmap="gray",vmin=0,vmax=1,interpolation="nearest")
        ax.set_title(f"idx {preds['indices'][j]}: {preds['labels'][j]} -> {p[j].argmax()}\n"
                     f"confidence {p[j].max():.2f}",fontsize=9)
    save(fig,"errors",["predictions.npz","sklearn.load_digits"],
         "First eight mistakes in ascending dataset index; seed 11 fixed before experiments.")
    # A CSV links every scalar to its method/seed.
    with (root/"scalar_metrics.csv").open("w",newline="",encoding="utf8") as stream:
        keys=["accuracy","macro_f1","macro_precision","macro_recall","nll","brier","ece"]
        writer=csv.DictWriter(stream,fieldnames=["method","seed"]+keys)
        writer.writeheader()
        for r in records: writer.writerow(dict(method=r["method"],seed=r["seed"],
                                              **{k:r["metrics"][k] for k in keys}))
    (root/"figure_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf8")
    print(f"Generated {len(manifest)} figures in PDF/SVG/PNG: {out}")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--results",default="results")
    generate(parser.parse_args().results)
