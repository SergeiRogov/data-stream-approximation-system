import collections
from ground_truth.base_truth import BaseTruth


class DecayingTruth(BaseTruth):
    def __init__(self, alpha=0.1):
        self.alpha = alpha
        self.counts = collections.defaultdict(float)

    def decay_all(self):
        for key in list(self.counts.keys()):
            self.counts[key] *= (1 - self.alpha)
            if self.counts[key] < 1e-6:
                del self.counts[key]

    def add(self, item, count=1):
        self.decay_all()
        self.counts[item] += self.alpha * count

    def query(self, item):
        return self.counts.get(item, 0.0)

    def get_all(self):
        return dict(self.counts)
