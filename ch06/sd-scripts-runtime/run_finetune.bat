set USE_LIBUV=0

accelerate launch --num_processes=2 --multi_gpu --num_machines=1 --gpu_ids=0,1 --num_cpu_threads_per_process=8 sdxl_train.py    ^
    --pretrained_model_name_or_path="F:/NOVELAI/astolfo_mix/sdxl/cmp/x215c-AstolfoMix-24101101-6e545a3.safetensors"             ^
    --in_json "H:/just_astolfo/meta_lat.json"                                                                                   ^
    --train_data_dir="H:/just_astolfo/kohyas_finetune"                                                                          ^
    --output_dir="F:/NOVELAI/astolfo_xl/just_astolfo/model_out"                                                                 ^
    --log_with=tensorboard                                                                                                      ^
    --logging_dir="F:/NOVELAI/astolfo_xl/just_astolfo/tensorboard"                                                              ^
    --log_prefix=just_astolfo_24120801_                                                                                         ^
    --save_model_as=safetensors                                                                                                 ^
    --caption_extension=".txt"                                                                                                  ^
    --use_8bit_adam                                                                                                             ^
    --train_batch_size=1 --learning_rate=1e-5 --max_train_epochs=6                                                              ^
    --train_text_encoder                                                                                                        ^
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    ^
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    ^
    --enable_bucket --cache_latents                                                                                             ^
    --save_every_n_epochs=1                                                                                                     ^