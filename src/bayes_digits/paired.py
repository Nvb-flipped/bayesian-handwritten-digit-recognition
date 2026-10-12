"""Post hoc paired finite-image analysis conditional on the frozen models."""
import numpy as np
from scipy.stats import norm
from .metrics import reliability


def image_scores(labels, probabilities):
    """Return image-level error, NLL and class-summed Brier (models, images)."""
    labels=np.asarray(labels)
    p=np.asarray(probabilities)
    if p.ndim==2:
        p=p[None]
    if p.shape[1]!=len(labels) or not np.isfinite(p).all() or (p<0).any() or not np.allclose(p.sum(-1),1):
        raise ValueError('Aligned finite normalized probabilities required')
    truth=np.eye(p.shape[-1])[labels]
    return dict(error=(p.argmax(-1)!=labels).astype(float),
                nll=-np.log(np.clip(p[:,np.arange(len(labels)),labels],1e-15,1)),
                brier=((p-truth)**2).sum(-1))


def paired_analysis(labels, laplace, matched, repetitions=5000, seed=20261012):
    """Jointly resample image positions; never treat model seeds as datasets."""
    la=image_scores(labels,laplace)
    ma=image_scores(labels,matched)
    if np.asarray(laplace).ndim!=3 or np.asarray(laplace).shape!=np.asarray(matched).shape or repetitions<2:
        raise ValueError('Matched shapes and at least two bootstrap repetitions required')
    rng=np.random.default_rng(seed)
    indices=rng.integers(0,len(labels),size=(repetitions,len(labels)))
    output={}
    for metric in la:
        deltas=la[metric]-ma[metric]
        # Average fixed models first; resample the SAME image position in all models.
        bootstrap=deltas.mean(0)[indices].mean(1)
        output[metric]=dict(estimate=float(deltas.mean()),
            per_seed=deltas.mean(1).tolist(),percentile95=np.quantile(bootstrap,[.025,.975]).tolist())
    # ECE is nonlinear: recompute bin membership/support in every resample.
    l=np.asarray(laplace); m=np.asarray(matched); y=np.asarray(labels)
    values=np.empty(repetitions)
    for b,idx in enumerate(indices):
        values[b]=np.mean([reliability(y[idx],lp[idx])[1]-reliability(y[idx],mp[idx])[1]
                          for lp,mp in zip(l,m)])
    per_seed=[reliability(y,lp)[1]-reliability(y,mp)[1] for lp,mp in zip(l,m)]
    output['ece']=dict(estimate=float(np.mean(per_seed)),per_seed=per_seed,
                       percentile95=np.quantile(values,[.025,.975]).tolist())
    return output


def wilson_interval(successes, count, confidence=.95):
    """Wilson binomial score interval; no interval for an empty bin."""
    if count<0 or not 0<confidence<1:
        raise ValueError("Nonnegative support and confidence in (0, 1) required")
    if count==0:
        return None
    if not 0<=successes<=count:
        raise ValueError('Success count must lie within bin support')
    z=norm.ppf((1+confidence)/2)
    p=successes/count
    denominator=1+z*z/count
    center=(p+z*z/(2*count))/denominator
    half=z*np.sqrt(p*(1-p)/count+z*z/(4*count*count))/denominator
    return [0. if successes==0 else float(max(0,center-half)),
            1. if successes==count else float(min(1,center+half))]
