"""Classification and probability-quality metrics with explicit conventions."""
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def reliability(labels, probabilities, bins=10):
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == labels
    ids = np.minimum((confidence * bins).astype(int), bins-1)
    records = []
    for b in range(bins):
        mask = ids == b
        records.append(dict(bin=b, low=b/bins, high=(b+1)/bins, count=int(mask.sum()),
                            confidence=float(confidence[mask].mean()) if mask.any() else None,
                            accuracy=float(correct[mask].mean()) if mask.any() else None))
    ece = sum(r["count"]/len(labels) * abs(r["confidence"]-r["accuracy"])
              for r in records if r["count"])
    return records, float(ece)


def evaluate(labels, probabilities, bins=10):
    p = np.asarray(probabilities)
    if not np.isfinite(p).all() or (p < 0).any() or not np.allclose(p.sum(1), 1):
        raise ValueError("Invalid class probabilities")
    predictions = p.argmax(1)
    report = classification_report(labels, predictions, labels=list(range(p.shape[1])),
                                   output_dict=True, zero_division=0)
    curve, ece = reliability(labels, p, bins)
    return dict(accuracy=float(accuracy_score(labels, predictions)),
                macro_f1=report["macro avg"]["f1-score"],
                macro_precision=report["macro avg"]["precision"],
                macro_recall=report["macro avg"]["recall"],
                nll=float(-np.log(np.clip(p[np.arange(len(labels)), labels], 1e-15, 1)).mean()),
                brier=float(np.sum((p-np.eye(p.shape[1])[labels])**2, axis=1).mean()),
                ece=ece, per_class={str(k):report[str(k)] for k in range(p.shape[1])},
                confusion=confusion_matrix(labels, predictions, labels=list(range(p.shape[1]))).tolist(),
                reliability=curve)

