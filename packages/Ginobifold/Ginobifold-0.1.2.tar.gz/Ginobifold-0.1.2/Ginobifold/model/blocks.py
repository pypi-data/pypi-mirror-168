import torch
import torch.nn as nn
from Ginobifold.model.base import PairUpdate, Transition, OutProductMean, RowAttentionWithPair, \
    ColAttention, TriColAttention, TriRowAttention, GlobalColAttention, inplace_assign


class MSAAttenBlock(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z):
        super().__init__()
        self.row_atten = RowAttentionWithPair(c_m, h_m, c_a_m, c_z)
        self.col_atten = ColAttention(c_m, h_m, c_a_m)
        self.transition = Transition(c_m)

    def forward(self, m, m_mask, z):
        m = m + self.row_atten(m, m_mask, z)
        m = m + self.col_atten(m, m_mask)
        m = m + self.transition(m)
        return m


class ExtraMSAAttenBlock(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z):
        super().__init__()
        self.row_atten = RowAttentionWithPair(c_m, h_m, c_a_m, c_z)
        self.col_atten = GlobalColAttention(c_m, h_m, c_a_m)
        self.transition = Transition(c_m)

    def forward(self, m, m_mask, z):
        m = m + self.row_atten(m, m_mask, z)
        m = m + self.col_atten(m, m_mask)
        m = m + self.transition(m)
        return m


class PairUpdateBlock(nn.Module):
    def __init__(self, c_tz, c_u_tz):
        super().__init__()
        self.row_update = PairUpdate(c_tz, c_u_tz, row_mode=True)
        self.col_update = PairUpdate(c_tz, c_u_tz, row_mode=False)

    def forward(self, tz, tz_mask):
        tz = tz + self.row_update(tz, tz_mask)
        tz = tz + self.col_update(tz, tz_mask)
        return tz


class PairAttenBlock(nn.Module):
    def __init__(self, c_z, h_z, c_a_z, pt):
        super().__init__()
        self.row_atten = TriRowAttention(c_z, h_z, c_a_z)
        self.col_atten = TriColAttention(c_z, h_z, c_a_z)
        self.transition = Transition(c_z, pt)

    def forward(self, z, z_mask):
        z = z + self.row_atten(z, z_mask)
        z = z + self.col_atten(z, z_mask)
        z = z + self.transition(z)
        return z


#############################################################################
class PairCoreBlock(nn.Module):
    def __init__(self, c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
        super().__init__()
        self.opm = OutProductMean(c_m, c_opm, c_z)
        self.pair_update = PairUpdateBlock(c_z, c_u_z)
        self.pair_atten = PairAttenBlock(c_z, h_z, c_a_z, pt)

    def forward(self, m, m_mask, z, z_mask):
        z = z + self.opm(m, m_mask)
        z = self.pair_update(z, z_mask)
        z = self.pair_atten(z, z_mask)
        return z


##############################################################################
#       Up are basis blocks
#       Down are Stack blocks
##############################################################################


class TemplatePairStackBlock(nn.Module):
    def __init__(self, c_t, c_u_t, c_a_t, h_t, pt):
        super().__init__()
        self.row_atten = TriRowAttention(c_t, h_t, c_a_t)
        self.col_atten = TriColAttention(c_t, h_t, c_a_t)
        self.row_update = PairUpdate(c_t, c_u_t, row_mode=True)
        self.col_update = PairUpdate(c_t, c_u_t, row_mode=False)
        self.transition = Transition(c_t, pt)

    def forward(self, t, t_mask):
        t = t + self.row_atten(t, t_mask)
        t = t + self.col_atten(t, t_mask)
        t = t + self.row_update(t, t_mask)
        t = t + self.col_update(t, t_mask)
        t = t + self.transition(t)
        return t  # * t_mask[..., None] # TODO: Need to review Openfold and AF2


class ExtraMSAStackBlock(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
        super().__init__()
        self.msa_atten = ExtraMSAAttenBlock(c_m, h_m, c_a_m, c_z)
        self.pair_core = PairCoreBlock(c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt)

    def forward(self, m, m_mask, z, z_mask):
        m = self.msa_atten(m, m_mask, z)
        z = self.pair_core(m, m_mask, z, z_mask)
        return m, z


class EvoformerStackBlock(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
        super().__init__()

        self.msa_atten = MSAAttenBlock(c_m, h_m, c_a_m, c_z)
        self.pair_core = PairCoreBlock(c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt)

    def forward(self, m, m_mask, z, z_mask):
        m = self.msa_atten(m, m_mask, z)  # TODO: Test checkpoint
        z = self.pair_core(m, m_mask, z, z_mask)
        return m, z


# class MSAAttenBlock(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m, c_z):
#         super().__init__()
#         self.row_atten = RowAttentionWithPair(c_m, h_m, c_a_m, c_z)
#         self.col_atten = ColAttention(c_m, h_m, c_a_m)
#         self.transition = Transition(c_m)
#
#     def forward(self, m, m_mask, z, inplace=True):
#         if inplace:
#             m += self.row_atten(m, m_mask, z)
#             m += self.col_atten(m, m_mask)
#             m += self.transition(m)
#         else:
#             m = m + self.row_atten(m, m_mask, z)
#             m = m + self.col_atten(m, m_mask)
#             m = m + self.transition(m)
#         return m
#
#
#
#
#
#
#
# class ExtraMSAAttenBlock(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m, c_z):
#         super().__init__()
#         self.row_atten = RowAttentionWithPair(c_m, h_m, c_a_m, c_z)
#         self.col_atten = GlobalColAttention(c_m, h_m, c_a_m)
#         self.transition = Transition(c_m)
#
#     def forward(self, m, m_mask, z, inplace=True):
#         if inplace:
#             m += self.row_atten(m, m_mask, z)
#             m += self.col_atten(m, m_mask)
#             m += self.transition(m)
#         else:
#             m = m + self.row_atten(m, m_mask, z)
#             m = m + self.col_atten(m, m_mask)
#             m = m + self.transition(m)
#         return m
#
#
# class PairUpdateBlock(nn.Module):
#     def __init__(self, c_tz, c_u_tz):
#         super().__init__()
#         self.row_update = PairUpdate(c_tz, c_u_tz, row_mode=True)
#         self.col_update = PairUpdate(c_tz, c_u_tz, row_mode=False)
#
#     def forward(self, tz, tz_mask, inplace=True):
#         if inplace:
#             tz += self.row_update(tz, tz_mask)
#             tz += self.col_update(tz, tz_mask)
#         else:
#             tz = tz + self.row_update(tz, tz_mask)
#             tz = tz + self.col_update(tz, tz_mask)
#         return tz
#
#
# class PairAttenBlock(nn.Module):
#     def __init__(self, c_z, h_z, c_a_z, pt):
#         super().__init__()
#         self.row_atten = TriRowAttention(c_z, h_z, c_a_z)
#         self.col_atten = TriColAttention(c_z, h_z, c_a_z)
#         self.transition = Transition(c_z, pt)
#
#     def forward(self, z, z_mask, inplace=True):
#         if inplace:
#             z += self.row_atten(z, z_mask)
#             z += self.col_atten(z, z_mask)
#             z += self.transition(z)
#         else:
#             z = z + self.row_atten(z, z_mask)
#             z = z + self.col_atten(z, z_mask)
#             z = z + self.transition(z)
#         return z
#
#
# #############################################################################
# class PairCoreBlock(nn.Module):
#     def __init__(self, c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
#         super().__init__()
#         self.opm = OutProductMean(c_m, c_opm, c_z)
#         self.pair_update = PairUpdateBlock(c_z, c_u_z)
#         self.pair_atten = PairAttenBlock(c_z, h_z, c_a_z, pt)
#
#     def forward(self, m, m_mask, z, z_mask, inplace=True):
#         if inplace:
#             z += self.opm(m, m_mask)
#             # TODO inplace assignment
#             inplace_assign(z, self.pair_update(z, z_mask))
#             inplace_assign(z, self.pair_atten(z, z_mask))
#         else:
#             z = z + self.opm(m, m_mask)
#             z = self.pair_update(z, z_mask)
#             z = self.pair_atten(z, z_mask)
#         return z
#
#
# ##############################################################################
# #       Up are basis blocks
# #       Down are Stack blocks
# ##############################################################################
#
#
# class TemplatePairStackBlock(nn.Module):
#     def __init__(self, c_t, c_u_t, c_a_t, h_t, pt):
#         super().__init__()
#         self.row_atten = TriRowAttention(c_t, h_t, c_a_t)
#         self.col_atten = TriColAttention(c_t, h_t, c_a_t)
#         self.row_update = PairUpdate(c_t, c_u_t, row_mode=True)
#         self.col_update = PairUpdate(c_t, c_u_t, row_mode=False)
#         self.transition = Transition(c_t, pt)
#
#     def forward(self, t, t_mask, inplace=True):
#         import time
#         begin = time.time()
#
#         if inplace:
#             t += self.row_atten(t, t_mask)
#             t += self.col_atten(t, t_mask)
#             t += self.row_update(t, t_mask)
#             t += self.col_update(t, t_mask)
#             t += self.transition(t)
#         else:
#             t = t + self.row_atten(t, t_mask)
#             t = t + self.col_atten(t, t_mask)
#             t = t + self.row_update(t, t_mask)
#             t = t + self.col_update(t, t_mask)
#             t = t + self.transition(t)
#         print("TemplatePairStack Block foward time", time.time() - begin)
#         return t  # * t_mask[..., None]
#
#
# class ExtraMSAStackBlock(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
#         super().__init__()
#         self.msa_atten = ExtraMSAAttenBlock(c_m, h_m, c_a_m, c_z)
#         self.pair_core = PairCoreBlock(c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt)
#
#     def forward(self, m, m_mask, z, z_mask, inplace=True):
#         import time
#         begin = time.time()
#         if inplace:
#             inplace_assign(m, self.msa_atten(m, m_mask, z))
#             inplace_assign(z, self.pair_core(m, m_mask, z, z_mask))
#         else:
#             m = self.msa_atten(m, m_mask, z)
#             z = self.pair_core(m, m_mask, z, z_mask)
#         print("ExtraMSAStack Block foward time", time.time() - begin)
#         return m, z
#
#
# class EvoformerStackBlock(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt):
#         super().__init__()
#
#         self.msa_atten = MSAAttenBlock(c_m, h_m, c_a_m, c_z)
#         self.pair_core = PairCoreBlock(c_m, c_z, c_opm, c_u_z, c_a_z, h_z, pt)
#
#     def forward(self, m, m_mask, z, z_mask, inplace=True):
#         if inplace:
#             inplace_assign(m, self.msa_atten(m, m_mask, z))
#             inplace_assign(z, self.pair_core(m, m_mask, z, z_mask))
#         else:
#             m = self.msa_atten(m, m_mask, z)  # Test checkpoint
#             z = self.pair_core(m, m_mask, z, z_mask)
#         return m, z


if __name__ == '__main__':
    ...
