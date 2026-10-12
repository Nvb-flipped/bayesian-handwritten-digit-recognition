"""Regenerate all vector/raster figures exclusively from recorded evidence."""
import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np
from .data import load_data
from .laplace import hessian
from .paired import wilson_interval

COLORS=["#0072B2","#D55E00","#009E73"]
MARKERS=["o","s","^"]
STYLES=["-","--",":"]
METHOD_COLORS=["#666666","#0072B2","#D55E00"]
width_mm=170
WIDTH=width_mm/25.4
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["DejaVu Sans"],"font.size":9,"axes.labelsize":9,"xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":8,"legend.frameon":False,"axes.linewidth":.65,"axes.spines.top":False,"axes.spines.right":False,
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
        if name=="comparison":
            fig.set_layout_engine("none")
            for i,axis in enumerate(fig.axes): axis.set_position([.105+.315*i,.25,.225,.57])
        if name=="classes":
            fig.set_layout_engine("none")
            fig.axes[0].set_position([.07,.24,.33,.64])
            fig.axes[1].set_position([.645,.24,.33,.64])
            fig.axes[2].set_position([.43,.24,.025,.64])
        if name=="calibration":
            fig.set_layout_engine("none")
            for i,axis in enumerate(fig.axes):
                axis.set_position([.10+.49*(i%2),.66 if i<2 else .18,.39,.24])
        fig.savefig(out/f"{name}.pdf")
        fig.savefig(out/f"{name}.svg")
        svg=out/f"{name}.svg"
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf8").splitlines())+"\n",encoding="utf8",newline="\n")
        fig.savefig(out/f"{name}.png",dpi=300)
        manifest.append(dict(name=name,sources=sources,description=description,
                             inches=fig.get_size_inches().tolist(),raster_dpi=300,
                             generator="src/bayes_digits/figures.py",
                             supporting_source_sha256={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [Path("src/bayes_digits/paired.py"),Path("src/bayes_digits/laplace.py"),Path("src/bayes_digits/data.py")]},
                             generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             source_sha256={s:hashlib.sha256((root/s).read_bytes()).hexdigest()
                                            for s in sources if (root/s).is_file()}))
        # Optional installed QA helper; clean-clone generation has no private dependency.
        if os.environ.get("FIGURE_QA_PATH"):
            sys.path.insert(0,os.environ["FIGURE_QA_PATH"])
            from audit_panel_alignment import require_matplotlib_panel_alignment
            axes=[ax for ax in fig.axes if ax.get_label()!="<colorbar>"]
            exemptions=[]
            if name=="covariance_geometry":
                # Square image/geometry panels intentionally differ from Cartesian charts.
                exemptions=[dict(panels=["c"],
                    checks=["row","panel-width"],reason="Square image or equal-coordinate geometry panels retain aspect; unequal chart widths are deliberate.")]
            qa=root/"refinement_05"/"alignment"
            qa.mkdir(parents=True,exist_ok=True)
            if len(axes)>1:
                require_matplotlib_panel_alignment(fig,axes=axes,
                panel_ids=[chr(97+i) for i in range(len(axes))],exemptions=exemptions,
                json_out=qa/f"{name}.json")
        plt.close(fig)
    def panel(ax,letter,title):
        ax.set_title(f"{letter.lower()}  {title}",loc="left",fontsize=9,fontweight="bold",pad=9)
    fig,axes=plt.subplots(1,2,figsize=(WIDTH,2.65),width_ratios=[1,1],layout="constrained")
    counts=np.array([np.bincount(y[split[k]],minlength=10) for k in ["train","validation","test"]])
    axes[0].imshow(counts,cmap="Blues",aspect="auto",vmin=0,vmax=counts.max())
    for row in range(3):
        for col in range(10):
            axes[0].text(col,row,str(counts[row,col]),ha="center",va="center",fontsize=8,
                         color="white" if row==0 else "black")
    axes[0].set(xlabel="Digit",xticks=range(10),yticks=range(3),
        yticklabels=["Train\nn = 1077","Validation\nn = 360","Test\nn = 360"])
    axes[0].tick_params(length=0)
    panel(axes[0],"a","Exact split counts")
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

    fig,ax=plt.subplots(figsize=(WIDTH,3.05),layout="constrained")
    ax.axis("off")
    labels=["1  Learn features\nTrain 1077; validate 360",
        "2  Freeze representation\n32 tanh features + bias",
        "3  Estimate MAP heads\nTraining; alpha grid",
        "4  Exact training Hessian\n330 x 330 precision",
        "5  Gaussian posterior\nLocal head approximation",
        "6  Validate predictions\nSelect prior by NLL",
        "7  Lock all selections\nEpochs, priors, seeds",
        "8  Held-out integration\n512 draws; 360 test images",
        "9  Score probabilities\nRecognition, NLL, Brier, MI"]
    for i,text in enumerate(labels):
        row=i//3; col=i%3 if row!=1 else 2-i%3
        xpos=.015+col*.335; ypos=.70-row*.32
        color=["#EFF6FA","#F3F5F5","#FCF1E9"][row]
        ax.add_patch(FancyBboxPatch((xpos,ypos),.295,.225,boxstyle="round,pad=0.006",
            transform=ax.transAxes,edgecolor="#55616B",facecolor=color,linewidth=.7))
        ax.text(xpos+.1475,ypos+.1125,text,ha="center",va="center",transform=ax.transAxes,fontsize=8.5)
        if i%3<2:
            start=xpos+.301 if row!=1 else xpos-.006
            stop=xpos+.329 if row!=1 else xpos-.034
            ax.annotate("",xy=(stop,ypos+.1125),xytext=(start,ypos+.1125),xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->",linewidth=.9))
    for xcoord,y0,y1 in [(.8325,.694,.616),(.1625,.374,.296)]:
        ax.annotate("",xy=(xcoord,y1),xytext=(xcoord,y0),xycoords="axes fraction",
            arrowprops=dict(arrowstyle="->",linewidth=.9))
    save(fig,"inference",["config.json","selection_locked.json"],
         "Training and validation stages precede selection lock; test integration occurs only afterwards. Exact Hessian does not imply exact posterior.")

    precision,full,diagonal,contours=covariance_example()
    contrast=np.array([-1.,1.])
    variances=[float(contrast@c@contrast) for c in [full,diagonal]]
    fig,axes=plt.subplots(1,3,figsize=(WIDTH,2.7),layout="constrained")
    for ax,curve,c,color,letter,title in zip(axes[:2],contours,[full,diagonal],
            [COLORS[2],"#CC79A7"],"AB",["Full covariance","Diagonal precision"]):
        ax.plot(curve[:,0],curve[:,1],color=color,linewidth=2,
                linestyle="-" if letter=="A" else "--")
        ax.axhline(0,color="#dddddd",linewidth=.7)
        ax.set(xlabel=r"$w_0$",ylabel=r"$w_1$",xlim=(-1.25,1.25),ylim=(-1.25,1.25),
               xticks=[-1,0,1],yticks=[-1,0,1],aspect="equal")
        ax.text(0,-1.17,f"Marginal variance {c[0,0]:.3f}",ha="center",fontsize=8)
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

    fig,axes=plt.subplots(1,3,figsize=(WIDTH,2.6),layout="constrained")
    methods=["Gaussian NB","MAP","Laplace"]
    for letter,ax,key,label in zip("ABC",axes,["errors","nll","brier"],
                                  ["Errors / 360 images","NLL (nats)","Brier (class sum)"]):
        for j,method in enumerate(methods):
            members=[r for r in records if r["method"]==method]
            vals=[int(np.sum(r["metrics"]["confusion"])-np.trace(r["metrics"]["confusion"]))
                  if key=="errors" else r["metrics"][key] for r in members]
            for i,v in enumerate(vals):
                ax.scatter(j+(i-1)*.13 if len(vals)>1 else j,v,color=METHOD_COLORS[j],
                           marker=MARKERS[i] if len(vals)>1 else "D",s=25,zorder=3)
            if len(vals)>1:
                ax.errorbar(j,np.mean(vals),yerr=np.std(vals,ddof=1),color="black",capsize=4,fmt="_",zorder=2)
            if key=="errors":
                ax.text(j,max(vals)+3.0,"/".join(str(v) for v in vals),ha="center",fontsize=8)
        ax.set(xticks=np.arange(3),xticklabels=["GNB","MAP","LA"],ylabel=label,xlim=(-.5,2.5))
        ax.set_ylim(bottom=0)
        if key=="errors": ax.set_ylim(0,36)
        panel(ax,letter,["Recognition","Log loss","Brier score"]["ABC".index(letter)])
    fig.legend(handles=[Line2D([],[],marker=m,color="black",linestyle="none",label=f"seed {s}")
                        for s,m in zip(config["seeds"],MARKERS)],loc="outside lower center",ncol=3,fontsize=8)
    save(fig,"comparison",["metrics.json","summary.json"],"Raw seed results and sample SD; GNB evaluated once.")

    fig=plt.figure(figsize=(WIDTH,3.45),layout="constrained")
    grid=fig.add_gridspec(1,3,width_ratios=[1,.055,1])
    axes=[fig.add_subplot(grid[0,0]),fig.add_subplot(grid[0,2])]
    coloraxis=fig.add_subplot(grid[0,1]); coloraxis.set_label("<colorbar>")
    axes[1].set_box_aspect(1)
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
    fig.colorbar(im,cax=coloraxis,label="Row proportion")
    panel(axes[0],"A","Laplace confusion")
    f1={m:np.array([[r["metrics"]["per_class"][str(k)]["f1-score"] for k in range(10)]
                   for r in records if r["method"]==m]) for m in ["MAP","Laplace"]}
    delta=f1["Laplace"]-f1["MAP"]
    axes[1].axvline(0,color="#777777",linewidth=.8)
    for i,(color,marker) in enumerate(zip(COLORS,MARKERS)):
        axes[1].scatter(100*delta[i],np.arange(10)+(i-1)*.16,color=color,marker=marker,s=25,
                       label=f"seed {config['seeds'][i]}",zorder=3)
    axes[1].scatter(100*delta.mean(0),np.arange(10),marker="|",s=95,color="black",zorder=4)
    limit=max(1,100*np.abs(delta).max()+.6)
    axes[1].set(xlabel="F1(Laplace) - F1(MAP)\n(percentage points)",ylabel="Digit",
        yticks=range(10),ylim=(9.5,-.5),xlim=(-limit,limit))
    panel(axes[1],"b","Paired class differences")
    handles,labels=axes[1].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=3,fontsize=8)
    figure_data["classes"]={"mean_row_confusion":norm.tolist(),
        "f1_by_seed":{m:[[r["metrics"]["per_class"][str(k)]["f1-score"] for k in range(10)]
                           for r in records if r["method"]==m] for m in ["MAP","Laplace"]}}
    save(fig,"classes",["metrics.json"],"Row-normalized confusion; exact paired F1 differences against separately selected MAP, all three seeds and descriptive means. Signed scale preserves measured differences.")

    fig,axes=plt.subplots(2,2,figsize=(WIDTH,5.45),layout="constrained")
    figure_data["classes"]["paired_f1_difference"]=delta.tolist()
    figure_data["calibration"]={}
    figure_data["calibration_intervals"]={}
    for letter,ax,method,color in zip("abc",axes.ravel()[:3],methods,["#666666",COLORS[0],COLORS[1]]):
        r=next(r for r in records if r["method"]==method and (r["seed"]==seed or r["seed"] is None))
        bins=r["metrics"]["reliability"]
        figure_data["calibration"][method]=bins
        pmethod=preds["Gaussian_NB" if method=="Gaussian NB" else f"{method}_{seed}"]
        ids=np.minimum((pmethod.max(1)*10).astype(int),9)
        correct=pmethod.argmax(1)==preds["labels"]
        figure_data["calibration_intervals"][method]=[]
        for row in bins:
            n=row["count"]
            if not n: continue
            successes=int(correct[ids==row["bin"]].sum())
            lo,hi=wilson_interval(successes,n)
            figure_data["calibration_intervals"][method].append(dict(bin=row["bin"],count=n,
                successes=successes,wilson95=[lo,hi],sparse=n<20))
            ax.errorbar(row["confidence"],row["accuracy"],yerr=[[row["accuracy"]-lo],[hi-row["accuracy"]]],
                fmt="o",markersize=4,markerfacecolor=color if n>=20 else "white",
                markeredgecolor=color,ecolor=color,elinewidth=.8,capsize=2,clip_on=False)
        ax.plot([0,1],[0,1],color="#999999",linestyle="--",linewidth=.8)
        ax.set(xlabel="Mean confidence",ylabel="Observed accuracy",xlim=(-.02,1.02),ylim=(-.04,1.05),
            xticks=[0,.5,1],yticks=[0,.5,1])
        panel(ax,letter,f"{method} (n = 360)")
        # Exact support for all ten bins; explicit indices rather than a misleading area encoding.
        for i,row in enumerate(bins):
            ax.text(.05+.1*i,-.32,str(i),transform=ax.transAxes,ha="center",va="top",fontsize=7.5)
            ax.text(.05+.1*i,-.44,str(row["count"]),transform=ax.transAxes,ha="center",va="top",fontsize=7.5)
        ax.text(0,-.57,"Bin index (top); image count (bottom)",transform=ax.transAxes,fontsize=7.5,va="top")
    ax=axes[1,1]
    p=preds[f"Laplace_{seed}"]; good=p.argmax(1)==preds["labels"]; mi=preds[f"MI_{seed}"]
    for mask,label,color,style in [(good,"Correct",COLORS[0],"-"),(~good,"Errors",COLORS[1],"--")]:
        values=np.sort(mi[mask])
        ax.step(np.r_[0,values],np.r_[0,np.arange(1,len(values)+1)/len(values)],where="post",
            linewidth=1.5,color=color,linestyle=style,label=f"{label} (n = {mask.sum()})")
    ax.set(xlabel="Posterior MI (nats)",ylabel="Fraction within group",ylim=(0,1.03),xlim=(0,None))
    ax.legend(fontsize=8,loc="upper center",bbox_to_anchor=(.5,-.25),ncol=2)
    panel(ax,"d",f"Laplace disagreement (seed {seed})")
    ax.text(.5,-.52,"Reliability: 95% Wilson bars\nOpen points: fewer than 20 images",transform=ax.transAxes,
            ha="center",va="top",fontsize=8)
    figure_data["uncertainty"]={"correct":mi[good].tolist(),"errors":mi[~good].tolist()}
    save(fig,"calibration",["metrics.json","predictions.npz"],
        "Separated reliability panels with marginal Wilson bin-accuracy intervals and exact support; open points identify sparse bins (<20). MI ECDFs are separately normalized (352 correct, 8 errors).")

    fig,axes=plt.subplots(1,2,figsize=(WIDTH,2.9),sharey=True,layout="constrained")
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

    fig,axes=plt.subplots(1,2,figsize=(WIDTH,2.9),layout="constrained")
    sens=json.loads((root/"sensitivity.json").read_text())
    for s,color,style,marker in zip(config["seeds"],COLORS,STYLES,MARKERS):
        v=[r for r in sens if r["seed"]==s]
        axes[0].scatter([r["alpha"]*(1+.035*(config["seeds"].index(s)-1)) for r in v],
                     [r["laplace_validation_nll"] for r in v],marker=marker,color=color,label=f"seed {s}",s=30)
    axes[0].set(xlabel="Prior precision alpha (log10)",ylabel="Validation NLL (nats)",xscale="log",ylim=(0,None))
    axes[0].set_xticks([.1,1,10],labels=["0.1","1","10"])
    axes[0].minorticks_off()
    axes[0].legend(fontsize=8)
    for j,method,color in zip(range(3),["Matched MAP","Laplace","Diagonal Laplace"],
                              [METHOD_COLORS[1],METHOD_COLORS[2],"#CC79A7"]):
        vals=[r["metrics"]["nll"] for r in records if r["method"]==method]
        for i,v in enumerate(vals): axes[1].scatter(j+(i-1)*.13,v,color=color,marker=MARKERS[i],s=25)
        axes[1].errorbar(j,np.mean(vals),yerr=np.std(vals,ddof=1),fmt="_",capsize=4,color="black")
    axes[1].set(xticks=range(3),xticklabels=["Matched\nMAP","Full\nLaplace","Diagonal\nLaplace"],
                ylabel="Test NLL (nats)",ylim=(0,None))
    panel(axes[0],"A","Validation-only selection"); panel(axes[1],"B","Fixed-prior controls")
    save(fig,"sensitivity",["sensitivity.json","metrics.json"],"Prior selection uses validation; frozen-prior ablations use test.")

    bad=np.flatnonzero(p.argmax(1)!=preds["labels"])
    bad=bad[np.argsort(preds["indices"][bad])][:8]
    fig,axes=plt.subplots(2,4,figsize=(WIDTH,3.7),layout="constrained")
    for ax in axes.ravel(): ax.axis("off")
    for ax,j in zip(axes.ravel(),bad):
        ax.imshow(x[preds["indices"][j]].reshape(8,8),cmap="gray",vmin=0,vmax=1,interpolation="nearest")
        ax.set_title(f"True {preds['labels'][j]} -> prediction {p[j].argmax()}\n"
                     f"p(pred) {p[j].max():.2f}\n"
                     f"p(true) {p[j,preds['labels'][j]]:.2f}; index {preds['indices'][j]}",fontsize=8.5)
    save(fig,"errors",["predictions.npz","sklearn.load_digits"],
         "First eight mistakes in ascending dataset index; seed 11 fixed before experiments.")
    diagnostic=root/"review_diagnostics"
    if (diagnostic/"summary.json").exists():
        values=json.loads((diagnostic/"summary.json").read_text())
        assert all(row["samples"]>0 for row in values), "Log sample counts must be positive"
        reference=json.loads((diagnostic/"matched_map.json").read_text())
        fig,axes=plt.subplots(1,2,figsize=(WIDTH,2.8),layout="constrained")
        for s,color,style,marker in zip(config["seeds"],COLORS,STYLES,MARKERS):
            rows=[v for v in values if v["feature_seed"]==s]
            baseline=next(v["matched_map_nll"] for v in reference if v["feature_seed"]==s)
            counts=[v["samples"] for v in rows]
            axes[0].errorbar(counts,[v["nll"]["mean"]-baseline for v in rows],
                yerr=[v["nll"]["sd"] for v in rows],marker=marker,linestyle=style,
                color=color,capsize=3,label=f"feature seed {s}")
            axes[1].plot(counts,[v["nll"]["sd"] for v in rows],marker=marker,linestyle=style,color=color)
        for ax in axes:
            ax.set_xscale("log",base=2)
            ax.set(xticks=[128,512,2048],xticklabels=[128,512,2048],
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
