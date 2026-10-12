"""Run the declared Prompt 05 analysis on exact saved predictions."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from bayes_digits.paired import paired_analysis, wilson_interval
from bayes_digits.metrics import reliability
from bayes_digits.experiment import save_json


def run(root='results', repetitions=5000):
    root=Path(root)
    output=root/'refinement_05'
    output.mkdir(exist_ok=True)
    config=json.loads((root/'config.json').read_text())
    saved=np.load(root/'predictions.npz')
    seeds=config['seeds']; y=saved['labels']
    laplace=np.array([saved[f'Laplace_{s}'] for s in seeds])
    matched=np.array([saved[f'Matched_MAP_{s}'] for s in seeds])
    estimates=paired_analysis(y,laplace,matched,repetitions)
    curves={}
    for method,key in [('Gaussian NB','Gaussian_NB'),('MAP',f'MAP_{seeds[0]}'),('Laplace',f'Laplace_{seeds[0]}')]:
        p=saved[key]; correct=p.argmax(1)==y; bins=reliability(y,p)[0]
        for row in bins:
            ids=np.minimum((p.max(1)*10).astype(int),9)
            successes=int(correct[ids==row['bin']].sum())
            row.update(successes=successes,wilson95=wilson_interval(successes,row['count']),sparse=row['count']<20)
        curves[method]=bins
    record=dict(analysis='Post hoc; Laplace minus matched-prior MAP',
        estimand='Mean score difference across three fixed fitted models on the same images',
        resampling_unit='Image position, jointly across all methods/seeds',
        images=len(y),fixed_seeds=seeds,repetitions=repetitions,bootstrap_seed=20261012,
        interval='95% paired percentile bootstrap; conditional on fixed fitted models',
        assumptions='Exchangeable test images; unknown writer dependence is not accounted for',
        limitations='Post hoc, one split; not seed uncertainty, MC integration uncertainty, a population guarantee or a significance test',
        differences=estimates,reliability_seed=seeds[0],reliability=curves,
        source_sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [root/'predictions.npz',root/'config.json']},
        generator_sha256={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in [Path('src/bayes_digits/paired.py'),Path('scripts/paired_analysis.py')]})
    save_json(output/'paired.json',record)
    # Preserve bootstrap variability separately from initialization and MC SD.
    print(json.dumps(estimates,indent=2))
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--results',default='results')
    parser.add_argument('--repetitions',type=int,default=5000)
    args=parser.parse_args(); run(args.results,args.repetitions)
