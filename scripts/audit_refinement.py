"""Verify presentation refinement preserves the executed Prompt 02 evidence."""
import hashlib
import io
import json
from pathlib import Path
import subprocess

import numpy as np

from bayes_digits.experiment import save_json


def audit():
    baseline = "93b625e"
    root = Path("results")
    names = ["config.json", "dataset.json", "environment.json", "metrics.json",
             "predictions.npz", "selection_locked.json", "sensitivity.json",
             "splits.npz", "summary.json"]
    paths = [root / name for name in names]
    paths += sorted(root.glob("history_*.json"))
    paths += sorted((root / "models").glob("*"))
    paths += sorted((root / "review_diagnostics").glob("*"))
    hashes = {}
    for path in paths:
        name = path.as_posix()
        original = subprocess.check_output(["git", "show", f"{baseline}:{name}"])
        assert original == path.read_bytes(), f"Executed evidence changed: {name}"
        hashes[name] = hashlib.sha256(original).hexdigest()
    tables = sorted(p for p in Path("report").glob("*.tex")
                    if p.name not in {"main.tex", "student_reflection.tex"})
    for path in tables:
        original = subprocess.check_output(["git", "show", f"{baseline}:{path.as_posix()}"])
        assert original == path.read_bytes(), f"Numerical table changed: {path}"

    old = np.load(io.BytesIO(subprocess.check_output(
        ["git", "show", f"{baseline}:results/predictions.npz"])))
    current = np.load(root / "predictions.npz")
    assert old.files == current.files
    assert all(np.array_equal(old[k], current[k]) for k in old.files)
    records = json.loads((root / "metrics.json").read_text())
    data = json.loads((root / "figure_data.json").read_text())
    raw_observations = 0
    for method in ["MAP", "Laplace"]:
        measured = np.array([[r["metrics"]["per_class"][str(k)]["f1-score"]
                              for k in range(10)] for r in records if r["method"] == method])
        plotted = np.array(data["classes"]["f1_by_seed"][method])
        assert np.array_equal(measured, plotted)
        assert np.all((1 - plotted >= 0) & (1 - plotted <= 1))
        raw_observations += plotted.size
    confusion = np.array([r["metrics"]["confusion"] for r in records if r["method"] == "Laplace"])
    normalized = (confusion / confusion.sum(2, keepdims=True)).mean(0)
    assert np.array_equal(normalized, data["classes"]["mean_row_confusion"])

    toy = data["covariance_geometry"]
    precision = np.array(toy["precision"])
    covariances = [np.array(toy[key]) for key in
                   ["full_covariance", "diagonal_precision_covariance"]]
    np.testing.assert_allclose(covariances[0], np.linalg.inv(precision))
    np.testing.assert_allclose(covariances[1], np.diag(1 / np.diag(precision)))
    contrast = np.array([-1., 1.])
    np.testing.assert_allclose([contrast @ cov @ contrast for cov in covariances], [1., 4/3])
    np.testing.assert_allclose(toy["contrast_variances"], [1., 4/3])
    for curve, cov in zip(toy["contours"], covariances):
        points = np.array(curve)
        np.testing.assert_allclose(np.einsum("ni,ij,nj->n", points, np.linalg.inv(cov), points),
                                   np.ones(len(points)), atol=1e-12)

    save_json(root / "refinement_audit.json", dict(
        baseline_commit=baseline, executed_files_bitwise_unchanged=len(paths),
        evidence_sha256=hashes, primary_arrays_bitwise_unchanged=len(current.files),
        numerical_table_files_bitwise_unchanged=len(tables),
        raw_f1_observations_preserved=raw_observations, confusion_proportions_unchanged=True,
        covariance_contours_and_contrast_variances_verified=True,
        historical_experiment_environment_preserved=True,
        current_plotting_provenance="results/figure_manifest.json"))
    print(f"Refinement audit passed: {len(paths)} unchanged evidence files, "
          f"{len(current.files)} arrays, {len(tables)} tables, {raw_observations} raw F1 observations; toy geometry verified.")


if __name__ == "__main__":
    audit()
