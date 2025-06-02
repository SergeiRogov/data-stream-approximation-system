import numpy as np
import hashlib
from summarization_algorithms.count_min_sketch_base import CountMinSketchBase


class SlidingCountMinSketch(CountMinSketchBase):
    def __init__(self, width, depth, window_size):
        super().__init__(width, depth)
        self.window_size = window_size
        self.total_slots = width * depth
        self.field_num = window_size // self.total_slots + 2
        self.counters = np.zeros((depth, width, self.field_num), dtype=int)
        self.clock_pos = 0
        self.cycle_num = 0
        self.last_time = 0

    def _hash(self, item, i):
        """
        Return the i-th hash value for an item using SHA-256.
        """
        h = hashlib.sha256((str(item) + str(i)).encode('utf-8'))
        return int(h.hexdigest(), 16) % self.width

    def _advance_time(self, time):
        while self.last_time < time:
            d = self.clock_pos // self.width
            w = self.clock_pos % self.width
            self.counters[d][w][(self.cycle_num + 1) % self.field_num] = 0
            self.clock_pos = (self.clock_pos + 1) % self.total_slots
            if self.clock_pos == 0:
                self.cycle_num = (self.cycle_num + 1) % self.field_num
            self.last_time += 1

    def add(self, item, count=1):
        for _ in range(count):
            self._advance_time(self.totalCount)
            for i in range(self.depth):
                pos = self._hash(item, i)
                index = (self.cycle_num + (pos + i * self.width < self.clock_pos)) % self.field_num
                self.counters[i][pos][index] += 1
            self.totalCount += 1

    def query(self, item):
        min_est = float('inf')
        for i in range(self.depth):
            pos = self._hash(item, i)
            est = self.counters[i][pos].sum()
            min_est = min(min_est, est)
        return min_est

    def reset(self):
        self.counters.fill(0)
        self.clock_pos = 0
        self.cycle_num = 0
        self.last_time = 0
        self.totalCount = 0

    def get_load_factor(self):
        """
        Return the load factor: maximum number of non-zero counters in any row, divided by width.
        """
        max_nonzero = 0
        for d in range(self.depth):
            row = self.counters[d]
            nonzero_count = sum(1 for cell in row if cell.any())
            max_nonzero = max(max_nonzero, nonzero_count)
        return max_nonzero / self.width


if __name__ == '__main__':
    from ground_truth.decaying_truth import DecayingTruth
    cms = SlidingCountMinSketch(width=10, depth=4, window_size=11)
    truth = DecayingTruth(window_size=11)
    print(f"Num of slices: {cms.field_num}")
    for item in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        print(f"----------------------------------")

        print(f"Being inserted: {item}")
        cms.add(item)
        truth.add(item)
        print(cms.counters)
        print(f"Num of items in window: {truth.window_item_count}")
        print(f"Being queried: {item}")
        print(f"CMS: {cms.query(item)}")
        print(f"Truth: {truth.query(item)}")

