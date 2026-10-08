"""Regenerate all vector/raster figures exclusively from recorded evidence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np
from .data import load_data
from .laplace import hessian

COLORS=["#0072B2","#D55E00","#009E73"]
MARKERS=["o","s","^"]
STYLES=["-","--",":"]
plt.rcParams.update({"font.size":10.5,"axes.spines.top":False,"axes.spines.right":False,
                     "pdf.fonttype":42,"svg.fonttype":"none","savefig.facecolor":"white"})


def covariance_example():
    """Exact toy geometry, derived from the same Hessian as the worked example."""
    precision=hessian(np.zeros((2,1)),np.ones((2,1)),1.)
    full=np.linalg.inv(precision)
    diagonal=np.diag(1/np.diag(precision))  # Diagonalize precision before inversion.
    angle=np.linspace(0,2*np.pi,401)
    unit=np.array([np.cos(angle),np.sin(angle)])
    return precision,full,diagonal,[(np.linalg.cholesky(c)@unit).T for c in [full,diagonal]]


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
    figure_data={}
    def save(fig,name,sources,description):
        for suffix in ["pdf","svg","png"]:
            fig.savefig(out/f"{name}.{suffix}",dpi=300)
        manifest.append(dict(name=name,sources=sources,description=description,
                             inches=fig.get_size_inches().tolist(),raster_dpi=300,
                             generator="src/bayes_digits/figures.py",
                             generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             source_sha256={s:hashlib.sha256((root/s).read_bytes()).hexdigest()
                                            for s in sources if (root/s).is_file()}))
        plt.close(fig)
    def panel(ax,letter,title):
        ax.set_title(f"{letter}  {title}",loc="left",fontsize=11,fontweight="bold",pad=9)
    fig,axes=plt.subplots(1,2,figsize=(7,2.9),width_ratios=[1.15,1],layout="constrained")
    for i,k in enumerate(["train","validation","test"]):
        axes[0].bar(np.arange(10)+(i-1)*.25,np.bincount(y[split[k]],minlength=10),
                    width=.25,label=f"{k} (n={len(split[k])})",color=COLORS[i],
                    hatch=["","//",".."][i])
    axes[0].set(xlabel="Digit",ylabel="Images",xticks=np.arange(10))
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=3,fontsize=9)
    panel(axes[0],"A","Class balance")
    example_indices=[int(split["train"][np.flatnonzero(y[split["train"]]==k)[0]]) for k in range(10)]
    axes[1].axis("off")
    for k,index in enumerate(example_indices):
        ax=axes[1].inset_axes([.01+(k%5)*.198,.53-(k//5)*.47,.185,.34])
        ax.imshow(x[index].reshape(8,8),cmap="gray",vmin=0,vmax=1,interpolation="nearest")
        ax.set(xticks=[],yticks=[],xlabel=str(k))
        ax.xaxis.label.set_size(10)
    panel(axes[1],"B","Training examples")
    figure_data["dataset"]={k:np.bincount(y[split[k]],minlength=10).tolist() for k in split.files}
    figure_data["dataset"]["example_indices"]=example_indices
    save(fig,"dataset",["splits.npz","dataset.json","config.json"],"Split balance and deterministic digit examples; images from sklearn.load_digits.")

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
    save(fig,"inference",["config.json"],"Project inference stages, with training and validation roles.")

    precision,full,diagonal,contours=covariance_example()
    contrast=np.array([-1.,1.])
    variances=[float(contrast@c@contrast) for c in [full,diagonal]]
    fig,axes=plt.subplots(1,3,figsize=(7,2.7),layout="constrained")
    for ax,curve,c,color,letter,title in zip(axes[:2],contours,[full,diagonal],
            [COLORS[2],"#CC79A7"],"AB",["Full covariance","Diagonal precision"]):
        ax.plot(curve[:,0],curve[:,1],color=color,linewidth=2,
                linestyle="-" if letter=="A" else "--")
        ax.axhline(0,color="#dddddd",linewidth=.7)
        ax.axvline(0,color="#dddddd",linewidth=.7)
        ax.set(xlabel=r"$w_0$",ylabel=r"$w_1$",xlim=(-1.25,1.25),ylim=(-1.25,1.25),
               xticks=[-1,0,1],yticks=[-1,0,1],aspect="equal")
        ax.text(0,-1.17,f"Marginal variance {c[0,0]:.3f}",ha="center",fontsize=8.5)
        panel(ax,letter,title)
    d=np.linspace(-3.5,3.5,401)
    for variance,color,style,label in zip(variances,[COLORS[2],"#CC79A7"],["-","--"],
            ["Full: variance 1","Diagonal: variance 4/3"]):
        axes[2].plot(d,np.exp(-d*d/(2*variance))/np.sqrt(2*np.pi*variance),
                     color=color,linestyle=style,linewidth=1.8,label=label)
    axes[2].set(xlabel=r"Contrast $d=w_1-w_0$",ylabel="Gaussian density",xlim=(-3.5,3.5),ylim=(0,.44))
    panel(axes[2],"C","Logit contrast")
    axes[2].legend(fontsize=8,loc="upper center",bbox_to_anchor=(.5,-.26))
    figure_data["covariance_geometry"]={"example":"Exact two-label scalar-feature toy; not fitted experiment evidence",
        "precision":precision.tolist(),"full_covariance":full.tolist(),"diagonal_precision_covariance":diagonal.tolist(),
        "contrast_variances":variances,"contour_mahalanobis_squared":1.,
        "contours":[c.tolist() for c in contours]}
    save(fig,"covariance_geometry",["../src/bayes_digits/laplace.py"],
         "Worked-example radius-one Mahalanobis contours and exact Gaussian logit-contrast densities; toy calculation, not ten-class measurements.")

    fig,axes=plt.subplots(1,3,figsize=(7,2.6),layout="constrained")
    methods=["Gaussian NB","MAP","Laplace"]
    for letter,ax,key,label in zip("ABC",axes,["errors","nll","brier"],
                                  ["Errors / 360 images","NLL (nats)","Brier (class sum)"]):
        for j,method in enumerate(methods):
            members=[r for r in records if r["method"]==method]
            vals=[int(np.sum(r["metrics"]["confusion"])-np.trace(r["metrics"]["confusion"]))
                  if key=="errors" else r["metrics"][key] for r in members]
            for i,v in enumerate(vals):
                ax.scatter(j+(i-1)*.13 if len(vals)>1 else j,v,color=COLORS[j],
                           marker=MARKERS[i] if len(vals)>1 else "D",s=25,zorder=3)
            if len(vals)>1:
                ax.errorbar(j,np.mean(vals),yerr=np.std(vals,ddof=1),color="black",capsize=4,fmt="_",zorder=2)
            if key=="errors":
                ax.text(j,max(vals)+1.5,"/".join(str(v) for v in vals),ha="center",fontsize=8)
        ax.set(xticks=np.arange(3),xticklabels=["GNB","MAP","LA"],ylabel=label,xlim=(-.5,2.5))
        ax.set_ylim(bottom=0)
        if key=="errors": ax.set_ylim(0,34)
        panel(ax,letter,["Recognition","Log loss","Brier score"]["ABC".index(letter)])
    fig.legend(handles=[Line2D([],[],marker=m,color="black",linestyle="none",label=f"seed {s}")
                        for s,m in zip(config["seeds"],MARKERS)],loc="outside lower center",ncol=3,fontsize=8)
    save(fig,"comparison",["metrics.json","summary.json"],"Raw seed results and sample SD; GNB evaluated once.")

    fig,axes=plt.subplots(1,2,figsize=(7,3.9),width_ratios=[1.2,1],layout="constrained")
    selected=[r for r in records if r["method"]=="Laplace"]
    counts=np.array([r["metrics"]["confusion"] for r in selected])
    norm=(counts/counts.sum(2,keepdims=True)).mean(0)
    im=axes[0].imshow(norm,vmin=0,vmax=1,cmap="Blues")
    for i in range(10):
        for j in range(10):
            if norm[i,j]>.005:
                axes[0].text(j,i,f"{100*norm[i,j]:.0f}",ha="center",va="center",fontsize=9,
                             color="white" if norm[i,j]>.55 else "black")
    axes[0].set(xlabel="Predicted digit",ylabel="True digit",xticks=range(10),yticks=range(10))
    fig.colorbar(im,ax=axes[0],fraction=.046,label="Row proportion")
    panel(axes[0],"A","Laplace confusion")
    for offset,method,color in zip([-.18,.18],["MAP","Laplace"],COLORS[1:]):
        members=[r for r in records if r["method"]==method]
        vals=np.array([[r["metrics"]["per_class"][str(k)]["f1-score"] for k in range(10)] for r in members])
        deficit=1-vals
        centers=np.arange(10)+offset
        axes[1].vlines(centers,deficit.min(0),deficit.max(0),color=color,linewidth=1.2)
        for i,marker in enumerate(MARKERS):
            axes[1].scatter(centers+(i-1)*.045,deficit[i],marker=marker,s=20,
                facecolors=color if method=="MAP" else "white",edgecolors=color,
                linewidths=1,zorder=3,clip_on=False)
        axes[1].scatter(centers,deficit.mean(0),marker="_",s=70,color="black",zorder=4)
    axes[1].set(xlabel="Digit",ylabel="F1 deficit (1 − F1)",xticks=range(10),ylim=(0,.12),xlim=(-.5,9.5))
    panel(axes[1],"B","F1 deficit")
    axes[1].legend(handles=[Line2D([],[],color=COLORS[1],marker="o",linestyle="none",label="MAP (filled)"),
        Line2D([],[],color=COLORS[2],marker="o",markerfacecolor="white",linestyle="none",label="Laplace (open)")],
        fontsize=9,loc="upper left")
    fig.legend(handles=[Line2D([],[],marker=m,color="black",linestyle="none",label=f"seed {s}")
                        for s,m in zip(config["seeds"],MARKERS)],loc="outside lower center",ncol=3,fontsize=9)
    figure_data["classes"]={"mean_row_confusion":norm.tolist(),
        "f1_by_seed":{m:[[r["metrics"]["per_class"][str(k)]["f1-score"] for k in range(10)]
                           for r in records if r["method"]==m] for m in ["MAP","Laplace"]}}
    save(fig,"classes",["metrics.json"],"Row-normalized confusion; all three seed F1 deficits, arithmetic means and observed min-max ranges. No SD/CI bars.")

    fig=plt.figure(figsize=(7,3.8),layout="constrained")
    grid=fig.add_gridspec(2,2,height_ratios=[3,1],width_ratios=[1,1])
    axes=[fig.add_subplot(grid[0,0]),fig.add_subplot(grid[:,1])]
    occupancy=fig.add_subplot(grid[1,0],sharex=axes[0])
    figure_data["calibration"]={}
    for method,color,marker in zip(methods,COLORS,["^","o","s"]):
        r=next(r for r in records if r["method"]==method and (r["seed"]==seed or r["seed"] is None))
        bins=[b for b in r["metrics"]["reliability"] if b["count"]]
        axes[0].scatter([b["confidence"] for b in bins],[b["accuracy"] for b in bins],
                        s=30,marker=marker,color=color,label=method,clip_on=False,zorder=3)
        figure_data["calibration"][method]=r["metrics"]["reliability"]
    axes[0].plot([0,1],[0,1],"k--",linewidth=1)
    axes[0].set(xlabel="Mean confidence",ylabel="Observed accuracy",xlim=(0,1),ylim=(0,1),
                xticks=np.linspace(0,1,6),yticks=np.linspace(0,1,6))
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=3,fontsize=9)
    panel(axes[0],"A","Reliability (seed 11)")
    p=preds[f"Laplace_{seed}"]
    good=p.argmax(1)==preds["labels"]
    mi=preds[f"MI_{seed}"]
    for mask,label,color,style in [(good,"Correct",COLORS[0],"-"),(~good,"Errors",COLORS[1],"--")]:
        values=np.sort(mi[mask])
        if len(values):
            axes[1].step(np.r_[0,values],np.r_[0,np.arange(1,len(values)+1)/len(values)],
                         where="post",linewidth=1.6,color=color,linestyle=style,
                         label=f"{label} (n={mask.sum()})")
    axes[1].set(xlabel="Posterior MI (nats)",ylabel="Fraction within group",ylim=(0,1),xlim=(0,None))
    axes[1].legend(fontsize=9,loc="lower right")
    panel(axes[1],"B","Disagreement distribution")
    figure_data["uncertainty"]={"correct":mi[good].tolist(),"errors":mi[~good].tolist()}
    occupancy.set(yticks=range(3),yticklabels=["GNB","MAP","LA"],ylim=(2.5,-.5),
                  xlabel="Confidence-bin boundaries",xticks=np.linspace(0,1,6))
    occupancy.tick_params(axis="x",labelsize=8)
    occupancy.tick_params(axis="y",labelsize=9,length=0)
    occupancy.set_title("Images per bin (n = 360 each)",loc="left",fontsize=9,pad=5)
    for j,method in enumerate(methods):
        for i,b in enumerate(figure_data["calibration"][method]):
            occupancy.text(.05+.1*i,j,str(b["count"]),ha="center",va="center",fontsize=8)
    for edge in np.arange(0,1.01,.1): occupancy.axvline(edge,color="#dddddd",linewidth=.5)
    for edge in [-.5,.5,1.5,2.5]: occupancy.axhline(edge,color="#dddddd",linewidth=.5)
    save(fig,"calibration",["metrics.json","predictions.npz"],
         f"Unconnected, equal-size reliability points with exact bin-count table; within-group MI ECDFs, fixed seed {seed}.")

    fig,axes=plt.subplots(1,2,figsize=(7,2.9),sharey=True,layout="constrained")
    for s,color,style,marker in zip(config["seeds"],COLORS,STYLES,MARKERS):
        h=json.loads((root/f"history_{s}.json").read_text())
        axes[0].plot([v["epoch"] for v in h],[v["train_nll"] for v in h],color=color,
                     linestyle=style,marker=marker,markevery=20,markersize=4,linewidth=1.8,label=f"seed {s}")
        axes[1].plot([v["epoch"] for v in h],[v["validation_nll"] for v in h],color=color,
                     linestyle=style,marker=marker,markevery=20,markersize=4,linewidth=1.8)
    for ax in axes: ax.set(xlabel="Completed epoch",ylabel="Mean NLL (nats)",yscale="log",
                          ylim=(.025,3),xlim=(0,120),xticks=[0,30,60,90,120])
    panel(axes[0],"A","Training"); panel(axes[1],"B","Validation")
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=3,fontsize=9)
    save(fig,"convergence",[f"history_{s}.json" for s in config["seeds"]],"Feature network NLL, before convex last-layer refitting.")

    fig,axes=plt.subplots(1,2,figsize=(7,2.9),layout="constrained")
    sens=json.loads((root/"sensitivity.json").read_text())
    for s,color,style,marker in zip(config["seeds"],COLORS,STYLES,MARKERS):
        v=[r for r in sens if r["seed"]==s]
        axes[0].plot([r["alpha"] for r in v],[r["laplace_validation_nll"] for r in v],
                     marker=marker,linestyle=style,color=color,label=f"seed {s}")
    axes[0].set(xlabel="Prior precision alpha (log10)",ylabel="Validation NLL (nats)",xscale="log",ylim=(0,None))
    axes[0].legend(fontsize=8)
    for j,method,color in zip(range(3),["Matched MAP","Laplace","Diagonal Laplace"],
                              [COLORS[1],COLORS[2],"#CC79A7"]):
        vals=[r["metrics"]["nll"] for r in records if r["method"]==method]
        for i,v in enumerate(vals): axes[1].scatter(j+(i-1)*.13,v,color=color,marker=MARKERS[i],s=25)
        axes[1].errorbar(j,np.mean(vals),yerr=np.std(vals,ddof=1),fmt="_",capsize=4,color="black")
    axes[1].set(xticks=range(3),xticklabels=["Matched\nMAP","Full\nLaplace","Diagonal\nLaplace"],
                ylabel="Test NLL (nats)",ylim=(0,None))
    panel(axes[0],"A","Validation-only selection"); panel(axes[1],"B","Fixed-prior controls")
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
    diagnostic=root/"review_diagnostics"
    if (diagnostic/"summary.json").exists():
        values=json.loads((diagnostic/"summary.json").read_text())
        reference=json.loads((diagnostic/"matched_map.json").read_text())
        fig,axes=plt.subplots(1,2,figsize=(7,2.8),layout="constrained")
        for s,color,style,marker in zip(config["seeds"],COLORS,STYLES,MARKERS):
            rows=[v for v in values if v["feature_seed"]==s]
            baseline=next(v["matched_map_nll"] for v in reference if v["feature_seed"]==s)
            counts=[v["samples"] for v in rows]
            axes[0].errorbar(counts,[v["nll"]["mean"]-baseline for v in rows],
                yerr=[v["nll"]["sd"] for v in rows],marker=marker,linestyle=style,
                color=color,capsize=3,label=f"feature seed {s}")
            axes[1].plot(counts,[v["nll"]["sd"] for v in rows],marker=marker,linestyle=style,color=color)
        for ax in axes:
            ax.set(xscale="log",xticks=[128,512,2048],xticklabels=[128,512,2048],
                   xlabel="Posterior samples (log2)",ylim=(0,None))
            ax.minorticks_off()
        axes[0].set_ylabel("NLL minus matched MAP (nats)")
        axes[1].set_ylabel("Sampling-repeat NLL SD (nats)")
        panel(axes[0],"A","Fixed-model NLL penalty"); panel(axes[1],"B","Integration variability")
        axes[0].legend(fontsize=8,loc="lower left")
        figure_data["monte_carlo"]=values
        save(fig,"monte_carlo",["review_diagnostics/summary.json","review_diagnostics/matched_map.json"],
             "Post hoc fixed-model diagnostic; eight independent sampling repetitions per model/count, not a test-set CI.")
    # A CSV links every scalar to its method/seed.
    with (root/"scalar_metrics.csv").open("w",newline="",encoding="utf8") as stream:
        keys=["accuracy","macro_f1","macro_precision","macro_recall","nll","brier","ece"]
        writer=csv.DictWriter(stream,fieldnames=["method","seed"]+keys)
        writer.writeheader()
        for r in records: writer.writerow(dict(method=r["method"],seed=r["seed"],
                                              **{k:r["metrics"][k] for k in keys}))
    (root/"figure_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf8",newline="\n")
    (root/"figure_data.json").write_text(json.dumps(figure_data,indent=2),encoding="utf8",newline="\n")
    print(f"Generated {len(manifest)} figures in PDF/SVG/PNG: {out}")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--results",default="results")
    generate(parser.parse_args().results)
