# DammK ML / AI CMD pack V3 #

- V1 and V2 are located in [ml-ai-init-cmds](https://github.com/6DammK9/ml-ai-init-cmds).

## From stratch. Tested on 240316 ##

- Must activate environment first!
- ~~Python 3.11 still too new~~ Using 3.12 right now
- May need linux subsystem (WSL2) which may collides with Windows environment
- Do not use install CMDs in jupyter environment! You will crash your computer!
- Only use pip for last resort (e.g. `torchvision`)
- Be familiar with **minor** software version difference (should be fine for educational use)

## Computation environment ##

- My current ~~PC~~ workstation: [Supermicro X12DPi-N6-AS081](https://www.v2ex.com/t/907306) *(1 of 1?)*, Win 10 22H2, no linux subsystem, 32c64t Xeon Platinum 8358 ES ["QV2E"](https://www.ebay.com/itm/125887688097) x2, 512GB DDR4 *([32GB 2400 ECC](https://harddiskdirect.com/hp24d4r7d4mam-32-kingston-32gb-pc4-19200-ddr4-2400mhz-ecc-registered-cl17-rdimm-1-2v-dual-rank-memory-modules.html) x16, I'm poor)*, RTX 2080 Ti **[22G](https://www.ebay.com/itm/374465596451)** x2, [DC P4510 4TB](https://www.solidigm.com/products/data-center/d7/p4510.html#form=U.2%2015mm&cap=4%20TB) x2, [Micron 1300 512GB](https://www.storagereview.com/news/micron-1300-ssd-announced), WD Black 2TB SATA HDD ["WD2003FYYS"](https://www.disctech.com/Western-Digital-RE4-WD2003FYYS-2TB-Enterprise-SATA-Hard-Disk-Drives)

## Video / IG links ##

- *Coming soon* (Will upload to builds gg)

## Here's the CMDs ##

```bash
#!/bin/bash

# I think months later, it should works?
conda create -n novelai-env -c conda-forge scikit-learn python=3.12
conda activate novelai-env

# For my lovely notebooks
conda install -c conda-forge jupyterlab
conda install -c conda-forge jupyterlab_widgets
conda install -c conda-forge ipywidgets

# Start jupyter
jupyter lab

# Prefer conda-forge with auto version (older version is not preferred)

# Check CUDA Version via nvidia-smi, currently only 
# torchvision-0.17.1+cu121-cp312-cp312-win_amd64.whl
# Win11 DLL fix: https://github.com/conda/conda/issues/11795#issuecomment-1340010125
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121
# Doesn't work
# conda install -c conda-forge pytorch-gpu
# conda install -c conda-forge torchvision
# Should return true
python -c "import torch; print(torch.cuda.is_available())"

# Should be fine with almost no risk
conda install -c conda-forge pandas
conda install -c conda-forge matplotlib
conda install -c conda-forge scikit-image
conda install -c conda-forge scipy
conda install -c conda-forge networkx
conda install -c conda-forge tqdm
conda install -c conda-forge opencv

# Not related (used for AI art research)
pip install safetensors
```
