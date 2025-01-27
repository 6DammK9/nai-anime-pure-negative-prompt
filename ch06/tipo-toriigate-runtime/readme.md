Under construction.

- TIPO here points to an [undisclosed dataset](https://discord.com/channels/1027129024054575174/1027407524334411816/1331702641285398529). The gated public version is [KBlueLeaf/danbooru2023-metadata-database](https://huggingface.co/datasets/KBlueLeaf/danbooru2023-metadata-database). *There are 200k delta to my current 2024 set, so I need to think about how to blend 2 approaches.*

- ToriiGate points to directly using this model for caption generation. I will avoid generating files inplace, maybe using the `meta_cap_dd.json` for index tracing, then merge the `meta_lat.json`, then finally generate `1ktar.tar` inplace.
