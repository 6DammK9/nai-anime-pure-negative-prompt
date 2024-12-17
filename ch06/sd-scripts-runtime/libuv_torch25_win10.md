# Dedicated workaround of LIBUV on pytorch 2.5 in Win 10 #

## How to trigger ##

- Any dummy python process is good. `print(1)` also fine. Root cause in [pytorch](https://github.com/pytorch/pytorch/issues/139990).

```log
> accelerate launch pp.py
File "C:\Users\User\.conda\envs\kohyas-env\Lib\site-packages\torch\distributed\elastic\rendezvous\static_tcp_rendezvous.py", line 70, in next_rendezvous
self._store = TCPStore(  # type: ignore[call-arg]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: use_libuv was requested but PyTorch was build without libuv support
```

- Meanwhile there is a OS specific minor bug. Discussed in [pytorch](https://github.com/pytorch/pytorch/issues/118378).

```log
> accelerate launch pp.py
File "C:\Users\User\.conda\envs\kohyas-env\Lib\site-packages\torch\distributed\elastic\rendezvous\static_tcp_rendezvous.py", line 70, in next_rendezvous
self._store = TCPStore(  # type: ignore[call-arg]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: unmatched '}' in format string
```

## Analysis and the workaround ##

- From [sd-scripts/pull/1686](https://github.com/kohya-ss/sd-scripts/pull/1686), inject `init_method="env://?use_libuv=False"` and `InitProcessGroupKwargs` are proposed. **It doesn't work for me.**
- After a few console log, `accelerate launch *.py` **never visit** any user level codes, which cause me headahce.
- From [the introduction of LIBUV in 2.4](https://pytorch.org/tutorials/intermediate/TCPStore_libuv_backend.html), **most exit routes are not effective.**
- By looking for the stack stace, [static_tcp_rendezvous.py](https://github.com/pytorch/pytorch/blob/main/torch/distributed/elastic/rendezvous/static_tcp_rendezvous.py) calls `TCPStore` directly, making `use_libuv=False` is the only exit route.
- Therefore here is the solution, in [static_tcp_rendezvous.py](https://github.com/pytorch/pytorch/blob/main/torch/distributed/elastic/rendezvous/static_tcp_rendezvous.py) 

```py
#print([self.master_addr, self.master_port, os.environ["USE_LIBUV"]])
if self.master_addr == "127.0.0.1":
    self.master_addr = "localhost"

if not self._store:
    self._store = TCPStore(  # type: ignore[call-arg]
        self.master_addr,
        self.master_port,
        self.world_size,
        is_master,
        self.timeout,
        multi_tenant=True,
        use_libuv=False,
    )
```

- Then in [rendezvous.py](https://github.com/pytorch/pytorch/blob/main/torch/distributed/rendezvous.py)

```py
attempt = os.environ["TORCHELASTIC_RESTART_COUNT"]
if hostname == "127.0.0.1":
    hostname = "localhost"
tcp_store = TCPStore(hostname, port, world_size, False, timeout, use_libuv=False)
return PrefixStore(f"/worker/attempt_{attempt}", tcp_store)
```

- Running the placeholder script will exit without error.

```log
> accelerate launch pp.py
C:\Users\User\.conda\envs\kohyas-env\Lib\site-packages\transformers\utils\generic.py:441: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
C:\Users\User\.conda\envs\kohyas-env\Lib\site-packages\transformers\utils\generic.py:309: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
W1210 01:07:59.483000 30124 site-packages\torch\distributed\elastic\multiprocessing\redirects.py:29] NOTE: Redirects are currently not supported in Windows or MacOs.
Using RTX 3090 or 4000 series which doesn't support faster communication speedups. Ensuring P2P and IB communications are disabled.
['127.0.0.1', 29500, '0']
1
1
```

## If code is not accessible ##

- [Build libuv.](https://github.com/libuv/libuv?tab=readme-ov-file#build-instructions) Impossible for most users.

- Downgrade pyTorch to `2.3.1` or earlier.