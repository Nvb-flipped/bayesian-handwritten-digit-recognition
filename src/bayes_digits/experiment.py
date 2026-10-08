"""Train/validate all candidates, lock selections, then access final test features."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import time
import joblib
import numpy as np
import scipy
import sklearn
import torch
from sklearn.naive_bayes import GaussianNB
from .data import load_data
from .features import train_features, transform
from .laplace import fit_posterior, map_predict
from .metrics import evaluate


def save_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8", newline="\n")


def reproduce(config_path):
    started = time.perf_counter()
    config = json.loads(Path(config_path).read_text())
    out = Path(config["output"])
    out.mkdir(parents=True, exist_ok=True)
    models = out / "models"
    models.mkdir(exist_ok=True)
    save_json(out/"config.json", config)
    x, y, split, digest = load_data(config["split_seed"])
    tr, va = split["train"], split["validation"]
    np.savez_compressed(out/"splits.npz", **split)
    dataset = dict(name="sklearn.load_digits (UCI optdigits test subset)",
                   sha256=digest, shape=list(x.shape),
                   split_sizes={k:len(v) for k,v in split.items()},
                   class_counts={k:np.bincount(y[v],minlength=10).tolist() for k,v in split.items()})
    save_json(out/"dataset.json", dataset)
    candidates = []
    for smoothing in config["nb_smoothing"]:
        model = GaussianNB(var_smoothing=smoothing).fit(x[tr],y[tr])
        score = evaluate(y[va], model.predict_proba(x[va]),config["calibration_bins"])["nll"]
        candidates.append((score,smoothing,model))
    nb_nll, nb_smoothing, nb = min(candidates,key=lambda r:r[0])
    joblib.dump(nb, models/"gaussian_nb.joblib")
    runs, selections, sensitivity = [], [], []
    for seed in config["seeds"]:
        clock = time.perf_counter()
        feature, history, epoch = train_features(x[tr],y[tr],x[va],y[va],config,seed)
        ft, fv = transform(feature,x[tr]), transform(feature,x[va])
        options = []
        for alpha in config["prior_precisions"]:
            posterior = fit_posterior(ft,y[tr],alpha)
            map_score = evaluate(y[va],map_predict(posterior.mean,fv))["nll"]
            lp, _ = posterior.predict(fv,config["posterior_samples"],seed+1000)
            laplace_score = evaluate(y[va],lp)["nll"]
            options.append((alpha,posterior,map_score,laplace_score))
            sensitivity.append(dict(seed=seed,alpha=alpha,map_validation_nll=map_score,
                                    laplace_validation_nll=laplace_score,
                                    gradient_max=posterior.gradient_max,
                                    iterations=posterior.iterations))
        m = min(options,key=lambda r:r[2])
        l = min(options,key=lambda r:r[3])
        selection = dict(seed=seed,feature_epoch=epoch,map_alpha=m[0],laplace_alpha=l[0],
                         map_validation_nll=m[2],laplace_validation_nll=l[3],
                         training_seconds=time.perf_counter()-clock)
        selections.append(selection)
        torch.save(dict(state_dict=feature.state_dict(),hidden=config["hidden"]),
                   models/f"features_{seed}.pt")
        np.savez_compressed(models/f"posterior_{seed}.npz", mean=l[1].mean,
                            precision=l[1].precision,map_mean=m[1].mean)
        save_json(out/f"history_{seed}.json",history)
        runs.append((seed,feature,m[1],l[1]))
        print(f"Seed {seed}: feature epoch {epoch}; MAP alpha {m[0]}, Laplace alpha {l[0]}",flush=True)
    # This file is written BEFORE any test transformation or prediction.
    save_json(out/"selection_locked.json",dict(rule="minimum validation NLL; grid order breaks ties",
              nb_smoothing=nb_smoothing,nb_validation_nll=nb_nll,selections=selections))
    save_json(out/"sensitivity.json",sensitivity)
    te = split["test"]
    records = []
    probabilities = dict(labels=y[te],indices=te)
    nbp = nb.predict_proba(x[te])
    records.append(dict(method="Gaussian NB",seed=None,metrics=evaluate(y[te],nbp)))
    probabilities["Gaussian_NB"] = nbp
    for seed,feature,map_head,laplace in runs:
        ftest = transform(feature,x[te])
        lap,mi = laplace.predict(ftest,config["posterior_samples"],seed+2000)
        diag,_ = laplace.predict(ftest,config["posterior_samples"],seed+2000,diagonal=True)
        variants = {"MAP":map_predict(map_head.mean,ftest),"Laplace":lap,
                    "Matched MAP":map_predict(laplace.mean,ftest),"Diagonal Laplace":diag}
        for method,p in variants.items():
            records.append(dict(method=method,seed=seed,
                                metrics=evaluate(y[te],p,config["calibration_bins"])))
            probabilities[f"{method.replace(' ','_')}_{seed}"] = p
        probabilities[f"MI_{seed}"] = mi
    np.savez_compressed(out/"predictions.npz",**probabilities)
    save_json(out/"metrics.json",records)
    scalar_keys = ["accuracy","macro_f1","macro_precision","macro_recall","nll","brier","ece"]
    summary = {}
    for method in ["Gaussian NB","MAP","Laplace","Matched MAP","Diagonal Laplace"]:
        members=[r for r in records if r["method"]==method]
        summary[method]={key:dict(mean=float(np.mean([r["metrics"][key] for r in members])),
                         sd=float(np.std([r["metrics"][key] for r in members],ddof=1)) if len(members)>1 else None)
                         for key in scalar_keys}
        summary[method]["runs"] = len(members)
    save_json(out/"summary.json",summary)
    environment = dict(python=sys.version,platform=platform.platform(),processor=platform.processor(),
                       numpy=np.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,
                       torch=torch.__version__,cuda_available=torch.cuda.is_available(),
                       detected_gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                       requested_device=config["device"],
                       used_device=("cuda" if torch.cuda.is_available() else "cpu")
                       if config["device"]=="auto" else config["device"],
                       seconds=time.perf_counter()-started,
                       command=" ".join(sys.argv))
    try:
        environment["git_revision"]=subprocess.check_output(
            ["git","rev-parse","HEAD"],stderr=subprocess.DEVNULL,text=True).strip()
    except subprocess.CalledProcessError:
        environment["git_revision"]=None
    environment["source_sha256"]={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(Path("src").rglob("*.py"))}
    save_json(out/"environment.json",environment)
    print(json.dumps(summary,indent=2),flush=True)
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",default="configs/default.json")
    args=parser.parse_args()
    reproduce(args.config)


if __name__ == "__main__":
    main()
