"""Meaningful checks of new estimands, intervals and mathematical boundaries."""
import numpy as np
from scipy.special import softmax
from bayes_digits.paired import image_scores, paired_analysis, wilson_interval
from bayes_digits.laplace import hessian, Posterior


def test_paired_scores_and_identical_models():
    y=np.array([0,1,1]); p=np.array([[.9,.1],[.6,.4],[.2,.8]])
    scores=image_scores(y,p)
    np.testing.assert_allclose(scores['error'],[[0,1,0]])
    np.testing.assert_allclose(scores['nll'],[-np.log(p[np.arange(3),y])])
    np.testing.assert_allclose(scores['brier'],[[.02,.72,.08]])
    identical=paired_analysis(y,p[None],p[None],repetitions=20)
    assert all(v['estimate']==0 and v['percentile95']==[0,0] for v in identical.values())


def test_wilson_sparse_and_empty_bins():
    assert wilson_interval(0,0) is None
    low,high=wilson_interval(1,1)
    assert np.isclose(low,.20654931437723745) and np.isclose(high,1)
    low,high=wilson_interval(0,1)
    assert np.isclose(low,0) and np.isclose(high,.7934506856227626)


def test_hessian_indexing_and_common_shift_curvature():
    f=np.array([[1.,2.],[-.2,.7],[.1,-.8]])
    w=np.array([[.3,.4],[-.1,.2],[.6,-.2]])
    p=softmax(f@w.T,axis=1); alpha=.7
    exact=hessian(w,f,alpha)
    for k in range(3):
        for a in range(2):
            for l in range(3):
                for b in range(2):
                    independent=np.sum(p[:,k]*((k==l)-p[:,l])*f[:,a]*f[:,b])+alpha*(k==l)*(a==b)
                    assert np.isclose(exact[2*k+a,2*l+b],independent)
    v=np.tile([.8,-.4],3)
    np.testing.assert_allclose(exact@v,alpha*v,atol=1e-12)
    assert np.linalg.eigvalsh(exact).min()>=alpha-1e-12


def test_predictive_mi_matches_direct_entropy():
    posterior=Posterior(np.zeros((2,2)),np.eye(4),0,0)
    f=np.array([[.5,1.],[-.3,1.]])
    draws=posterior.samples(32,44)
    samples=softmax(np.einsum('nd,skd->snk',f,draws),axis=-1)
    mean=samples.mean(0)
    direct=-(mean*np.log(mean)).sum(1)+(samples*np.log(samples)).sum(2).mean(0)
    p,mi=posterior.predict(f,32,44)
    np.testing.assert_allclose(p,mean)
    np.testing.assert_allclose(mi,direct)
    assert (mi>=0).all() and (mi<=np.log(2)+1e-12).all()
