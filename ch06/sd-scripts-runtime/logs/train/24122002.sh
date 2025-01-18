accelerate launch --num_cpu_threads_per_process 4
    sdxl_train.py                                                                                                               
    --pretrained_model_name_or_path="E:/astolfo_xl/just_astolfo/model_out_24122002/epoch-000005-05.safetensors"             
    --in_json "F:/just_astolfo/meta_lat.json"                                                                                   
    --train_data_dir="F:/just_astolfo/kohyas_finetune"                                                                          
    --output_dir="F:/astolfo_xl/just_astolfo/model_out_24122002"                                                        
    --log_with=tensorboard                                                                                                      
    --logging_dir="E:/astolfo_xl/just_astolfo/tensorboard"                                                              
    --log_prefix=just_astolfo_24122002_                                                                                         
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                                             
    --train_batch_size=1 --learning_rate=1e-6 --max_train_epochs=5      
    --max_data_loader_n_workers 2                                                                                                       
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                             
    --save_every_n_epochs=1       