import torch
import torch.nn as nn
from Ginobifold.model.base import Dense, relpos

import tqdm
'''
  Features:
    tf: target features  N 22
    ri: residue index    N
    mf: msa features      
    emf: extra msa features
    tppf: template pair features
    tpaf: template angle features 
    
  presentations:
    m: msa/single  presentation
    z: pair presentation
    x_beta: coordinates of beta atoms
    m1: the first row of m 
    
  Channels:
    cz: channels of pair presentation
    cm: channels of mas/single presentation  
    ce: channels of extra msa presentation  
    ctf: channels of target features 
'''


class InputEmbedder(nn.Module):
    def __init__(self, c_tf, c_mf, c_z, c_m, window_size: int):
        super().__init__()
        self.window_size = window_size

        self.dense_tf_z1 = Dense(c_tf, c_z)
        self.dense_tf_z2 = Dense(c_tf, c_z)

        self.dense_tf_m = Dense(c_tf, c_m)
        self.dense_mf_m = Dense(c_mf, c_m)

        self.dense_ri_z = Dense(2 * window_size + 1, c_z)

    def forward(self, tf: torch.Tensor, ri: torch.Tensor, mf: torch.Tensor):
        tf_z1 = self.dense_tf_z1(tf)
        tf_z2 = self.dense_tf_z2(tf)
        # TODO Change add sequence can lead to different results
        z = tf_z1[..., None, :] + self.dense_ri_z(relpos(ri, self.window_size)) + tf_z2[..., None, :, :]

        tf_cm = self.dense_tf_m(tf)[None]
        mf_cm = self.dense_mf_m(mf)
        m = tf_cm + mf_cm
        return m, z


class RecyclingEmdbedder(nn.Module):
    def __init__(self, c_m, c_z, min_bin, max_bin, num_bins):
        super().__init__()

        self.bins = torch.linspace(min_bin, max_bin, num_bins, requires_grad=False).cuda()
        self.lower_bound = self.bins ** 2
        self.inf = 1E9
        self.upper_bound = torch.cat([self.lower_bound[1:], self.lower_bound.new_tensor([self.inf])], dim=-1)

        self.norm_m = nn.LayerNorm(c_m)
        self.norm_z = nn.LayerNorm(c_z)
        self.dense_dist_z = Dense(num_bins, c_z)

    def forward(self, m1_prev: torch.Tensor, z_prev: torch.Tensor, x_prev: torch.Tensor):
        m_update = self.norm_m(m1_prev)
        z_update = self.norm_z(z_prev)
        dist = (x_prev[..., None, :] - x_prev[..., None, :, :]).square().sum(dim=-1, keepdims=True)
        dist_bin = (dist > self.lower_bound) * (dist < self.upper_bound).type(x_prev.dtype)
        z_update = z_update + self.dense_dist_z(dist_bin)
        return m_update, z_update


class ExtraMSAEmbedder(nn.Module):
    def __init__(self, c_emf, c_e):
        super().__init__()
        self.dense_emf_e = Dense(c_emf, c_e)

    def forward(self, emf: torch.Tensor):
        return self.dense_emf_e(emf)


class TemplatePairEmbedder(nn.Module):
    def __init__(self, c_tppf, c_z):
        super().__init__()
        self.dense_tppf_z = Dense(c_tppf, c_z)

    def forward(self, tppf):
        return self.dense_tppf_z(tppf)


class TemplateAngleEmbedder(nn.Module):
    def __init__(self, c_tpaf, c_m):
        super().__init__()
        self.dense_tpaf_m1 = Dense(c_tpaf, c_m, act="relu")
        # self.dense_tpaf_m1 = Dense(c_tpaf, c_m)
        self.dense_m1_m2 = Dense(c_m, c_m)


    def forward(self, tpaf: torch.Tensor):
        # Exist Precision Problem
        output=self.dense_tpaf_m1(tpaf)
        output=self.dense_m1_m2(output)
        return output


#######################################################################################

class FeatureEmbedder(nn.Module):
    def __init__(self, *,
                 c_tf, c_mf, c_z, c_m, window_size,
                 min_bin, max_bin, num_bins,
                 c_emf, c_e,
                 c_tpaf, c_tppf):
        super().__init__()
        # self.input_embedder = torch.jit.script(InputEmbedder(c_tf, c_mf, c_z, c_m, window_size))
        self.input_embedder = InputEmbedder(c_tf, c_mf, c_z, c_m, window_size)
        self.recycle_embedder = RecyclingEmdbedder(c_m, c_z, min_bin, max_bin, num_bins)
        #
        self.extra_msa_embedder = ExtraMSAEmbedder(c_emf, c_e)
        #
        self.template_angle_embedder = TemplateAngleEmbedder(c_tpaf, c_m)
        self.template_pair_embedder = TemplatePairEmbedder(c_tppf, c_z)

    def forward(self, *,
                m_mask,  # tpa_mask(merged in feature transform),#s_mask,z_mask,em_mask
                tf, ri, mf,

                emf,
                tpaf, tppf, x_prev=None, m1_prev=None, z_prev=None):
        # m,z
        m, z = self.input_embedder(tf, ri, mf)

        if m1_prev is None:
            batch_dims = list(m.shape[:-3])
            num_res = m.shape[-2]
            m1_prev = m.new_zeros(batch_dims + list(m.shape[-2:]), requires_grad=False)
            z_prev = m.new_zeros(z.shape, requires_grad=False)
            x_prev = m.new_zeros(batch_dims + [num_res, 3], requires_grad=False)
        m1_prev_emb, z_prev_emb = self.recycle_embedder(m1_prev, z_prev, x_prev)

        m[..., 0, :, :] = m[..., 0, :, :] + m1_prev_emb

        z = z + z_prev_emb

        # tp TODO template angle feats are a bit different from openfold maybe it is the precision
        tpm = self.template_angle_embedder(tpaf)
        m = torch.cat([m, tpm], dim=-3)
        # m_mask=torch.cat([m_mask,tpa_mask],dim=-2)
        tpz = self.template_pair_embedder(tppf)  # used as template embedder
        # em
        em = self.extra_msa_embedder(emf)  # used as extamsa embedder
        # mask part

        return m, z, em, tpz  # s_mask,z_mask,em_mask


if __name__ == '__main__':
    ...
