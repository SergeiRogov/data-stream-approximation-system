import numpy as np
import hashlib
from summarization_algorithms.count_min_sketch_base import CountMinSketchBase


class DecayCMS(CountMinSketchBase):
    def __init__(self, width, depth, alpha=0.1, *args, **kwargs):
        super().__init__(width, depth, *args, **kwargs)
        self.alpha = alpha
        self.hash_tables = np.zeros((depth, width), dtype=float)

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
            prev = self.hash_tables[row, col]
            self.hash_tables[row, col] = (1 - self.alpha) * prev + self.alpha * count
        self.totalCount += count

    def query(self, item):
        return min(self.hash_tables[row, col] for row, col in enumerate(self._hash(item)))

    def reset(self):
        self.hash_tables.fill(0)
        self.totalCount = 0

    def get_load_factor(self):
        return max(np.count_nonzero(row) for row in self.hash_tables) / self.width
