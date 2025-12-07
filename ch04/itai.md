# Semi ITAI Build: China hardware with major Linux Distribution #

*It will be easy peasy if I just pick [KX6000 CPU](https://www.tomshardware.com/pc-components/cpus/alleged-zhaoxin-kx-6000g-benchmarks-surface-chinese-made-chips-perform-like-cpus-from-the-late-2000s-but-uses-less-power) and [Fantasy 2 GPU](https://www.tomshardware.com/news/innosilicon-unveils-fantasy-2-gpu), and just grab a LAN cable and install Windows 10.*

## Gallery / BuildsGG mirror ##

- [builds.gg](https://builds.gg/dammk/semi-itai-build-china-hardware-with-major-linux-distribution-39402)

- [Google Drive](https://drive.google.com/drive/folders/1XuQUYO9rmrrHIraU35kwTN3ZFxvvYDtk?usp=sharing)

- [Youtube Shorts](https://youtube.com/shorts/m-L19Y-dzfA?si=ToQjtdEzMf1AxDL8)

## Hardware list ##

*Driver / software support will be discussed later.*

- CPU: Huawei Kunpeng 920 8 Core "2251K". Sold as [D920L11K](https://support.huawei.com/enterprise/en/bulletins-product/ENEWS2000023442). It is the server variant of [D920S10](https://e.huawei.com/en/products/computing/kunpeng/desktop-board/d920s10). PCIE 3.0 instead of 4.0 from full server version.

- Motherboard: ["BC32MBHB"](https://world.taobao.com/lang/zh-tw/goods/11814911.htm), bundled with [Powerleader PT620K](http://ec.ctiforum.com/jishu/qiye/qiye_news/591335.html) 2U server (shown in BIOS logo). **Supports 4Rx4 64G RDIMM, and 3200Mhz.** Soldered with CPU. *Desktop uATX board layout.* Also, **only AMD / ITAI GPU will boot!** Tested with multiple Nvidia and even Aspeed GPU, all boot with no screen.

- Memory: 2x [UNILC DDR4 2666Mhz 8G 1RX8 UDIMM "SCE08GU03H1F1C-26V"](https://product.yesky.com/product/1100/1100448/). Note: Probably using [skhynix die](https://zhuanlan.zhihu.com/p/34562360), hiding under purple metal case. *The only module escaped the [price surge](https://www.tomshardware.com/pc-components/ram/ddr4-costs-soar-as-manufacturers-pull-the-plug).*

- Storage (NVME M2): [UNIC P5160 256G "UNSPC256AKMM"](https://detail.zol.com.cn/solid_state_drive/index1309290.shtml). *No other storage is used.*

- GPU: [JEMO Jingjha JM9100 4G](https://www.jemoic.com/products_6/381.html). Half height with VGA output. Chip series is believed as  *Vulkan API is a pending promise.*

- Wifi: [LB-Link M2625XP1](https://www.lb-link.com/M2625XP1-2T2R-802-11a-b-g-n-ac-ax-WiFi-B5-2-Module-pd524485168.html) Wifi-6 pcie card. Core is [Senscomm Wisen-2 "SCM2625"](https://www.senscomm.com/en/station-device-chipsets-en/).

- PSU: [Delta DPS-350JB-1B 350W SFX](https://forums.tomshardware.com/threads/is-a-delta-350w-psu-trustable.3741673/). *Probably is a counterfeit PSU.*

- CPU fan: ["Generic ITAI CPU fan"](https://vn.world.taobao.com/item/MllMQmd1VHpiNzRRMjhCWXJwVEZZQT09.htm).Turns out it is a **generic 115X heatsink**. Orginal 2U server use an generic 1U active blower heatsink.

- Case fan: [Thermalight TL-B8](https://www.thermalright.com/product/tl-b8/) with [Thermalight TL-B4020](https://www.thermalright.com/product/tl-b4020/). **The motherboard only supports PWM fan, even 2 pin fan won't spin.**

- Case: [GTR S608-S](http://www.gtr.com.hk/GTR/case/micro_sfx/master.htm). Micro SFX Case / OEM Desktop SFF case in common size. *Explains the less popular size above.* Original 2U server was using Flex 1u PSU instead.

## Software list ##

### Match Linux Kernel Version first (5.x) ###

*This is the nightmare. Background timeline is important: Since the ITAI OS serves for utility services which aims for LTS support, kernel side integration is lacking behind, seriously.*

- In 2405, [UOS claimed supporting dual kernel](https://faq.uniontech.com/solution/5cb3/39f8/05fd), which was still **4.19 and 5.10**. Similarly, commercial OS such as KylinOS and EulerOS, followed the **exact same version number**.

- At the same time, The opensource versions, [Deepin 23](https://www.deepin.org/zh/deepin-community-monthly-report-2024-08/), [openKylin 2.0](https://www.openatom.org/journalism/detail/wz0ZVCzcnOav), and [openEULER 24.03](https://www.openeuler.org/zh/interaction/summit-list/2403-version-release/), **all announced to load 6.6**.

- However, in [GPU driver page](https://www.jemoic.com/drive_67), when trying to **build the actual dkms driver**, all of them will throw error unless the Kernel is **5.x**, even the driver update date is very recent (e.g. 2510, 1 month ago).

- Meanwhile, CPU archieture may screw things up. In this example, Kunpeng 920 use tsv110 as archieture, which is 64bit ARM v8.2. [openSUSE has a dedicated grub edit to install OS](https://zh.opensuse.org/index.php?title=%E9%B2%B2%E9%B9%8F920%E5%8F%B0%E5%BC%8F%E6%9C%BA%E5%AE%89%E8%A3%85&variant=zh), ubuntu 22.04 just hangs and refuse to install.

```sh
linux /vmlinuz-5.4.18-53-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv initcall_blacklist=hisi_ddrc_pmu_module_init arm64.nompam
```

- Therefore the only *non ITAI OS* will be [Ubuntu 20.04](https://en.wikipedia.org/wiki/Ubuntu_version_history) (`*.deb` drivers) or [OpenSUSE 15.5](https://en.wikipedia.org/wiki/OpenSUSE) (`*.rpm` or `*.deb` with `alien`). Other distro such as [manjaro](../ch06/manjaro-runtime/readme.md) / fedora / centos follows the same approach. However, driver packages are almost exclusively `*.deb`, or you need to build the `dkms` stuffs from source code (meanwhile there is "GUI integration package").

### Prodecure to set up the OS and drivers (Ubuntu 20.04) ###

- First install OS, which should be easy without hurdle. Pick logical volume is fine.

- Ubuntu 20.04 logical volume is capped by 100GB, or only half of the space by default. Follow [this guide](https://askubuntu.com/questions/1417938/ubuntu-does-not-use-full-disk-space-how-to-extend) to extend the volume.

```sh
# Confirm the logical volume / disk drive is present.
lsblk

sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

- Then **add KylinOS repo and perform system update**. This will be useful to identify ITAI hardwares (it will identify and mark Kungpeng 920).

- The KylinOS V10 SP1 aarch64 is likely using [Kernel 5.4](https://www.hiascend.com/forum/thread-0201113562091848003-1-1.html), which match my own install. [However some of them may still stuck in 4.19](https://support.huaweicloud.com/intl/zh-cn/alaudacp-cnam/alaudacp_02.html)

```sh
# Add entry in /etc/apt/sources.list
# deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1-2203-updates main restricted universe multiverse

gpg --keyserver keyserver.ubuntu.com --recv-keys F49EC40DDCE76770
gpg --export --armor F49EC40DDCE76770 | sudo apt-key add - && sudo apt-get update 

# This may be in multiple times
sudo apt-get upgrade
```

- Now install some basic packages for the GUI and drivers. Notice that 20.04 is not bundled as Desktop variant (new in 24.04?)

```sh
# DKMS as drivers
sudo apt install dkms
# Wifi tools
sudo apt install net-tools
sudo apt install wireless-tools
# Desktop GUI
sudo apt install ubuntu-gnome-desktop

# I forgot which package, keep installing
# VAAPI
vainfo
# Vulkan
vulkaninfo
# OpenGL
glxinfo
# htop but cooler
btop
# fastfetch but compatable with 20.04
neofetch
```

- Now it is good to install the drivers. Strangely the repo does not index the driver we need. Head to [the pool page](https://archive.kylinos.cn/kylin/KYLIN-ALL/) to navigate and obtain.

- **Do not install mwv207-mesa-dkms! It will crash the XOrg session!**

- **Also it is very risky to reinstall the drivers! Install in sequence!** [Perform some workarounds if you can't remove and switch Wifi module.](https://askubuntu.com/questions/972215/a-start-job-is-running-for-wait-for-network-to-be-configured-ubuntu-server-17-1)

```sh
wget https://archive.kylinos.cn/kylin/KYLIN-ALL/pool/mwv207-dkms_1.6.17-0kylin1_all.deb
wget https://archive.kylinos.cn/kylin/KYLIN-ALL/pool/mwv207-dev_1.6.16-0kylin1_arm64.deb
wget https://archive.kylinos.cn/kylin/KYLIN-ALL/pool/mwv207-vaapi_1.6.2-0kylin1_arm64.deb
wget https://archive.kylinos.cn/kylin/KYLIN-ALL/pool/mwv207-vdpau_1.2.1-0kylin1_arm64.deb   
wget https://archive.kylinos.cn/kylin/KYLIN-ALL/pool/scm2625-pcie-dkms_2.1.2-V13_all.deb
# dkms driver a.k.a. compile from source
sudo ipkg -i mwv207-dkms_1.6.17-0kylin1_all.deb
sudo ipkg -i scm2625-pcie-dkms_2.1.2-V13_all.deb
# It should show "installed"
dkms status
# It also show nothing "UNCLAIMED"
sudo lshw
# If you see error for wifi module, either the module or the OS is already corrupted
sudo dmesg
# Continue to remaining integration. Note: risky to uninstall
sudo ipkg -i mwv207-dev_1.6.16-0kylin1_arm64.deb
sudo ipkg -i mwv207-vaapi_1.6.2-0kylin1_arm64.deb
sudo ipkg -i mwv207-vdpau_1.2.1-0kylin1_arm64.deb
# Restart the machine
sudo reboot
# The program should show "Jingjha JM9100" instead of "LLVM pipeline"
glmark2
# "Senscomm SCM2625" should be found.
nmcli dev status
```

### (Not recommended) Make gcc switchable for more 3D programs ###

- [Furmark 2 ARM](https://geeks3d.com/furmark/downloads/) or [same OpenGL games](https://github.com/supertuxkart/stk-code) may require a more moden compiler. **Just admire that we are using decommissioned server parts which is likely EOS.**

```sh
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install gcc-13 g++-13

sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/gcc-13 60
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 60

sudo update-alternatives --config g++
sudo update-alternatives --config gcc
```

### Finally, deepseek on Kunpeng 920 (desktop) ###

- It should be easy without hurdle. I suggest use `docker compose` for OpenWebUI + ollama bundle. Check out [this guide](https://ivonblog.com/posts/ollama-llm-docker/) or [this guide](https://blog.darkthread.net/blog/ollam-open-webui/).

- For ollama server, [set system wide environment variable](https://askubuntu.com/questions/161924/how-do-i-set-persistent-environment-variables-for-root) with `OLLAMA_HOST=0.0.0.0`, or edit the docker compose file. `ufw` is inactive by default.

```sh
# Install docker
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install ollama (native, remember set OLLAMA_HOST=0.0.0.0 for real ollama server)
curl -fsSL https://ollama.com/install.sh | sh
# Remember that our JM9100 don't even have Vulkan API! We are using CPU inference actually. Well, GB10 and Mac Pro are aarch64 also isn't it?
ollama pull deepseek-r1:1.5b
```

### Extra: Workarounds on Web Browser ###

- Even GPU supports OpenGL 4.0, Firefox has additional conditions (MESA integration) to activate, which is impossible to turn on. [Force activate software WebGL rendering instead.](https://support.mozilla.org/en-US/questions/1326160)

- Otherwise, `chromium`, or [ungoogled-chromium](https://askubuntu.com/questions/1298493/how-to-install-ungoogled-chromium-on-ubuntu-20-04) has WebGL enabled by default, also with basic audio / video streaming feature.

- *BTW don't load heavy BIM models.*
