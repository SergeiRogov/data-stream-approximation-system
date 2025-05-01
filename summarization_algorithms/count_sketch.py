from summarization_algorithms.count_min_sketch_base import CountMinSketchBase
import numpy as np
import hashlib
import random


class CountSketch(CountMinSketchBase):
    """
    Fast-AGMS / Count Sketch implementation.
    This sketch provides unbiased frequency estimation and supports both positive and negative updates (turnstile model).
    """
    def __init__(self, width, depth):
        super().__init__(width, depth)
        self.hash_tables = np.zeros((self.depth, self.width), dtype=int)

    def _hash_index(self, x):
        """
        Hash function to map the item to column indices in each row.
        """
        base_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.depth):
            base_hash.update(str(i).encode('utf-8'))
            yield int(base_hash.hexdigest(), 16) % self.width

    def _hash_sign(self, x):
        """
        Second hash function to determine whether to add or subtract (+1 or -1).
        """
        rng = random.Random(hash(x))
        for _ in range(self.depth):
            yield 1 if rng.choice([True, False]) else -1

    def add(self, item, count=1):
        self.totalCount += abs(count)
        for row, idx, sign in zip(self.hash_tables, self._hash_index(item), self._hash_sign(item)):
            row[idx] += sign * count

    def query(self, item):
        estimates = []
        for row, idx, sign in zip(self.hash_tables, self._hash_index(item), self._hash_sign(item)):
            estimates.append(sign * row[idx])
        return int(np.median(estimates))

    def reset(self):
        self.totalCount = 0
        self.hash_tables.fill(0)

    def get_load_factor(self):
        return max(np.count_nonzero(row) for row in self.hash_tables) / self.width
