"""Reload models, regenerate reported metrics, and compare a fresh full run."""
import json
from pathlib import Path
import sys
import numpy as np
import torch
from bayes_digits.data import load_data
from bayes_digits.features import FeatureNetwork, transform
from bayes_digits.laplace import Posterior, map_predict
from bayes_digits.metrics import evaluate
from bayes_digits.experiment import reproduce, save_json

root=Path("results")
config=json.loads((root/"config.json").read_text())
x,y,s,_=load_data(config["split_seed"])
saved=np.load(root/"predictions.npz")
records=json.loads((root/"metrics.json").read_text())
for r in records:
    key=r["method"].replace(" ","_")
    if r["seed"] is not None: key+=f"_{r['seed']}"
    assert evaluate(y[s["test"]],saved[key],config["calibration_bins"])==r["metrics"]
for seed in config["seeds"]:
    checkpoint=torch.load(root/"models"/f"features_{seed}.pt",weights_only=True)
    feature=FeatureNetwork(checkpoint["hidden"])
    feature.load_state_dict(checkpoint["state_dict"])
    feature.eval()
    head=np.load(root/"models"/f"posterior_{seed}.npz")
    p=Posterior(head["mean"],head["precision"],0,0)
    f=transform(feature,x[s["test"]])
    probabilities,_=p.predict(f,config["posterior_samples"],seed+2000)
    assert np.array_equal(probabilities,saved[f"Laplace_{seed}"])
    assert np.array_equal(map_predict(head["map_mean"],f),saved[f"MAP_{seed}"])
config["output"]="tmp/reproduction"
path=Path("tmp/reproduction_config.json")
path.parent.mkdir(exist_ok=True)
save_json(path,config)
reproduce(path)
again=np.load("tmp/reproduction/predictions.npz")
assert saved.files==again.files
assert all(np.array_equal(saved[k],again[k]) for k in saved.files)
assert json.loads((root/"summary.json").read_text())==json.loads(Path("tmp/reproduction/summary.json").read_text())
save_json(root/"audit.json",dict(metrics_regenerated=True,checkpoint_predictions_bitwise_equal=True,
    full_reproduction_bitwise_equal=True,independent_command=sys.argv,
    probability_arrays_checked=len(saved.files),tests="Seven pytest tests; see execution log"))
print("Audit passed: metrics, checkpoint reloads, and full rerun match exactly.")

