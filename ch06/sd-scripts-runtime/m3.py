from accelerate import Accelerator
import torchvision.models as models
import library.sdxl_model_util as sdxl_model_util
import library.sdxl_original_unet as sdxl_original_unet
import torch

def main():
    accelerator = Accelerator()

    #It works
    if False:
        model = models.mobilenet_v3_small()
        model.half().to("cuda:0")
        model = accelerator.prepare(model)

    #unet doesn't work. te1 te2 works.
    if False:
        model_version=None
        ckpt_path="F:/NOVELAI/astolfo_mix/sdxl/cmp/x215c-AstolfoMix-24101101-6e545a3.safetensors"
        device='cpu'
        dtype=None
        disable_mmap=False
        #['../model/sdxl1_0.safetensors', 'cpu', None, False]

        text_model1, text_model2, vae, unet, logit_scale, ckpt_info = sdxl_model_util.load_models_from_sdxl_checkpoint(model_version, ckpt_path, device, dtype) #disable_mmap
        unet = accelerator.prepare(unet)
        #text_model1 = accelerator.prepare(text_model1)
        #text_model2 = accelerator.prepare(text_model2)

    #doesn't work unless "some layers are removed" but there is no clear pattern (why?)
    if True:
        unet = sdxl_original_unet.SdxlUNet2DConditionModel()
        p = sum(p.numel() for p in unet.parameters())
        print(p)
        unet.half().to("cuda:0")
        unet = accelerator.prepare(unet)

        #device_ids=[0]
        #output_device=0
        #kwargs={}
        #unet = torch.nn.parallel.DistributedDataParallel(
        #    unet, device_ids=device_ids, output_device=output_device, **kwargs
        #)

#accelerate launch m3.py
if __name__ == "__main__":
    main()
    print(1)
