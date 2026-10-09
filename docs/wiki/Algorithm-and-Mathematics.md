# Method and mathematics

[Home](Home.md) · [Protocol](Dataset-and-Experiment-Protocol.md) · [Results](Results-and-Visualization.md)

For $x\in[0,1]^{64}$, learn $h_\phi(x)=\tanh(Ax+a)\in\mathbb R^{32}$ and append one, $f(x)=[h_\phi(x);1]$. Freeze $\phi$. Row-major flattening of $W\in\mathbb R^{10\times33}$ gives $\theta\in\mathbb R^{330}$.

Categorical softmax likelihood and Gaussian prior $p(\theta)=\mathcal N(0,\alpha^{-1}I)$ (including biases) give:

```math
L(\theta)=\sum_n\left[\log\sum_k\exp(w_k^\top f_n)-w_{y_n}^\top f_n\right]+\frac{\alpha}{2}\|\theta\|_2^2.
```

L-BFGS finds the unique MAP head for fixed features and $\alpha>0$. With $p_n=\mathrm{softmax}(Wf_n)$, exact conditional curvature is:

```math
H=\sum_n[\mathrm{diag}(p_n)-p_np_n^\top]\otimes(f_nf_n^\top)+\alpha I.
```

A second-order expansion gives $q(\theta)=\mathcal N(\hat\theta,H^{-1})$. If $H=LL^\top$, draw $\theta=\hat\theta+L^{-\top}\epsilon$. The transpose is tested by covariance simulation.

```math
\bar p_k(x)=\frac1{512}\sum_{s=1}^{512}\mathrm{softmax}(W^{(s)}f(x))_k,\qquad
\hat y=\arg\max_k\bar p_k(x).
```

Posterior disagreement equals $\mathcal H(\bar p)-\frac1S\sum_s\mathcal H(p^{(s)})$. It is conditional on point-estimated features, not complete network uncertainty.

Full matrix storage is $O(P^2)$ and factorization $O(P^3)$. The diagonal ablation drops off-diagonal **precision** entries before inversion. Matched MAP uses the same prior/features while omitting averaging. Validation prior tuning is not empirical-Bayes evidence optimization. The approximation is local and prior-sensitive.

## Verified numerical example

Two classes with scalar feature 1, one observation of each label and prior precision 1 have the unique MAP $W=(0,0)^\top$. Each observation contributes categorical curvature:

```math
\frac14\begin{bmatrix}1&-1\\-1&1\end{bmatrix}.
```

Thus:

```math
H=\begin{bmatrix}1.5&-0.5\\-0.5&1.5\end{bmatrix},\qquad
H^{-1}=\begin{bmatrix}0.75&0.25\\0.25&0.75\end{bmatrix}.
```

The logit difference $w_1-w_0$ has variance $0.75+0.75-2(0.25)=1$. Diagonalizing precision before inversion gives $(2/3)I$ and difference variance $4/3$. Marginal variances become smaller but difference variance increases. This shows how correlations cancel a shared logit shift. A unit test verifies the exact MAP/Hessian, both contrast variances and radius-one Mahalanobis contours. The [geometry diagram](../../results/figures/covariance_geometry.pdf) shows the full ellipse, diagonal-precision circle and exact contrast densities. Contours satisfy $w^\top\Sigma^{-1}w=1$; they are not 68% joint credible regions. It is a toy calculation, not an empirical causal explanation of the ten-class results.

![Verified toy covariance geometry](https://raw.githubusercontent.com/Nvb-flipped/bayesian-handwritten-digit-recognition/main/results/figures/covariance_geometry.png)
