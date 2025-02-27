#Run in sudo

#nvidia-xconfig --enable-all-gpus
#nvidia-xconfig --cool-bits=28
#nvidia-settings -a "[gpu:0]/GPUFanControlState=0" -a "[fan:0]/GPUTargetFanSpeed=60"
#nvidia-settings -a "[gpu:1]/GPUFanControlState=0" -a "[fan:1]/GPUTargetFanSpeed=60"
#nvidia-settings -a "[gpu:2]/GPUFanControlState=0" -a "[fan:2]/GPUTargetFanSpeed=60"
#nvidia-settings -a "[gpu:3]/GPUFanControlState=0" -a "[fan:3]/GPUTargetFanSpeed=60"

nvidia-smi -i 0 -pl 235
nvidia-smi -i 1 -pl 235
nvidia-smi -i 2 -pl 235
nvidia-smi -i 3 -pl 235

mkdir -p "/run/media/user/PM863a"
chmod 777 "/run/media/user/PM863a"
mount -t ntfs-3g /dev/sda1 "/run/media/user/PM863a"

mkdir -p "/run/media/user/Intel P4510 3"
chmod 777 "/run/media/user/Intel P4510 3"
mount -t ntfs-3g /dev/nvme0n1p2 "/run/media/user/Intel P4510 3"

#conda activate kohyas-env
#cd /home/user/novelai