import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from Ginobifold.utils.mathutils import updateRTbyBB
from Ginobifold.model.base import Dense, DeepClone, AttentionMaskBias
from Ginobifold.residue_torch_constants import make_pos

import tqdm


class InvariantPointAttention(nn.Module):
    def __init__(self, c_s, c_z, c_ipa, h_ipa, num_qk, num_v):
        super().__init__()
        self.num_qk = num_qk
        self.num_v = num_v
        self.h_ipa = h_ipa
        self.normsize = math.sqrt(1. / (3 * c_ipa))
        self.normsize_B = math.sqrt(1 / 3.)
        self.normsize_hw = math.sqrt(1. / (3 * self.num_qk * 9. / 2))

        self.dense_q = Dense(c_s, h_ipa * c_ipa)
        self.dense_kv = Dense(c_s, h_ipa * 2 * c_ipa)
        self.dense_q3 = Dense(c_s, h_ipa * 3 * num_qk)
        self.dense_kv3 = Dense(c_s, h_ipa * 3 * (num_qk + num_v))
        self.dense_b = Dense(c_z, h_ipa)
        self.hw = nn.Parameter(torch.zeros([h_ipa]))
        self.dense_o = Dense(h_ipa * (c_z + c_ipa + num_v * 4), c_s)

    def forward(self, s, z, rots, trans, mask):
        Q = self.dense_q(s).view(s.shape[:-1] + (self.h_ipa, -1))
        KV = self.dense_kv(s).view(s.shape[:-1] + (self.h_ipa, 2, -1))
        K, V = KV[..., 0, :], KV[..., 1, :]

        Q3 = self.dense_q3(s).view(s.shape[:-1] + (3, self.num_qk * self.h_ipa)).transpose(-1, -2)
        Q3 = torch.einsum("...ij,...kj->...ki", rots, Q3) + trans[..., :, None, :]
        Q3 = Q3.view(Q3.shape[:-2] + (self.h_ipa, self.num_qk, 3))

        KV3 = self.dense_kv3(s)  # I (H, C, 3)
        KV3 = KV3.view(KV3.shape[:-1] + (3, -1)).transpose(-1, -2)

        KV3 = torch.einsum("...ij,...kj->...ki", rots, KV3) + trans[..., :, None, :]
        KV3 = KV3.view(KV3.shape[:-2] + (self.h_ipa, -1, 3))
        K3, V3 = KV3[..., :self.num_qk, :], KV3[..., self.num_qk:, :]  # N H C 3

        B = self.dense_b(z)
        # n1 h c, n2 h c -> h n1 n2
        AT = torch.einsum("... i h c, j h c -> ... i j h", Q, K) * self.normsize
        AT = AT + B * self.normsize_B
        ############
        AT3 = torch.sum(torch.square(Q3.unsqueeze(-4) - K3.unsqueeze(-5)), dim=-1)
        hw = F.softplus(self.hw, 1, 20).view(*((1,) * len(Q3.shape[:-2]) + (-1, 1))) * self.normsize_hw
        AT3 = torch.sum(AT3 * hw, dim=-1) * (-0.5)
        B3 = AttentionMaskBias(mask[..., None] * mask[..., None, :])[..., None]
        #################
        AT = F.softmax(AT + AT3 + B3, dim=-2)

        ###
        O = torch.einsum("...IJH,...JHC->...IHC", AT, V)
        O = O.reshape(O.shape[:-2] + (-1,))

        O3 = torch.einsum("... I J H, ... J H C D -> ... I H C D", AT, V3)

        O3 = O3.reshape(O3.shape[:-3] + (-1, 3))
        O3 = torch.einsum("...ji,...kj->...ki", rots, O3 - trans[..., :, None, :])

        O3_norm = torch.sqrt(torch.sum(torch.square(O3), dim=-1) + 1E-20)
        O_pair = torch.einsum("...IJH,...IJC->...IHC", AT, z)
        O_pair = O_pair.view(O_pair.shape[:-2] + (-1,))
        # print(O.shape,O3.shape,O3_norm.shape,O_pair.shape)
        # quit()
        O_final = torch.cat((O, O3[..., 0], O3[..., 1], O3[..., 2], O3_norm, O_pair), dim=-1)
        s = self.dense_o(O_final)
        return s


class STransitionLayer(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.dense1 = Dense(c, c, act="relu")
        self.dense2 = Dense(c, c, act="relu")
        self.dense3 = Dense(c, c)

    def forward(self, s):
        return s + self.dense3(self.dense2(self.dense1(s)))


class STransition(nn.Module):
    def __init__(self, c, num_layers):
        super().__init__()
        self.layers = DeepClone(STransitionLayer(c), num_layers)
        self.layernorm = nn.LayerNorm(c)

    def forward(self, s):
        for layer_id, layer in enumerate(self.layers):
            s = layer(s)
        s = self.layernorm(s)
        return s


class AngleResnetBlock(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.dense1 = Dense(c, c, act="relu")
        self.dense2 = Dense(c, c)
        self.relu = nn.ReLU()

    def forward(self, a):
        return a + self.dense2(self.dense1(self.relu(a)))


class AngleResnet(nn.Module):
    def __init__(self, c_in, c_h, num_layers):
        super().__init__()
        self.dense_init = Dense(c_in, c_h)
        self.dense_in = Dense(c_in, c_h)
        self.layers = DeepClone(AngleResnetBlock(c_h), num_layers)
        self.dense_out = Dense(c_h, 14)
        self.relu = nn.ReLU()

    def forward(self, s, s_init):
        s = self.dense_in(self.relu(s)) + self.dense_init(self.relu(s_init))
        for layer_id, layer in enumerate(self.layers):
            s = layer(s)
        unnorm_s = self.dense_out(self.relu(s))
        unnorm_s = unnorm_s.view(unnorm_s.shape[:-1] + (7, 2))
        s_norm = torch.sqrt(torch.clamp(torch.sum(torch.square(unnorm_s), dim=-1, keepdim=True), min=1E-20))
        s = unnorm_s / s_norm
        return unnorm_s, s


class StructureModule(nn.Module):
    def __init__(self, c_s, c_z, c_ipa, c_resnet, h_ipa, num_qk, num_v, num_blocks, num_tlayers, num_resnet):
        super().__init__()
        self.num_blocks = num_blocks

        self.layernorm_s = nn.LayerNorm(c_s)
        self.layernorm_z = nn.LayerNorm(c_z)
        self.dense_in = Dense(c_s, c_s)
        self.ipa = InvariantPointAttention(c_s, c_z, c_ipa, h_ipa, num_qk, num_v)
        self.layernorm_ipa = nn.LayerNorm(c_s)
        self.transition = STransition(c_s, num_tlayers)
        self.backbone_out = Dense(c_s, 6)
        self.angle_out = AngleResnet(c_s, c_resnet, num_resnet)

    def forward(self, s, z, s_mask, aatype):
        s = self.layernorm_s(s)
        z = self.layernorm_z(z)
        s_init = s
        #######
        s = self.dense_in(s)
        inds = torch.zeros(s.shape[:-1], dtype=torch.long)
        rots = torch.eye(3)[None][inds].cuda()
        trans = torch.zeros([1, 3])[inds].cuda()
        for i in tqdm.tqdm(range(self.num_blocks),bar_format='StructureModule {l_bar}{bar}{r_bar}'):
            # TODO: May Exist Very Small Precision Error
            s = s + self.ipa(s, z, rots, trans, s_mask)
            s = self.layernorm_ipa(s)
            s = self.transition(s)
            BB = self.backbone_out(s)
            rots, trans = updateRTbyBB(rots, trans, BB)
        _, Torsions = self.angle_out(s, s_init)
        x = make_pos(aatype, rots, trans * 10, Torsions)
        return s, x, rots, trans, Torsions


if __name__ == '__main__':
    ...