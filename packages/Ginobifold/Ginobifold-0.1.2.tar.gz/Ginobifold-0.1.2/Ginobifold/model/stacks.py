import torch
import torch.nn as nn
from typing import List, Union

from Ginobifold.model.blocks import EvoformerStackBlock, TemplatePairStackBlock, ExtraMSAStackBlock
from Ginobifold.model.base import DeepClone, Dense, TemplatePointwiseAttention

import tqdm
import sys

class TemplatePairStack(nn.Module):
    def __init__(self, c_z, c_t, c_u_t, c_a_t, h_t, pt, num_blocks):
        super().__init__()
        self.blocks = DeepClone(
            TemplatePairStackBlock(c_t, c_u_t, c_a_t, h_t, pt),
            num_blocks
        )  # type: Union[nn.ModuleList[TemplatePairStackBlock],List[TemplatePairStackBlock]]
        self.layernorm = nn.LayerNorm(c_t)
        self.template_pointwise_atten = TemplatePointwiseAttention(c_z, c_t, h_t, c_a_t)

    def forward(self, t, tp_mask, z, z_mask):
        if tp_mask.sum() > 0: # If no template, skip this step
            sys.stdout.flush()
            for block in tqdm.tqdm(self.blocks,bar_format='TemplatePairStack {l_bar}{bar}{r_bar}'):
                t = block(t, z_mask[..., None, :, :])
            t = self.layernorm(t)
            t = self.template_pointwise_atten(t, z)
            # TODO: need to multipie template mask??????
            z = z + t # *tp_mask.sum() TODO: if have temp, that should use
            return z
        else:
            return z


class ExtraMSAStack(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt, num_blocks):
        super().__init__()
        self.blocks = DeepClone(
            ExtraMSAStackBlock(c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt),
            num_blocks
        )  # type: Union[nn.ModuleList[ExtraMSAStackBlock],List[ExtraMSAStackBlock]]

    def forward(self, em, em_mask, z, z_mask):
        sys.stdout.flush()
        for block in tqdm.tqdm(self.blocks,bar_format='ExtraMSAStack {l_bar}{bar}{r_bar}'):
            em, z = block(em, em_mask, z, z_mask)
        return z


class EvoformerStack(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u, c_a_z, h_z, num_blocks, c_s, pt):
        super().__init__()

        self.blocks = DeepClone(
            EvoformerStackBlock(c_m, h_m, c_a_m, c_z, c_opm, c_u, c_a_z, h_z, pt),
            num_blocks
        )  # type: Union[nn.ModuleList[EvoformerStackBlock],List[EvoformerStackBlock]]

        self.dense_m_s = Dense(c_m, c_s)

    def forward(self, m, m_mask, z, z_mask):
        sys.stdout.flush()
        for block in tqdm.tqdm(self.blocks,bar_format='EvoformerStack {l_bar}{bar}{r_bar}'):
            m, z = block(m, m_mask, z, z_mask)
        s = self.dense_m_s(m[..., 0, :, :])
        return m, z, s


if __name__ == '__main__':
    ...