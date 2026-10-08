import numpy as np
import pytest
import torch
from bayes_digits.data import load_data
from bayes_digits.features import train_features, transform
from bayes_digits.laplace import objective_gradient, hessian, fit_posterior, map_predict, Posterior
from bayes_digits.metrics import evaluate, reliability


def test_splits_fixed_disjoint_complete():
    x,y,s,d=load_data()
    assert x.shape==(1797,64)
    assert [len(s[k]) for k in ["train","validation","test"]]==[1077,360,360]
    assert len(set(np.concatenate(list(s.values()))))==1797
    assert all(np.array_equal(s[k],load_data()[2][k]) for k in s)
    assert 0<=x.min()<=x.max()<=1


def test_exact_gradient_and_hessian_against_autograd():
    rng=np.random.default_rng(1)
    f=rng.normal(size=(7,3))
    labels=np.arange(7)%3
    flat=rng.normal(size=9)
    ft=torch.tensor(f,dtype=torch.float64)
    yt=torch.tensor(labels)
    wt=torch.tensor(flat,dtype=torch.float64,requires_grad=True)
    def loss(w):
        return torch.nn.functional.cross_entropy(ft@w.reshape(3,3).T,yt,reduction="sum")+0.7*(w*w).sum()/2
    grad=torch.autograd.grad(loss(wt),wt)[0].detach().numpy()
    exact=torch.autograd.functional.hessian(loss,wt).detach().numpy()
    assert np.allclose(objective_gradient(flat,f,labels,0.7,3)[1],grad,atol=1e-10)
    assert np.allclose(hessian(flat.reshape(3,3),f,0.7),exact,atol=1e-10)


def test_covariance_sampling_orientation():
    h=np.array([[4.,1.],[1.,2.]])
    p=Posterior(np.zeros((2,1)),h,0,0)
    samples=p.samples(100000,3).reshape(-1,2)
    assert np.allclose(np.cov(samples,rowvar=False),np.linalg.inv(h),atol=0.005)


def test_posterior_convergence_normalization_serialization(tmp_path):
    f=np.column_stack([np.linspace(-2,2,40),np.ones(40)])
    y=(f[:,0]>0).astype(int)
    p=fit_posterior(f,y,1.,2)
    probs,mi=p.predict(f,128,11)
    assert p.gradient_max<1e-3
    assert np.linalg.eigvalsh(p.precision).min()>0
    assert np.allclose(probs.sum(1),1)
    assert (mi>=0).all()
    path=tmp_path/"p.npz"
    np.savez(path,mean=p.mean,precision=p.precision)
    saved=np.load(path)
    restored=Posterior(saved["mean"],saved["precision"],0,0)
    assert np.array_equal(restored.predict(f,128,11)[0],probs)


def test_metrics_known_values_and_boundaries():
    y=np.array([0,1])
    perfect=np.eye(2)
    m=evaluate(y,perfect)
    assert m["accuracy"]==1 and m["brier"]==0 and m["nll"]==0 and m["ece"]==0
    uniform=np.full((2,2),0.5)
    assert np.isclose(evaluate(y,uniform)["nll"],np.log(2))
    assert np.isclose(evaluate(y,uniform)["brier"],0.5)
    assert sum(r["count"] for r in reliability(y,perfect)[0])==2
    with pytest.raises(ValueError):
        evaluate(y,perfect*2)


def test_feature_training_reproduces_and_overfits():
    x,y,s,_=load_data()
    idx=np.concatenate([np.flatnonzero(y==k)[:2] for k in range(10)])
    c=dict(hidden=32,threads=2,device="cpu",epochs=150,learning_rate=0.03,
           feature_weight_decay=0)
    a,ha,_=train_features(x[idx],y[idx],x[idx],y[idx],c,11)
    b,hb,_=train_features(x[idx],y[idx],x[idx],y[idx],c,11)
    assert ha==hb
    assert np.array_equal(transform(a,x[idx]),transform(b,x[idx]))
    with torch.no_grad():
        logits=a(torch.tensor(x[idx],dtype=torch.float32))
    assert (logits.argmax(1).numpy()==y[idx]).all()
    assert ha[-1]["train_nll"]<0.02
    assert np.isclose(ha[-1]["train_nll"],torch.nn.functional.cross_entropy(
        logits,torch.tensor(y[idx])).item(),atol=1e-7)
    assert ha[-1]["train_nll"]==ha[-1]["validation_nll"]


def test_symmetric_binary_map_and_logit_covariance():
    # Two labels at the same scalar feature have a unique zero MAP under alpha=1.
    f=np.ones((2,1))
    posterior=fit_posterior(f,np.array([0,1]),1.,2)
    expected=np.array([[1.5,-0.5],[-0.5,1.5]])
    assert np.allclose(posterior.mean,0,atol=1e-10)
    assert np.allclose(posterior.precision,expected,atol=1e-10)
    contrast=np.array([1.,-1.])
    assert np.isclose(contrast@np.linalg.solve(expected,contrast),1.)
    assert np.isclose(np.sum(contrast**2/np.diag(expected)),4/3)


def test_positive_prior_required():
    with pytest.raises(ValueError):
        fit_posterior(np.ones((3,1)),np.array([0,1,0]),0,2)
def test_json_evidence_has_portable_newlines(tmp_path):
    from bayes_digits.experiment import save_json
    import json
    path = tmp_path / "evidence.json"
    save_json(path, {"setting": [1, 2], "description": "recorded"})
    raw = path.read_bytes()
    assert b"\n" in raw and b"\r" not in raw
    assert json.loads(raw) == {"setting": [1, 2], "description": "recorded"}
