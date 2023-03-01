# Prompt Dystopia #

- [Full discussion (Chinese) (I have no time to paraphase and translate)](https://discord.com/channels/1033769426216046622/1033771987450994718/1077260057743462472)

### TLDR (may not factual, I'm not NLP expert)  ###

- **READ THE CODE! I WILL NOT EXPLAIN!** [THE CLIP hack in WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/sd_hijack_clip.py)
- **READ THE CLIP implementation also!** [The CLIP being hacked](https://huggingface.co/transformers/v4.8.0/model_doc/clip.html)
- **Extensive experiment!**
- To make it as simple as possible, I just use `(bad:0),(xxx:0)`. ~~Also I wrote this as I learnt from the discussion above, which I may change it.~~
- Prompt weight is performed **after transformation in Text Encoder**. e.g. `['bad' * 0|',' * 1|'xxx' *0]`.
- Position embedding in CLIP **is not preserved**. i.e. `',' * 1` contains information from both `bad` and `xxx` (without `* 0`).
- CLIP is trained **without masking token** i.e. `['bad'|','|'xxx'|EOS * till 77 tokens]`. Note: This is for **trained material**. GG.
- Now your prompt is a bit weaken: `['bad' * 0|',' * 1|'xxx' * 0|EOS * till 77 tokens]`. Then information of the "neutralized" `bad` and `xxx` is still spread to all 77 tokens.
- The "grammar / vocabulary" learnt from CLIP **is pretrained and frozen** (unless the broken Dreambooth "TTE" models). It is "natural", as [BPE](https://en.wikipedia.org/wiki/Byte_pair_encoding). 
- Therefore, `bad_hands` are just treated `[bad|_|hands]` and all 3 tokens are treated "individually as each token in its all possible combinations with neighours", which tends to be `bad` + `hands`. So `bad` already includes most of `bad_xxx` in Danbooru tags. 
- So called "prompt averaging"... is `np.mean` on the output. Pray for you [embeddings](https://www.tensorflow.org/text/guide/word_embeddings) are non-zero mean.
- "Batch of 77 tokens" (workaround for Asian style super long prompts) is another `np.mean`. **Your prompts may annihilate each other**.
- Negative prompt... "yeah somehow it works". Actually the definition of "empty set" is confusing here. All `EOS` (padding) or just vector `0`?
- Then my prompt is short as hell (to minimize the risk). *Or just follow the meta: keep playing the models itself.*

### Some test cases ###

- You may test with postive prompt only. But I prefer "not bad" (most scattered images are prevented, showing legit contents).

- Fill all 77 tokens! Try adjust `(,:1.5)` with exponential scale around 1.
- Assume the prompt below is shorten as `bad(0,1.5)`. Try `bad(0,{0.5, 0.707, 1, 1.414, 2})` and `bad(0.2, {1, 1.414})` ("std") for the differences.  

```
(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)(,:1.5)(bad:0)
```

- From the original 18 long words, to my own single word (down to token).

```
(bad:0), (comic:0), (cropped:0), (error:0), (extra:0), (low:0), (lowres:0), (speech:0), (worst:0)
```

- Pure color block (`bad(0,0)`)

```
(_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_:0)
```

### Image to make it not 100% boring ###

- `bad(0.2, 1.2)`

![img/07248-2023-02-21_89d59c3dde_NAI-latest-ema-only_3448857685-704x512.png](img/07248-2023-02-21_89d59c3dde_NAI-latest-ema-only_3448857685-704x512.png)
