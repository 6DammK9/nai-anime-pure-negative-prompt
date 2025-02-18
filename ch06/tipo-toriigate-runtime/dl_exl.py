from huggingface_hub import snapshot_download

model_id="Minthy/ToriiGate-v0.4-7B-exl2-4bpw"

snapshot_download(model_id)

sample_local_path="C:/Users/User/.cache/huggingface/hub/models--Minthy--ToriiGate-v0.4-7B-exl2-8bpw/snapshots/db4ff9e988b09765c98d9ef5485afeb60a0054e6"

print("Done!")