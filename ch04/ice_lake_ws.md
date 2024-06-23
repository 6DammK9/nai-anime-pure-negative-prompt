*Article archive for posting to public website like [builds.gg](https://builds.gg/dammk/ice-lake-ai-ml-workstation-which-shouldnt-exist-36884) and [pcpartpicker](https://pcpartpicker.com/b/VZy48d). Images will be included there, [and Google Drive also.](https://drive.google.com/drive/folders/1v_b23L6OAVj7WgRmqmIbPVnCLCDriWzI?usp=sharing).

# Ice lake AI / ML Workstation which shouldn't exist #

tldr: This is a bizarre Workstation transformed from my X99 E-ATX PC which was a ROG R5E with an i7-5960X. Case / fans / PSU remains.

Follow [my Instagram](https://www.instagram.com/6dammk9/) for lots of parts hunting / bizarre PC build.

## How the parts are gathered (definitely not ebay) ##

- In precise, most parts are from Xianyu / Taobao / DCFever and offline deals. The listed custom parts are stripped from ebay for "proof of existance". 
- In western (or anywhere actually), it is *barely possible* to gather from AliExpress and ebay, except the server motherboard should be widely available.
- The build is completed for around a month with parts sourcing (which is pain), with daily parts hunting, catalog analysis, contacting sellers etc.
- Listed price are actually close to actual paid price, with minimal transportation fee (less then 1%) and no tax.

## Part list with details ##

It is obviously a dual CPU build with all 16 RAM sticks installed, providing 64c/128t and 512GB of memory. I didn't duplicate all the entries. It is also dual 22G GPU, and SATA + U.2 SSD with 10TB capacity. 

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

**4TB RAM. For real.**. [8x Samsung 64G 4RX4 LR-DIMM 2400MHz](https://www.ebay.com/itm/173343022411), and then [8x Intel 2nd gen PMem 512GB DCPMM 3200MHz](https://www.ebay.com/p/24058980642). [Check out LTT's video on how to archieve this insane amount of RAM.](https://www.youtube.com/watch?v=uHAfTty9UWY)

First boot is a pain. BIOS version reports confusing info, finally I cleared CMOS (reset BIOS) and it boots fine. Memory training is long (5min), however it becomes fast after the first boot.

The motherboard supports 2133 / 2400 in BIOS, which is undocumented in user maual. Since I can't afford too many items at the same time, the DIMM part is still slow. ~~I may upgrade it to 3200 once I have enough budget.~~ Also I have found that PMem may requires large CL / CAS value (latency) because of the memory die. If you operate with low bandwith DIMM meanwhile with low latency, memeory faults may raise and make your boot time a lot longer, and cause some BSODs.

PMem will be very hot (full loading) when loading into Windows. It will use around 60GB, and you need [WS / Enterprise Win 10 / 11](https://www.compuram.de/blog/en/how-much-ram-can-be-addressed-under-the-current-32-bit-and-64-bit-operating-systems/) to support 2TB+ of RAM.

On top of that, a dedicated RAM cooler, [GSkill FTB-3500C5-D](https://www.ebay.com/itm/266465959152) has been applied when the case airflow is not enough. An upgraded Taobao RGB PWM Compact cooler is coming soon.

### GPU ###

Under so much physical constrains, I choose the famous [RTX 2080 ti blower cards with the 22G hack](https://2080ti22g.com/). Both cards are identical. The card's exterior / PCB is the exact same ["ebay Leadtek RTX 2080 ti blower"](https://www.ebay.com/itm/374465596451), which are "not reference PCB" with only 10 phase VRM, instead of 13. The 22G mod is so obvious (from the same "Leadtek" manufacturer), even the BIOS was picked randomly (I received Gigabyte blower BIOS instead of the preferred [WinFast RTX 2080 Ti Hurricane](https://www.techpowerup.com/vgabios/258295/258295)). Power state bug / undesired fan speed curve / miscalculated TDP may occur if wrong BIOS is applied, even core funcionality (AI under CUDA) is kept. Beside the BIOS, the PCB resembles [Gainward RTX 2080 Ti Phoenix GS](https://www.igorslab.de/en/rescue-a-gainward-rtx-2080-ti-phoenix-gs-waermeleit-pads-right-replace-practice/), but its BIOS will cause the bugs above.

Unlike the retail version, the tail of the card has reordered the video output, leaving a sigle row of DPx3 + HDMI, without USB-C connector. In the front side, the FE LED / fan connector is also removed, leaving only 2 set of 4-pin connector. Without the blockage of the 2nd row of video output connector, the airflow is improved, along with [vapor chamber](https://www.gigabyte.com/Graphics-Card/GV-N208TTURBO-OC-11GC-rev-10#kf) instead of full copper, [and the binned "300A" core](https://www.overclock.net/threads/official-nvidia-rtx-2080-ti-owners-club.1706276/), the temperature is suprisingly well, with core 70C and hotspot 75C under 80% / 3000 RPM fan speed, which is as good as most 3 fan heatsink like Asus ROG StRIX 2080TI. The actual VRAM DRMOS specificaion is not observed, but it should be fine with without overclock headroom.

The build quality of the "22G custom" is fine. Lead-free solder with minimal adhesive ("502 / black rubber as seen in CPU lid") are common practice after iterlations (discussed in some Chinese GPU / Notebook repair videos, [example of Lenovo Legion with high failure rate because of excessive adhesive and extra low melting point solder.](https://www.youtube.com/watch?v=wUnQLhoHQZk&ab_channel=%E9%9D%93%E4%BB%94%E4%BF%AE%E6%9C%BAPC-Repair)). However the packaging appears inconsistent. My first card is well packaged with an unmarked box, but the second card is just wrapped with bubble wrap only, resulting damaged solder points in PCIE connectors and resulting 3.0 x1 speed only. Such bandwith limit yields 80% extra time required for image geeneration, majorly in tensor transportation between GPU and CPU. Yet it is still a lot faster then [cheap options like 1080ti / P100 / P40 / M40](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch04/readme.md#chapter-04b-extra-making-use-of-m40-24gb-for-generating-large-images). 

Also, the SFF connector still blocked the placement of the front side of the card, resulting even the card is perfectly fine (e.g. watercooled RTX 3090 in 4.0 x16), only X8 is accessible because of incomplete PCIE slot connection.

The [NV-Link adapter](https://www.amazon.com/Nvidia-Corporation-900-14932-2500-000-Link-Bridge/dp/B07JZLHPCG) is useless here therefore I don't include it in the list. I boudght it for other build (2080ti FE) which were sold already.

### Storage ###

For storage, 2x [Intel / Solidigm DC P4510 3.84TB](https://www.amazon.com/Intel-SSDPE2KX040T8-SSDPE2KX040T801-Lenovo-Supermicro/dp/B0BCFVBSD8) are installed, resulting 8TB of storage. Its price may go cheap because of former mining SSD. Mine has 1.3 PBW used, resulting 94% health. Yes, its life span is 13.88 PBW as writtn in the SATA healthcheck! It will be handy for extensive model merging which is storage intensive. It came with [U.2 to PCIE adapter](https://www.amazon.com/GINTOOYUN-Expansion-Card%EF%BC%8CSFF-Riser-Adapter/dp/B08P16LMHW), soon I bought it with SFF8639 adapter cable and connect it to supported motherboard like ASUS ROG R5E10 and EVGA X299 Dark, and finally this board via SFF8654. 

However, for OS drive, I use the traditional single 2.5 inch SATA SSD [Intel / Solidigm D3 S4510 1.92TB](https://www.amazon.com/Intel-D3-S4510-Solid-State-Drive/dp/B07GL4LLWL). Besides less sensitive to heat, I have found that if both OS drive and model drive are on NVME, CPU / PCH may have trouble on rapid context switching while receiving IO boost, making the OS being instable. Meanwhile, it just has same lifespan which is more than 6PBW!

For the least exicting part, the [WD Black Label 2TB](https://www.amazon.com/-/zh_TW/WD2003FYYS/dp/B00DOS5KXC) still remains, storing non AI / ML, or OS stuffs, usually downloaded software, docuements, maybe a some BT materials. *I will replace it with SSD also to keep everything "Intel themed".*

Meanwhile, *for fun and future VROC use*, [Hyper M.2 x16 Card V2](https://www.amazon.com/ASUS-M-2-X16-V2-Threadripper/dp/B07NQBQB6Z?th=1) and 4x [Intel Pro 6000P 256G](https://www.amazon.com/Intel-SSDPEKKF256G7X1-6000p-Express-Retail/dp/B01LW6USJD/ref=cm_cr_arp_d_product_top?ie=UTF8) has been used for PoC test for compatibility. And... [Samsung PM981 256GB](https://www.amazon.com/-/zh_TW/MZVLB256HBHQ/dp/B07B8W7BFD) has been proven not working. Later I'll try for 24x [Intel 760P 128G](https://www.amazon.com/Intel-760P-128GB-80mm-PCIe/dp/B078VBGSVL/ref=cm_cr_arp_d_product_top?ie=UTF8) to see if the CPUs can handle the traffic as advertised. Finally I may try 4x [Intel OPTANE SSD DC P4801X 375GB](https://www.amazon.com/Intel-OPTANE-SSD-P4801X-375GB/dp/B084RJ5QC3) or just [Intel OPTANE SSD DC P4800X 375GB](https://www.amazon.com/Intel-P4800X-Internal-Solid-State/dp/B07589MW3P) if I am concerned on power consumption towards MB. [ LSI SAS 9300-8i from stripped Inspur servers](https://www.aliexpress.com/item/1005005972744899.html) are also considered when I can get them cheap (60x cheaper from brand new).

### PSU ###

After my old [EVGA 1600W P2](https://www.amazon.com/-/zh_TW/EVGA-Supernova-%E9%9B%BB%E6%BA%90%E4%BE%9B%E6%87%89%E5%99%A8-PLUS-%E7%99%BD%E9%87%91%E8%AA%8D%E8%AD%89/dp/B00NJG61JQ?th=1) got tripped because of its age, I bought a [Silverstone HELA 2050 Platinum](https://www.amazon.com/Silverstone-Cybenetics-Certified-SST-HA2050-PT-SST-AX2050MCPT/dp/B09P8CSLVD?th=1) to make sure it can withstand the notorious power spikes from the 2080ti. 

The daily maximum power consumption is around 1200W, which are 250W x4 for CPU and GPU, and another 200W for the board and memory, and 1500W including the spikes. Its idle power consumption is high, reaching around 400W especially [I turn off C-state because of the huge lag](https://www.tomshardware.com/news/sleepy-intel-ice-lake-xeons-take-longer-to-ramp-up-frequency). Meanwhile, DSC is on for the 2080ti because I'm using [4K144Hz monitor](https://www.price.com.hk/product.php?p=522679) (not listed, [a unbranded monitor built from panel](https://www.displayspecifications.com/en/model/82bf263d)). 

Similar to 1600P2 and most top tier PSUs, it features 16 AWG PSU cables, supporting AMD 295X2 which is as power hungry as the ice lake CPUs. Since the motherboard has been load balanced with 3 rails, the CPU 8pin cable should be capable with reduced load with a little bit of headroom.
 
### Cooling (Case / fan / thermal paste) ###

The [Corsair Graphite Series 760T Full Tower Windowed Case](https://www.newegg.com/arctic-white-corsair-graphite-series-atx-full-tower/p/N82E16811139055) looks like mid tower nowdays, but technically it has 8 pcie slots and supports "EATX", which is actually EEB size. However, although the motherboard is claimed SSB also, the screw hole is not following ATX form factor (view the image again). Therefore I installed 4 out of 9 screw holes only, leaving the board hanging in diagonal.

Case fan is majorly a set of Cooler Master ARGB fans. MasterFan [MF140R](https://www.amazon.com/-/zh_TW/R4-140R-15PC-R1/dp/B07GSSY21G), [SickleFlow 140](https://www.amazon.com/Cooler-Master-SickleFlow-ARGB-Cooling/dp/B08GD8Q55F?th=1) are common ARGB fans and perform fairly well. For the exhaust fan, after calculation of the airflow (42 CFM from CPU), I switched to [JETFLO 120 BLUE LED](https://www.coolermaster.com/zh-tw/products/jetflo-120-blue/?tab=tech_spec) for massive airflow, lighting, and relatively low noise". 

I have reused Jonsbo [FR140S](https://www.jonsbo.com/products/FR140S.html) and [FR-925 ARGB](https://www.jonsbo.com/en/products/FR9253.html) from previous build. 

Thermal paste is technically unknown becuase I bought the CPU "guled" with the heatsink. However the seller tell me that it is in fact [Arctic MX4](https://gamersnexus.net/guides/3346-thermal-paste-application-benchmark-too-much-thermal-paste), which is also common and perform consistantly well. As stated in the CPU heatsink, the temperature is fine.

### Miscellaneous ###

GPU stand is important. [CoolerMaster Universal Video Card Holder](https://www.amazon.com/-/zh_TW/MCA-0005-KUH00/dp/B01M5DCMPM?th=1) is a minimalistic and useful stand. It may not strong enough for 4090, but it should be sufficient with 2 blower cards which are quite light in weight. There is also a [knockoff ARGB stand](https://www.performance-pcs.com/system-hardware/gpu-holder/vertical-video-card-bracket-argb-vga-stand-chassis-lamp-motherboard-aura-sync-rgb-board-jack-faith-light-pollution.html) which is used for HDD case cover.

The front 3.5 bay is not empty. [Asus ROG Front Base](https://www.amazon.com/-/zh_TW/ASUS-ROG-Front-Base/dp/B00JXED39O/ref=cm_cr_arp_d_product_top?ie=UTF8) was used for the previous build (same series with the R5E) but it is incompatable with this build. It is disabled and not included in the list.

*Ah. [He is so cute](https://www.amazon.com/Taito-Fate-Apocrypha-Action-Figure/dp/B077SLPXKG).* 

## End of part list ##

Thank you very much for reading my lengthy part list and analysis till the very last! Also check out my [ROG RGB open air build!](https://builds.gg/dammk/flashbang-rog-open-air-miku-hatsune-34047)  

## Extra: How I get the parts ##

I think it worths mentioning. General advice: **Always look for RMA procedure and make sure you can afford the risk!** [Also here is a Youtube channel covering most of the contents below](https://www.youtube.com/@techyescity/videos). However I'm building workstation instead of mainstream parts, therefore it is another level.

|Online / Offline|Location|Risk|Description|
|---|---|---|
|Offline|Storefront in shopping malls.|Low|Usually **brand new**, sold by retailer with distributers a.k.a ["行貨"](https://en.wiktionary.org/wiki/%E8%A1%8C%E8%B2%A8#Chinese). Even ["水貨"](https://en.wiktionary.org/wiki/%E6%B0%B4%E8%B2%A8#Chinese) are handled carefully. For example, most RTX 4090 under [tariff](https://uk.pcmag.com/graphics-cards/149212/us-to-block-nvidia-from-shipping-more-geforce-rtx-4090-gpus-to-china) are "水貨". **Beware of full builds. The part list may be problematic.**|
|Offline|"Huaqiangbei" style storefront|Low|Usually recycled 2nd hand PC parts, but can be tested in sight. Quality of parts depends on how many people duming old PCs to there (as high as water cooled X299 set / dual core C621 workstation). **Don't ask for repair even they have such service.**|
|Offline|Direct deal with part recyclers|Low|Quite polarized: Either know nothing about PC, or extremely knowledgeable as an expert on the parts they are collecting. Usually they never promote / publish for every items they have collected. *Special case for me: It is even cheaper then XianYu, which should be the cheapest in the world.* **Work best for specific parts.**|
|Offline|Scrapyard / Junkyard style storefronts|High|**You must know why the part appears in the scrapyard.** Usually [obselete server parts](https://en.wikipedia.org/wiki/Global_waste_trade) / parts with sealed packagings are safe to bet. Even you know repairing stuffs, they can be totaled (e.g. damaged PCB / damaged core).|
|Online|Local web stores|Low|Same as offline storefront, but they operate websites instead. It can be DIY parts up to branded servers / workstations which don't exist in shopping mall. **Make sure your online payment is ready**|
|Online|Local second hand marketplace ([dcfever](https://www.dcfever.com/index.php), [carousell](https://www.carousell.com.hk/), [fb marketplace](https://www.facebook.com/marketplace/))|Medium|**Always look for trade history.** Try to build trust to trade partners. If trade history is scarse, pay attention to conversation and figure out why they are selling right now.|
|Online|Foreign web stores ([taobao](https://world.taobao.com/) = [aliexpress](https://www.aliexpress.com/), [temu](https://www.temu.com/) = [tmall](https://www.tmall.hk/), [amazon](https://www.amazon.com/) etc.)|Medium|Either regular goods from irregular brand, or legit minor goods from anywhere. **Make sure delivery is good. They can DOA because of poor transporting.** Meanwhile **impossible to send back for repairing because of importing laws.**|
|Online|Foreign second hand marketplace ([xianyu](https://goofish.com/), [ebay](https://www.ebay.com/))|High|**Combined from all points above.** Extremely challenging. Now guaranteed close to 0% win rate on gambling damaged GPUs a.k.a. ["賭卡"](https://www.youtube.com/watch?v=cEOyIntYtiU). Also **impossible to send back for repairing because of importing laws.** My current part list there are specific obselete server parts / outlaw hardware mods like [Optane Pmem](https://www.ebay.com/p/24058980642) and [RTX 2080ti 22G](https://2080ti22g.com/). Later I'll hunt for VROC related parts (CPU bifurcation and VROC dongle) and some cheap Optane parts. **You need middle agents unless you are residents there.**|

|Parts|Location|Description|
|---|---|---|
|CPU|Offline deal (user) < xianyu|Sell because of power efficiency (AMD YES) and difficulty to serve as production server (instable under high temperature and power consumption).|
|MB|Offline deal (user) < xianyu|Same deal with CPU. Never thought that PC parts can have heritage.|
|RAM|Offline deal (user + specialist)|2x from the deal with CPU, 6x from recycle specalist. Really lucky because 3200AA RDIMM is rare and I just gathered all of them in local city. Previous 16x 2400T sets are offline deal from another WS user (HP Z840).|
|PMem|xianyu|Caught a new wave of recycled server parts. I thought that they were ES / QS parts, however turns out they are all legit production parts.|
|PSU|dcfever|Straight from RMA, never used. Previous owner bought another PSU (hopefully not mining PSU).|
|PC case|dcfever|Bought for years. I kept this full tower case for "big" builds, and it is.|
|Case fans|dcfever / carousell|Collected across years. Notice that some models are not retailed / discontinued.|
|RAM cooler|taobao|Rare use case, rare parts.|
|SSD|dcfever|Ex mining SSDs. However I'm confident that they only spent < 2PBW given the DWPDs over around an year. Any SSDs with > 2 PBWs are fine, even they have their firmware (SMART) cleared. ~~Thanks for driving enterprise SSDs down after the hype.~~|
|SSD (Optane)|xianyu|Planned. Will be interesting for OS drive under VROC.|
|RGB / cable accessories|"Huaqiangbei" style store / dcfever|Just buy anywhere I can reach. I need them fast.|
|Astolfo figure|Hobby store|In sale.|

|Brand new via store|
|"Brand new second hand"|PSU (from RMA, never used)|
|Second hand (local web platform:  )||