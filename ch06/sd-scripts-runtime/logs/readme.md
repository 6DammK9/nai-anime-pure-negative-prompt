# Model Descriptions #

- See `sd-scripts-runtime\logs\train` for complete file.
- The `train/*.sh` may not represent the actual command. This list is referring the model output.

- `model_out_24120801`: SDXL, 20 dataset, very first run with TTE on, 1e-5 + 1e-5
- `model_out_24121001`: SDXL, 6k dataset, TTE on, 1e-5 + 1e-5
- `model_out_24121401`: SDXL, 6k dataset, TTE off, 1e-5
- `model_out_24121901`: SDXL, 6k dataset, TTE only, 1e-5
- `model_out_24121902`: SDXL, 20 dataset, TTE only, 1e-5
- `model_out_24122001`: SD2, 6k dataset, TTE on, 1e-5 + 1e-5
- `model_out_24122002`: SDXL, 20 dataset, TTE only, 1e-5 + 1e-5
- `model_out_24122101`: SD2, 6k dataset, TTE off, 1e-5 + 1e-5
- `model_out_25012301`: SDXL, 6k dataset, TTE only, test for Linux multigpu, 5e-6 + 3e-6
- `model_out_25012801`: SDXL, 6k dataset, TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022101`: SDXL, 6k dataset, Dual Tag (pick caption or tags), TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022102`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022103`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 63% UNET, 1e-6 + 1e-5
- `model_out_25022301`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 100% UNET + GA 4 step, 2e-6 + 2e-5
- `model_out_25022401`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 71% UNET + GA 4 step, 4e-7 + 4e-6
- `model_out_25022501`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 71% UNET + GA 4 step, 1e-6 + 1e-5
- `model_out_25022502`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 71% UNET + GA 4 step, 2e-6 + 8e-6
- `model_out_25022601`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 71% UNET + GA 4 step, ramdisk, 1.5e-6 + 1.2e-5
