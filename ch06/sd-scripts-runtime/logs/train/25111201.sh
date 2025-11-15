export OMP_NUM_THREADS=4
accelerate launch --num_cpu_threads_per_process=8 sdxl_train_v2.py --pretrained_model_name_or_path="/run/media/user/Intel P4510 3/astolfo_xl/x10a-AstolfoKarmix-25083001-3e3aea3.safetensors" --in_json "/run/media/user/Intel P4510 3/just_astolfo/meta_lat.json" --train_data_dir="/run/media/user/Intel P4510 3/just_astolfo/kohyas_finetune" --output_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/model_out" --log_with=tensorboard --logging_dir="/run/media/user/Intel P4510 3/astolfo_xl/just_astolfo/tensorboard" --log_prefix=just_astolfo_25111201_ --seed=25111201 --save_model_as=safetensors --caption_extension=".txt" --enable_wildcard --use_8bit_adam --learning_rate="1.5e-6" --v_parameterization --zero_terminal_snr --max_train_epochs=10 --xformers --pin_memory --gradient_checkpointing --gradient_accumulation_steps=4 --max_grad_norm=0 --max_data_loader_n_workers=8 --persistent_data_loader_workers --train_batch_size=1 --full_bf16 --mixed_precision=bf16 --save_precision=fp16 --enable_bucket --cache_latents --skip_cache_check --save_every_n_epochs=1
#--train_text_encoder --learning_rate_te1="1.2e-5" --learning_rate_te2="1.2e-5"
#--min_snr_gamma=5
#--save_every_n_steps=10000 --skip_until_initial_step --initial_step=320000
#--deepspeed --mem_eff_attn --torch_compile --dynamo_backend=inductor 
#--initial_epoch=1
#numactl --cpunodebind=1 --membind=1 
#--enable_profiler