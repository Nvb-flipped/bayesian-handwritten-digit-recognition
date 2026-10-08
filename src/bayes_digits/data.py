"""A documented local image dataset with immutable, stratified partitions."""
import hashlib
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split


def load_data(seed=3024):
    dataset = load_digits()
    x = dataset.data.astype(np.float64) / 16.0  # Known acquisition range, not fitted.
    y = dataset.target.astype(np.int64)
    indices = np.arange(len(y))
    development, test = train_test_split(
        indices, test_size=0.2, stratify=y, random_state=seed)
    train, validation = train_test_split(
        development, test_size=0.25, stratify=y[development], random_state=seed)
    splits = dict(train=train, validation=validation, test=test)
    assert len(set(train) & set(validation)) == 0
    assert len(set(development) & set(test)) == 0
    digest = hashlib.sha256(dataset.data.tobytes() + y.tobytes()).hexdigest()
    return x, y, splits, digest

