# Dedicated workaround of GLOO on (huggingface) accelerate in Win 10 #

## How to trigger ##

- After fixing `libuv`, there are more errors mentioning `backend`.

## Analysis and the workaround ##

- It is the classic "windows doesn't have `nccl` error". For mismatched library version, override settings in [sd-scripts/pull/1686](https://github.com/kohya-ss/sd-scripts/pull/1686) may not be effective.

- Fix [accelerate/state.py](https://github.com/huggingface/accelerate/blob/main/src/accelerate/state.py#L737) with `backend="gloo"`:

```py
self.distributed_type = DistributedType.MULTI_GPU
if not torch.distributed.is_initialized():
    #self.backend = kwargs.pop("backend", "nccl")
    self.backend = kwargs.pop("backend", "gloo")
    # Special case for `TrainingArguments`, where `backend` will be `None`
    if self.backend is None:
        #self.backend = "nccl"
        self.backend = "gloo"
    torch.distributed.init_process_group(backend=self.backend, **kwargs)
```

- (If it blames) Then fix [accelerator.py](https://github.com/huggingface/accelerate/blob/main/src/accelerate/accelerator.py#L432):

```py
self.state = AcceleratorState(
    mixed_precision=mixed_precision,
    cpu=cpu,
    dynamo_plugin=dynamo_plugin,
    deepspeed_plugin=deepspeed_plugin,
    fsdp_plugin=fsdp_plugin,
    megatron_lm_plugin=megatron_lm_plugin,
    _from_accelerator=True,
    backend = "gloo"
    **kwargs,
)
```