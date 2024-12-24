```sh
git checkout sd3
```

- `torch==2.3.1+cu124` doesn't exist.

- Fallback to `bitsandbytes==0.44.0` but `python -m bitsandbytes` still works.

- Modified `accelerate/default_config.yaml` to run `MULTI_GPU` with 1 GPU only.

- Dataset is 10 images so it will be easy. Somehow `*.npz` is not present. Should not be a problem. OOM = success.

```sh
python ./finetune/merge_dd_tags_to_metadata.py "../dataset/kohyas_finetune" "../dataset/meta_cap_dd.json"
python ./finetune/prepare_buckets_latents.py "../dataset/kohyas_finetune" "../dataset/meta_cap_dd.json" "../dataset/meta_lat.json" "../model/215c.safetensors" --batch_size 1 --max_resolution 1024,1024 --mixed_precision fp16
```

- switch `accelerate launch` to `python` should OOM. BTW it still use around 32GB of RAM.

```sh
accelerate launch
    sdxl_train.py                                                                                                               
    --pretrained_model_name_or_path="../model/sdxl1_0.safetensors"      
    --in_json "../dataset/meta_lat.json"                                                                                 
    --train_data_dir="../dataset/kohyas_finetune"                                                                        
    --output_dir="../train_result/model_out"                                                                                    
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                                             
    --train_batch_size=1 --learning_rate=1e-5 --max_train_epochs=10                                                             
    --train_text_encoder                                                                                                        
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    
    --mixed_precision=fp16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                             
    --save_every_n_epochs=5  
```

- After fixing `libuv`, fix [state.py](https://github.com/huggingface/accelerate/blob/main/src/accelerate/state.py#L737) and [accelerator.py](https://github.com/huggingface/accelerate/blob/main/src/accelerate/accelerator.py#L432) with `backend="gloo"`.

- Now here comes the exact same `RuntimeError: Trying to create tensor with negative dimension -1727503612: [-1727503612]`. [Here is a similar issue.](https://github.com/InternLM/InternLM-XComposer/issues/352). [Looks like there is literally no support on windows.](https://github.com/huggingface/accelerate/issues/3026)

- PoC created. More complicated. It points to [this issue](https://github.com/pytorch/pytorch/issues/68407), and [torch.nn.Module.register_buffer](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.register_buffer), and [torch.nn.parallel.DistributedDataParallel](https://pytorch.org/docs/stable/notes/ddp.html)