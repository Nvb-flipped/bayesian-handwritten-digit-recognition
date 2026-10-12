"""Independent supplementary check using SciPy bootstrap and count-weighted ECE."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import bootstrap, binomtest


def audit():
    source=np.load('results/predictions.npz'); y=source['labels']
    record=json.loads(Path('results/refinement_05/paired.json').read_text())
    for name,digest in record['source_sha256'].items():
        assert hashlib.sha256((Path('results')/name).read_bytes()).hexdigest()==digest
    for name,digest in record['generator_sha256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest
    l=np.array([source[f'Laplace_{s}'] for s in record['fixed_seeds']])
    m=np.array([source[f'Matched_MAP_{s}'] for s in record['fixed_seeds']])
    truth=np.eye(10)[y]
    for key in ['error','nll','brier']:
        def score(p):
            if key=='error':return (p.argmax(2)!=y).astype(float)
            if key=='nll':return -np.log(np.maximum(p[:,np.arange(len(y)),y],1e-15))
            return np.sum((p-truth)**2,axis=2)
        delta=(score(l)-score(m)).mean(0)
        reference=bootstrap((delta,),np.mean,n_resamples=record['repetitions'],method='percentile',
            rng=np.random.default_rng(record['bootstrap_seed']))
        value=record['differences'][key]
        np.testing.assert_allclose(delta.mean(),value['estimate'],atol=1e-14)
        np.testing.assert_allclose(reference.confidence_interval,value['percentile95'],atol=1e-14)
    rng=np.random.default_rng(record['bootstrap_seed'])
    indices=rng.integers(0,len(y),size=(record['repetitions'],len(y)))
    weights=np.array([np.bincount(row,minlength=len(y)) for row in indices])
    def ece(p,w):
        groups=np.minimum(np.floor(10*p.max(1)).astype(int),9)
        residual=(p.argmax(1)==y)-p.max(1)
        matrix=np.eye(10)[groups]*residual[:,None]
        return np.abs(w@matrix).sum(-1)/len(y)
    delta=np.mean([ece(lp,weights)-ece(mp,weights) for lp,mp in zip(l,m)],axis=0)
    value=record['differences']['ece']
    np.testing.assert_allclose(np.quantile(delta,[.025,.975]),value['percentile95'],atol=1e-14)
    np.testing.assert_allclose(np.mean([ece(lp,np.ones(len(y)))-ece(mp,np.ones(len(y)))
        for lp,mp in zip(l,m)]),value['estimate'],atol=1e-14)
    bins=0
    for rows in record['reliability'].values():
        assert sum(row['count'] for row in rows)==len(y)
        for row in rows:
            if row['count']:
                interval=binomtest(row['successes'],row['count']).proportion_ci(method='wilson')
                np.testing.assert_allclose(interval,row['wilson95'],atol=1e-14);bins+=1
            else:assert row['wilson95'] is None
    output=dict(source_arrays_unchanged=True,scipy_percentile_intervals_verified=3,
        independent_count_weighted_ece_verified=True,scipy_wilson_intervals_verified=bins,
        paired_record_sha256=hashlib.sha256(Path('results/refinement_05/paired.json').read_bytes()).hexdigest())
    Path('results/refinement_05/paired_audit.json').write_text(json.dumps(output,indent=2)+'\n',newline='\n')
    print(f'Paired audit passed: three SciPy bootstrap intervals, independent ECE and {bins} Wilson intervals.')


if __name__=='__main__':
    audit()
