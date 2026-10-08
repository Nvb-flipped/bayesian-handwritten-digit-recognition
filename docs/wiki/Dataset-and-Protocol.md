# Dataset and protocol

[Home](Home.md) · [Method](Method-and-Mathematics.md) · [Results](Experiments-and-Results.md)

The loader supplies 1,797 8×8 digit images, pixel values 0–16, ten classes. It contains UCI optdigits' original **test subset**. We repartition this subset, not the complete UCI collection.

[Loader provenance](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html), [UCI source and CC BY 4.0 license](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits), DOI 10.24432/C50P49, E. Alpaydin and C. Kaynak (1998).

Divide pixels by known maximum 16. No fitted preprocessing, augmentation, PCA or pretrained weights.

1. Stratified 20% test holdout, random state 3024.
2. Stratified 25% validation holdout from the remainder, same state.
3. **1,077 train / 360 validation / 360 test**. Saved indices are disjoint/complete.

Train supplies all fitted statistics, neural weights and posterior curvature. Validation selects feature epoch, NB smoothing and head prior. The selection lock is written after all full-run seeds' choices and before test transformation/prediction.

Shared split; initialization seeds 11/22/33. The earlier smoke run selected its own models before its test stage; its outcomes did not change the full configuration. Writer IDs are unavailable, so writer-disjointness is not established.

Baselines: Gaussian NB and a MAP neural head. Ablations: same-prior MAP and diagonal Laplace precision. No test tuning.

