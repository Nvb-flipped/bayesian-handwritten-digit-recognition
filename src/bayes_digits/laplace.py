"""Exact conditional softmax Hessian and Gaussian posterior integration.

W is class-major (K,D), including bias in the final column of each class.
The prior and likelihood use summed, not averaged, negative log likelihood.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax


def objective_gradient(flat, features, labels, precision, classes=10):
    w = flat.reshape(classes, features.shape[1])
    logits = features @ w.T
    loss = np.sum(logsumexp(logits, axis=1) - logits[np.arange(len(labels)), labels])
    probabilities = softmax(logits, axis=1)
    probabilities[np.arange(len(labels)), labels] -= 1
    gradient = probabilities.T @ features + precision * w
    return float(loss + 0.5 * precision * np.sum(w*w)), gradient.ravel()


def hessian(w, features, precision):
    p = softmax(features @ w.T, axis=1)
    curvature = -np.einsum("nk,nl->nkl", p, p)
    for k in range(w.shape[0]):
        curvature[:, k, k] += p[:, k]
    h = np.einsum("nkl,nf,ng->kflg", curvature, features, features, optimize=True)
    h = h.reshape(w.size, w.size)
    return (h + h.T) / 2 + precision * np.eye(w.size)


@dataclass
class Posterior:
    mean: np.ndarray
    precision: np.ndarray
    gradient_max: float
    iterations: int

    def samples(self, count, seed, diagonal=False):
        rng = np.random.default_rng(seed)
        eps = rng.standard_normal((self.mean.size, count))
        if diagonal:
            delta = eps / np.sqrt(np.diag(self.precision))[:, None]
        else:
            lower = np.linalg.cholesky(self.precision)
            delta = solve_triangular(lower.T, eps, lower=False)
        return (self.mean.ravel()[:, None] + delta).T.reshape(
            count, *self.mean.shape)

    def predict(self, features, count=512, seed=0, diagonal=False):
        draws = self.samples(count, seed, diagonal)
        p = softmax(np.einsum("nd,skd->snk", features, draws), axis=-1)
        mean = p.mean(axis=0)
        entropy = -np.sum(mean * np.log(np.clip(mean, 1e-15, 1)), axis=1)
        expected = -np.sum(p * np.log(np.clip(p, 1e-15, 1)), axis=2).mean(axis=0)
        return mean, np.maximum(entropy - expected, 0)


def fit_posterior(features, labels, precision, classes=10):
    if precision <= 0:
        raise ValueError("A proper positive Gaussian prior precision is required")
    fitted = minimize(objective_gradient, np.zeros(classes * features.shape[1]),
                      args=(features, labels, precision, classes), jac=True,
                      method="L-BFGS-B",
                      options=dict(maxiter=2000, ftol=1e-14, gtol=1e-7, maxls=40))
    grad = float(np.max(np.abs(fitted.jac)))
    if not fitted.success or grad > 1e-3:
        raise RuntimeError(f"MAP did not converge: {fitted.message}; gradient={grad}")
    mean = fitted.x.reshape(classes, features.shape[1])
    return Posterior(mean, hessian(mean, features, precision), grad, fitted.nit)


def map_predict(mean, features):
    return softmax(features @ mean.T, axis=1)

