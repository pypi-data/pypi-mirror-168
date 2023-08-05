import torch
from typing import Optional
import torch.nn.functional as F
# from Ginobifold.utils.mathutils import rigid_vec
from Ginobifold.utils.rigids import Rigid


class InputEmbedderFeatures():
    def __int__(self):
        self.tf: Optional[torch.Tensor] = None
        self.ri: Optional[torch.Tensor] = None
        self.mf: Optional[torch.Tensor] = None
        self.tpaf: Optional[torch.Tensor] = None
        self.tppf: Optional[torch.Tensor] = None
        self.emf: Optional[torch.Tensor] = None

    def __del__(self):
        del self.tf, self.ri, self.mf, self.tppf, self.tpaf, self.emf


class RecycleFeatures():
    def __int__(self):
        self.m1_prev: Optional[torch.Tensor] = None
        self.z_prev: Optional[torch.Tensor] = None
        self.x_prev: Optional[torch.Tensor] = None


class MaskFeatures():
    def __int__(self):
        self.s_mask: Optional[torch.Tensor] = None
        self.z_mask: Optional[torch.Tensor] = None
        self.tp_mask: Optional[torch.Tensor] = None
        self.em_mask: Optional[torch.Tensor] = None
        self.m_mask: Optional[torch.Tensor] = None
        self.aatype: Optional[torch.Tensor] = None

    def __del__(self):
        del self.s_mask, self.z_mask, self.tp_mask, self.em_mask, self.m_mask, self.aatype


def ParseOpenfoldParms(feats):
    s_mask = feats["seq_mask"][..., 0]
    z_mask = s_mask[..., None] * s_mask[..., None, :]

    m_mask = feats["msa_mask"][..., 0]
    tf = feats["target_feat"][..., 0]
    ri = feats["residue_index"][..., 0]
    mf = feats["msa_feat"][..., 0]
    tpaf1 = F.one_hot(feats["template_aatype"][..., 0], num_classes=22)
    tpaf2 = feats["template_torsion_angles_sin_cos"][..., 0]
    tpaf3 = feats["template_alt_torsion_angles_sin_cos"][..., 0]
    tpaf4 = feats["template_torsion_angles_mask"][..., 0]
    m_mask = torch.cat([m_mask, tpaf4[..., 2]], dim=-2)
    tpaf = torch.cat([tpaf1, tpaf2.reshape(*tpaf2.shape[:-2], 14),
                      tpaf3.reshape(*tpaf3.shape[:-2], 14), tpaf4], dim=-1)
    #### TPPF very important

    tppf_betamask = feats["template_pseudo_beta_mask"][..., 0]
    tppf_betamask2d = tppf_betamask[..., None] * tppf_betamask[..., None, :]
    tppf_beta = feats["template_pseudo_beta"][..., 0]
    tppf_distgram = torch.sum(
        torch.square(tppf_beta[..., None, :]
                     - tppf_beta[..., None, :, :]), dim=-1, keepdim=True)
    min_bin = 3.25
    max_bin = 50.75
    num_bins = 39
    lower = torch.linspace(min_bin, max_bin, num_bins, device=tppf_distgram.device).square()
    upper = torch.cat([lower[1:], lower.new_tensor([1E20])], dim=-1)
    tppf_distgram = ((tppf_distgram > lower) * (tppf_distgram < upper)).float()

    tppf_onehot = F.one_hot(feats["template_aatype"][..., 0], num_classes=22)
    n_res = feats["template_aatype"].shape[-2]  # TODO need to be careful
    tppf_onehot2d1 = tppf_onehot[..., None, :, :]
    tppf_onehot2d1 = tppf_onehot2d1.expand(*tppf_onehot2d1.shape[:-3], n_res, -1, -1)
    tppf_onehot2d2 = tppf_onehot[..., None, :]
    tppf_onehot2d2 = tppf_onehot2d2.expand(*tppf_onehot2d2.shape[:-3], -1, n_res, -1)
    # rigids = Rigid.make_transform_from_reference(
    #     n_xyz=feats["template_all_atom_positions"][..., 0, :,0],
    #     ca_xyz=feats["template_all_atom_positions"][..., 1, :,0],
    #     c_xyz=feats["template_all_atom_positions"][..., 2, :,0],
    #     eps=1E-8,
    # )
    # points = rigids.get_trans()[..., None, :, :]
    # rigid_vec = rigids[..., None].invert_apply(points)
    # inv_distance_scalar = torch.rsqrt(1E-20 + torch.sum(rigid_vec ** 2, dim=-1))
    # # rigid_v = rigid_vec(feats["template_all_atom_positions"][..., :3, :, 0])
    # # for i in range(4):
    # #     print(rigid_vec[i].sum())
    # # inv_dis_scalar = torch.rsqrt(torch.sum(rigid_v ** 2, dim=-1) + 1E-20)
    tppf_aamask = feats["template_all_atom_mask"][..., 0]

    tppf_bbmask = tppf_aamask[..., 0] * tppf_aamask[..., 1] * tppf_aamask[..., 2]
    tppf_bbmask2d = tppf_bbmask[..., None] * tppf_bbmask[..., None, :]
    # inv_distance_scalar = inv_distance_scalar * tppf_bbmask2d
    # unit_vector = (rigid_vec * inv_distance_scalar[..., None])
    if True:  # TODO: openfold don't use this
        # unit_vector=0*unit_vector
        unit_vector = torch.zeros([*tppf_distgram.shape[:-1], 3], device=tppf_distgram.device)
    to_concat = [tppf_distgram, tppf_betamask2d[..., None], tppf_onehot2d1.float(), tppf_onehot2d2.float(),
                 unit_vector.float(), tppf_bbmask2d[..., None].float()]
    tppf = torch.cat(to_concat, dim=-1)
    tppf = tppf * tppf_bbmask2d[..., None]
    ####
    emf = torch.cat([F.one_hot(feats["extra_msa"][..., 0], 23).float(),
                     feats["extra_has_deletion"][..., 0].unsqueeze(-1).float(),
                     feats["extra_deletion_value"][..., 0].unsqueeze(-1).float()], dim=-1)
    input_features = InputEmbedderFeatures()
    input_features.tf = tf.cuda()

    input_features.ri = ri.cuda()
    input_features.mf = mf.cuda()
    input_features.tpaf = tpaf.cuda()
    input_features.tppf = tppf.cuda()
    input_features.emf = emf.cuda()
    mask_features = MaskFeatures()
    mask_features.s_mask = s_mask.cuda()
    mask_features.z_mask = z_mask.cuda()
    mask_features.m_mask = m_mask.cuda()
    mask_features.em_mask = feats["extra_msa_mask"][..., 0].cuda()
    mask_features.aatype = feats["aatype"][..., 0].long().cuda()
    mask_features.tp_mask = feats["template_mask"][..., 0].cuda()
    return input_features, mask_features


def ParseFeaturesFromPKL(fname):
    feats = torch.load(fname)
    # print(feats.keys())
    return ParseOpenfoldParms(feats)


# feats = torch.load("feats/feats2.pt")
# a =
if __name__ == '__main__':
    ...
