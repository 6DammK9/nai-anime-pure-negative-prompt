# Model Descriptions #

- See `sd-scripts-runtime\logs\train` for complete file.
- The `train/*.sh` may not represent the actual command. This list is referring the model output.

## Placeholder session ##

- *Maybe it would be better to have some session?*

### 2412: Beginning of finetuning ###

Unless specified: SDXL, 215c base, AdamW8bit, 6k dataset, BS1. Learning rate is `unet + te (te1 = te2)`. *Single GPU, full UNET, tag only.*

- `model_out_24120801`: 20 dataset, very first run with TTE on, 1e-5 + 1e-5
- `model_out_24121001`: TTE on, 1e-5 + 1e-5
- `model_out_24121401`: TTE off, 1e-5
- `model_out_24121901`: TTE only, 1e-5
- `model_out_24121902`: 20 dataset, TTE only, 1e-5
- `model_out_24122001`: SD2, 21b base, TTE on, 1e-5 + 1e-5
- `model_out_24122002`: 20 dataset, TTE only, 1e-5 + 1e-5
- `model_out_24122101`: SD2, 21b base, TTE off, 1e-5 + 1e-5

### 2502: Exploring multi gpu and lots of tricks ###

*Different league in engineering: Customizing hardware + trainer code etc.*

Unless specified: SDXL, 215c base, AdamW8bit, 6k dataset, BS1. Learning rate is `unet + te (te1 = te2)`. *"Dual Tag (concat, a1111 token trick)"* has been applied.

- `model_out_25012301`: Tag only. TTE only + 100% UNET, test for Linux multigpu, 5e-6 + 3e-6
- `model_out_25012801`: Tag only. TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022101`: Dual Tag (pick caption or tags), TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022102`: TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022103`: TTE on + 63% UNET, 1e-6 + 1e-5
- `model_out_25022301`: TTE on + 100% UNET + GA 4 step, 2e-6 + 2e-5. Deepspeed Zero Stage 2 + Pytorch Dynamo + `mem_eff_attn`
- `model_out_25022401`: TTE on + 71% UNET + GA 4 step, 4e-7 + 4e-6
- `model_out_25022501`: TTE on + 71% UNET + GA 4 step, 1e-6 + 1e-5
- `model_out_25022502`: TTE on + 71% UNET + GA 4 step, 2e-6 + 8e-6
- `model_out_25022601`: TTE on + 71% UNET + GA 4 step, ramdisk on, 1.5e-6 + 1.2e-5

### 2503a: Exploring base model ###

*More focus on just get multi GPU training works in full scale (more mod in hardware + trainer code).*

Unless specified: SDXL, 255c base, AdamW8bit, 6k dataset, Dual Tag (concat, a1111 token trick), BS1, TTE on + 71% UNET + GA 4 step, 1.5e-6 + 1.2e-5.

- `model_out_25030301`: 255b base, ramdisk on
- `model_out_25030401`: ramdisk on, numa process 0
- `model_out_25030402`: ramdisk on, numa process 1
- `model_out_25030403`: ramdisk on, Single GPU. Speed reference.
- `model_out_25030801`: ramdisk on, 68% UNET, Adjusted for new trainer code / OS / hardware config.
- `model_out_25030802`: 12.4M dataset, steps 0-10k out of 778k
- `model_out_25031101`: 12.4M dataset, steps 10-40k out of 778k
- `model_out_25031401`: 12.4M dataset, steps 40-50k out of 778k
- `model_out_25031402`: 12.4M dataset, steps 50-60k out of 778k

### 2503a: Exploring optimizer ###

Unless specified: SDXL, 255c base, 12.4M dataset, Dual Tag (concat, a1111 token trick), BS1, TTE on + GA 4 step, 1e-6 + 1e-5.
For secondary parameters (adamW related, default in some libraries): `weight_decay=1e-2, betas=(0.9, 0.999, 0.9999)`

- `model_out_25031501`: CAME. 6k dataset.
