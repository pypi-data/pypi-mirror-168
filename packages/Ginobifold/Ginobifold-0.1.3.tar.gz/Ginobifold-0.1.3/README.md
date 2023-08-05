# Ginobifold: Simplied AF2 Inference Package
## How to use?
```python
from Ginobifold.predict import predict

predict(
    alignment_dir="/home/zhangkexin/research/data/alignments/T1104_base",  # set alignments folder
    mmcif_dir="/home/zhangkexin/research/data/pdb_mmcif/mmcif_files",  # set pdb mmcif files folder
    recycle=1,  # set recycles
    model_ids=(1,),  # set predicted model_ids in an array
    af2_params_dir=None,  # set af2 parameters folder. By default, it is "Ginobifold/params"
)
```

## STD OUT

![](view.png)
