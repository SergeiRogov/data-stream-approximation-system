import numpy as np
import hashlib
from count_min_sketch_base import CountMinSketchBase


class SlidingWindowDecayCMS(CountMinSketchBase):
    def __init__(self, width, depth, alpha=0.1, *args, **kwargs):
        super().__init__(width, depth, *args, **kwargs)
        self.alpha = alpha
        self.tables = np.zeros((depth, width), dtype=float)

    def _hash(self, x):
        """
        Generate multiple hash values for a given input item using hashlib.md5
        """
        base_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.depth):
            h = base_hash.copy()
            h.update(str(i).encode('utf-8'))
            yield int(h.hexdigest(), 16) % self.width

    def add(self, item, count=1):
        for row, col in enumerate(self._hash(item)):
            prev = self.tables[row, col]
            self.tables[row, col] = (1 - self.alpha) * prev + self.alpha * count
        self.totalCount += 1

    def query(self, item):
        return min(self.tables[row, col] for row, col in enumerate(self._hash(item)))

    def reset(self):
        self.tables.fill(0)
        self.totalCount = 0

    def get_load_factor(self):
        return max(np.count_nonzero(row) for row in self.tables) / self.width
