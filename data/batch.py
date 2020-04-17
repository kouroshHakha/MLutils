import numpy as np
import torch

class BatchGenerator:

    def __init__(self, x, y=None, bsize=16, seed=10):
        self.x = x
        self.y = y
        self.bsize = bsize

        np.random.seed(seed)

        self.indices_org = np.random.permutation(np.arange(len(x)))

    def get_items_circular(self, items, low_id, high_id):
        size = len(items)
        low = low_id % size

        if low != low_id:
            raise ValueError('low_id cannot be greater than size of list')
        high = high_id % size

        if high != high_id:
            if isinstance(items, np.ndarray):
                return np.concatenate([items[low:], items[:high]], axis=0)
            elif isinstance(items, torch.Tensor):
                return torch.cat([items[low:], items[:high]], dim=0)
            elif isinstance(items, list):
                return items[low:] + items[:high]
            else:
                raise ValueError(f'Unknown type for concatenation {items.__class__.__name__}')
        return items[low: high]

    def get_gen(self, tot_nbatch):
        last_off = max(len(self.indices_org) // self.bsize, 1)
        chunk_iter = 0
        for i in range(tot_nbatch):
            chunk = chunk_iter % last_off
            start = chunk * self.bsize
            selected = self.indices_org[start:start+self.bsize]
            chunk_iter += 1
            if self.y is not None:
                yield self.x[selected], self.y[selected]
            else:
                yield self.x[selected]
