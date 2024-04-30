# Observation of Pony Diffusion (v5.5 SD2.1 + V6 SDXL) #

## (New) Official notice on Pony V7 ##

- [Towards Pony Diffusion V7](https://civitai.com/articles/5069)

## Red pill from 4chan ##

- [ponyxl_loras_n_stuff](https://rentry.org/ponyxl_loras_n_stuff)
- [ponyxl_lora_previews](https://rentry.org/ponyxl_lora_previews) 
- [4ttgzvd0rx-a6jf](https://lite.framacalc.org/4ttgzvd0rx-a6jf) The spreadsheet.

## Thank you for writing the draft ##

- I don't have QQ. Therefore I won't care if my "observation" will collapse the "wave function" ~~eliminate superposition a.k.a confusion~~ there.

- [Original weibo post.](https://weibo.com/7152334518/O4SGtsI7K)

- [The referenced 4chan post.](https://boards.4chan.org/h/thread/7883612)

- [Discord post 1.](https://discord.com/channels/1077510466470952990/1109884866964754644/1217145257288794163), [Discord post 2.](https://discord.com/channels/930499730843250783/1019446913268973689/1217091897697505310)

![24031401.PNG](./img/24031401.PNG)

![24031402.PNG](./img/24031402.PNG)

## More to come. ##

### Why CivitAI made Pony model as a distinct category? ###

- As written in title, **they are all in unaltered SD archetiture**. Unlike [Fluffusion](https://rentry.co/fluffusion), which is SD1.5 + vpred, pony diffusion doesn't do it to the extreme.
- However, with **super high learning rate**, and **some fallacy on tagging** ([CivitAI article on claimed tagging approach](https://civitai.com/articles/4248)), it shifted the model weight great enough to make it unusuable with any SD related tools, *including ControlNet.*
- Merging / training LoRA on top of it will be only applicable to its variant, and outputing *pure noise* when mating with other (mainstream) models.

Following images are referenced to [ch05](../ch05/README_XL.MDs), model components are compared with ovr manner (average of a model pool):

`_212` as V5.5

![xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg](../ch05/img/xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg)

`_x14` as V6

![xyz_grid-0759-755545524-20160-1438-4.5-48-20240227220718.jpg](../ch05/img/x52a/xyz_grid-0759-755545524-20160-1438-4.5-48-20240227220718.jpg)

- The recent "pony merge" is not totally false / fake, it becomes possible because **the downstream finetunes are using general techniques** (e.g. taggers common with AnimagineXL V3 / kohakuXL), and shifting the model weights into a more common space. [T-ponynai3](https://civitai.com/models/317902/t-ponynai3) and [AutismMix SDXL](https://civitai.com/models/288584/autismmix-sdxl) are nice example.

`_x48`, `_x50` as V6's downstream finetunes

![xyz_grid-0730-755545524-20160-1446-4.5-48-20240220073619.jpg](../ch05/img/x49a/xyz_grid-0730-755545524-20160-1446-4.5-48-20240220073619.jpg)

![xyz_grid-0762-755545524-24192-1438-4.5-48-20240227230419.jpg](../ch05/img/x52a/xyz_grid-0762-755545524-24192-1438-4.5-48-20240227230419.jpg)

### (240405) So is the "hash" legit? ### 

- *It is just random prompt injectgion / token collision.* Continue to read for verification. The claim from the author is verified **not related, or not directly related to the actual model.**

- [My attempt for the "hash".](https://www.pixiv.net/en/artworks/117451812) *It is Ubhfubh Znevar va Fnxvzvpuna fglyr (ROT13).*

### Why it looks like "hash" but not being an algorithm? ###

- It is simple: prompts are digested into embeddings by [BPE](https://huggingface.co/learn/nlp-course/chapter6/5). [Live demo straight from NovelAI.](https://novelai.net/tokenizer).
- Its *quality tagging* is actaully messed up after BPE, and **such tagging is applied across 2.6M of images.**

![24031403.PNG](./img/24031403.PNG)

- With the **super high learning rate** ("100x" from a value not referenced yet), it does the *perfect score* by *outputing pure noise* with any pinch of oridinary prompts.

![24031404.png](./img/24031404.png)
  
- With same technique applied, even legit hash is applied (see code block below), **BPE will break the hashes into "subwords" which are obviously short enough to have collision.**

```
Name: 24031403.PNG
Size: 32155 bytes (31 KiB)
CRC32: 44C28C62
CRC64: 81A4ABBD85D9E8B0
SHA256: 3C52AB236D77964B64DD4736BE8BE742AA6BCBA371476AF151CFD06BE11CF759
SHA1: BD2D832A3A2B3B99B2793BFDA04D9C8A48A71788
BLAKE2sp: 3E609B081A24C516DE51D9EE4BF85D5DE8B610FCA4787CAAAD052767D1180529
```

- Base64 for some random action:

```
CRC32: RMKMYg==
CRC64: gaSrvYXZ6LA=
SHA256: PFKrI213lktk3Uc2vovnQqpry6NxR2rxUc/Qa+Ec91k=
SHA1: vS2DKjorO5myeTv9oE2cikinF4g=
BLAKE2sp: PmCbCBokxRbeUdnuS/hdXei2EPykeHyqrQUnZ9EYBSk=
```

- [Live spreadsheet](https://lite.framacalc.org/4ttgzvd0rx-a6jf), [official CSV link](https://lite.framacalc.org/4ttgzvd0rx-a6jf.csv) and [an archived CSV in ROT-13](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch02/1710739486.csv) ~~Github support CSV view like PowerBI?~~

- For example, Houshou Marine becomes `aua` (1 token) and sakimichan (-ish) style becomes `iwv`, `zix`, `px` and `smp` (3-4 tokens, any of them are fine).

### Why it is not what the author claimed, encryption / obfusciation, or hash? ###

- Under BPE / CLIP has already introduced information loss as embeddings / vectors, it *implies* to a kind of hashing.

- Predecending step can be arbitary to have a "hash like" feel, since *collision* occurs in embedding level, instead of prompt level. This is a kind of [prompt injection](https://www.robustintelligence.com/blog-posts/prompt-injection-attack-on-gpt-4), which yields "coincidence" and introducing undesired effect.

- PDv6 is claimed **artist name is not deleted nor hashed**, instead it is encrypted by [XOR](https://en.wikipedia.org/wiki/Exclusive_or) + [ROT-42](https://en.wikipedia.org/wiki/Caesar_cipher)

![24031501.jpg](./img/24031501.jpg)

- And... [a random screenshot has been provided.](https://medium.com/@kristiyan.velkov/meet-devin-the-worlds-first-ai-software-engineer-f0c35f221bdd)

![AJOLkbt.jpeg](https://i.imgur.com/AJOLkbt.jpeg)

- Quick PoC (wanted to OCR it for integrity, but it is too blury and I used different implementation): [rot42_xor.py](./rot42_xor.py) ~~Can make a 1-liner version~~

```log
>python rot42_xor.py houshou_marine  
xekixek_cqhydu
1E♠♫K/♀▼☺∟↨Y
```

- Given ciphertext "aua" and plaintext "houshou_marin" is provided, the *encryption algorithm* **does not match the claim**. Direct prompting the cipher text will yield complete random images (the "girl" is the bias of the PDv6, a few more seeds will see no human-focused images).

- Instead, given the discovered "single token prompts" and the nature of BPE, random characters may form clusters because of their super low frequency, and the cluster may share high [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) (*or low distince between embeddings*) to the actual [unconditioned / "unprompted" contents](https://huggingface.co/docs/diffusers/main/en/api/pipelines/latent_diffusion_uncond). It is a [side effect](https://en.wikipedia.org/wiki/Side_effect) of finetuning / pretraining SD models.
