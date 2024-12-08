# Notes on finetuning SDXL from full dataset #

- Assumed that you have followed the guide from building the dataset, and having a single folder having many `F.webp` and `F.txt` in a single folder.

- [Official guide.](https://github.com/kohya-ss/sd-scripts/blob/main/docs/fine_tune_README_ja.md)

- [Reddit post.](https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904) Clean and simple. I'm going to follow this guide.

- First, follow the official guide. I have cloned it long time ago to convert `*.safetensors` to `diffusers` like `convert_original_stable_diffusion_to_diffusers.py` and `convert_sdxl_to_diffusers.py`.

```sh
git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts
```

- Instead of `venv`, I make another `conda` environment.

- **Pay attention of** `torch<2.4`. I have experienced [this issue / PR](https://github.com/kohya-ss/sd-scripts/pull/1686) but failed to work around. 

```sh
conda create -n khoyas-env python=3.12
conda activate khoyas-env

pip install torch<2.4 torchvision --index-url https://download.pytorch.org/whl/cu124
pip install xformers --index-url https://download.pytorch.org/whl/cu124
pip install --upgrade -r requirements.txt
```

- Install `triton` via [madbuda/triton-windows-builds](https://huggingface.co/madbuda/triton-windows-builds)

```sh
pip install triton-3.0.0-cp312-cp312-win_amd64.whl
```

- Install `bitsandbytes==0.45.0` explictly for the library stack, otherwise you will see CUDA Toolkit errors and somehow cannot install CUDA Toolkit either (it may be my OS problem).

```sh
pip install bitsandbytes==0.45.0 
```

```logs
C:\Users\User\.conda\envs\khoyas-env did not contain ['cudart64_110.dll', 'cudart64_12.dll'] as expected!
```

- Run `pytyon -m bitsandbytes` first to install CUDA integrations:

```sh
> python -m bitsandbytes 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ BUG REPORT INFORMATION ++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++ OTHER +++++++++++++++++++++++++++
CUDA specs: CUDASpecs(highest_compute_capability=(8, 6), cuda_version_string='124', cuda_version_tuple=(12, 4))
PyTorch settings found: CUDA_VERSION=124, Highest Compute Capability: (8, 6).
To manually override the PyTorch CUDA version please see: https://github.com/TimDettmers/bitsandbytes/blob/main/docs/source/nonpytorchcuda.mdx
The directory listed in your path is found to be non-existent: \Users\User
The directory listed in your path is found to be non-existent: \\DESKTOP-3FL13RB
The directory listed in your path is found to be non-existent: PATH=E\x3a\NOVELAI\stable-diffusion-webui\stable-diffusion-webui\venv\Scripts
The directory listed in your path is found to be non-existent: PROMPT=(venv) $P$G:VIRTUAL_ENV=E\x3a\NOVELAI\stable-diffusion-webui\stable-diffusion-webui\venv:VIRTUAL_ENV_PROMPT=(venv) :_OLD_VIRTUAL_PROMPT=$P$G
CUDA SETUP: WARNING! CUDA runtime files not found in any environmental path.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++ DEBUG INFO END ++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Checking that the library is importable and CUDA is callable...
SUCCESS!
Installation was successful!
```

- `pip list` should see the `+cu124` stuffs. Now configure the `accelerate`, [kohya implements some of Accelerate.](https://www.reddit.com/r/StableDiffusion/comments/160z10m/how_do_i_do_multi_gpu_lora_training/)
- You can explictly set the config in CLI stage later. 
- From [this PR](https://github.com/kohya-ss/sd-scripts/pull/1686), inject `init_method="env://?use_libuv=False"` in `InitProcessGroupKwargs`. Search and replace works.

```log
> accelerate config
--------------------------------------------------------------------------------------
In which compute environment are you running?
This machine
--------------------------------------------------------------------------------------
Which type of machine are you using?
No distributed training
Do you want to run your training on CPU only (even if a GPU / Apple Silicon / Ascend NPU device is available)? [yes/NO]:NO
Do you wish to optimize your script with torch dynamo?[yes/NO]:NO
Do you want to use DeepSpeed? [yes/NO]: NO
What GPU(s) (by id) should be used for training on this machine as a comma-seperated list? [all]:all
--------------------------------------------------------------------------------------
Do you wish to use FP16 or BF16 (mixed precision)?
bf16
accelerate configuration saved at F:\WORKS\HUGGINGFACE\accelerate\default_config.yaml
```

- Now try that guide and inspect the `*.json`. Since the dataset guide has enforced to whole dataset, it may be great to limit the dataset into a small and obvious dataset.

- I have made my own subset which has obvious training target.

```log
> python just-astolfo.py
6224 pairs to be copied.
Copying image-caption pairs: 100%|████████████████████████████████████████████████| 6224/6224 [01:27<00:00, 70.81it/s
```

- (Cultural difference) My case is called "DD Tags", which is "Danbooru Tags". E621 falls in this category also. 

- [Official guide](https://github.com/kohya-ss/sd-scripts/blob/main/docs/train_README-ja.md) use `meta_cap_dd.json` and `meta_lat.json`, so I'm going to follow them.

```log
> python ./finetune/merge_dd_tags_to_metadata.py "H:/just_astolfo/khoyas_finetune" "H:/just_astolfo/meta_cap_dd.json"
2024-12-08 14:44:59 INFO     found 6224 images.                                         merge_dd_tags_to_metadata.py:23                    
                    INFO     new metadata will be created /                             merge_dd_tags_to_metadata.py:33                             
新しいメタデータファイルが作成されます
                    INFO     merge tags to metadata json.                               merge_dd_tags_to_metadata.py:36
100%|███████████████████████████████████████████████████████████████████████████| 6224/6224 [00:01<00:00, 5094.49it/s] 
2024-12-08 14:45:01 INFO     writing metadata: H:/just_astolfo/meta_cap_dd.json         merge_dd_tags_to_metadata.py:53                    
                    INFO     done!                                                      merge_dd_tags_to_metadata.py:56
```

```log
> python ./finetune/merge_dd_tags_to_metadata.py "H:/e621_newest-webp-4Mpixel/khoyas_finetune" "H:/e621_newest-webp-4Mpixel/meta_cap_dd.json"

2024-12-08 15:17:51 INFO     found 4441660 images.                                      merge_dd_tags_to_metadata.py:23                    
                    INFO     new metadata will be created /                             merge_dd_tags_to_metadata.py:33
新しいメタデータファイルが作成されます
5%|███▍                                                                 | 223765/4441660 [21:54<6:55:24, 169.22it/s]
100%|████████████████████████████████████████████████████████████████████| 4441660/4441660 [7:03:24<00:00, 174.84it/s]
2024-12-08 22:21:15 INFO     writing metadata: H:/e621_newest-webp-4Mpixel/meta_cap_dd.json     merge_dd_tags_to_metadata.py:53
2024-12-08 22:21:52 INFO     done!                                                      merge_dd_tags_to_metadata.py:5
```

```log
> python ./finetune/merge_dd_tags_to_metadata.py "H:/danbooru2024-webp-4Mpixel/khoyas_finetune" "H:/danbooru2024-webp-4Mpixel/meta_cap_dd.json"

2024-12-08 15:20:32 INFO     found 8005010 images.                                      merge_dd_tags_to_metadata.py:23
                    INFO     new metadata will be created /                             merge_dd_tags_to_metadata.py:33
新しいメタデータファイルが作成されます
2%|█▋                                                                  | 192542/8005010 [19:13<13:42:23, 158.33it/s]
100%|███████████████████████████████████████████████████████████████████| 8005010/8005010 [13:05:21<00:00, 169.88it/s]
2024-12-09 04:25:53 INFO     writing metadata: H:/danbooru2024-webp-4Mpixel/meta_cap_dd.json    merge_dd_tags_to_metadata.py:53
2024-12-09 04:27:01 INFO     done!                                                      merge_dd_tags_to_metadata.py:56
```

- To "prepare ARB latents", **it reuires a SDXL or VAE model to run.** 

- Noticed by community members, this feature has been abondened for a while, and [has no support since FLUX.1](https://github.com/kohya-ss/sd-scripts/issues/1542), and the reddit post was using SD1.5 which leaves SDXL in great unknown.

- I prefer [madebyollin/sdxl-vae-fp16-fix](https://huggingface.co/madebyollin/sdxl-vae-fp16-fix) if this script is safe to use. `batch_size` is somewhat optimal in 4 even it doesn't use many VRAM. It is tied with IOPS with the disk.

```log
> python ./finetune/prepare_buckets_latents.py "H:/just_astolfo/khoyas_finetune" "H:/just_astolfo/meta_cap_dd.json" "H:/just_astolfo/meta_lat.json" "E:/NOVELAI/stable-diffusion-webui/stable-diffusion-webui/models/VAE/sdxl-vae-fp16-fix.vae.safetensors" --batch_size 4 --max_resolution 1024,1024 --mixed_precision fp16

get_preferred_device() -> cuda
2024-12-08 15:51:42 INFO     found 6224 images. prepare_buckets_latents.py:70                    
                    INFO     loading existing metadata: H:/just_astolfo/meta_cap_dd.json    prepare_buckets_latents.py:73                    
                    INFO     load VAE: E:/NOVELAI/stable-diffusion-webui/stable-diffusion-webui/models/VAE/sdxl-vae-fp16-fix.vae.afetensors                   model_util.py:1268
100%|████████████████████████████████████| 6224/6224 [22:05<00:00,  4.70it/s] 
2024-12-08 16:14:22 INFO     bucket 0 (256, 1024): 16                      prepare_buckets_latents.py:194                    
                    INFO     bucket 1 (320, 1024): 13                      prepare_buckets_latents.py:194                    
                    INFO     bucket 2 (384, 1024): 23                      prepare_buckets_latents.py:194                    
                    INFO     bucket 3 (448, 1024): 29                      prepare_buckets_latents.py:194                    
                    INFO     bucket 4 (512, 1024): 71                      prepare_buckets_latents.py:194                    
                    INFO     bucket 5 (576, 1024): 204                     prepare_buckets_latents.py:194                    
                    INFO     bucket 6 (640, 1024): 479                     prepare_buckets_latents.py:194                    
                    INFO     bucket 7 (704, 1024): 2279                    prepare_buckets_latents.py:194                    
                    INFO     bucket 8 (768, 1024): 746                     prepare_buckets_latents.py:194                    
                    INFO     bucket 9 (832, 1024): 371                     prepare_buckets_latents.py:194                    
                    INFO     bucket 10 (896, 1024): 230                    prepare_buckets_latents.py:194                    
                    INFO     bucket 11 (960, 1024): 177                    prepare_buckets_latents.py:194                    
                    INFO     bucket 12 (1024, 256): 5                      prepare_buckets_latents.py:194                    
                    INFO     bucket 13 (1024, 320): 9                      prepare_buckets_latents.py:194                    
                    INFO     bucket 14 (1024, 384): 4                      prepare_buckets_latents.py:194                    
                    INFO     bucket 15 (1024, 448): 11                     prepare_buckets_latents.py:194                    
                    INFO     bucket 16 (1024, 512): 29                     prepare_buckets_latents.py:194                    
                    INFO     bucket 17 (1024, 576): 89                     prepare_buckets_latents.py:194                    
                    INFO     bucket 18 (1024, 640): 139                    prepare_buckets_latents.py:194                    
                    INFO     bucket 19 (1024, 704): 418                    prepare_buckets_latents.py:194                    
                    INFO     bucket 20 (1024, 768): 203                    prepare_buckets_latents.py:194                    
                    INFO     bucket 21 (1024, 832): 156                    prepare_buckets_latents.py:194                    
                    INFO     bucket 22 (1024, 896): 124                    prepare_buckets_latents.py:194                    
                    INFO     bucket 23 (1024, 960): 114                    prepare_buckets_latents.py:194                    
                    INFO     bucket 24 (1024, 1024): 285                   prepare_buckets_latents.py:194                    
                    INFO     mean ar error: 0.023306217513876078           prepare_buckets_latents.py:196                    
                    INFO     writing metadata: H:/just_astolfo/meta_lat.json                              prepare_buckets_latents.py:199                    
                    INFO     done!                                         prepare_buckets_latents.py:202

```

- Then it is the finetune stage. `fine_tune.py` is for SD1.5. SDXL use `train_sdxl.py` instead. I use my own [6DammK9/AstolfoMix-XL](https://huggingface.co/6DammK9/AstolfoMix-XL/blob/main/x215c-AstolfoMix-24101101-6e545a3.safetensors) to train. *I want to see if finetuning (pretrain?) on merged model works.*
- This is written for 4x RTX3090 24GB with full scale finetune (may OOM). I prefer the parameters from [cagliostrolab/animagine-xl-3.1](https://huggingface.co/cagliostrolab/animagine-xl-3.1#hyperparameters).
- `4e-7` is official SDXL learning rate. 
- `--enable_bucket` will be enabled in auto if `*.npz` and `meta_lat.json` are present.
- Optimizer will be defaulted as `AdamW` without 8bit. `--use_8bit_adam` is not used.
- `--shuffle_caption` is also not used. I think making multiple caption will be out of my reach.
- *Ctrl-C, right click, "Paste as one line".*
- `--train_text_encoder` is required if the CLIP should be finetuned. Otherwise it will be UNET only. 
- Both `--cache_latents` and `--cache_text_encoder_outputs` are added to brutally reduce the memory usage. However it takes time to initiate the process.
- **8 bit optimizer is required.** `--train_text_encoder` just increase the VRAM usage from 21GB to 22GB, which is still under the limit.

```sh
accelerate launch --num_cpu_threads_per_process 8 sdxl_train.py
    --pretrained_model_name_or_path="F:/NOVELAI/astolfo_mix/sdxl/cmp/x215c-AstolfoMix-24101101-6e545a3.safetensors"
    --in_json "H:/just_astolfo/meta_lat.json"
    --train_data_dir="H:/just_astolfo/khoyas_finetune"
    --output_dir="F:/NOVELAI/astolfo_xl/just_astolfo/finetune_job"
    --save_model_as=safetensors
    --caption_extension=".txt"
    --use_8bit_adam
    --train_batch_size=1 --learning_rate=4e-7 --max_train_steps=10000 
    --xformers --diffusers_xformers --gradient_checkpointing
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16
    --enable_bucket --cache_latents
    --save_every_n_epochs=1
```

- **It runs.** And it runed for ~~2 EPs~~ 10k steps (10k images) for around 3.5 hours. See `finetune_sdxl.log` for full log.

```log
steps: 100%|████████████████████████████████████████████| 10000/10000 [3:17:44<00:00,  1.19s/it, avr_loss=0.109]
```

- I have made some preview via **A1111** (not the kohyas GUI or any script!), there is some changes, but definitely not hitting the "target".

- The real multi-gpu set up can be found in [this issue](https://github.com/kohya-ss/sd-scripts/issues/812) and [this issue](https://github.com/bmaltais/kohya_ss/issues/1915).

- `set USE_LIBUV=0` is required for Windows. If the CLI is not effective, just set via system settings.

- Added the "GUI" from [this PR](https://github.com/kohya-ss/sd-scripts/pull/428). 

- Reminder: Inject `init_method="env://?use_libuv=False"` in `InitProcessGroupKwargs`!

```sh
SET USE_LIBUV=0 && accelerate launch 
    sdxl_train.py                                                                                                               
    --pretrained_model_name_or_path="F:/NOVELAI/astolfo_mix/sdxl/cmp/x215c-AstolfoMix-24101101-6e545a3.safetensors"             
    --in_json "H:/just_astolfo/meta_lat.json"                                                                                   
    --train_data_dir="H:/just_astolfo/khoyas_finetune"                                                                          
    --output_dir="F:/NOVELAI/astolfo_xl/just_astolfo/model_out"                                                                 
    --log_with=tensorboard                                                                                                      
    --logging_dir="F:/NOVELAI/astolfo_xl/just_astolfo/tensorboard"                                                              
    --log_prefix=just_astolfo_24120801_                                                                                         
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                                             
    --train_batch_size=1 --learning_rate=1e-5 --max_train_epochs=6                                                              
    --train_text_encoder                                                                                                        
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                             
    --save_every_n_epochs=1                                                                                                     
```

` master_addr is only used for static rdzv_backend and when rdzv_endpoint is not specified.`