import sys

import torch
import torch.nn as nn

from Ginobifold.model.feature_embedder import FeatureEmbedder
from Ginobifold.model.stacks import TemplatePairStack, ExtraMSAStack, EvoformerStack
from Ginobifold.model.structure_module import StructureModule
from Ginobifold.model.heads import PerResidueLDDTCaHeads, compute_plddt
from Ginobifold.configs import GetRecursivekwargs, GlobalConfig

from Ginobifold.featurizer.feature_transform import ParseOpenfoldParms, RecycleFeatures
from Ginobifold.import_weight import P_InputEmbedder, model_parms, parmkeys, load_af2_parms
from Ginobifold.openfold.openfold_feats import openfold_feats
from Ginobifold.residue_torch_constants import pseudo_beta_index
from Ginobifold.residue_constants import makepdb

import time
import tqdm


class GinobifoldPredictor(nn.Module):
    def __init__(self, config: GlobalConfig, recycle=1, ofile_name=".pdb"):
        super().__init__()
        self.config = config
        self.ofile_name = ofile_name
        self.feature_embedder = FeatureEmbedder(**GetRecursivekwargs(config.ModelConfig.FeatureEmbedderConfig))
        if self.config.FeatureConfig.use_template:
            self.template_pair_stack = TemplatePairStack(**GetRecursivekwargs(config.ModelConfig.TemplatePairStack))
        self.extra_msa_stack = ExtraMSAStack(**GetRecursivekwargs(config.ModelConfig.ExtraMSAStackConfig))
        self.evoformer_stack = EvoformerStack(**GetRecursivekwargs(config.ModelConfig.EvoformerStackConfig))
        self.structure_module = StructureModule(**GetRecursivekwargs(config.ModelConfig.StructureModuleConfig))
        self.recycles = recycle
        self.lddt_heads = PerResidueLDDTCaHeads(**GetRecursivekwargs(config.ModelConfig.HeadsConfig.plddt))

    def forward(self, input_f, mask_f):
        begin = time.time()
        recycle_f = RecycleFeatures()
        x, s = None, None
        for i in range(self.recycles):
            # Feature Embedder
            sys.stdout.flush()
            for _ in tqdm.tqdm(range(1), bar_format="FeatureEmbedder {l_bar}{bar}{r_bar}"):
                m, z, em, t = self.feature_embedder(**GetRecursivekwargs(input_f), **GetRecursivekwargs(recycle_f),
                                                    m_mask=mask_f.m_mask)
            # Template Pair Stack, Optional, only for model_1, model_2
            if self.config.FeatureConfig.use_template:
                z = self.template_pair_stack(t=t, tp_mask=mask_f.tp_mask, z=z, z_mask=mask_f.z_mask)  # 2 * 2
            # Extra MSA stack
            z = self.extra_msa_stack(em=em, z=z, em_mask=mask_f.em_mask, z_mask=mask_f.z_mask)  # 4 * 2
            # Evoformer
            m, z, s = self.evoformer_stack(m, mask_f.m_mask, z, mask_f.z_mask)  # 48 + 8+ 4
            # Structure Module
            s, x, _, _, _ = self.structure_module(s, z, mask_f.s_mask, mask_f.aatype)
            # Update Recycle TODO May need to embed in structure module?
            recycle_f.m1_prev = m[..., 0, :, :]
            recycle_f.x_prev = x[pseudo_beta_index(mask_f.aatype)]
            recycle_f.z_prev = z
            # output
        lddt_logits = self.lddt_heads(s)
        plddt = compute_plddt(lddt_logits)
        print("Forwarding Time", time.time() - begin)
        with open(self.ofile_name, "w") as f:
            f.write(makepdb(mask_f.aatype.tolist(), x.tolist(), plddt.tolist()))

    def load_af2_params(self, model_id=1, af2_parsms_dir=None):
        load_af2_parms(self, model_id=model_id, af2_parsms_dir=af2_parsms_dir)


def predict(
        alignment_dir="/home/zhangkexin/research/data/alignments/T1104_base",
        mmcif_dir="/home/zhangkexin/research/data/pdb_mmcif/mmcif_files",
        recycle=1,
        model_ids=(1,),
        af2_params_dir=None,
):
    config = GlobalConfig()
    feats = openfold_feats(alignment_dir=alignment_dir, mmcif_dir=mmcif_dir)
    input_f, mask_f = ParseOpenfoldParms(feats)
    for model_id in model_ids:
        if model_id in [3, 4, 5]:
            config.FeatureConfig.use_template = False
        model = GinobifoldPredictor(config, recycle=recycle,
                                    ofile_name=f"model_{model_id}.recycle_{recycle}.pdb").cuda()
        model.load_af2_params(model_id, af2_parsms_dir=af2_params_dir)
        with torch.no_grad():
            model(input_f, mask_f)


if __name__ == '__main__':
    predict(
        alignment_dir="/home/zhangkexin/research/data/alignments/T1104_base", # set alignments folder
        mmcif_dir="/home/zhangkexin/research/data/pdb_mmcif/mmcif_files", # set pdb mmcif files folder
        recycle=1,      # set recycles
        model_ids=(1,), # set predicted model_ids in an array
        af2_params_dir=None, # set af2 parameters folder. By default, it is "Ginobifold/params"
    )





# input_embedder=InputEmbedder(**GetRecursivekwargs(GlobalConfig.ModelConfig.FeatureEmbedderConfig.InputEmbedderConfig))
# P_InputEmbedder(input_embedder,parmkeys.evoformer,f=lambda x: nn.Parameter(x.cuda()),parms=model_parms(1))
# m,z=input_embedder(input_f.tf,input_f.ri,input_f.mf)
#
# tensor([[[ 3.2327e-02, -2.0335e-01, -6.8520e-01,  ...,  2.0111e-01,
#            -7.1309e-01,  7.2195e-02],
#          [ 2.9497e-01, -2.9494e-01, -2.6579e-01,  ...,  1.7839e-01,
#            -3.3050e-01,  2.2752e-01],
#          [-2.7635e-01, -5.7955e-02, -4.7752e-01,  ...,  1.0183e-01,
#           3.7563e-02,  2.7599e-01],
#          ...,
#          [ 5.1419e-01, -1.8614e-01,  2.5297e-01,  ...,  3.6994e-01,
#            -1.2390e-01,  4.6572e-02],
#          [ 1.1661e+00,  1.6410e-01,  5.5879e-01,  ...,  4.1619e-02,
#            1.6198e-01,  9.1585e-01],
#          [ 2.2661e-01, -2.1592e-01, -6.4050e-01,  ...,  6.7671e-01,
#            -2.6638e-01, -1.9612e-01]],
#
#         [[ 3.5062e-01, -1.9687e-01, -7.6194e-02,  ..., -2.8888e-03,
#            7.0814e-04, -9.9331e-02],
#          [ 3.8427e-01, -3.8185e-01,  1.0113e-01,  ..., -1.1179e-01,
#            -7.6614e-03, -1.9125e-01],
#          [ 5.1177e-01, -3.2248e-01, -7.3320e-02,  ..., -1.9760e-01,
#            3.6220e-02,  2.0905e-01],
#          ...,
#          [-8.8528e-02, -1.8445e-01, -1.3513e-01,  ...,  9.9890e-01,
#           -2.3072e-01, -8.8872e-01],
#          [ 1.2045e+00,  1.7251e-01,  6.1464e-01,  ...,  1.5944e-01,
#            3.0467e-01,  1.0091e+00],
#          [ 1.2642e-01,  3.1516e-02, -3.1156e-02,  ...,  5.6542e-01,
#            -2.2835e-01,  2.4115e-01]],
#
#         [[ 3.5062e-01, -1.9687e-01, -7.6194e-02,  ..., -2.8889e-03,
#            7.0811e-04, -9.9331e-02],
#          [ 3.8427e-01, -3.8185e-01,  1.0113e-01,  ..., -1.1179e-01,
#            -7.6615e-03, -1.9125e-01],
#          [ 5.3392e-01, -1.8545e-02,  1.8341e-01,  ..., -1.9573e-01,
#            -1.4113e-01,  5.3624e-01],
#          ...,
#          [ 1.9599e-01, -8.3636e-03, -5.9061e-01,  ...,  6.3552e-01,
#            -3.8139e-01,  5.1181e-02],
#          [ 1.2045e+00,  1.7251e-01,  6.1464e-01,  ...,  1.5944e-01,
#            3.0467e-01,  1.0091e+00],
#          [ 2.3360e-01,  8.5783e-02, -1.2789e-01,  ..., -2.4428e-02,
#            -2.2614e-01,  4.6668e-01]],
#
#         ...,
#
#         [[ 3.5062e-01, -1.9687e-01, -7.6194e-02,  ..., -2.8889e-03,
#            7.0810e-04, -9.9331e-02],
#          [ 3.8427e-01, -3.8185e-01,  1.0113e-01,  ..., -1.1179e-01,
#            -7.6615e-03, -1.9125e-01],
#          [ 5.1177e-01, -3.2248e-01, -7.3320e-02,  ..., -1.9760e-01,
#            3.6220e-02,  2.0905e-01],
#          ...,
#          [ 6.2719e-01, -4.3001e-01,  3.2091e-01,  ...,  5.3149e-02,
#            -1.0367e-01, -7.8163e-02],
#          [ 1.2045e+00,  1.7251e-01,  6.1464e-01,  ...,  1.5944e-01,
#            3.0467e-01,  1.0091e+00],
#          [ 4.5545e-01,  1.4601e-01,  1.8239e-01,  ..., -5.1949e-03,
#            -3.2770e-01,  5.3767e-01]],
#
#         [[ 3.5062e-01, -1.9687e-01, -7.6194e-02,  ..., -2.8886e-03,
#            7.0821e-04, -9.9331e-02],
#          [ 5.4381e-01, -2.2164e-01,  8.7934e-01,  ..., -2.0561e-02,
#            -6.3338e-02, -4.9455e-02],
#          [ 5.1177e-01, -3.2248e-01, -7.3320e-02,  ..., -1.9760e-01,
#            3.6221e-02,  2.0905e-01],
#          ...,
#          [-2.4706e-01,  2.4251e-01, -1.1786e-01,  ...,  7.7906e-03,
#           -7.8605e-01, -1.4278e-01],
#          [ 1.2045e+00,  1.7251e-01,  6.1464e-01,  ...,  1.5944e-01,
#            3.0466e-01,  1.0091e+00],
#          [ 2.1145e-01, -2.1815e-01, -3.8462e-01,  ..., -2.6298e-02,
#            -4.8793e-02,  1.3949e-01]],
#
#         [[ 3.5062e-01, -1.9687e-01, -7.6194e-02,  ..., -2.8889e-03,
#            7.0811e-04, -9.9331e-02],
#          [ 3.8427e-01, -3.8185e-01,  1.0113e-01,  ..., -1.1179e-01,
#            -7.6615e-03, -1.9125e-01],
#          [ 5.1177e-01, -3.2248e-01, -7.3320e-02,  ..., -1.9760e-01,
#            3.6220e-02,  2.0905e-01],
#          ...,
#          [ 8.8860e-01,  6.5598e-01,  3.3082e-03,  ...,  4.7710e-01,
#            3.4874e-01, -3.6107e-02],
#          [ 1.2045e+00,  1.7251e-01,  6.1464e-01,  ...,  1.5944e-01,
#            3.0467e-01,  1.0091e+00],
#          [-6.2372e-03, -1.1654e-01, -3.2901e-01,  ...,  2.5764e-01,
#           2.3021e-01,  1.1899e-01]]], device='cuda:0')
# tensor([[[-0.5059, -2.3519,  0.1131,  ...,  0.8005,  0.6374,  0.3199],
#          [-0.0330, -2.6697,  0.7650,  ..., -0.8945, -0.0178, -0.2616],
#          [ 1.4607, -3.3349, -0.0669,  ...,  0.2744,  0.0785,  0.4598],
#          ...,
#          [ 0.5118, -0.9838,  0.4856,  ...,  0.0505,  0.7544,  0.0098],
#          [ 0.4978, -1.8208,  0.7925,  ..., -0.4061, -0.0192, -1.1033],
#          [ 0.2146, -1.1908,  0.6701,  ...,  0.1134, -0.1508, -0.1174]],
#
#         [[-0.5471, -1.5327,  0.9679,  ...,  0.3544,  0.1439,  0.2519],
#          [-0.3873, -3.0109, -0.0301,  ...,  0.2949,  0.2798, -0.4670],
#          [ 0.2360, -2.1506,  0.2105,  ..., -0.4422, -0.5823, -0.1561],
#          ...,
#          [ 0.5179, -0.9630,  0.2527,  ...,  0.0468,  0.5249, -0.3443],
#          [ 0.5039, -1.8000,  0.5597,  ..., -0.4097, -0.2487, -1.4574],
#          [ 0.2207, -1.1699,  0.4373,  ...,  0.1098, -0.3803, -0.4715]],
#
#         [[ 0.7416, -2.6055,  0.5052,  ...,  1.0558,  1.2894, -0.0812],
#          [-0.2879, -2.2594,  1.4318,  ..., -0.0113,  0.5196,  0.1262],
#          [ 0.0224, -2.5594,  0.0224,  ...,  0.8870,  0.4486,  0.2996],
#          ...,
#          [ 0.6647, -1.0097,  0.6269,  ...,  0.1830,  1.0287, -0.0373],
#          [ 0.6507, -1.8467,  0.9339,  ..., -0.2735,  0.2550, -1.1503],
#          [ 0.3674, -1.2167,  0.8115,  ...,  0.2460,  0.1235, -0.1644]],
#
#         ...,
#
#         [[ 0.4283, -1.0240,  0.6249,  ..., -0.0593,  0.8654, -0.1698],
#          [ 0.5407, -1.7039,  0.7145,  ..., -0.5612,  0.7373, -0.6026],
#          [ 0.8037, -1.2056,  0.3928,  ..., -0.1053,  0.4024, -0.1430],
#          ...,
#          [-0.5059, -2.3519,  0.1131,  ...,  0.8005,  0.6374,  0.3199],
#          [-0.1595, -2.8268,  0.9823,  ..., -0.8491, -0.6633, -0.9418],
#          [ 0.7880, -3.3602,  0.3497,  ...,  0.3834, -0.3637,  0.3058]],
#
#         [[ 0.4994, -1.0862,  0.5751,  ..., -0.1265,  0.7965, -0.9477],
#          [ 0.6119, -1.7661,  0.6647,  ..., -0.6284,  0.6684, -1.3805],
#          [ 0.8748, -1.2678,  0.3430,  ..., -0.1725,  0.3334, -0.9209],
#          ...,
#          [-0.4821, -1.6158,  1.1510,  ...,  0.2909,  0.3045, -0.1719],
#          [-0.4488, -3.2512,  0.3703,  ...,  0.2768, -0.2052, -1.5711],
#          [-0.3717, -2.2590,  0.8101,  ..., -0.3967, -0.8639, -0.7339]],
#
#         [[ 0.2437, -1.2557,  0.3693,  ...,  0.1955,  0.2924, -0.1273],
#          [ 0.3562, -1.9355,  0.4589,  ..., -0.3064,  0.1644, -0.5601],
#          [ 0.6191, -1.4373,  0.1372,  ...,  0.1495, -0.1706, -0.1005],
#          ...,
#          [ 0.4043, -2.8113,  0.1082,  ...,  1.1781,  0.4422,  0.0083],
#          [-0.7518, -2.6223,  1.2521,  ...,  0.1563, -0.9732, -0.4645],
#          [-0.9877, -2.7906,  0.0421,  ...,  1.1183, -0.8408,  0.2352]]],
#        device='cuda:0')
