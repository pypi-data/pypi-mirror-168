import torch
import torch.nn as nn


class RMSELoss(nn.Module):
    def __init__(self, reduction='mean', eps=1e-9):
        super().__init__()
        self.mse = nn.MSELoss(reduction='none')
        self.reduction = reduction
        self.eps = eps

    def forward(self, y_pred, y_true):
        loss = torch.sqrt(self.mse(y_pred, y_true) + self.eps)
        if self.reduction == 'none':
            loss = loss
        elif self.reduction == 'sum':
            loss = loss.sum()
        elif self.reduction == 'mean':
            loss = loss.mean()
        return loss


class WeightedMSELoss(nn.Module):
    def __init__(self, n_labels, weights):
        super().__init__()
        self.mse = nn.MSELoss()
        self.n_labels = n_labels
        self.weights = weights

    def forward(self, y_pred, y_true):
        score = 0
        for i, w in zip(range(self.n_labels), self.weights):
            score += self.mse(y_pred[:, i], y_true[:, i]) * w
        return score


class MCRMSELoss(nn.Module):
    def __init__(self, n_labels):
        super().__init__()
        self.rmse = RMSELoss()
        self.n_labels = n_labels

    def forward(self, y_pred, y_true):
        score = 0
        for i in range(self.n_labels):
            score += self.rmse(y_pred[:, i], y_true[:, i]) / self.n_labels
        return score
