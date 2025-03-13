"""
count_min_sketch.py
Regular Count-Min Sketch implementation.
"""
from summarization_algorithms.count_min_sketch_base import CountMinSketchBase
import array
import hashlib


class CountMinSketch(CountMinSketchBase):
    """
    Regular Count-Min Sketch implementation.
    """

    def __init__(self, width, depth):
        """
        Initialize sketch with width, depth, and seed.
        """
        super().__init__(width, depth)
        self.hash_tables = [array.array("l", (0 for _ in range(self.width))) for _ in range(self.depth)]

    def _hash(self, x):
        """
        Generate multiple hash values for a given input item `x`
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
        Return an estimation of the amount of times `item` has ocurred.
        The returned value always overestimates the real value.
        """
        return min(table[i] for table, i in zip(self.hash_tables, self._hash(item)))

    def reset(self):
        """
        Reset the sketch by clearing all tables and setting the count to 0.
        """
        self.totalCount = 0  # Reset the count of items
        for table in self.hash_tables:
            for i in range(len(table)):
                table[i] = 0
