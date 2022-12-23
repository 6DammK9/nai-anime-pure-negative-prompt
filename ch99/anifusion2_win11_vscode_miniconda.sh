#!/bin/bash

# Win11 + VSCode + miniconda3 version for https://gist.github.com/enryu43/fccaa7f165ffcb214780d203c565761f

conda create -n anifusion2-env -c conda-forge scikit-learn python=3.10
conda activate anifusion2-env
# Win11 DLL fix: https://github.com/conda/conda/issues/11795#issuecomment-1340010125
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu116
# Doesn't work
# conda install -c conda-forge pytorch-gpu
# conda install -c conda-forge torchvision
# Should return true
python -c "import torch; print(torch.cuda.is_available())"

# clone web ui and go into its directory
git clone https://github.com/enryu43/anifusion2-sd-webui.git
cd anifusion2-sd-webui

mkdir repositories
git clone https://github.com/enryu43/anifusion-stable-diffusion2.git repositories/stable-diffusion
git clone https://github.com/CompVis/taming-transformers.git repositories/taming-transformers

# install requirements of Stable Diffusion
pip install transformers==4.19.2 diffusers invisible-watermark --prefer-binary

# install k-diffusion
pip install git+https://github.com/crowsonkb/k-diffusion.git --prefer-binary

# install requirements of web ui
pip install -r requirements.txt  --prefer-binary
# It is not really needed, but is imported in SD code.
pip install open-clip-torch invisible-watermark

# update numpy to ~~latest version~~ 1.23.5 (numba 0.56.4 requires numpy<1.24,>=1.18)
pip install -U numpy==1.23.5  --prefer-binary

# WGET for Windows: https://eternallybored.org/misc/wget/
# https://huggingface.co/enryu43/anifusion_sd_unet/resolve/main/original_ckpt.bin -O model.ckpt
# Alternatively, for 768x768 model:
wget https://huggingface.co/enryu43/anifusion_sd_unet_768/resolve/main/original_ckpt.bin -O model.ckpt

# Finally, start the UI
python webui.py --listen