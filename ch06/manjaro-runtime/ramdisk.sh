#Run in sudo

mount -o remount,size=65G /dev/shm

#astolfo_xl/dataset/datasetname/

mkdir -p "/dev/shm/astolfo_xl"
chmod 777 "/dev/shm/astolfo_xl"

mkdir -p "/dev/shm/astolfo_xl/dataset"
mkdir -p "/dev/shm/astolfo_xl/meta"
mkdir -p "/dev/shm/astolfo_xl/basemodel"
cp -r "/run/media/user/Intel P4510 3/astolfo_xl/x215c-AstolfoMix-24101101-6e545a3.safetensors" "/dev/shm/astolfo_xl/basemodel"
cp -r "/run/media/user/Intel P4510 3/just_astolfo/kohyas_finetune" "/dev/shm/astolfo_xl/dataset"
mv "/dev/shm/astolfo_xl/dataset/kohyas_finetune" "/dev/shm/astolfo_xl/dataset/just_astolfo"
cp -r "/run/media/user/Intel P4510 3/just_astolfo/test1" "/dev/shm/astolfo_xl/dataset"
cp -r "/run/media/user/Intel P4510 3/just_astolfo/test2" "/dev/shm/astolfo_xl/dataset"
cp -r "/run/media/user/Intel P4510 3/just_astolfo/meta_lat_v3.json" "/dev/shm/astolfo_xl/meta"
cp -r "/run/media/user/Intel P4510 3/just_astolfo/test_lat_v3b.json" "/dev/shm/astolfo_xl/meta"
