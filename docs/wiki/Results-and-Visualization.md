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

All ten figures have been redesigned from exact saved data in PDF/SVG/300-DPI PNG. Dataset counts remain exact and examples deterministic. The architecture diagram separates training/validation from the locked test stage. Paired per-digit $F_1(\mathrm{Laplace})-F_1(\mathrm{MAP})$ replaces the deficit display: individual seed shapes and black descriptive means retain genuine signed differences against separately selected MAP. Confusion cells retain rounded percentages and full-precision source data. Training losses retain completed-epoch values and shared positive logarithmic limits; prior candidates are discrete unconnected points rather than an interpolated optimum. Failure images retain native pixels and deterministic indices, with true/predicted probabilities. Covariance geometry remains a tested mathematical toy, not measured ten-class evidence.

Calibration uses three separate reliability panels, exact ten-bin image counts and marginal 95% Wilson bin-accuracy intervals. Open points flag n < 20; empty bins are omitted without erasing their counts. Intervals assume independent bin outcomes and are not simultaneous calibration bands or mean-confidence intervals. The fourth panel separately normalizes MI ECDFs over 352 correct predictions and just eight errors (seed 11). This small error group cannot establish an error detector.

## Post hoc paired image analysis

Prompt 05 resamples the same 360 positions jointly over both methods and three fixed models, 5,000 repetitions, seed 20261012. Estimates are Laplace minus matched-prior MAP; the analysis is exploratory and conditional on fitted models/draws.

| Difference | Estimate | Conditional 95% percentile interval |
|---|---:|---:|
| Error, percentage points | 0.00000 | [−0.27778, +0.27778] |
| NLL, nats | 0.05389 | [0.03994, 0.06612] |
| Brier, class sum | 0.01358 | [0.00823, 0.01878] |
| ECE, ten bins | 0.05536 | [0.04162, 0.05959] |

Unknown writer dependence, new splits, retraining and fresh posterior draws are not covered. ECE is recomputed in every resample and remains bin-dependent and biased. These intervals differ from seed SD and MC-repeat SD; no significance or equivalence claim is made. [Full calculation and source hashes](../../results/refinement_05/paired.json). [Current audit and plot rationale](../refinement_05.md).

The controlled comparison demonstrates the score penalty for this posterior average, not why the approximation is inaccurate. Local Gaussian assumptions, omitted feature uncertainty and prior/feature-scale effects are plausible unisolated causes. Softmax nonlinearity means the predictive average need not match MAP; convexity of negative log only compares mixture NLL to average sampled-head NLL, not MAP NLL. Original primary measurements and model choices are unchanged.

## Post hoc integration diagnostic

After the initial test results were known, Prompt 02 fixed the existing models/priors and specified 128/512/2048 draws with eight independent repetitions per model/count (72 predictions). This is a numerical diagnostic, not model selection. At 512 draws, within-model NLL SD is 0.0013–0.0019 nats. At 2048 draws, mean Laplace-minus-matched-MAP NLL remains 0.0511–0.0555 nats across the three models. It supports a persistent probability-score penalty in this setting. Repetition SD describes integration variation, not data-sampling uncertainty. All 18 primary arrays remain bitwise unchanged from a28a563.

Limits: one small dataset, one split, no writer separation, point-estimated features, local Gaussian, coarse prior grid, reused validation partition and finite Monte Carlo samples. No general algorithm ranking is claimed.

![Measured classifier comparison](https://raw.githubusercontent.com/Nvb-flipped/bayesian-handwritten-digit-recognition/main/results/figures/comparison.png)

![Per-class confusion and paired per-digit F1 differences](https://raw.githubusercontent.com/Nvb-flipped/bayesian-handwritten-digit-recognition/main/results/figures/classes.png)
