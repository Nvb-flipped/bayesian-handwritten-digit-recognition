"""Deterministic feature training; the test set is not an argument."""
import copy
import numpy as np
import torch
from torch import nn


class FeatureNetwork(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.features = nn.Sequential(nn.Linear(64, hidden), nn.Tanh())
        self.head = nn.Linear(hidden, 10)

    def forward(self, x):
        return self.head(self.features(x))


def train_features(x, y, xv, yv, config, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(config["threads"])
    requested = config["device"]
    device = torch.device("cuda" if requested == "auto" and torch.cuda.is_available()
                          else "cpu" if requested == "auto" else requested)
    model = FeatureNetwork(config["hidden"]).to(device)
    xt = torch.tensor(x, dtype=torch.float32, device=device)
    yt = torch.tensor(y, dtype=torch.long, device=device)
    vt = torch.tensor(xv, dtype=torch.float32, device=device)
    vy = torch.tensor(yv, dtype=torch.long, device=device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"],
                                 weight_decay=config["feature_weight_decay"])
    history, best, best_state, epoch_best = [], float("inf"), None, 0
    for epoch in range(1, config["epochs"] + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(model(xt), yt)
        if not torch.isfinite(loss):
            raise ValueError("Nonfinite training loss")
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            validation = nn.functional.cross_entropy(model(vt), vy).item()
        history.append(dict(epoch=epoch, train_nll=loss.item(), validation_nll=validation))
        if validation < best:
            best, epoch_best = validation, epoch
            best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    return model.cpu().eval(), history, epoch_best


@torch.no_grad()
def transform(model, x):
    f = model.features(torch.tensor(x, dtype=torch.float32)).numpy().astype(np.float64)
    return np.column_stack([f, np.ones(len(f))])

