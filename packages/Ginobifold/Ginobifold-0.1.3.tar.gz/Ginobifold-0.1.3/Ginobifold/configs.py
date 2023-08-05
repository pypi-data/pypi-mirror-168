# Quickly Parse Args without using ml_collections

def GetRecursivekwargs(Config):
    kwargs = {}
    attrs = {i: getattr(Config, i) for i in dir(Config) if not i.startswith("__")}
    for attr in attrs:
        if isinstance(attrs[attr], type(Config)):
            kwargs.update(GetRecursivekwargs(attrs[attr]))
        else:
            kwargs.update({attr: attrs[attr]})
    return kwargs


class GlobalConfig:
    class FeatureConfig:
        use_template = True

    class ModelConfig:
        class FeatureEmbedderConfig:
            class InputEmbedderConfig:
                c_tf = 22
                c_mf = 49
                c_z = 128
                c_m = 256
                window_size = 32

            class RecyclingEmdbedderConfig:
                c_m = 256
                c_z = 128
                min_bin = 3.25
                max_bin = 20.75
                num_bins = 15

            class TemplateAngleEmbedderConfig:
                c_tpaf = 57
                c_m = 256

            class TemplatePairEmbedderConfig:
                c_tppf = 88
                c_z = 128

            class ExtraMSAEmbedderConfig:
                c_emf = 25
                c_e = 64

        class TemplatePairStack:
            num_blocks = 2

            class TemplatePairStackBlock:
                c_t = 64
                c_u_t = 64
                c_a_t = 16
                h_t = 4
                pt = 2

            class TemplatePointwiseAttention:  # Need to split later
                c_z = 128
                c_t = 64
                h_t = 4
                c_a_t = 16

        class ExtraMSAStackConfig:
            num_blocks = 4

            class ExtraMSAStackBlockConfig:
                c_m = 64
                h_m = 8
                c_a_m = 8
                c_z = 128
                c_opm = 32
                c_u_z = 128
                c_a_z = 32
                h_z = 4
                pt = 4

        class EvoformerStackConfig:
            num_blocks = 48
            c_s = 384

            class EvoformerStackBlockConfig:
                c_m = 256
                c_z = 128
                c_a_z = 32
                c_a_m = 32
                c_opm = 32
                c_u = 128
                h_z = 4
                h_m = 8
                pt = 4

        class StructureModuleConfig:
            c_s = 384
            c_z = 128
            c_ipa = 16
            c_resnet = 128
            h_ipa = 12
            num_qk = 4
            num_v = 8
            num_blocks = 8
            num_tlayers = 1
            num_resnet = 2

        class HeadsConfig:
            class plddt:
                c_in = 384
                c_h = 128
                num_bins = 50


if __name__ == '__main__':
    ...
    # print(V2.shape)
    # print(AT1.sum(),AT1.shape)
    # print(AT2.sum(),AT2.shape)
    # print()
    # print(AT1.permute([0,3,2,1])[0]-AT2[0])
