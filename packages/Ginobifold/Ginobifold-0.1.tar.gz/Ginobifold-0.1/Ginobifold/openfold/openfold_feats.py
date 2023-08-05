import torch
import os
from Ginobifold.openfold.data import templates,data_pipeline,feature_pipeline
from Ginobifold.openfold.config import model_config

config = model_config(
    "model_1",
    train=False,
    low_prec=False
)

def openfold_feats(
        alignment_dir,
        mmcif_dir='/public/home/pangaq/folding/params/pdb_mmcif/mmcif_files/',
        max_template_date="2021-12-20",
        kalign_binary_path='/public/home/pangaq/openfold/lib/conda/envs/openfold_venv/bin/kalign',
        release_dates_path=None,
        obsolete_pdbs_path=None
):
    template_featurizer = templates.TemplateHitFeaturizer(
        mmcif_dir=mmcif_dir,
        max_template_date=max_template_date,
        max_hits=config.data.predict.max_templates,
        kalign_binary_path=kalign_binary_path,
        release_dates_path=release_dates_path,
        obsolete_pdbs_path=obsolete_pdbs_path
    )

    data_processor = data_pipeline.DataPipeline(template_featurizer=template_featurizer,)
    feature_processor = feature_pipeline.FeaturePipeline(config.data)
    local_alignment_dir=os.path.abspath(alignment_dir)
    files = os.listdir(local_alignment_dir)

    for f in files:
        if f.endswith('a3m'):
            cmd = 'head -n 2 '+os.path.join(local_alignment_dir,f) +' > '+os.path.join(local_alignment_dir) +'/input.fasta'
            os.system(cmd)
    fasta_path = os.path.join(local_alignment_dir) +'/input.fasta'
    feature_dict = data_processor.process_fasta(
        fasta_path=fasta_path, alignment_dir=local_alignment_dir
    )

    processed_feature_dict = feature_processor.process_features(
        feature_dict, mode='predict',
    )
    with torch.no_grad():
        batch = {
            k:torch.as_tensor(v)
            for k,v in processed_feature_dict.items()
        }
    return batch
