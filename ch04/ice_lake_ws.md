*Article archive for posting to public website like builds.gg (cannot make new post) and [pcpartpicker](https://pcpartpicker.com/b/VZy48d). Images will be included there, [and Google Drive also.](https://drive.google.com/drive/folders/1v_b23L6OAVj7WgRmqmIbPVnCLCDriWzI?usp=sharing).

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

The [NV-Link adapter](https://www.amazon.com/Nvidia-Corporation-900-14932-2500-000-Link-Bridge/dp/B07JZLHPCG) is useless here therefore I don't include it in the list. I boudght it for other build (2080ti FE) which were sold already.

### Storage ###

For storage, 2x [Intel / Solidigm DC P4510 4TB](https://www.solidigm.com/products/data-center/d7/p4510.html) are installed, resulting 8TB of storage. Its price may go cheap because of former mining SSD. Mine has 1.3 PBW used, resulting 94% health. Yes, its life span is 13.88 PBW as writtn in the SATA healthcheck! It will be handy for extensive model merging which is storage intensive. It came with [U.2 to PCIE adapter](https://www.amazon.com/GINTOOYUN-Expansion-Card%EF%BC%8CSFF-Riser-Adapter/dp/B08P16LMHW), soon I bought it with SFF8639 adapter cable and connect it to supported motherboard like ASUS ROG R5E10 and EVGA X299 Dark, and finally this board via SFF8654. 

However, for OS drive, I use the traditional single 2.5 inch SATA SSD [Micron 1300 512GB](https://hppart.uk/products/for-hp-861193-001-micron-1300-2-5-512gb-mtfddak512tdl-ssd-solid-state-drive-new). Besides less sensitive to heat, I have found that if both OS drive and model drive are on NVME, CPU / PCH may have trouble on rapid context switching while receiving IO boost, making the OS being instable.

For the least exicting part, the [WD Black Label 2TB](https://www.amazon.com/-/zh_TW/WD2003FYYS/dp/B00DOS5KXC) still remains, storing non AI / ML, or OS stuffs, usually downloaded software, docuements, maybe a some BT materials.

### PSU ###

It is obvious: [EVGA 1600W P2](https://www.amazon.com/-/zh_TW/EVGA-Supernova-%E9%9B%BB%E6%BA%90%E4%BE%9B%E6%87%89%E5%99%A8-PLUS-%E7%99%BD%E9%87%91%E8%AA%8D%E8%AD%89/dp/B00NJG61JQ?th=1) is a great PSU, besides its age. I bought it while 2020's BTC halving, from a stripped mining rig. It is one of the few PSUs featuring 16 AWG PSU cables, supporting AMD 295X2 which is as power hungry as the ice lake CPUs. Since the motherboard has been load balanced with 3 rails, the CPU 8pin cable should be capable with reduced load with a little bit of headroom.

I don't test the maximum power consumption yet, it should be around 1200W, which are 250W x4 for CPU and GPU, and another 200W for the board and memory. However its power consumption while idle is high, I recorded 300W with little to no tasks. It may be caused by undesired power state between ES CPU and early BIOS version, and the DSC from the 2080ti because I'm using [4K144Hz monitor]([https://www.displayspecifications.com/en/model/82bf263d](https://www.price.com.hk/product.php?p=522679)) (not listed).  

### Cooling (Case / fan / thermal paste) ###

The [Corsair Graphite Series 760T Full Tower Windowed Case](https://www.newegg.com/arctic-white-corsair-graphite-series-atx-full-tower/p/N82E16811139055) looks like mid tower nowdays, but technically it has 8 pcie slots and supports "EATX", which is actually EEB size. However, although the motherboard is claimed SSB also, the screw hole is not following ATX form factor (view the image again). Therefore I installed 4 out of 9 screw holes only, leaving the board hanging in diagonal.

Case fan is a set of Cooler Master ARGB fans. MasterFan [MF120R](https://www.amazon.com/-/zh_TW/Cooler-Master-MasterFan-MF120R-R4-120R-20PC-R1/dp/B07H4NYFVG?th=1), [MF140R](https://www.amazon.com/-/zh_TW/R4-140R-15PC-R1/dp/B07GSSY21G), SickleFlow [SF120R](https://www.amazon.com/Cooler-Master-Independently-Controlled-Addressable-Management/dp/B07P989CQ6) and [SF140](https://www.amazon.com/Cooler-Master-SickleFlow-Individually-Customizable/dp/B08HJPHJMH) are common ARGB fans and perform fairly well.

Thermal paste is technically unknown becuase I bought the CPU "guled" with the heatsink. However the seller tell me that it is in fact [Arctic MX4](https://gamersnexus.net/guides/3346-thermal-paste-application-benchmark-too-much-thermal-paste), which is also common and perform consistantly well. As stated in the CPU heatsink, the temperature is fine.

### Miscellaneous ###

GPU stand is important. [CoolerMaster Universal Video Card Holder](https://www.amazon.com/-/zh_TW/MCA-0005-KUH00/dp/B01M5DCMPM?th=1) is a minimalistic and useful stand. It may not strong enough for 4090, but it should be sufficient with 2 blower cards which are quite light in weight. There is also a [knockoff ARGB stand](https://www.performance-pcs.com/system-hardware/gpu-holder/vertical-video-card-bracket-argb-vga-stand-chassis-lamp-motherboard-aura-sync-rgb-board-jack-faith-light-pollution.html) which is used for HDD case cover.

The front 3.5 bay is not empty. [Asus ROG Front Base](https://www.amazon.com/-/zh_TW/ASUS-ROG-Front-Base/dp/B00JXED39O/ref=cm_cr_arp_d_product_top?ie=UTF8) was used for the previous build (same series with the R5E) but it is incompatable with this build. It is disabled and not included in the list.

*Ah. [He is so cute](https://www.amazon.com/Taito-Fate-Apocrypha-Action-Figure/dp/B077SLPXKG).* 

## End of part list ##

Thank you very much for reading my lengthy part list and analysis till the very last! Also check out my [ROG RGB open air build!](https://builds.gg/dammk/flashbang-rog-open-air-miku-hatsune-34047)  