# Setting up the dedicated linux environment for multi GPU training #

## 0. Why abondoning Windows? ##

- After the [gloo / libuv hack in the stack](https://github.com/kohya-ss/sd-scripts/pull/1686), the performance uplift is close to none. 10% with 4x cards, huge RAM usage (160GB+), huge VRAM usage (23GB+), make the IO latency too high to handle.

- Even WSL is feasible, and claimed working in kohyas, I think I can mitigate the risk by quick install with other SSDs. ~~The Windows SSD for latent preparation is from my hardware bench and it never withstand for 24 hours.~~ The OS is generally lighter and has less bloatware than windows ~~even Manjaro is considered not stable because of rolling update~~, *meanwhile the package manager is common,* so that I can try to use full blown Linux desktop instead of LAN remote CLI.

- The usage of that Linux OS is very precise: MultiGPU training on SDXL, meanwhile some diary ~~ch06~~, adhoc coding ~~should be minimal? Whole ch06 is to prepare everything for this, I don't even have git access in this machine!~~, web searching for help, and that's all. Even social app is not preferred ~~I can do it with my mobile~~. Meanwhile I do have some basic knowledge on CLI / OS / driver / firmware (BIOS), it is feasible for me to get familiar to an environment which is a ["cult"](https://www.reddit.com/r/archlinux/comments/1dzmkol/should_i_join_this_cult_and_finally_install_arch/?rdt=61591) for a "Desktop PC" (it is not entirely an AI rig!).

- I pick Manjaro is because of ["mwhd"](https://wiki.manjaro.org/index.php/Configure_Graphics_Cards), a dedicated hardware detection and driver management for the GPUS. ~~it is never plug and play in Linux!~~ The automation is enough for me to get the essential CUDA / CUDNN stuffs ready, like what I expected in Windows. *Ubuntu should have auto detection enabled... until there are unexpected events.*

- Talking about the Nvidia drivers, *never assume everything can be solved by your own*, I worked with a Jetson Nano (Maxwell), [updating python requries rebuilding the whole OS image, and limited in a particular Jetpack Version!](https://jetson-docs.com/libraries/python/l4t32.7.1/py3.10.11) Try to minimalmize any manual operation in this topic, even it outweights the risks I'm facing by using Arch Linux.

## 1. Getting familiar with the OS ##

- **It is an entire chapter before using python!**

### 1.1 Installing the OS ###

- *Don't rush and read next session first.*

- OS install media is straightforward. [I use rufus to burn the image to a USB drive. DD mode has been activated in auto.](https://wiki.manjaro.org/index.php/Burn_an_ISO_File) **8GB is enough, 32GB is overkill.**

- For the ISO image, I picked x86 with GNOME. There will be options to set the Desktop layout back to windows-ish layout. [As soon as in "Manjaro Hello".](https://forum.manjaro.org/t/manjaro-hello-always-launches/102373) 

- Better turn off "Fast Boot" and set "Boot with Legacy".

- The install process is as usual as other Linux: Boot as PE > Install OS > Navigate the options. If you have internet connection, I prefer [Libre Office](https://www.libreoffice.org/) ~~although I think I don't have to use this~~.

- It takes around 10GB for the barebone OS. *Probably 128GB SSD is fine until you install too many conda envionments and cached huggingface models.* For my case, it should be kohyas only, and preprocessing is even considered in windows ~~I need VSCode for code developement~~.

- **Remember to set the power setting and prevent hibernation!** I set them via GUI.

- My screen is blank between GRUB and the desktop appears. Be patient.

- *Terminal has tabs.*

- *Unless specified, I always use GUI "Add/Remove Software" (pamac), "(GNOME) Settings" and "System Monitor".*

### 1.2 Hardware discussion ###

- Remove all AI GPUs / disk drives etc. and leave only the basic hardwares running (a tiny GPU, a blank OS drive, LAN / WIFI module which is supported in UEFI, and USB install media) for the OS installation.

- For USB wifi, I'm using [USB-AC53 Nano](https://www.asus.com/hk-en/networking-iot-servers/adapters/all-series/usb-ac53-nano/). I bought a brunch more adapters and none of them works out of the box.

- I want a "board display" without using the GPUs. I am using [Displaylink DL-3500 "USB to HDMI" video card](https://www.synaptics.com/products/displaylink-graphics/integrated-chipsets/dl-3000) which requires manual driver installation. 

- The "not AI" "tiny" GPU is recommended to be a RTX Ampere card, which requires the exact same driver. I'm using RTX 3050. I can swap to 4x RTX 3090 after the envionemnt is settled.

#### 1.2.1 The Nvidia driver ####

- **You need the proprietary Nvidia driver for the CUDA support.**

```sh
user $ mhwd -l
# Confirm video-nvidia is present.
user $ sudo mhwd -i pci video-nvidia
# This is the auto install command (if the one above failed)
user $ sudo mhwd -a pci nonfree 0300
```

- View and set audio output accordingly.

- I use `nvtop` for hardware monitoring. ~~GPUZ but in ASCII.~~

- I use `nvidia-smi` (built in) to limit the GPU power. Quick math: $350W * 0.65 = 225W$

```sh
#to set a power limit of 140W use (-i 0 apples to only the 1st gpu)
sudo nvidia-smi -i 0 -pl 140
#to see what your card is using run this command
nvidia-smi -q -d power
#you can use anything between “Default Power Limit” and “Max Power Limit”
#nvidia-smi also has a -pm option to enable persist mode
```

- Refer to [the guide for linux](https://wiki.archlinux.org/title/NVIDIA/Tips_and_tricks), `nvidia-xconfig` is required for setting fan speeds.

```sh
sudo nvidia-xconfig --enable-all-gpus
sudo nvidia-xconfig --cool-bits=4
sudo nvidia-settings -a "[gpu:0]/GPUFanControlState=1" -a "[fan:0]/GPUTargetFanSpeed=60"
```

#### 1.2.2 The DisplayLink driver ####

- [The arch linux guide](https://wiki.archlinux.org/title/DisplayLink) is sufficient and effective, even I don't need the `*-git` package.

- **Never use this as boot display.** There is driver / OS bug preventing it appears as X11 display, even the services / driver are all booted and hooked. **Switch HDMI after you see the desktop with the GPU display.**

- **Enable [AUR](https://wiki.manjaro.org/index.php/Arch_User_Repository) manually.** "Three dots > Preferences > Third Party > Enable AUR support > confirm".

- Try your best to follow the guide. Soon you will get the details *by following the links*. It is different in windows. It is a kind of driver store / framework.

- View and set audio output accordingly.

- **The cursor may flashes a lot.** ~~Change to 1080p 60hz may help.~~ It is because the GPU are rendering the screen instead of the USB one. See session 1.6 for attempt to regain the primary display.


#### 1.2.3 AX200 pcie wifi module ####

- *No idea* why it doesn't work, even it is in motherboard and detected in `lspci` arleady. [This thread may help.](https://bbs.archlinux.org/viewtopic.php?id=290632) `dmesg` will show the `iwlwifi` errors.

### 1.3 (Optional) Browser / DRM Plugins for streaming ###

- *Skip this session if you don't need a few days to test system stability.* I usually open local TV live (streaming) while I'm away. The streams may need [Google Widevine DRM](https://developers.google.com/widevine/drm/overview).

- Linux use Firefox by default. [It requries enabling DRM plugin manually.](https://support.mozilla.org/en-US/kb/enable-drm). However the frontend scripts may favor to Chromium and the actual experience may be buggy in Firefox.

- ~~Try not to use Google Chrome and Microsoft Edge!~~ For [(Ungoogled) Chromium](https://github.com/ungoogled-software/ungoogled-chromium), it should be [enabled out of the box](https://superuser.com/questions/1824683/unable-to-play-drm-protected-content-on-ungoogled-chromium-even-after-installing). Reboot after installation to confirm.

- *I don't have any requirement on networking operation so please refer to your experience if you need it.* ~~VPN / Socks etc.~~

### 1.4 (Optional) IDE, kind of ###

- *I think you have a preferred IDE already. Refer to the (Arch) Linux install guide or alternatives.*

- However, I have a ugly option: [JupyterLab](https://jupyter.org/) is included in `pamac`. Meanwhile Python 3.12 has been included in OS image. *Avoid run Python Notebook, or run shell command inside, will be fine.* By default it is hooked to home directory.

- (With GUI) You can open JupyterLab in **any (user) directory** you want. The port will be incremented. ~~Keep it as IDE will be fine.~~

- Meanwhlie, I use [miniconda](https://docs.anaconda.com/miniconda/install) along with `venv`, even it may require may more disk space. By default conda environment is hooked in home directory.

```sh
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### 1.5 Installing the hardware ###

- GPUs is detected in auto. Use `nvtop` / `nvidia-smi` to view the progress. Still require to boot with display via GPU.

- The NTFS drives should be detected also, but not mounted instantly. You can either use GUI or command line (CLI only for fancy drive name e.g. "New Volume")

```sh
mkdir -p "/run/media/user/PM863a"
chmod 777 "/run/media/user/PM863a"
mount -t ntfs-3g /dev/sdb1 "/run/media/user/PM863a"

mkdir -p "/run/media/user/Intel P4510 3"
chmod 777 "/run/media/user/Intel P4510 3"
mount -t ntfs-3g /dev/nvme0n1p2 "/run/media/user/Intel P4510 3"
```

### 1.6 Saving GPU resources for heavy AI use ###

#### 1.6.1 Disable xorg extension to minimalize VRAM usage ####

- `nvtop` will view which process using the VRAM.

- Turns out [gtk4-ding](https://extensions.gnome.org/extension/5263/gtk4-desktop-icons-ng-ding/) is using 150M+ of VRAM. **Disable this extension will wipe out the desktop.** However the task bar persists.

```sh
gnome-extension disable gtk4-ding@smedius.gitlab.com
```

- Remaining `gnome-shell` / `xorg` will use around 200MB and I think that it is close to minimum for my current task. *If SDXL finetuning still requires 23.8GB of VRAM, I will just freeze some layers to compromise.*

- **All the remining sections are my try-hard findings.** Skip to Session 2 if not interested.

#### 1.6.2 (May work but I crashed) Disable xorg hardware acceleration ####

- This [nvidia 550.144.03 X config](https://download.nvidia.com/XFree86/Linux-x86_64/550.144.03/README/xconfigoptions.html), [xorg X11R7.0 docuement](https://www.x.org/releases/X11R7.0/doc/html/SiS2.html) propose another keyword, and supported in [this post](https://cloud.tencent.com/developer/article/2432782):

- This [post](https://unix.stackexchange.com/questions/408582/how-to-disable-hardware-acceleration-in-linux) propose other keyword, backed with [xorg X11R7.6 docuement](https://www.x.org/archive/X11R7.6/doc/man/man5/xorg.conf.5.xhtml):

- This [post](https://bbs.archlinux.org/viewtopic.php?id=256372) turns out the most cloest to my concern, but I found that my screen just works with the error messages:

```
Section "Device"
    Identifier     "Device1"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
    BoardName      "NVIDIA GeForce RTX 3090"
    BusID          "PCI:23:0:0"
    Option         "AllowEmptyInitialConfiguration" "true"
    Option         "Accel" "off"
    Option        "SidebandSocketPath" "/var/run/nvidia-xdriver"
    Option        "ConnectToAcpid" "0"
EndSection
```

- Turns out fixing directory `/var/run/nvidia-xdriver` will lead to "File or directory not found":

```sh
sudo mkdir -p /var/run/nvidia-xdriver
sudo chmod 777 /var/run/nvidia-xdriver
```

- The setting will be effective, however the driver somehow ignores the setting:

```log
[    56.604] (**) NVIDIA(G0): Option "ConnectToAcpid" "0"
[    56.604] (**) NVIDIA(G0): Option "AllowEmptyInitialConfiguration" "true"
[    56.604] (**) NVIDIA(G0): Option "SidebandSocketPath" "/var/run/nvidia-xdriver"
[    56.604] (**) NVIDIA(G0): Option "Accel" "off"
[    56.604] (**) NVIDIA(G0): Disabling 2D acceleration
...
[    56.636] (WW) NVIDIA: Failed to bind sideband socket to
[    56.636] (WW) NVIDIA:     '/var/run/nvidia-xdriver/nvidia-xdriver-e3193365' No such
[    56.636] (WW) NVIDIA:     file or directory
[    56.638] (II) NVIDIA: Reserving 24576.00 MB of virtual memory for indirect memory
[    56.638] (II) NVIDIA:     access.
...
[    56.642] (II) NVIDIA(0): ACPI: failed to connect to the ACPI event daemon; the daemon
[    56.642] (II) NVIDIA(0):     may not be running or the "AcpidSocketPath" X
[    56.642] (II) NVIDIA(0):     configuration option may not be set correctly.  When the
[    56.642] (II) NVIDIA(0):     ACPI event daemon is available, the NVIDIA X driver will
[    56.642] (II) NVIDIA(0):     try to use it to receive ACPI event notifications.  For
[    56.642] (II) NVIDIA(0):     details, please see the "ConnectToAcpid" and
[    56.642] (II) NVIDIA(0):     "AcpidSocketPath" X configuration options in Appendix B: X
[    56.643] (II) NVIDIA(0):     Config Options in the README.
```

- **It just screwed up in an unexpected way.** Turns out the driver / Xorg / OS stack just refused to communicate. The root cause may be the xorg is not running in sudo, but this thing is a part of Manjaro-GNOME-ArchLinux distro. I have no idea to further modifying it without wasting time on editing the system file in another OS (WSL2 with updated Linux Kernel).  

```log
[    56.732] (EE) NVIDIA(G0): Failed to allocate primary buffer: failed to set CPU access
[    56.732] (EE) NVIDIA(G0):     for surface.  Please see Chapter 8: Common Problems in the
[    56.732] (EE) NVIDIA(G0):     README for troubleshooting suggestions.
[    56.732] (EE) NVIDIA(G0):  *** Aborting ***
[    56.769] (EE)
Fatal server error:
[    56.769] (EE) AddScreen/ScreenInit failed for gpu driver 0 -1
[    56.769] (EE)
[    56.769] (EE)
[    56.769] (EE) Please also check the log file at "/home/user/.local/share/xorg/Xorg.0.log" for additional information.
[    56.769] (EE)
[    57.001] (EE) Server terminated with error (1). Closing log file.
```

- More over, remote desktop / Ubuntu server is not considered ~~I'll freeze layers instead! SDXL is good for single GPU under 23GB! OOM is just because of the overhead of multiGPU!~~

#### 1.6.2 If screwed up ####

- **This guide will be useful for no SSH and no TTY.**

- SSH: Just enable remote sharing and... hopefully your local network can reach port 22.

- TTY: `Ctrl + alt + F1` to `F6`. Always check the Numlock LED. My case is bad: Just no screen output.

- Live USB *sometimes* works. **Make sure you boot live USB without the host drive.** Plug it with USB adapter afterward.

- Windows with WSL2 also *sometimes* works. Checkout [Official guide](https://learn.microsoft.com/en-us/windows/wsl/wsl2-mount-disk).

```sh
# In Windows
wmic diskdrive list brief
wsl --mount \\.\PHYSICALDRIVE1 --bare
# In Linux
sudo mkdir /media/manjaro
sudo chmod 777 /media/manjaro
lsblk
sudo mount -t ext4 /dev/sdd1 /media/manjaro
sudo umount /dev/sdd1
# In Windows (after work)
wsl --unmount \\.\PHYSICALDRIVE1
```

- If it doesn't work, [update Linux kernel for the WSL2](https://learn.microsoft.com/en-us/community/content/wsl-user-msft-kernel-v6). [Check out this thread](https://unix.stackexchange.com/questions/315063/mount-wrong-fs-type-bad-option-bad-superblock) and [this github issue](https://github.com/linuxboot/heads/issues/1796):

```log
mount: wrong fs type, bad option, bad superblock on /dev/sdd1,
       missing codepage or helper program, or other error
```

- The "update Linux kernel" is a bit counter intuitive. The hint is located in `dmesg`:

```log
> sudo dmesg
[    4.015655] EXT4-fs (sdd1): couldn't couldn't mount RDWR because of unsupported optional features (10000)
```

- [Install a dedicated Linux distro](https://cloudbytes.dev/snippets/how-to-install-multiple-instances-of-ubuntu-in-wsl2) if you are feared about old Ubuntu with new Linux kernel. *Hint: bzimage is just a file, it won't hurt you.*

- Check xorg log `/home/user/.local/share/xorg/Xorg.0.log` and `/home/user/.local/share/xorg/Xorg.0.log` for more hints. 

- Alternatively (**I don't know the user group convention!**), [ext4fsd](https://github.com/bobranten/Ext4Fsd), the modified version of `ext2fsd` will **mount the Linux OS drive directly to Winodws Drive.** You can perform backup for important files.

#### 1.6.3 (Not working) Change Source / Sink provider ####

- Without any command, the boot GPU display is still using the sources:

```log
> $ xrandr --listproviders
Providers: number : 5
Provider 0: id: 0x1b7 cap: 0x1, Source Output crtcs: 4 outputs: 7 associated providers: 4 name:NVIDIA-0
Provider 1: id: 0x70e cap: 0x2, Sink Output crtcs: 1 outputs: 1 associated providers: 1 name:modesetting
Provider 2: id: 0x6c4 cap: 0x2, Sink Output crtcs: 4 outputs: 6 associated providers: 1 name:NVIDIA-G2
Provider 3: id: 0x35a cap: 0x2, Sink Output crtcs: 4 outputs: 7 associated providers: 1 name:NVIDIA-G0
Provider 4: id: 0x4fd cap: 0x2, Sink Output crtcs: 4 outputs: 7 associated providers: 1 name:NVIDIA-G1
```

- After getting stuck for a while, this command **fails** although it is listed in [the Arch Linux guide](https://wiki.archlinux.org/title/PRIME):

```sh
sudo xrandr --setprovideroffloadsink NVIDIA-0 modesetting
```

```log
X Error of failed request:  BadValue (integer parameter out of range for operation)
  Major opcode of failed request:  140 (RANDR)
  Minor opcode of failed request:  34 (RRSetProviderOffloadSink)
  Value in failed request:  0x1b7
  Serial number of failed request:  19
  Current serial number in output stream:  20
```

- Either [this](https://wiki.archlinux.org/title/NVIDIA_Optimus#Using_PRIME_render_offload) and [this](https://wiki.archlinux.org/title/NVIDIA#Automatic_configuration) and [this](https://bbs.archlinux.org/viewtopic.php?id=292421) doesn't help.

- Then [visiting the xorg.conf guide](https://man.archlinux.org/man/xorg.conf.d.5.en) will propose additional settings, **No effect either**:

```conf
#/etc/X11/xorg.conf.d/20-evdi.conf
Section "OutputClass"
	Identifier "DisplayLink"
	MatchDriver "evdi"
	Driver "modesetting"
    Option "AllowEmptyInitialConfiguration"
    Option "PrimaryGPU" "yes"
	Option "AccelMethod" "none"
EndSection
```

- Meanwhile bottom session of [the original guide](https://wiki.archlinux.org/title/DisplayLink) propose adding the device, **I cannot even reach to the desktop screen**:

```conf
#/etc/X11/xorg.conf
    Screen      4  "Screen4" RightOf "Screen3"
...
Section "Device"
    Identifier    "usbdev"
    Driver        "modesetting"
    Option        "kmsdev" "/dev/dri/card5"
EndSection
...
Section "Screen"
    Identifier    "Screen4"
    Device        "usbdev"
EndSection
```

## 2 Setting up the environment ##

### 2.1 A1111 WebUI Environment ###

- `\r\n` screw everything up. Meanwhile it requries some native modules to work.

- Nuke the `venv`.

```sh
conda install -c conda-forge gcc
sed 's/\r$//' webui.sh > webui-r.sh
sed 's/\r$//' webui-user.sh > webui-0.sh

git config --global --add safe.directory "/run/media/user/PM863a/stable-diffusion-webui/*"

# Add `source ./webui-r.sh` in last line
sh webui-user-0.sh
```

### 2.2 Training Environment ###

- It should be similar to the guide in Windows. I will add Linux specific content here (should be close to none?)

- Instead of running in external drive, I'll move the scripts to the local drive.

- `sd3` branch will be used.

```sh
accelerate config
------------------------------------------
In which compute environment are you running?
This machine                                                                                                                                       
------------------------------------------
Which type of machine are you using?                                                                                                               
multi-GPU                                                                                                                                          
How many different machines will you use (use more than 1 for multi-node training)? [1]: 1                                                         
Should distributed operations be checked while running for errors? This can avoid timeout issues but will be slower. [yes/NO]: yes                 
Do you wish to optimize your script with torch dynamo?[yes/NO]:NO                                                                                  
Do you want to use DeepSpeed? [yes/NO]: NO                                                                                                         
Do you want to use FullyShardedDataParallel? [yes/NO]: NO                                                                                          
Do you want to use Megatron-LM ? [yes/NO]: NO                                                                                                      
How many GPU(s) should be used for distributed training? [1]:4                                                                                     
What GPU(s) (by id) should be used for training on this machine as a comma-seperated list? [all]:0,1,2,3                                           
Would you like to enable numa efficiency? (Currently only supported on NVIDIA hardware). [yes/NO]: NO
----------------------------------------
Do you wish to use FP16 or BF16 (mixed precision)?
bf16                                                                                                                                               
accelerate configuration saved at /home/user/.cache/huggingface/accelerate/default_config.yaml    
```

- Assumed dataset is ready. Finetune with toy dataset. There is no "Paste as single line" so "deformat" it in a new file.

```sh
accelerate launch 
    sdxl_train.py                                                                                                               
    --pretrained_model_name_or_path="/run/media/user/PM863a/stable-diffusion-webui/models/Stable-diffusion/x215c-AstolfoMix-24101101-6e545a3.safetensors"             
    --in_json "/run/media/user/Intel P4510 3/just_astolfo/meta_lat.json"    
    --train_data_dir="/run/media/user/Intel P4510 3/just_astolfo/kohyas_finetune"
    --output_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/model_out"                                                            
    --log_with=tensorboard                                                                                                      
    --logging_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/tensorboard"        
    --log_prefix=just_astolfo_25012301_                                                                                         
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                                             
    --train_batch_size=1 --learning_rate=5e-6 --max_train_epochs=10                                                             
    --train_text_encoder --learning_rate_te1=3e-6 --learning_rate_te2=3e-6
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                             
    --save_every_n_epochs=1    
```

- And tensorboard:

```sh
tensorboard --logdir "/run/media/user/PM863a/astolfo_xl/just_astolfo/tensorboard"
```

- **Crap, I am OOM again.**

- **Crap, with the "Train TE only trick", the speedup is ~~still 10%~~ legit!** Around 3x for 4x cards.

- [Discussion in Puget Systems.](https://www.pugetsystems.com/labs/hpc/multi-gpu-sd-training/?srsltid=AfmBOooXQwfw4U8OnEtYIHHSEl8UXCdJNQx75dNF23vEZZkPgPrTLcWz)