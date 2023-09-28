set MODEL_DIR=C:\SD_DIR\models\Stable-diffusion\
set LOG_DIR=.\logs\
del "%LOG_DIR%result-02.json"
python safetensors_util.py metadata "%MODEL_DIR%02-vbp23-cbp2-sd.safetensors" >> "%LOG_DIR%result-02.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-02.json" "%LOG_DIR%result-02a.json"
timeout 1
del "%LOG_DIR%result-03.json"
python safetensors_util.py metadata "%MODEL_DIR%03-vcbp-mzpikas_tmnd-sd.safetensors" >> "%LOG_DIR%result-03.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-03.json" "%LOG_DIR%result-03a.json"
timeout 1
del "%LOG_DIR%result-04.json"
python safetensors_util.py metadata "%MODEL_DIR%04-vcbp_mzpt_d8-sd.safetensors" >> "%LOG_DIR%result-04.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-04.json" "%LOG_DIR%result-04a.json"
timeout 1
del "%LOG_DIR%result-05.json"
python safetensors_util.py metadata "%MODEL_DIR%05-vcbp_mtd8_cwl-sd.safetensors" >> "%LOG_DIR%result-05.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-05.json" "%LOG_DIR%result-05a.json"
timeout 1
del "%LOG_DIR%result-06.json"
python safetensors_util.py metadata "%MODEL_DIR%06-vcbp_mtd8cwl_bd-sd.safetensors" >> "%LOG_DIR%result-06.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-06.json" "%LOG_DIR%result-06a.json"
timeout 1
del "%LOG_DIR%result-07.json"
python safetensors_util.py metadata "%MODEL_DIR%07-vcbp_mtd8cwl_bdaw-sd.safetensors" >> "%LOG_DIR%result-07.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-07.json" "%LOG_DIR%result-07a.json"
timeout 1
del "%LOG_DIR%result-08.json"
python safetensors_util.py metadata "%MODEL_DIR%08-vcbpmt_d8cwlbd_aweb5-sd.safetensors" >> "%LOG_DIR%result-08.json"
timeout 1
node extract_merge_info.js "%LOG_DIR%result-08.json" "%LOG_DIR%result-08a.json"
timeout 1