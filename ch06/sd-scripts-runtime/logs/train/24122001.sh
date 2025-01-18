accelerate launch --num_cpu_threads_per_process 4
    fine_tune.py                                                                                                               
    --pretrained_model_name_or_path="E:/astolfo_xl/just_astolfo/model_out_24122001/epoch-000005-05.safetensors"             
    --in_json "F:/just_astolfo/meta_lat_sd1.json"                                                                                   
    --train_data_dir="F:/just_astolfo/kohyas_finetune_sd1"                                                                          
    --output_dir="F:/astolfo_xl/just_astolfo/model_out_24122001"                                                        
    --log_with=tensorboard                                                                                                      
    --logging_dir="E:/astolfo_xl/just_astolfo/tensorboard"                                                              
    --log_prefix=just_astolfo_24122001_                                                                                         
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                               
    --train_batch_size=1 --learning_rate=1e-5 --max_train_epochs=5   
    --v2 --v_parameterization --min_snr_gamma=5 --zero_terminal_snr   
    --max_data_loader_n_workers 2                                                                                                       
    --xformers --diffusers_xformers --gradient_checkpointing                                                                       
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                        
    --save_every_n_epochs=1       