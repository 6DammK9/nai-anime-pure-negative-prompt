export OMP_NUM_THREADS=4
accelerate launch --num_cpu_threads_per_process=8 sdxl_train_v2.py --pretrained_model_name_or_path="/run/media/user/Intel P4510 3/astolfo_xl/x255c-AstolfoMix-25022801-1458190.safetensors" --in_json "/run/media/user/Intel P4510 3/just_astolfo/meta_lat_v3.json" --train_data_dir="/run/media/user/Intel P4510 3/just_astolfo/kohyas_finetune" --output_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/model_out" --log_with=tensorboard --logging_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/tensorboard" --log_prefix=just_astolfo_25031505_ --seed=25031501 --save_model_as=safetensors --caption_extension=".txt" --enable_wildcard --use_8bit_adam --learning_rate="1.5e-6" --train_text_encoder --learning_rate_te1="1.2e-5" --learning_rate_te2="1.2e-5" --max_train_epochs=10 --xformers --pin_memory --gradient_checkpointing --gradient_accumulation_steps=4 --max_grad_norm=0 --max_data_loader_n_workers=8 --persistent_data_loader_workers --train_batch_size=1 --full_bf16 --mixed_precision=bf16 --save_precision=fp16 --enable_bucket --cache_latents --skip_cache_check --save_every_n_epochs=1
#--optimizer_type "pytorch_optimizer.CAME" --optimizer_args "weight_decay=1e-2"
#--optimizer_type="pytorch_optimizer.Lion" --optimizer_args="weight_decay=1e-2" "cautious=True"
#--optimizer_type="Lion8bit" "weight_decay=1e-2"
#--optimizer_type="AdaFactor" --optimizer_args "relative_step=False" "clip_threshold=1.0" "weight_decay=1e-2"
#--optimizer_type="AdaFactor" --optimizer_args "relative_step=True" "warmup_init=True" "weight_decay=1e-2"
#--optimizer_type="AdamW4bit" --optimizer_args "weight_decay=1e-2"
#--optimizer_type="AdamW8bit" --optimizer_args "weight_decay=1e-2"
#--use_8bit_adam 
#--deepspeed --mem_eff_attn --torch_compile --dynamo_backend=inductor 
#--skip_until_initial_step --initial_step=1 --initial_epoch=1
#numactl --cpunodebind=1 --membind=1 