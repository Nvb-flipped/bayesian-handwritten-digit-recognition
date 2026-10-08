# Research and method decision

Search date: 8 October 2026, Asia/Shanghai. This is a bounded agent-conducted narrative review, not systematic or independently human-reviewed.

## Actual discovery queries

1. Laplace Redux Effortless Bayesian Deep Learning NeurIPS 2021 Daxberger
2. Posterior Network uncertainty estimation without OOD samples NeurIPS 2020 Natural Posterior Network 2021
3. 2022 Bayesian neural network classification variational inference last layer uncertainty paper
4. site:proceedings.mlr.press Guo 2017 On Calibration of Modern Neural Networks
5. MacKay 1992 Bayesian Interpolation Neural Computation 4 415 447 DOI

Primary proceedings, author manuscripts, institutional bibliography and dataset documentation were opened. OpenReview forums returned a verification challenge; PDFs and arXiv records remained accessible. The NeurIPS BibTeX link returned an internal tool error; proceedings/PDF supplied author order and venue. No exhaustive search count or fictional search history is claimed.

## Candidates

| Verified method | Defining probability mechanism | Course relevance | Compute/reproduction | Evaluation and risk |
|---|---|---|---|---|
| Laplace Redux, NeurIPS 2021 | Gaussian approximation to weight posterior | Prior, likelihood, curvature, predictive integration | Small full head matrix is auditable; large networks need approximations | Accuracy/probability scores; local approximation, prior sensitivity |
| Natural Posterior Network, ICLR 2022 | Density-driven conjugate updates | Bayesian exponential-family inference | Neural features and normalizing flows | Calibration/recognition; density learning complexity |
| Variational Bayesian Last Layers, ICLR 2024 | Deterministic variational last-layer inference | Approximate posterior and variational optimization | Efficient output layer; exact published objective needs careful coding | Accuracy/calibration; variational assumptions |

Sources:

- [Laplace proceedings](https://papers.nips.cc/paper/2021/hash/a7c9585703d275249f30a088cebba0ad-Abstract.html), [paper](https://papers.nips.cc/paper/2021/file/a7c9585703d275249f30a088cebba0ad-Paper.pdf), [author code](https://github.com/runame/laplace-redux). Authors: Erik Daxberger, Agustinus Kristiadi, Alexander Immer, Runa Eschenhagen, Matthias Bauer, Philipp Hennig.
- [NatPN manuscript](https://arxiv.org/abs/2105.04471), [ICLR 2022 PDF](https://openreview.net/pdf?id=tV3N0DWMxCg). Authors: Bertrand Charpentier, Oliver Borchert, Daniel Zügner, Simon Geisler, Stephan Günnemann.
- [VBLL manuscript and ICLR 2024 metadata](https://arxiv.org/abs/2404.11599), [conference PDF](https://openreview.net/pdf?id=Sx7BIiPzys). Authors: James Harrison, John Willes, Jasper Snoek.

Selected: conditional last-layer Laplace, at the older end of the requested 2021–2026 range. Selection prioritized transparent mathematics and feasible execution. The paper makes established Laplace inference practical; Bayes and Laplace theory are older. No test result was used to select the algorithm.

## Adaptation and protocol

The AI independently implemented a 64→32 tanh representation and exact 330-parameter head Hessian. This is one variant, not the complete author library or benchmark study. Prior precision is selected by validation NLL, not marginal-likelihood optimization.

Research questions: retained recognition accuracy; proper-score effect of averaging; effect of correlations. Matched MAP and diagonal-precision controls were specified before full execution. The small image dataset permits three stochastic seeds and full numerical checks.

## Other verified references

- [UCI creators/DOI/license](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits): E. Alpaydin, C. Kaynak (1998), DOI 10.24432/C50P49, CC BY 4.0.
- [Loader documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html): 1,797 images, 8×8, integer range 0–16; original UCI test subset.
- [Guo et al., ICML 2017](https://proceedings.mlr.press/v70/guo17a.html): Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger, PMLR 70:1321–1330.
- [Caltech author bibliography](https://feeds.library.caltech.edu/people/MacKay-D-J-C/article.html): D. J. C. MacKay, Bayesian Interpolation, Neural Computation 4(3):415–447 (1992), DOI 10.1162/neco.1992.4.3.415; historical background only.
- [Scientific Agent Skills](https://arxiv.org/abs/2609.00065): Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel, Aubrey M. Brueckner (2026); record revised 2 September 2026; DOI 10.48550/arXiv.2609.00065. Acknowledges guidance, not classifier evidence.

Verification was by the AI agent opening source content, not by an independent human reviewer.

