"""
count_mean_min_sketch.py
Count-Mean-Min Sketch implementation.
"""
from summarization_algorithms.count_min_sketch_base import CountMinSketchBase
import numpy as np
import hashlib


class CountMeanMinSketch(CountMinSketchBase):
    """
    Implementation of Count-Mean-Min Sketch, a variation of Count-Min Sketch with noise adjustment.
    """
    def __init__(self, width, depth):
        """
        Initialize sketch with width and depth.
        """
        super().__init__(width, depth)
        self.hash_tables = np.zeros((self.depth, self.width), dtype=int)

    def _hash(self, x):
        """
        Generate multiple hash values for a given input item
        """
        base_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.depth):
            base_hash.update(str(i).encode('utf-8'))
            yield int(base_hash.hexdigest(), 16) % self.width

    def add(self, item, count=1):
        """
        Add the element 'item' as if it had appeared 'count' times
        """
        self.totalCount += count
        for table, i in zip(self.hash_tables, self._hash(item)):
            table[i] += count

    def query(self, item):
        """
        Return an estimation of the frequency of `item`, adjusting for noise.
        """
        residues = []
        cms_estimates = []
        for row, idx in zip(self.hash_tables, self._hash(item)):
            raw = row[idx]
            noise = (self.totalCount - raw) / (self.width - 1) if self.width > 1 else 0
            residue = raw - noise
            residues.append(residue)
            cms_estimates.append(raw)

        return max(0, min(round(np.median(residues)), min(cms_estimates)))

    def reset(self):
        """
        Reset the sketch by clearing all tables and setting the count to 0.
        """
        self.totalCount = 0
        self.hash_tables.fill(0)

    def get_load_factor(self):
        """
        Return the load factor: maximum number of non-zero counters in any row, divided by width.
        """
        return max(sum(1 for cell in row if cell > 0) for row in self.hash_tables) / self.width
