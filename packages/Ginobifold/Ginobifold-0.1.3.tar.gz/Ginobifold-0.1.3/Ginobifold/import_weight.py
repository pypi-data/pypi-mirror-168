import numpy as np
import os
from ml_collections import config_dict
import torch
import torch.nn as nn


# parms = {k: torch.from_numpy(v) for k, v in np.load(os.path.join(os.path.split(__file__)[0],"params/params_model_1.npz")).items()}


def model_parms(i,af2_parsms_dir=None):
    print(f"# AF2 model {i} params preparing!")
    if af2_parsms_dir is None:
        return {k: torch.from_numpy(v) for k, v in np.load(os.path.join(os.path.split(__file__)[0],f"params/params_model_{i}.npz")).items()}
    else:
        return {k: torch.from_numpy(v) for k, v in np.load(os.path.join(os.path.abspath(af2_parsms_dir),f"params_model_{i}.npz")).items()}




# import json
# with open("par.json","w") as f:
#     json.dump(parmkeys.to_dict(),f,indent=2)

################### Base ######################

def P_Dense(a, b, f,parms):
    a.w = f(parms[b.weights])
    a.b = f(parms[b.bias])


def P_Layernorm(a, b, f,parms):
    a.weight = f(parms[b.scale])
    a.bias = f(parms[b.offset])


##################### Embedders ##################

def P_InputEmbedder(a, b, f,parms):
    P_Dense(a.dense_tf_z1, b.left_single, f,parms=parms)
    P_Dense(a.dense_tf_z2, b.right_single, f,parms=parms)
    P_Dense(a.dense_tf_m, b.preprocess_1d, f,parms=parms)
    P_Dense(a.dense_mf_m, b.preprocess_msa, f,parms=parms)
    P_Dense(a.dense_ri_z, b.pair_activiations, f,parms=parms)


def P_RecyclingEmbedder(a, b, f,parms):
    P_Dense(a.dense_dist_z, b.prev_pos_linear, f,parms=parms)
    P_Layernorm(a.norm_m, b.prev_msa_first_row_norm, f,parms=parms)
    P_Layernorm(a.norm_z, b.prev_pair_norm, f,parms=parms)


def P_TemplateAngleEmbedder(a, b, f,parms):
    P_Dense(a.dense_tpaf_m1, b.template_single_embedding, f,parms=parms)
    P_Dense(a.dense_m1_m2, b.template_projection, f,parms=parms)


def P_TemplatePairEmbedder(a, b, f,parms):
    P_Dense(a.dense_tppf_z, b.template_embedding.single_template_embedding.embedding2d, f,parms=parms)


def P_ExtraMSAEmbedder(a, b, f,parms):
    P_Dense(a.dense_emf_e, b.extra_msa_activations, f,parms=parms)


def P_FeatureEmbedder(a, b, f,parms):
    P_InputEmbedder(a.input_embedder, b, f,parms=parms)
    P_RecyclingEmbedder(a.recycle_embedder, b, f,parms=parms)
    if "template_embedding" in b:
        P_TemplateAngleEmbedder(a.template_angle_embedder, b, f,parms=parms)
        P_TemplatePairEmbedder(a.template_pair_embedder, b, f,parms=parms)
    P_ExtraMSAEmbedder(a.extra_msa_embedder, b, f,parms=parms)


############################ blocks ##################################

def P_Atten_no_G(a, b, f,parms):
    a.dense_q.w = f(parms[b.query_w])
    a.dense_k.w = f(parms[b.key_w])
    a.dense_v.w = f(parms[b.value_w])
    a.dense_o.w = f(parms[b.output_w])
    a.dense_o.b = f(parms[b.output_b])


def P_Atten(a, b, f,parms):  # Attention and the Global ATtention
    a.dense_q.w = f(parms[b.query_w])
    a.dense_k.w = f(parms[b.key_w])
    a.dense_v.w = f(parms[b.value_w])
    a.dense_o.w = f(parms[b.output_w])
    a.dense_o.b = f(parms[b.output_b])
    a.dense_g.w = f(parms[b.gating_w])
    a.dense_g.b = f(parms[b.gating_b])


def P_Atten_Q(a, b, f,parms):  # Colwise Attention. The Col  Global Atten is similar
    P_Atten(a.attention, b.attention, f,parms=parms)
    P_Layernorm(a.layernorm, b.query_norm, f,parms=parms)


def P_Atten_Q_D(a, b, f,parms):  # Trirow/col Attention
    P_Atten_Q(a, b, f,parms=parms)
    a.dense_z.w = f(parms[b.feat_2d_weights])


def P_Atten_Q_D_Q(a, b, f,parms):  # rowwise attention
    P_Atten_Q_D(a, b, f,parms=parms)
    P_Layernorm(a.layernorm_z, b.feat_2d_norm, f,parms=parms)


def P_PairUpdateRC(a, b, f,parms):
    P_Layernorm(a.norm_in, b.layer_norm_input, f,parms=parms)
    P_Layernorm(a.norm_out, b.center_layer_norm, f,parms=parms)
    P_Dense(a.dense_q1, b.left_projection, f,parms=parms)
    P_Dense(a.dense_q2, b.left_gate, f,parms=parms)
    P_Dense(a.dense_k1, b.right_projection, f,parms=parms)
    P_Dense(a.dense_k2, b.right_gate, f,parms=parms)
    P_Dense(a.dense_v2, b.gating_linear, f,parms=parms)
    P_Dense(a.dense_v1, b.output_projection, f,parms=parms)


def P_Transition(a, b, f,parms):
    P_Layernorm(a.norm, b.input_layer_norm, f,parms=parms)
    P_Dense(a.dense1, b.transition1, f,parms=parms)
    P_Dense(a.dense2, b.transition2, f,parms=parms)


def P_Opm(a, b, f,parms):
    P_Layernorm(a.layernorm, b.layer_norm_input, f,parms=parms)
    P_Dense(a.dense_q, b.left_projection, f,parms=parms)
    P_Dense(a.dense_k, b.right_projection, f,parms=parms)
    a.dense_g.w = f(parms[b.output_w])
    a.dense_g.b = f(parms[b.output_b])


def P_MSA_Atten(a, b, f,parms):
    P_Atten_Q_D_Q(a.row_atten, b.msa_row_attention_with_pair_bias, f,parms=parms)
    P_Atten_Q(a.col_atten, b.msa_column_attention, f,parms=parms)
    P_Transition(a.transition, b.msa_transition, f,parms=parms)


def P_ExtraMSA_Atten(a, b, f,parms):
    P_Atten_Q_D_Q(a.row_atten, b.msa_row_attention_with_pair_bias, f,parms=parms)
    P_Atten(a.col_atten, b.msa_column_global_attention.attention, f,parms=parms)
    P_Layernorm(a.col_atten.layernorm, b.msa_column_global_attention.query_norm, f,parms=parms)
    P_Transition(a.transition, b.msa_transition, f,parms=parms)


def P_Pair_Update(a, b, f,parms):
    P_PairUpdateRC(a.row_update, b.triangle_multiplication_outgoing, f,parms=parms)
    P_PairUpdateRC(a.col_update, b.triangle_multiplication_incoming, f,parms=parms)


def P_Pair_Atten(a, b, f,parms):
    P_Atten_Q_D(a.row_atten, b.triangle_attention_starting_node, f,parms=parms)
    P_Atten_Q_D(a.col_atten, b.triangle_attention_ending_node, f,parms=parms)
    P_Transition(a.transition, b.pair_transition, f,parms=parms)


def D_Pair_Core(a, b, f,parms):
    P_Opm(a.opm, b.outer_product_mean, f,parms=parms)
    P_Pair_Update(a.pair_update, b, f,parms=parms)
    P_Pair_Atten(a.pair_atten, b, f,parms=parms)


######################## ###########################################

def P_EvoformerStackBlock(a, b, f,parms):
    P_MSA_Atten(a.msa_atten, b, f,parms=parms)
    D_Pair_Core(a.pair_core, b, f,parms=parms)


def P_ExtraMSAStackBlock(a, b, f,parms):
    P_ExtraMSA_Atten(a.msa_atten, b, f,parms=parms)
    D_Pair_Core(a.pair_core, b, f,parms=parms)


def P_TemplatePairStackBlock(a, b, f,parms):
    # Attention: map order is not forward order
    P_Pair_Update(a, b.__layer_stack_no_state, f,parms=parms)
    P_Pair_Atten(a, b.__layer_stack_no_state, f,parms=parms)


#################### stacks ########################################
def P_TemplatePairStack(a, b, f, n,parms):
    for i in range(n):
        ff = lambda x: f(x[i])
        P_TemplatePairStackBlock(a.blocks[i], b.single_template_embedding.template_pair_stack, ff,parms=parms)
    P_Layernorm(a.layernorm, b.single_template_embedding.output_layer_norm, f,parms=parms)
    P_Atten_no_G(a.template_pointwise_atten.attention, b.attention, f,parms=parms)


def P_ExtraMSAtack(a, b, f, n,parms):
    for i in range(n):
        ff = lambda x: f(x[i])
        P_ExtraMSAStackBlock(a.blocks[i], b.extra_msa_stack, ff,parms=parms)


def P_EvoformerStack(a, b, f, n,parms):
    for i in range(n):
        ff = lambda x: f(x[i])
        P_EvoformerStackBlock(a.blocks[i], b.evoformer_iteration, ff,parms=parms)
    P_Dense(a.dense_m_s, b.single_activations, f,parms)


############### structure module ##################################

def P_SMinit(a, b, f,parms):
    P_Layernorm(a.layernorm_s, b.single_layer_norm, f,parms=parms)
    P_Layernorm(a.layernorm_z, b.pair_layer_norm, f,parms=parms)
    P_Dense(a.dense_in, b.initial_projection, f,parms=parms)
    P_Layernorm(a.layernorm_ipa, b.fold_iteration.attention_layer_norm, f,parms=parms)


def P_IPA(a, b, f,parms):
    P_Dense(a.dense_q, b.q_scalar, f,parms=parms)
    P_Dense(a.dense_kv, b.kv_scalar, f,parms=parms)
    P_Dense(a.dense_q3, b.q_point_local, f,parms=parms)
    P_Dense(a.dense_kv3, b.kv_point_local, f,parms=parms)
    P_Dense(a.dense_b, b.attention_2d, f,parms=parms)
    P_Dense(a.dense_o, b.output_projection, f,parms=parms)
    a.hw = f(parms[b.trainable_point_weights])


def P_SMTransition(a, b, f,parms):
    P_Dense(a.layers[0].dense1, b.fold_iteration.transition, f,parms=parms)
    P_Dense(a.layers[0].dense2, b.fold_iteration.transition_1, f,parms=parms)
    P_Dense(a.layers[0].dense3, b.fold_iteration.transition_2, f,parms=parms)
    P_Layernorm(a.layernorm, b.fold_iteration.transition_layer_norm, f,parms=parms)


def P_SMResnet(a, b, f,parms):
    P_Dense(a.dense_init, b.input_projection_1, f,parms=parms)
    P_Dense(a.dense_in, b.input_projection, f,parms=parms)
    P_Dense(a.dense_out, b.unnormalized_angles, f,parms=parms)
    P_Dense(a.layers[0].dense1, b.resblock1, f,parms=parms)
    P_Dense(a.layers[0].dense2, b.resblock2, f,parms=parms)
    P_Dense(a.layers[1].dense1, b.resblock1_1, f,parms=parms)
    P_Dense(a.layers[1].dense2, b.resblock2_1, f,parms=parms)


def P_StructureModule(a, b, f,parms):
    P_SMinit(a, b, f,parms=parms)
    P_IPA(a.ipa, b.fold_iteration.invariant_point_attention, f,parms=parms)
    P_SMTransition(a.transition, b, f,parms=parms)
    P_SMResnet(a.angle_out, b.fold_iteration.rigid_sidechain, f,parms=parms)
    P_Dense(a.backbone_out, b.fold_iteration.affine_update, f,parms=parms)


##################### heads #####################

def P_PLDDTCA(a,b,f,parms):
    P_Layernorm(a.layernorm,b.input_layer_norm,f,parms=parms)
    P_Dense(a.dense1,b.act_0,f,parms=parms)
    P_Dense(a.dense2,b.act_1,f,parms=parms)
    P_Dense(a.dense3,b.logits,f,parms=parms)




def load_af2_parms(a, f=None,model_id=1,af2_parsms_dir=None):
    parms=model_parms(model_id,af2_parsms_dir=af2_parsms_dir)
    if f is None:
        f = lambda x: nn.Parameter(x.cuda())

    PREFIX = "alphafold/alphafold_iteration"
    parmkeys = dict()
    for key in parms.keys():
        its = key.replace("//", "/").split("/")
        map_ = parmkeys
        for itid, it in enumerate(its[2:-1]):
            if it in map_:
                map_ = map_[it]
            else:
                map_[it] = dict()
                map_ = map_[it]
        map_[its[-1]] = key
    parmkeys = config_dict.ConfigDict(parmkeys)

    P_FeatureEmbedder(a.feature_embedder, parmkeys.evoformer, f,parms=parms)
    if "template_embedding" in parmkeys.evoformer:
        P_TemplatePairStack(a.template_pair_stack, parmkeys.evoformer.template_embedding, f, 2,parms=parms)
    P_ExtraMSAtack(a.extra_msa_stack, parmkeys.evoformer, f, 4,parms=parms)
    P_EvoformerStack(a.evoformer_stack, parmkeys.evoformer, f, 48,parms=parms)
    P_StructureModule(a.structure_module, parmkeys.structure_module, f,parms=parms)
    P_PLDDTCA(a.lddt_heads,parmkeys.predicted_lddt_head,f,parms=parms)
    print("# Parameters Mapped!")


if __name__ == '__main__':
    ...
