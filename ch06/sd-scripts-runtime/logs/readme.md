# Model Descriptions #

- See `sd-scripts-runtime\logs\train` for complete file.
- The `train/*.sh` may not represent the actual command. This list is referring the model output.

## AstolfoXL: 2412 to 2505 ##

- *Maybe it would be better to have some session?*

### 2412: Beginning of finetuning ###

Unless specified: SDXL, 215c base, AdamW8bit, 6k dataset, 10EP, BS1. Learning rate is `unet + te (te1 = te2)`. *Single GPU, full UNET, tag only.*

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

Unless specified: SDXL, 215c base, AdamW8bit, 6k dataset, 10EP, 4GPU, BS1. Learning rate is `unet + te (te1 = te2)`. *"Dual Tag (concat, a1111 token trick)"* has been applied.

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

**2503a/b/c are interleaved in timeline.**

*More focus on just get multi GPU training works in full scale (more mod in hardware + trainer code).*

Unless specified: SDXL, 255c base, AdamW8bit, 6k dataset, 10EP, Dual Tag (concat, a1111 token trick), 4GPU, BS1, TTE on + 71% UNET + GA 4 step, 1.5e-6 + 1.2e-5.

- `model_out_25030301`: 255b base, ramdisk on
- `model_out_25030401`: ramdisk on, numa process 0
- `model_out_25030402`: ramdisk on, numa process 1
- `model_out_25030403`: ramdisk on, Single GPU. Speed reference.
- `model_out_25030801`: ramdisk on, 68% UNET, Adjusted for new trainer code / OS / hardware config.

### 2503b: Exploring optimizer ###

Unless specified: SDXL, 255c base, 6k dataset, 10EP, Dual Tag (concat, a1111 token trick), 4GPU, BS1, TTE on + GA 4 step, 1e-6 + 1e-5.
For secondary parameters (adamW related, default in some libraries): `weight_decay=1e-2, betas=(0.9, 0.999, 0.9999)`

- More options (e.g. AdamW4bit, CAME, C-Lion etc.) are commented out due to ~~my laziness~~ they crash / OOM / hang on start.

- Some LR are 10x lower (1e-7 + 1e-6) because of algorithm recommendation. However the speed ratio overrided the consideration.

- `model_out_25031501`: Lion. ~~Was testing CAME and C-Lion.~~
- `model_out_25031502`: AdaFactor, relative step.
- `model_out_25031503`: AdaFactor, overrided schedule.
- `model_out_25031504`: Lion 8bit.
- `model_out_25031505`: AdamW8bit. ~~Was testing AdamW4bit.~~
- `model_out_25033102`: AdamW8bit. Sanity check because of OS / Hardware update. ~~And then testesd for GA 16 steps.~~

### 2503c: Production run ###

Unless specified: SDXL, 255c base, AdamW8bit, 12.4M dataset, 1EP, Dual Tag (concat, a1111 token trick), 4GPU, BS1, TTE on + 71% UNET + GA 4 step, 1.5e-6 + 1.2e-5.

Total steps = 12.4M / (4GPU * BS1 * GA 4 step) = 778k steps.

- `model_out_25030802`: steps 0-10k out of 778k
- `model_out_25031101`: steps 10-40k out of 778k
- `model_out_25031401`: steps 40-50k out of 778k
- `model_out_25031402`: steps 50-60k out of 778k
- `model_out_25031601`: steps 60-70k out of 778k
- `model_out_25031701`: steps 70-100k out of 778k
- `model_out_25032201`: steps 100-170k out of 778k
- `model_out_25032901`: steps 170-190k out of 778k
- `model_out_25033101`: steps 190-210k out of 778k
- `model_out_25040601`: steps 210-220k out of 778k
- `model_out_25040602`: steps 220-240k out of 778k
- `model_out_25040901`: steps 240-320k out of 778k
- `model_out_25041301`: steps 320-**1EP** (778k)

## AstolfoVpredXL: 2511 to 2602 ##

### 2511a: Cracking the way how vpred works ###

Unless specified: SDXL, AK-NIL-1.2 base, AdamW8bit, 6k dataset, 10EP, Dual Tag (concat, a1111 token trick), 4GPU, BS1, GA 4 step. VPred mode, zstnr, min gamma 5.

Quick reference: AK = eps model, AC = vpred model. Target is turn eps model to vpred model. eps model with vpred runtime = blur image (no content).

Merge as "weighted sum", 1.0 = full trained weight, 0.0 = base model weight.

- `model_out_25111001`: TTE on + 71% UNET, 1.5e-6 + 1.2e-5. Failure with blur image.
- `model_out_25111002`: TTE on + 71% UNET, 1.5e-6 + 1.2e-5. **eps mode.** Success.
- `model_out_25111201`: TTE off + 100% UNET, 1.5e-6. min gamma off. Failure with blur image.
- `model_out_25111202`: **AC-NoobAI-1.0.** TTE off + 100% UNET, 1.5e-6. min gamma off. Success.
- `model_out_25111301`: **AC-NIL-0.1.**. TTE on + 71% UNET, 1.5e-6 + 1.2e-5. Sucess after merge (0.55).
- Honorable mention: Merge "AC-NoobAI-1.0" with "AK-NIL-1.2", success only when AC = 0.9.
- `model_out_25111501`: **AC-NIL-0.1.**. TTE on + 71% UNET, **1.0e-5 + 1.0e-5.** Kinda works.
- `model_out_25111601`: TTE off, **1.0e-5.** Kinda works.

### 2511b: Full dataset goes south ###

Unless specified: SDXL, AK-NIL-1.2 base, AdamW8bit, 12.4M dataset, 1EP, Dual Tag (concat, a1111 token trick), 4GPU, BS1, GA 4 step. VPred mode, zstnr, min gamma 5. 1.5e-6 + 1.2e-5.

Quick reference: AK = eps model, AC = vpred model. Target is turn eps model to vpred model. eps model with vpred runtime = blur image (no content).

Merge as "weighted sum", 1.0 = full trained weight, 0.0 = base model weight.

- `model_out_25111701`: Failed. Stopped after 55k steps.
- `model_out_25112101`: **AC-NIL-0.11.** (unreleased, the `25111701h-05-10k-75`). Got `nan` after 14k steps.
- `model_out_25112201`: **Return to eps mode.** steps 0-**1EP** (778k). **Works after merge.**

### 2601: Try again ###

Unless specified: SDXL, AK-Evo 2EP base, AdamW8bit, 6k dataset, Dual Tag (concat, a1111 token trick), 4GPU, BS1, GA 4 step. VPred mode, zstnr, min gamma 5. 1.0e-5, TTE off.

- `model_out_26011001`: **2EP base.** 10EP. Failed. 
- `model_out_26011101`: 8EP. Has hope after merge (0.85).
- `model_out_26011102`: 8+49EP. Has hope after merge (0.82).
- `model_out_26011501`: **Straight to 2.5EP VPred, 12.4M dataset**. "0 uncond" needs merge 0.82, "null uncond" works out of box.

### 2602: Go RF ###

Unless specified: SDXL, AstolfoVL 2.5EP base, AdamW8bit, 12.4M dataset, Dual Tag (concat, a1111 token trick), 4GPU, BS1, GA 4 step. Flow Matching / RF mode, logit-normal(0,1), timestep shift 3. LR 1.0e-5, TTE off.

- `model_out_26022301`: **6k dataset 10EP, 1GPU**. Validation run in developement machine. Success.
