*Article archive for posting to public website like builds.gg (cannot make new post) and pcpartpicker.

# Ice lake AI / ML Workstation which shouldn't exist #

tldr: This is a bizarre Workstation transformed from my X99 E-ATX PC which was a ROG R5E with an i7-5960X. Case / fans / PSU remains.

Follow [my Instagram](https://www.instagram.com/6dammk9/) for lots of parts hunting / bizarre PC build.

## How the parts are gathered (definitely not ebay) ##

- In precise, most parts are from Xianyu / Taobao / DCFever and offline deals. The listed custom parts are stripped from ebay for "proof of existance". 
- In western (or anywhere actually), it is *barely possible* to gather from AliExpress and ebay, except the server motherboard should be widely available.
- The build is completed for around a month with parts sourcing (which is pain), with daily parts hunting, catalog analysis, contacting sellers etc.
- Listed price are actually close to actual paid price, with minimal transportation fee (less then 1%) and no tax.

## Part list with details ##

It is obviously a dual CPU build with all 16 RAM sticks installed, providing 64c/128t and 512GB of memory. I didn't duplicate all the entries. It is also dual 22G GPU, and dual U.2 SSD with 8TB capacity. 

[Published part list in pcpartpicker.](https://pcpartpicker.com/user/DammK/saved/PgrtWZ)

### CPU ###

As listed in the ebay page, the CPU ["QV2E" a.k.a. Intel Xeon​ Platinum ​8358 ES](https://www.ebay.com.hk/itm/125887688097) has very low compability, which supports [X12DPI-N6](https://www.amazon.com/SUPERMICRO-MBD-X12DPI-N6-B-Server-Motherboard-C621A/dp/B0BZRBMLGQ) series only, with the early 1.1b BIOS, and in dual CPU configuration only, hence the low price. Its 32c64t is not the best among the ice lake CPUs, but it is balanced with higher single core frequency.

### CPU power cable ###

Its TDP is 250W, and all 250W are going into the single CPU 8 pin connector, which should be dangerous for most PC PSUs. Although average 18 AWG cable is capable for up to 7A per cable, or around 360W per socket, the single 12V rail in the PSU may not capable to output so much power. Besides top tier PSU like my EVGA 1600W P2 having 16 AWG cable and the mega 1600W single rail, cheaper miner PSU may not fufill the condition. Therefore, using "PCIE 8pin to CPU 8 pin" will provide greater compability. [NVIDIA Tesla GPU "ESP12V" Power Adapter](https://www.ebay.com/itm/134592371927) is the best choice, where the Tesla cards consumes 250W also. 

### CPU Cooler ###

CPU cooler should be ["coolserver LGA4189-M96"](https://m.coolserver.com.cn/product_view_335_287.html) for official brand name, however [Leopard](https://www.ebay.com/itm/234900698174) / [Jaguar](https://www.ebay.com/itm/166352798317) should be fine. Unlike Noctua fans, its 92mm fan with 6 heat pipes are somewhat capable with the 250W CPU (rated power limit is 320W). Maximum CPU temperature in the built case is 83C, which is fine within temperature limit. 

### Motherborad ###

This motherboard is suprisingly an **exclusive** [Supermicro X12DPi-N6-AS081](https://www.v2ex.com/t/907306) with [3x CPU 8 PIN connector](https://www.chinafix.com/thread-1331197-1-1.html) and additional VRM heatsink. "AS081" will be shown in CPU-Z, which should be verified by official (so don't upgrade BIOS!). It is calimed to support 330W CPUs like [8383C](https://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%208383C.html). [Here is an example of this board with 300W 8375C.](https://xmrig.com/benchmark/4tREmm).

Its connector location is awful, which limit GPU choice and special connectors are required. For example, [vertical SFF8654](https://www.amazon.com/Cablecc-SFF-8639-Slimline-SFF-8654-Mainboard/dp/B09CYC3HRY?th=1) and [SFF8087](https://www.amazon.com/Cable-Matters-Internal-SFF-8087-Breakout/dp/B012BPLYJC) connectors will block the clearance of both length and height of the GPUs.

Its BMC and IPMI is new to me. BMC provide boot bodes, and IPMI supports BIOS flash and somehow supported in AIDA 64.

In theory, under such physical constraint, it should be compatable with most professional blower cards like RTX 8000 / A6000 / Ada6000, and the recent modded RTX 3090 / 4090. With custom built fan case, P100 / V100 with external blower should be fine also.

### Memory ###

All 16 RAM sticks are identical, which should boots with single Attempt. Make sure you don't mix the RAM, even in same frequency with different bank / rank configuration. 

The motherboard supports 2133 / 2400 in BIOS, which is undocumented in user maual.

The RAM sticks should be [Kingston KSM series](https://www.amazon.com/-/zh_TW/KSM24RD4-32MEI/dp/B07BGFDNZ1) but [covered with HP parts number](https://www.ebay.com/itm/265799563533). 

### GPU ###

Under so much physical constrains, I choose the famous [RTX 2080 ti blower cards with the 22G hack](https://2080ti22g.com/). Both cards are identical. The card's exterior / PCB is the exact same ["ebay Leadtek RTX 2080 ti blower"](https://www.ebay.com/itm/374465596451), which are "not reference PCB" with only 10 phase VRM, instead of 13. The 22G mod is so obvious (from the same "Leadtek" manufacturer), even the BIOS was picked randomly (I received Gigabyte blower BIOS instead of the preferred [WinFast RTX 2080 Ti Hurricane](https://www.techpowerup.com/vgabios/258295/258295)). Power state bug / undesired fan speed curve / miscalculated TDP may occur if wrong BIOS is applied, even core funcionality (AI under CUDA) is kept. Beside the BIOS, the PCB resembles [Gainward RTX 2080 Ti Phoenix GS](https://www.igorslab.de/en/rescue-a-gainward-rtx-2080-ti-phoenix-gs-waermeleit-pads-right-replace-practice/), but its BIOS will cause the bugs above.

Unlike the retail version, the tail of the card has reordered the video output, leaving a sigle row of DPx3 + HDMI, without USB-C connector. In the front side, the FE LED / fan connector is also removed, leaving only 2 set of 4-pin connector. Without the blockage of the 2nd row of video output connector, the airflow is improved, along with [vapor chamber](https://www.gigabyte.com/Graphics-Card/GV-N208TTURBO-OC-11GC-rev-10#kf) instead of full copper, [and the binned "300A" core](https://www.overclock.net/threads/official-nvidia-rtx-2080-ti-owners-club.1706276/), the temperature is suprisingly well, with core 70C and hotspot 75C under 80% / 3000 RPM fan speed, which is as good as most 3 fan heatsink like Asus ROG StRIX 2080TI. The actual VRAM DRMOS specificaion is not observed, but it should be fine with without overclock headroom.

The build quality of the "22G custom" is fine. Lead-free solder with minimal adhesive ("502 / black rubber as seen in CPU lid") are common practice after iterlations (discussed in some Chinese GPU / Notebook repair videos, [example of Lenovo Legion with high failure rate because of excessive adhesive and extra low melting point solder.](https://www.youtube.com/watch?v=wUnQLhoHQZk&ab_channel=%E9%9D%93%E4%BB%94%E4%BF%AE%E6%9C%BAPC-Repair)). However the packaging appears inconsistent. My first card is well packaged with an unmarked box, but the second card is just wrapped with bubble wrap only, resulting damaged solder points in PCIE connectors and resulting 3.0 x1 speed only. Such bandwith limit yields 80% extra time required for image geeneration, majorly in tensor transportation between GPU and CPU. Yet it is still a lot faster then [cheap options like 1080ti / P100 / P40 / M40](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch04/readme.md#chapter-04b-extra-making-use-of-m40-24gb-for-generating-large-images). 

Also, the SFF connector still blocked the placement of the front side of the card, resulting even the card is perfectly fine (e.g. watercooled RTX 3090 in 4.0 x16), only X8 is accessible because of incomplete PCIE slot connection.

The NV-Link adapter is useless here therefore I don't include it in the list. I boudght it for other build (2080ti FE) which were sold already.

### Storage ###

For storage, 2x P4510 are installed, only listed 1 for the same reason. Therefore there are 8TB of SSD storage which should be sufficient for research. OS drive is the Micron 1300, which is in single.
