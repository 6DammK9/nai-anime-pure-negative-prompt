accelerate launch --num_cpu_threads_per_process 4
    sdxl_train.py                                                                                                               
    --pretrained_model_name_or_path="E:/stable-diffusion-webui/models/Stable-diffusion/x215c-AstolfoMix-24101101-6e545a3.safetensors"             
    --in_json "F:/just_astolfo/test_lat.json"                                                                                   
    --train_data_dir="F:/just_astolfo/test"                                                                          
    --output_dir="E:/astolfo_xl/just_astolfo/model_out_24121902"                                                        
    --log_with=tensorboard                                                                                                      
    --logging_dir="E:/astolfo_xl/just_astolfo/tensorboard"                                                              
    --log_prefix=just_astolfo_24121902_                                                                                         
    --save_model_as=safetensors                                                                                                 
    --caption_extension=".txt"                                                                                                  
    --use_8bit_adam                                                                                                             
    --train_batch_size=1 --learning_rate=0 --max_train_epochs=20   
    --train_text_encoder --learning_rate_te1=1e-5 --learning_rate_te2=1e-5       
    --max_data_loader_n_workers 2                                                                                                       
    --xformers --diffusers_xformers --gradient_checkpointing                                                                    
    --full_bf16 --mixed_precision=bf16 --save_precision=fp16                                                                    
    --enable_bucket --cache_latents                                                                                             
    --save_every_n_epochs=10       