import numpy as np
import hashlib
from summarization_algorithms.count_min_sketch_base import CountMinSketchBase


class SlidingCountMinSketch(CountMinSketchBase):
    def __init__(self, width, depth, window_size, days=3):
        """
        width: number of buckets in each segment
        depth: number of hash functions / segments
        window_size: size of the sliding window (N)
        d_fields: number of temporal fields per bucket (d)
        """
        super().__init__(width, depth)
        self.window_size = window_size
        self.days = days  # number of fields
        self.counters = np.zeros((depth, width, days), dtype=int)
        self.scan_pointer = 0
        self.totalCount = 0  # counts items inserted (acts like virtual time)

        # For scan rate: (d-1)*m / N buckets scanned per arrival
        self.buckets_per_step = max(1, int((self.days - 1) * self.width * self.depth / self.window_size))

    def _hash(self, item, i):
        """
        Return the i-th hash value for an item using SHA-256.
        """
        h = hashlib.sha256((str(item) + str(i)).encode('utf-8'))
        return int(h.hexdigest(), 16) % self.width

    def _advance_time(self):
        """
        Shift fields in (d-1)*m/N buckets to simulate advancing days.
        """
        for _ in range(self.buckets_per_step):
            d = self.scan_pointer // self.width
            w = self.scan_pointer % self.width
            for j in reversed(range(1, self.days)):
                self.counters[d][w][j] = self.counters[d][w][j - 1]
            self.counters[d][w][0] = 0  # new day begins
            self.scan_pointer = (self.scan_pointer + 1) % (self.depth * self.width)

    def add(self, item, count=1):
        for _ in range(count):
            self._advance_time()
            for i in range(self.depth):
                pos = self._hash(item, i)
                self.counters[i][pos][0] += 1  # Update today's field
            self.totalCount += 1

    def query(self, item):
        """
        Query estimated frequency by summing across all d fields.
        """
        min_est = float('inf')
        for i in range(self.depth):
            pos = self._hash(item, i)
            est = self.counters[i][pos].sum()
            min_est = min(min_est, est)
        return min_est

    def reset(self):
        self.counters.fill(0)
        self.scan_pointer = 0
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
    print(f"Num of slices: {cms.days}")
    for item in [1, 2, 3, 4, 1, 1, 1, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        print(f"----------------------------------")

        print(f"Being inserted: {item}")
        cms.add(item)
        truth.add(item)
        # print(cms.counters)
        print(f"Num of items in window: {truth.window_item_count}")
        print(f"Being queried: {item}")
        print(f"CMS: {cms.query(item)}")
        print(f"Truth: {truth.query(item)}")

