export OMP_NUM_THREADS=4
export CUDA_VISIBLE_DEVICES=0
accelerate launch --num_cpu_threads_per_process=8 sdxl_train.py --pretrained_model_name_or_path="G:/x1a-AstolfoVL-2_5ep.safetensors" --in_json "H:/just_astolfo/meta_lat.json" --train_data_dir="H:/just_astolfo/kohyas_finetune" --output_dir="G:/model_out" --log_with=tensorboard --logging_dir="G:/tensorboard" --log_prefix=just_astolfo_26022301_ --seed=26022301 --save_model_as=safetensors --caption_extension=".txt" --enable_wildcard --use_8bit_adam --learning_rate="1e-5" --flow_model --flow_uniform_shift --contrastive_flow_matching --max_train_epochs=10 --xformers --pin_memory --gradient_checkpointing --gradient_accumulation_steps=4 --max_grad_norm=0 --max_data_loader_n_workers=8 --persistent_data_loader_workers --train_batch_size=1 --full_bf16 --mixed_precision=bf16 --save_precision=fp16 --enable_bucket --cache_latents --skip_cache_check --save_every_n_epochs=3
#accelerate launch --num_cpu_threads_per_process=8 sdxl_train_v2.py

#--train_text_encoder --learning_rate_te1="1e-5" --learning_rate_te2="1e-5" 
#--save_every_n_steps=10000 --skip_until_initial_step --initial_step=320000
#--deepspeed --mem_eff_attn --torch_compile --dynamo_backend=inductor 
#--initial_epoch=1
#numactl --cpunodebind=1 --membind=1 
#--enable_profiler

#--v_parameterization --zero_terminal_snr --min_snr_gamma=5
#--flow_timestep_distribution="logit_normal" --flow_logit_mean=0.0 --flow_logit_std=1.0 --flow_uniform_static_ratio=3.0 --cfm_lambda=0.05

#--optimizer_type "pytorch_optimizer.CAME" --optimizer_args "weight_decay=1e-2"
#--optimizer_type="pytorch_optimizer.Lion" --optimizer_args="weight_decay=1e-2" "cautious=True"
#--optimizer_type="Lion8bit" "weight_decay=1e-2"
#--optimizer_type="AdaFactor" --optimizer_args "relative_step=False" "clip_threshold=1.0" "weight_decay=1e-2"
#--optimizer_type="AdaFactor" --optimizer_args "relative_step=True" "warmup_init=True" "weight_decay=1e-2"

#7x7=50-1