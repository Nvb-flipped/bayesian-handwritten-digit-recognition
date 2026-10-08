"""Quantify integration variation without fitting or selecting any model."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import torch
from bayes_digits.data import load_data
from bayes_digits.features import FeatureNetwork, transform
from bayes_digits.laplace import Posterior, map_predict
from bayes_digits.metrics import evaluate
from bayes_digits.experiment import save_json


def run(config_path='configs/review_diagnostics.json'):
    started=time.perf_counter()
    settings=json.loads(Path(config_path).read_text())
    root=Path(settings['results'])
    output=Path(settings['output'])
    output.mkdir(parents=True,exist_ok=True)
    primary=json.loads((root/'config.json').read_text())
    torch.set_num_threads(primary['threads'])
    x,y,_,_=load_data(primary['split_seed'])
    test=np.load(root/'splits.npz')['test']
    hashes={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((root/'models').glob('*'))}
    records=[]
    probabilities=dict(labels=y[test],indices=test)
    references=[]
    for seed in primary['seeds']:
        saved=torch.load(root/'models'/f'features_{seed}.pt',weights_only=True)
        model=FeatureNetwork(saved['hidden'])
        model.load_state_dict(saved['state_dict'])
        model.eval()
        f=transform(model,x[test])
        arrays=np.load(root/'models'/f'posterior_{seed}.npz')
        posterior=Posterior(arrays['mean'],arrays['precision'],0,0)
        reference=evaluate(y[test],map_predict(posterior.mean,f),primary['calibration_bins'])
        references.append(dict(feature_seed=seed,matched_map_nll=reference['nll']))
        for count in settings['sample_counts']:
            for repetition in range(settings['repetitions']):
                sampling_seed=settings['sampling_seed_base']+seed*10000+count*10+repetition
                p,_=posterior.predict(f,count,sampling_seed)
                metrics=evaluate(y[test],p,primary['calibration_bins'])
                records.append(dict(feature_seed=seed,samples=count,repetition=repetition,
                                    sampling_seed=sampling_seed,
                                    metrics={k:metrics[k] for k in ['nll','brier','ece','accuracy']}))
                probabilities[f'p_{seed}_{count}_{repetition}']=p
            print(f'Fixed feature seed {seed}: {count} draws, {settings["repetitions"]} repetitions',flush=True)
    summary=[]
    for seed in primary['seeds']:
        for count in settings['sample_counts']:
            members=[r for r in records if r['feature_seed']==seed and r['samples']==count]
            summary.append(dict(feature_seed=seed,samples=count,
                **{key:dict(mean=float(np.mean([r['metrics'][key] for r in members])),
                            sd=float(np.std([r['metrics'][key] for r in members],ddof=1)))
                   for key in ['nll','brier','ece','accuracy']}))
    # Bind this post hoc diagnostic to unchanged selected checkpoints.
    assert all(hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest
               for name,digest in hashes.items())
    save_json(output/'config.json',settings)
    save_json(output/'records.json',records)
    save_json(output/'summary.json',summary)
    save_json(output/'matched_map.json',references)
    np.savez_compressed(output/'probabilities.npz',**probabilities)
    save_json(output/'provenance.json',dict(analysis='Post hoc; fixed models; no selection',
        checkpoint_sha256=hashes,config_sha256=hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        command=sys.argv,seconds=time.perf_counter()-started,records=len(records),test_images=len(test),
        variability_unit='Independent posterior sampling repetitions conditional on each fitted model/test set'))
    print(f'Saved {len(records)} fixed-model diagnostic predictions; model hashes unchanged.')


if __name__=='__main__':
    run(sys.argv[1] if len(sys.argv)>1 else 'configs/review_diagnostics.json')
