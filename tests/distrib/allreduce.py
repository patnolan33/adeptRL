import os

import torch
import torch.distributed as dist

WORLD_SIZE = int(os.environ['WORLD_SIZE'])
GLOBAL_RANK = int(os.environ['RANK'])
LOCAL_RANK = int(os.environ['LOCAL_RANK'])
NB_NODE = int(os.environ['NB_NODE'])
LOCAL_SIZE = WORLD_SIZE // NB_NODE

print('w', WORLD_SIZE)
print('g', GLOBAL_RANK)
print('l', LOCAL_RANK)
print('n', NB_NODE)


def on_worker():
    return LOCAL_RANK != 0


def on_host():
    return LOCAL_RANK == 0


if __name__ == '__main__':
    nb_gpu = torch.cuda.device_count()
    print('Device Count', nb_gpu)

    dist.init_process_group(
        backend='nccl',
        world_size=WORLD_SIZE,
        rank=LOCAL_RANK
    )

    print('LOCAL_RANK', LOCAL_RANK, 'initialized.')
    t = torch.tensor([1., 2., 3.]).to(f'cuda:{LOCAL_RANK}')

    # tags to identify tensors
    # loop thru workers
    dist.barrier()
    handle = dist.all_reduce(t, async_op=True)
    handle.wait()

    print(t)
