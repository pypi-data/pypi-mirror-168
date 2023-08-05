import torch
import torch.nn as nn
import torch.nn.functional as F
from Ginobifold.model.base import Dense


class PerResidueLDDTCaHeads(nn.Module):
    def __init__(self, num_bins, c_in, c_h):
        super().__init__()
        self.layernorm = nn.LayerNorm(c_in)
        self.dense1 = Dense(c_in, c_h, act="relu")
        self.dense2 = Dense(c_h, c_h, act="relu")
        self.dense3 = Dense(c_h, num_bins)

    def forward(self, s):
        s = self.layernorm(s)
        s = self.dense1(s)
        s = self.dense2(s)
        s = self.dense3(s)
        return s  # lddt logits


def compute_plddt(lddt_logits: torch.Tensor):
    num_bins = lddt_logits.shape[-1]
    bin_width = 1.0 / num_bins
    bounds = torch.arange(
        start=0.5 * bin_width, end=1.0, step=bin_width, device=lddt_logits.device
    )
    probs = torch.nn.functional.softmax(lddt_logits, dim=-1)
    pred_lddt_ca = torch.sum(
        probs * bounds.view(*((1,) * len(probs.shape[:-1])), *bounds.shape),
        dim=-1,
    )
    return pred_lddt_ca * 100
