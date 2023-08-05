import sys

import torch
import torch.nn as nn

from Ginobifold.model.feature_embedder import FeatureEmbedder
from Ginobifold.model.stacks import TemplatePairStack, ExtraMSAStack, EvoformerStack
from Ginobifold.model.structure_module import StructureModule
from Ginobifold.model.heads import PerResidueLDDTCaHeads, compute_plddt
from Ginobifold.configs import GetRecursivekwargs, GlobalConfig

from Ginobifold.featurizer.feature_transform import ParseOpenfoldParms, RecycleFeatures
from Ginobifold.import_weight import P_InputEmbedder, model_parms, load_af2_parms
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
        model_ids=(3,), # set predicted model_ids in an array
        af2_params_dir=None, # set af2 parameters folder. By default, it is "Ginobifold/params"
    )





# input_embedder=InputEmbedder(**GetRecursivekwargs(GlobalConfig.ModelConfig.FeatureEmbedderConfig.InputEmbedderConfig))
# P_InputEmbedder(input_embedder,parmkeys.evoformer,f=lambda x: nn.Parameter(x.cuda()),parms=model_parms(1))
# m,z=input_embedder(input_f.tf,input_f.ri,input_f.mf)
