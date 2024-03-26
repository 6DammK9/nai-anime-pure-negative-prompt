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

- My current ~~PC~~ workstation: [Supermicro X12DPi-N6-AS081](https://www.v2ex.com/t/907306) *(1 of 1? [3x CPU 8pin](https://www.chinafix.com/thread-1331197-1-1.html))*, Win 10 22H2, no linux subsystem, 32c64t Xeon Platinum 8358 ES ["QV2E"](https://www.ebay.com/itm/125887688097) x2, 512GB DDR4 *([32GB 2400 ECC](https://harddiskdirect.com/hp24d4r7d4mam-32-kingston-32gb-pc4-19200-ddr4-2400mhz-ecc-registered-cl17-rdimm-1-2v-dual-rank-memory-modules.html) x16, I'm poor)*, RTX 2080 Ti **[22G](https://www.ebay.com/itm/374465596451)** x2, [DC P4510 4TB](https://www.solidigm.com/products/data-center/d7/p4510.html#form=U.2%2015mm&cap=4%20TB) x2, [Micron 1300 512GB](https://www.storagereview.com/news/micron-1300-ssd-announced), WD Black 2TB SATA HDD ["WD2003FYYS"](https://www.disctech.com/Western-Digital-RE4-WD2003FYYS-2TB-Enterprise-SATA-Hard-Disk-Drives)

## Video / IG links ##

- *Coming soon* (Will upload to builds gg)

## Here's the CMDs ##

```bash
#!/bin/bash

# A1111 requires strictly 3.10. Tested in 3.10.6. However it is in venv so I ignore it haha.
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
conda install -c conda-forge safetensors
conda install -c conda-forge fuzzywuzzy
conda install -c conda-forge python-levenshtein
conda install -c conda-forge pyyaml
```

## Python 3.12 IS PROVEN NOT WORKING in A1111 1.8.0

- Install [Python 3.10.11](https://www.python.org/downloads/release/python-31011/) instead.

- If you don't want to reinstall Miniconda, edit `webui-user.bat`. `venv` will be installed based from the assigned `python`:

```bash
set PYTHON=C:\Users\User\AppData\Local\Programs\Python\Python310\python.exe
```

<details>
    <summary>Open if you're interested. Welcome to the dependency hell in python.</summary>

- As on 240316, it has trouble to install from fresh with python 3.12. Search and replace:

```py
torch_command = os.environ.get('TORCH_COMMAND', f"pip install torch==2.2.1 torchvision==0.17.1 --extra-index-url {torch_index_url}")
```

- Also it can't install `xformers` (under investigation)

- Direct running `webui-user.bat` will crash with strange cpp stacktrace. `pip install -r requirements.txt` will install a lot more libraries but crash when installing `transformers`. It is caused by specifying unsupported `transformers==4.30.2`. `pip install transformers` instead (will lead to `4.39.1`)

- Notice the changes in `requirements.txt`:

```txt
pytorch_lightning<2.0.0
transformers>=4.30.2
spandrel
```

```bash
# A1111 workarounds
pip install transformers
pip install -r requirements.txt

webui-user.bat
```

- Then edit `launch_utils.py` to bypass checking on original `requirements_versions.txt`:

```py
#L313
if packaging.version.parse(version_required) != packaging.version.parse(version_installed):
    print("Version mismatch", package, version_required, version_installed)
    continue
    #return False

#L425
if not requirements_met(requirements_file):
    print("Exit instead of pip install.")
    exit()
    run_pip(f"install -r \"{requirements_file}\"", "requirements")
    startup_timer.record("install requirements")
```

- Then increase logging in `webui-user.bat`:

```bash
set COMMANDLINE_ARGS=--loglevel=DEBUG --log-startup --no-half-vae --api --port=7860 --device-id=0
```

```log
  checks: done in 0.095s
  git version info: done in 0.095s
Python 3.12.1 | packaged by conda-forge | (main, Dec 23 2023, 07:53:56) [MSC v.1937 64 bit (AMD64)]
Version: v1.8.0
Commit hash: bef51aed032c0aaa5cfd80445bc4cf0d85b408b5
  torch GPU test: done in 3.670s
  clone repositores: done in 0.266s
Version mismatch GitPython 3.1.32 3.1.42
Version mismatch Pillow 9.5.0 10.2.0
Version mismatch accelerate 0.21.0 0.28.0
Version mismatch blendmodes 2022 2024.1.1
Version mismatch einops 0.4.1 0.7.0
Version mismatch fastapi 0.94.0 0.110.0
Version mismatch httpcore 0.15 1.0.4
Version mismatch jsonmerge 1.8.0 1.9.2
Version mismatch kornia 0.6.7 0.7.2
Version mismatch lark 1.1.2 1.1.9
Version mismatch numpy 1.26.2 1.26.4
Version mismatch omegaconf 2.2.3 2.3.0
Version mismatch open-clip-torch 2.20.0 2.7.0
Version mismatch psutil 5.9.5 5.9.8
Version mismatch pytorch_lightning 1.9.4 2.2.1
Version mismatch scikit-image 0.21.0 0.22.0
Version mismatch spandrel 0.1.6 0.3.1
Version mismatch transformers 4.30.2 4.39.1
Version mismatch httpx 0.24.1 0.27.0
    run extensions installers:
2024-03-27 00:35:52 DEBUG [root] Installing auto-MBW-rt
```

- Now it "stucks" in installing extensions. Installation still progress, but you can go to each directory and install the requirements via `pip install -r requirements.txt` again, if it fails after a long time.

- Then the worst part happens: `sd-webui-controlnet` require `mediapipe` which supports up to Python 3.11 only. Somehow it will ignore and continue:

```log
2024-03-27 00:51:24 DEBUG [root] Installing sd-webui-controlnet
Installing sd-webui-controlnet requirement: fvcore
Installing sd-webui-controlnet requirement: mediapipe
Couldn't install sd-webui-controlnet requirement: mediapipe.
Command: "E:\NOVELAI\stable-diffusion-webui\stable-diffusion-webui\venv\Scripts\python.exe" -m pip install mediapipe --prefer-binary
Error code: 1
stderr: ERROR: Could not find a version that satisfies the requirement mediapipe (from versions: none)
ERROR: No matching distribution found for mediapipe

Warning: Failed to install mediapipe, some preprocessors may not work.
Installing sd-webui-controlnet requirement: onnxruntime
Installing sd-webui-controlnet requirement: svglib
ControlNet init warning: Unable to install insightface automatically. Please try run `pip install insightface` manually.
Installing sd-webui-controlnet requirement: handrefinerportable
Couldn't install sd-webui-controlnet requirement: handrefinerportable.
Command: "E:\NOVELAI\stable-diffusion-webui\stable-diffusion-webui\venv\Scripts\python.exe" -m pip install https://github.com/huchenlei/HandRefinerPortable/releases/download/v1.0.0/handrefinerportable-2024.1.18.0-py2.py3-none-any.whl --prefer-binary
Error code: 1
stdout: Collecting handrefinerportable==2024.1.18.0
  Downloading https://github.com/huchenlei/HandRefinerPortable/releases/download/v1.0.0/handrefinerportable-2024.1.18.0-py2.py3-none-any.whl (13.1 MB)
     ---------------------------------------- 13.1/13.1 MB 8.3 MB/s eta 0:00:00
INFO: pip is looking at multiple versions of handrefinerportable to determine which version is compatible with other requirements. This could take a while.

stderr: ERROR: Could not find a version that satisfies the requirement mediapipe (from handrefinerportable) (from versions: none)
ERROR: No matching distribution found for mediapipe

Warning: Failed to install handrefinerportable. Some processors will not work.
Installing sd-webui-controlnet requirement: depth_anything
    sd-webui-controlnet: done in 76.922s
```

- Now finally it **throws tons of errors** about `__config__`, returning many `None` in so many `modules`, downloading so many default models, and finally crash in gradio:

```log
  File "E:\NOVELAI\stable-diffusion-webui\stable-diffusion-webui\venv\Lib\site-packages\gradio\blocks.py", line 286, in set_event_trigger
    "inputs": [block._id for block in inputs],
               ^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '_id'
```

</details>