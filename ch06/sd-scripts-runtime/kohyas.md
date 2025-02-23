# Code analysis for kohyas/sd-scripts #

- **This session is dedicated to factcheck when reading to codes. It is crucial to justify the training effect.**

- I use VSCode for the IDE. Its targeted search / text comparaion is cool.

## How "dual tags / caption" will be passed into the model ##

- `--caption_extension` has no effect on "native training", when `--in_json` has been provided (actually it is mandatory!). It only referened in `DreamBoothSubset` and `ControlNetSubset`.

- Meanwhile, that has a "technical debt" which mix up between Dreambooth and "Native train" method. That's why `--in_json` is mandatory.

```py
    use_dreambooth_method = args.in_json is None
```

- When both `caption` and `tags` are provided in `in_json`, user may expect "pick one in random" for training, however in fact **it is just concatenate together**. The `--caption_separator` is configurable: It is just a `,` with no meaning at all. 

- If `subset.caption_separator="\n"` with `--enable_wildcard` and force both `caption` and `tags` as one line will have one picked. However `--caption_separator="\n"` is impossible.

```py
caption = img_md.get("caption")
tags = img_md.get("tags")
if caption is None:
    caption = tags  # could be multiline
    tags = None

if subset.enable_wildcard:
    # tags must be single line
    if tags is not None:
        tags = tags.replace("\n", subset.caption_separator)

    # add tags to each line of caption
    if caption is not None and tags is not None:
        caption = "\n".join(
            [f"{line}{subset.caption_separator}{tags}" for line in caption.split("\n") if line.strip() != ""]
        )
else:
    # use as is
    if tags is not None and len(tags) > 0:
        caption = caption + subset.caption_separator + tags
        tags_list.append(tags)

if caption is None:
    caption = ""
```

- Now I have around 75 + 200 words to dump into the model, which is crazily long, and exceed CLIP model limit (77). Kohyas claimed he use "A1111 token trick". [This is a nice article on some A1111's inventions.](https://zhuanlan.zhihu.com/p/635975479) *(and the origin of this repo!)* [Code reference in A1111.](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/sd_hijack_clip.py#L253)

```py
if max_length > tokenizer.model_max_length:
    input_ids = input_ids.squeeze(0)
    iids_list = []
    if tokenizer.pad_token_id == tokenizer.eos_token_id:
        # v1
        # 77以上の時は "<BOS> .... <EOS> <EOS> <EOS>" でトータル227とかになっているので、"<BOS>...<EOS>"の三連に変換する
        # 1111氏のやつは , で区切る、とかしているようだが　とりあえず単純に
        for i in range(1, max_length - tokenizer.model_max_length + 2, tokenizer.model_max_length - 2):  # (1, 152, 75)
            ids_chunk = (
                input_ids[0].unsqueeze(0),
                input_ids[i : i + tokenizer.model_max_length - 2],
                input_ids[-1].unsqueeze(0),
            )
            ids_chunk = torch.cat(ids_chunk)
            iids_list.append(ids_chunk)
    else:
        # v2 or SDXL
        # 77以上の時は "<BOS> .... <EOS> <PAD> <PAD>..." でトータル227とかになっているので、"<BOS>...<EOS> <PAD> <PAD> ..."の三連に変換する
        for i in range(1, max_length - tokenizer.model_max_length + 2, tokenizer.model_max_length - 2):
            ids_chunk = (
                input_ids[0].unsqueeze(0),  # BOS
                input_ids[i : i + tokenizer.model_max_length - 2],
                input_ids[-1].unsqueeze(0),
            )  # PAD or EOS
            ids_chunk = torch.cat(ids_chunk)

            # 末尾が <EOS> <PAD> または <PAD> <PAD> の場合は、何もしなくてよい
            # 末尾が x <PAD/EOS> の場合は末尾を <EOS> に変える（x <EOS> なら結果的に変化なし）
            if ids_chunk[-2] != tokenizer.eos_token_id and ids_chunk[-2] != tokenizer.pad_token_id:
                ids_chunk[-1] = tokenizer.eos_token_id
            # 先頭が <BOS> <PAD> ... の場合は <BOS> <EOS> <PAD> ... に変える
            if ids_chunk[1] == tokenizer.pad_token_id:
                ids_chunk[1] = tokenizer.eos_token_id

            iids_list.append(ids_chunk)

    input_ids = torch.stack(iids_list)  # 3,77
```

- For SD3 / Flux, nope, just crop for the N tokens (77 for CLIP, 512 for T5XXL).

```py
def tokenize(self, text: Union[str, List[str]]) -> List[torch.Tensor]:
    text = [text] if isinstance(text, str) else text

    l_tokens = self.clip_l(text, max_length=77, padding="max_length", truncation=True, return_tensors="pt")
    g_tokens = self.clip_g(text, max_length=77, padding="max_length", truncation=True, return_tensors="pt")
    t5_tokens = self.t5xxl(text, max_length=self.t5xxl_max_length, padding="max_length", truncation=True, return_tensors="pt")

    l_attn_mask = l_tokens["attention_mask"]
    g_attn_mask = g_tokens["attention_mask"]
    t5_attn_mask = t5_tokens["attention_mask"]
    l_tokens = l_tokens["input_ids"]
    g_tokens = g_tokens["input_ids"]
    t5_tokens = t5_tokens["input_ids"]

    return [l_tokens, g_tokens, t5_tokens, l_attn_mask, g_attn_mask, t5_attn_mask]
```

- `text: Union[str, List[str]]` is almost always `str` (by tracing code).

- I can expect *I will screw up very hard if they are just concatanate together.* "generated long captions following raw tags" will not "finetune" the knowledge well. Currently I swap the sequence as "raw tags following generated long captions". I expect the effect will be minimal, because the string is way too long.

- After a while, I see the *original wildcard* and *line seperator* has been mentioned, with `random.choice`.

```py
if is_drop_out:
    caption = ""
else:
    # process wildcards
    if subset.enable_wildcard:
        # if caption is multiline, random choice one line
        if "\n" in caption:
            caption = random.choice(caption.split("\n"))

        # wildcard is like '{aaa|bbb|ccc...}'
        # escape the curly braces like {{ or }}
        replacer1 = "⦅"
        replacer2 = "⦆"
        while replacer1 in caption or replacer2 in caption:
            replacer1 += "⦅"
            replacer2 += "⦆"

        caption = caption.replace("{{", replacer1).replace("}}", replacer2)

        # replace the wildcard
        def replace_wildcard(match):
            return random.choice(match.group(1).split("|"))

        caption = re.sub(r"\{([^}]+)\}", replace_wildcard, caption)

        # unescape the curly braces
        caption = caption.replace(replacer1, "{").replace(replacer2, "}")
    else:
        # if caption is multiline, use the first line
        caption = caption.split("\n")[0]
```

- Maybe we just don't "use as is". And... patch the 14GB `meta_lat.json`.

```py
if subset.enable_wildcard:
    # tags must be single line
    if tags is not None:
        tags = tags.replace("\n", subset.caption_separator)

    # add tags to each line of caption
    if caption is not None and tags is not None:
        #caption = "\n".join(
        #    [f"{line}{subset.caption_separator}{tags}" for line in caption.split("\n") if line.strip() != ""]
        #)
        caption = "\n".join(
            [f"{tags}\n{line}" for line in caption.split("\n") if line.strip() != ""]
        )
else:
    # use as wildcard please
    if tags is not None and len(tags) > 0:
        #caption = caption + subset.caption_separator + tags
        caption = tags + "\n" + caption
        #caption = "{" + caption + "|" + tags + "}"
        tags_list.append(tags)
```

- After testing both `f"{tags}\n{caption}"` and `f"{tags},{caption}"`, they works as intended. Benefited from  "A1111 token trick", concatenate both strings (sequence shouldn't matter) will *learn concepts in a more precise way*. Paper ["Understanding and Mitigating Copying in Diffusion Models"](https://arxiv.org/abs/2305.20086) has discussed the "bias and variance tradeoff" between text contents and image contents for such T2I task.

## Fundamental dataset / training configurations ##

- *Obviously dataset will be shuffled.* Set seed for reproducible result.

```py
if args.seed is None:
    args.seed = random.randint(0, 2**32)
set_seed(args.seed)  # 乱数系列を初期化する
```

```py
train_dataloader = torch.utils.data.DataLoader(
    train_dataset_group,
    batch_size=1,
    shuffle=True,
    collate_fn=collator,
    num_workers=n_workers,
    persistent_workers=args.persistent_data_loader_workers,
)
```

## Support in various memory-efficient plugins ##

- *Tested in Linux only. Expect Windows requires custom wheels.*

- Kohyas use [accelerator](https://huggingface.co/docs/accelerate/package_reference/accelerator) as the trainer framework. *Any related topics can be applied with code patching, disregarding the lack of discussion in community.* Notice that NaifuDuffusion use [PyTorch Lightening](https://lightning.ai/docs/pytorch/stable/) which requires its own implementation of the following libraries (hint: the URLs are under huggingface)

- To enable the extensions below, you need to [configure the accelerate](https://huggingface.co/docs/accelerate/package_reference/cli) **by ignoring most community guides** and [enable the corrosponding options](https://github.com/kohya-ss/sd-scripts/blob/sd3/library/train_util.py#L3781) in the trainer. **There is no direct guide at all.** I need to investigate myself. ~~To test the results, there are no shortcuts: Keep train and eval.~~

- [xformers](https://huggingface.co/docs/diffusers/optimization/xformers) is widely used, especially for runtime also. Somehow it has been **disabled in UNET module.** It hints on other options.

```py
# モデルに xformers とか memory efficient attention を組み込む
if args.diffusers_xformers:
    # もうU-Netを独自にしたので動かないけどVAEのxformersは動くはず
    accelerator.print("Use xformers by Diffusers")
    # set_diffusers_xformers_flag(unet, True)
    set_diffusers_xformers_flag(vae, True)
else:
    # Windows版のxformersはfloatで学習できなかったりするのでxformersを使わない設定も可能にしておく必要がある
    accelerator.print("Disable Diffusers' xformers")
    train_util.replace_unet_modules(unet, args.mem_eff_attn, args.xformers, args.sdpa)
    if torch.__version__ >= "2.0.0":  # PyTorch 2.0.0 以上対応のxformersなら以下が使える
        vae.set_use_memory_efficient_attention_xformers(args.xformers)
```

- [Flash Attention](https://huggingface.co/docs/text-generation-inference/conceptual/flash_attention) in also widly used, however it is lack of disussion in trainers.

- [Dynamo Backend](https://huggingface.co/docs/accelerate/package_reference/accelerator#accelerate.Accelerator.dynamo_backend) is less discussed. [It is supported from the pyTorch layer](https://pytorch.org/TensorRT/tutorials/_rendered_examples/dynamo/torch_compile_stable_diffusion.html) but there is no discussion ever since.

- Must add `--torch_compile` and `--dynamo_backend=inductor` to enable.

```py
# torch.compile のオプション。 NO の場合は torch.compile は使わない
dynamo_backend = "NO"
if args.torch_compile:
    dynamo_backend = args.dynamo_backend
```

- [Deepspeed](https://huggingface.co/docs/accelerate/usage_guides/deepspeed) is widely discussed outside the SD community, especially it is quite promising in [pytorch lightening](https://lightning.ai/pages/community/serve-stable-diffusion-three-times-faster/).

- Refer to [deepspeed_utils.py](https://github.com/kohya-ss/sd-scripts/blob/main/library/deepspeed_utils.py)

- Must add `--deepspeed` to enable. Also must match all configurations with the `accelerate config`.

```py
deepspeed_plugin = DeepSpeedPlugin(
    zero_stage=args.zero_stage,
    gradient_accumulation_steps=args.gradient_accumulation_steps,
    gradient_clipping=args.max_grad_norm,
    offload_optimizer_device=args.offload_optimizer_device,
    offload_optimizer_nvme_path=args.offload_optimizer_nvme_path,
    offload_param_device=args.offload_param_device,
    offload_param_nvme_path=args.offload_param_nvme_path,
    zero3_init_flag=args.zero3_init_flag,
    zero3_save_16bit_model=args.zero3_save_16bit_model,
)
```
