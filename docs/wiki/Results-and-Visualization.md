# Experiments and results

[Home](Home.md) · [Method](Algorithm-and-Mathematics.md) · [Protocol](Dataset-and-Experiment-Protocol.md)

32 tanh features; 120 full-batch Adam epochs; learning rate 0.01; feature decay 0.0001; seeds 11/22/33; CPU/four PyTorch threads. Prior grid 0.1/1/10; NB smoothing 1e-9/0.001/0.1; selection by validation NLL. 512 posterior draws, full 330×330 conditional Hessian.

Selected feature epoch: 120 in all seeds. Laplace prior: 1/1/1. MAP prior: 0.1/0.1/1. NB smoothing: 0.1.

| Method | Accuracy (%) | NLL | Brier | ECE |
|---|---:|---:|---:|---:|
| Gaussian NB | 91.94 | 0.630 | 0.134 | 0.063 |
| MAP | 97.78 ± 0.28 | 0.099 ± 0.003 | 0.040 ± 0.002 | 0.017 ± 0.008 |
| Laplace | 97.69 ± 0.16 | 0.151 ± 0.003 | 0.055 ± 0.001 | 0.080 ± 0.003 |

SD is across initialization seeds on the **same** test set, not a confidence interval. NB runs once. NLL uses natural logs/probability floor 1e-15. Brier sums over classes. ECE uses ten equal-width top-label bins, including confidence 1 in the final bin.

| Frozen-prior variant | NLL | ECE |
|---|---:|---:|
| Matched MAP | 0.097 ± 0.002 | 0.025 ± 0.002 |
| Full Laplace | 0.151 ± 0.003 | 0.080 ± 0.003 |
| Diagonal Laplace | 0.229 ± 0.0002 | 0.147 ± 0.005 |

Correlations help relative to diagonal precision, but averaging worsens proper scores relative to matched MAP. Test results were not used to retune.

Digit 8 mean F1: 0.931; recall: 0.905. Seed 11 has eight errors/352 correct cases. All its mistakes are displayed in ascending original index. Averaging confusion over seeds does not increase unique test support beyond 360.

Nine evidence figures cover dataset, inference, comparison, classes, calibration/disagreement, convergence, prior/curvature sensitivity, sampling diagnostics and errors. The comparison plots error counts from zero and offsets seed points. Class errors use $1-F_1$ on a nonnegative axis, with all three seed values, means and observed min–max spans; these spans are not confidence intervals. The confusion cells display rounded integer percentages, with full-precision data retained. Reliability uses equal-size unconnected points and an aligned table of all ten confidence-bin counts, including zeros; MI uses separately normalized empirical cumulative distributions for correct/error groups. Curve losses are both measured after each epoch update on shared positive logarithmic limits. An additional explicitly labeled toy covariance diagram explains why smaller marginal variances can accompany larger logit-contrast variance; it is not ten-class experimental evidence. JSON/NPZ, transformed figure_data.json, source hashes and plot scripts supply provenance.

## Post hoc integration diagnostic

After the initial test results were known, Prompt 02 fixed the existing models/priors and specified 128/512/2048 draws with eight independent repetitions per model/count (72 predictions). This is a numerical diagnostic, not model selection. At 512 draws, within-model NLL SD is 0.0013–0.0019 nats. At 2048 draws, mean Laplace-minus-matched-MAP NLL remains 0.0511–0.0555 nats across the three models. It supports a persistent probability-score penalty in this setting. Repetition SD describes integration variation, not data-sampling uncertainty. All 18 primary arrays remain bitwise unchanged from a28a563.

Limits: one small dataset, one split, no writer separation, point-estimated features, local Gaussian, coarse prior grid, reused validation partition and finite Monte Carlo samples. No general algorithm ranking is claimed.

![Measured classifier comparison](https://raw.githubusercontent.com/Nvb-flipped/bayesian-handwritten-digit-recognition/main/results/figures/comparison.png)

![Per-class confusion and all measured F1 deficits](https://raw.githubusercontent.com/Nvb-flipped/bayesian-handwritten-digit-recognition/main/results/figures/classes.png)
