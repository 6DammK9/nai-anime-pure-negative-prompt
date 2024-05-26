# Chapter 99: Astolfo's CBP Test #

~~It should be fully revamped.~~ Not anymore.

I decided to give it a new purpose: Describing **Astolfo's Car-Backgound-Person test,** my own version of [House-Tree-Persion test](https://practicalpie.com/house-person-tree-test/) towards AI ([CN article](https://baike.baidu.hk/item/%E6%88%BF%E6%A8%B9%E4%BA%BA%E6%B8%AC%E9%A9%97/7660624)). Human projects *personality and subconscious*, AI projects *bias and vaiance*. Before causing controversy about [Turing test](https://en.wikipedia.org/wiki/Turing_test) or self-conscious of AI, *it never reflects on its own. It also can't answer followup quesions*. If you put this test on LLM, it usually unable to express what it has been drawn since it is likely conducted by different networks (e.g. Dall-E to Chat GPT, Imagen to Germini).

It is never meant to be a professional test. You should stick with [AI / ML test](https://arxiv.org/abs/2309.14859), or [CS related aesthetic scoring](https://arxiv.org/abs/2304.05977) as [quantitative test](https://watchthem.live/quantitative-vs-qualitative-testing/). My own qualitative test has been opposed by most community because it is considered subjective and unprofessional towards CS, and sometimes controversial like art issues. [I am the very few who try to link logical conditions with art appreciation, and try to determine the performance of an AI model, without prior on specific ML target.](../ch01/aesthetic.md) Meanwhile, I don't have resources to [fully conduct a test](https://github.com/deepghs/sdeval), to make assessment with nobody cares.

"Car-Backgound-Person test" are spread across this repo, so just try to find them. I want to keep this session clean. [This article may contains most of this "CBP" test.](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch05/xl_docs/r05_x72a.md)

(May explain further) Here is my comparasion of the original HTP test:

|HTP Test|CBP Test|
|---|---|
|House|Background, maybe a real location, or just undefined (AI will spit random but natural content). Should not be targeted to train.|
|Tree|Car, better with a real identity, should not be targeted to train.|
|Person|Person, can be an anime person, may be targeted to train. For my case, Astolfo was trained but never a primary target.|
|150 minutes|Usually 6 hours or more. Around 100 images with large number of steps (256 > 64 hires). Count for [yield](https://en.wikipedia.org/wiki/Crop_yield) and only consider the best few images.|
|Paper, crayon and pencil|Random seeds and parameters. Usually CFG value and STEP. Stable since SDXL.|
|Landscape|Landscape also. I prefer 16:9 to fit screen size, and it is challenging for AI trained with portraits in major.|
|Follow-up questions|It can't answer. Usually just more topics, both trained or not.|
|Project personality and mental state|Project bias and vaiance, or cognitive ability|
|Interaction between subjects|Interaction and anchored location of the subjects. Usually a legit image relies on nice anchored location by chance. See denoise preview for details.|
|Sketching progress|Denoising progress. Available in A1111.|
|Shapes / sizes / colors / lines of subjects|Same, also fragmentation of local areas, expecially intersections (weakness of SD).|
|House: Family relations|Background: Balance between finetuned and pretrained materials|
|Tree: Unconscious aspects|Car: Recall of pretrained materials (can be none!)|
|Person: Symbolic representation|Person: Precision of finetuned materials|
|*Not known yet, kind of personality*|High confidence: Overexposure / halo effect|
|*Not known yet, kind of personality*|Low confidence: Blur / Lack of color, tends to grey / dull green|
|Schizophrenia|Contents fall apart / blend together / fallen into abstract art / return pure noise, even resolution has been lowered. Usually means that the model is broken. TIES merge / some model without quality tag may have this issue.|
|*Not applicable, maybe drawing something violating the test.*|Black screen / Broken color with vague shape. VAE is not working / does not match. Notice that it is not related to model performance.|

### (Old content) My approach on testing a model ###

*It didn't change since. I just don't metion them.*

- NAI / **theory and explanation**: [925997e9.md](./925997e9.md)
- NAI / **Focusing on character**: [astolfo_fate.md](./astolfo_fate.md)
- NAI / **Focusing on object interation**: [astolfo_wrc.md](./astolfo_wrc.md)
- AV3 / **General exploration**: [6569e224.md](./6569e224.md)
- AV3 / **Focusing on character**: [astolfo_v3.md](./astolfo_v3.md)
- NNAI / **General exploration**: [888886dc.md](./888886dc.md)
- NNAI / **Focusing on character**: [astolfo_nnai.md](./astolfo_nnai.md)
