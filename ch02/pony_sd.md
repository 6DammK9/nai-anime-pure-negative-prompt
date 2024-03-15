# Observation of Pony Diffusion (v5.5 SD2.1 + V6 SDXL) #

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
- However, with **super high learning rate**, and **some fallacy on tagging**, it shifted the model weight great enough to make it unusuable with any SD related tools, *including ControlNet.*
- Merging / training LoRA on top of it will be only applicable to its variant, and outputing *pure noise* when mating with other (mainstream) models.

Following images are referenced to [ch05](../ch05/README_XL.MDs), model components are compared with ovr manner (average of a model pool):

`_212` as V5.5

![xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg](../ch05/img/xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg)

`_x14` as V6

![xyz_grid-0759-755545524-20160-1438-4.5-48-20240227220718.jpg](../ch05/img/xyz_grid-0759-755545524-20160-1438-4.5-48-20240227220718.jpg)

- The recent "pony merge" is not totally false / fake, it becomes possible because **the downstream finetunes are using general techniques** (e.g. taggers common with AnimagineXL V3 / kohakuXL), and shifting the model weights into a more common space.

`_x48`, `_x50` as V6's downstream finetunes

![xyz_grid-0730-755545524-20160-1446-4.5-48-20240220073619.jpg](../ch05/img/xyz_grid-0730-755545524-20160-1446-4.5-48-20240220073619.jpg)

![xyz_grid-0762-755545524-24192-1438-4.5-48-20240227230419.jpg](../ch05/img/xyz_grid-0762-755545524-24192-1438-4.5-48-20240227230419.jpg)

### Why the "hash" seems so short? ###

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

- [Live spreadsheet](https://lite.framacalc.org/4ttgzvd0rx-a6jf), and [an archived CSV](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch02/1710391046.csv) ~~Github support CSV view like PowerBI?~~

> houshou marine found as a 'hash' in aua, possibly incomplete

<details>
    <summary>Click to open.</summary>

![xyz_grid-0000-3788460102.png](./img/xyz_grid-0000-3788460102.png)

</details>

### Why even it is claimed encryption / obfusciation, it is still looks like a hash? ###

- Under BPE / CLIP has already introduced information loss as embeddings / vectors, it *implies* to a kind of hashing.

- Predecending step can be arbitary to have a "hash like" feel, since *collision* occurs in embedding level, instead of prompt level. This is a kind of [prompt injection](https://www.robustintelligence.com/blog-posts/prompt-injection-attack-on-gpt-4), which yields "coincidence" and introducing undesired effect.

- PDv6 is claimed **artist name is not deleted nor hashed**, instead it is encrypted by [XOR](https://en.wikipedia.org/wiki/Exclusive_or) + [ROT-42](https://en.wikipedia.org/wiki/Caesar_cipher)

![24031501.jpg](./img/24031501.jpg)

- And... [a random screenshot has been provided.](https://medium.com/@kristiyan.velkov/meet-devin-the-worlds-first-ai-software-engineer-f0c35f221bdd)

![AJOLkbt.jpeg](https://i.imgur.com/AJOLkbt.jpeg)

- Given ciphertext "aua" and plaintext "houshou_marin" is provided, *encryption algorithm* may be deduced:

~~I decided to include this updated session because I really think that the claims are plausible, especially the fallacy about embedding has already rooted in this model.~~
