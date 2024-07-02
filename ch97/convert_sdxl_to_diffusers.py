# Still working on 240702: https://github.com/Linaqruf/sdxl-model-converter/blob/main/convert_sdxl_to_diffusers.py
# kohya-ss/sd-scripts is required.
# Will save as model_path/model_name/
# python convert_sdxl_to_diffusers.py --save_precision_as=fp16 --model_to_load="F:/NOVELAI/astolfo_mix/sdxl/x116a-AstolfoMix-24060702-01823a9.safetensors"
# Upload all the files into the root directory of the repo is fine. Make sure you have add the header section of the README.MD to enable the widget.
# Example of the README: https://huggingface.co/6DammK9/AstolfoMix-XL/blob/main/README.md

import argparse
import os
import torch
from diffusers import StableDiffusionXLPipeline
import library.sdxl_model_util as sdxl_model_util

def convert_model(args):
    load_dtype = torch.float16 if args.fp16 else None
    save_dtype = get_save_dtype(args)

    is_load_checkpoint = determine_load_checkpoint(args.model_to_load)
    is_save_checkpoint = not is_load_checkpoint  # reverse of load model

    loaded_model_data = load_sdxl_model(args, is_load_checkpoint, load_dtype)
    convert_and_save_sdxl_model(args, is_save_checkpoint, loaded_model_data, save_dtype)

def get_save_dtype(args):
    if args.save_precision_as == "fp16":
        return torch.float16
    elif args.save_precision_as == "bf16":
        return torch.bfloat16
    elif args.save_precision_as == "float":
        return torch.float
    else:
        return None

def determine_load_checkpoint(model_to_load):
    if model_to_load.endswith('.ckpt') or model_to_load.endswith('.safetensors'):
        return True
    elif os.path.isdir(model_to_load):
        required_folders = {"unet", "text_encoder", "text_encoder_2", "tokenizer", "tokenizer_2", "scheduler", "vae"}
        if required_folders.issubset(set(os.listdir(model_to_load))) and os.path.isfile(os.path.join(model_to_load, "model_index.json")):
            return False
    return None  # handle this case as required

def load_sdxl_model(args, is_load_checkpoint, load_dtype):
    model_load_message = "checkpoint" if is_load_checkpoint else "Diffusers" + (" as fp16" if args.fp16 else "")
    print(f"Loading {model_load_message}: {args.model_to_load}")

    if is_load_checkpoint:
        loaded_model_data = load_from_sdxl_checkpoint(args)
    else:
        loaded_model_data = load_sdxl_from_diffusers(args, load_dtype)

    return loaded_model_data

def load_from_sdxl_checkpoint(args):
    text_encoder1, text_encoder2, vae, unet, _, _ = sdxl_model_util.load_models_from_sdxl_checkpoint(
        "sdxl_base_v1-0", args.model_to_load, "cpu"
    )
    return text_encoder1, text_encoder2, vae, unet

def load_sdxl_from_diffusers(args, load_dtype):
    pipeline = StableDiffusionXLPipeline.from_pretrained(
        args.model_to_load, torch_dtype=load_dtype, tokenizer=None, tokenizer_2=None, scheduler=None
        )
    text_encoder1 = pipeline.text_encoder
    text_encoder2 = pipeline.text_encoder_2
    vae = pipeline.vae
    unet = pipeline.unet
  
    return text_encoder1, text_encoder2, vae, unet

def convert_and_save_sdxl_model(args, is_save_checkpoint, loaded_model_data, save_dtype):
    text_encoder1, text_encoder2, vae, unet = loaded_model_data
    model_save_message = "checkpoint" + ("" if save_dtype is None else f" in {save_dtype}") if is_save_checkpoint else "Diffusers"
    print(f"Converting and saving as {model_save_message}: {args.model_to_save}")

    if is_save_checkpoint:
        save_sdxl_as_checkpoint(args, text_encoder1, text_encoder2, vae, unet, save_dtype)
    else:
        save_sdxl_as_diffusers(args,  text_encoder1, text_encoder2, vae, unet, save_dtype)

def save_sdxl_as_checkpoint(args, text_encoder1, text_encoder2, vae, unet, save_dtype):
    logit_scale = None
    ckpt_info = None

    key_count = sdxl_model_util.save_stable_diffusion_checkpoint(
        args.model_to_save, text_encoder1, text_encoder2, unet, args.epoch, args.global_step, ckpt_info, vae, logit_scale, save_dtype
        )
    print(f"Model saved. Total converted state_dict keys: {key_count}")

def save_sdxl_as_diffusers(args, text_encoder1, text_encoder2, vae, unet, save_dtype):
    reference_model_message = args.reference_model if args.reference_model is not None else 'default model'
    print(f"Copying scheduler/tokenizer config from: {reference_model_message}")
    sdxl_model_util.save_diffusers_checkpoint(
        args.model_to_save, text_encoder1, text_encoder2, unet, args.reference_model, vae, True, save_dtype
    )
    print(f"Model saved as {save_dtype}.")

def get_save_path(args, is_save_checkpoint):
    basename = os.path.splitext(args.model_to_load)[0]
    if is_save_checkpoint:
        return increment_filename(basename)
    else:
        return increment_filename(basename + ".safetensors")

def increment_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}({counter}){ext}"
        counter += 1
    return filename

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fp16", action="store_true", help="load as fp16 (Diffusers only)")
    parser.add_argument("--save_precision_as", type=str, default="no", choices=["fp16", "bf16", "float"], help="save precision")
    parser.add_argument("--epoch", type=int, default=0, help="epoch to write to checkpoint")
    parser.add_argument("--global_step", type=int, default=0, help="global_step to write to checkpoint")
    parser.add_argument("--reference_model", type=str, default=None, help="reference Diffusers model to copy scheduler/tokenizer config from, used when saving as Diffusers format, default is `runwayml/stable-diffusion-v1-5` or `stabilityai/stable-diffusion-2-1`")
    parser.add_argument("--model_to_load", type=str, required=True, help="model to load: checkpoint file or Diffusers model's directory")
    return parser

if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    args.model_to_save = get_save_path(args, determine_load_checkpoint(args.model_to_load))
    convert_model(args)
