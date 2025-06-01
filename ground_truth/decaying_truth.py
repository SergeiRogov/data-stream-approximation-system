from collections import deque
from ground_truth.base_truth import BaseTruth


class DecayingTruth(BaseTruth):
    def __init__(self, window_size=1000):
        self.window_size = window_size
        self.data = deque()  # list of items
        self.freq = {}

    def add(self, item):
        self.data.append(item)
        self.freq[item] = self.freq.get(item, 0) + 1

        if len(self.data) > self.window_size:
            old_item = self.data.popleft()
            self.freq[old_item] -= 1
            if self.freq[old_item] == 0:
                del self.freq[old_item]

    def query(self, item):
        return self.freq.get(item, 0)

    def get_top_k(self, k):
        return sorted(self.freq.items(), key=lambda x: -x[1])[:k]

    def get_all(self):
        return dict(self.freq)
