from count_min_sketch_base import CountMinSketchBase
import array


class CountMinSketch(CountMinSketchBase):

    def __init__(self, width, depth, seed=42):
        """
        Initialize sketch with width, depth, and seed.
        """
        super().__init__(width, depth, seed)
        self.tables = [array.array("l", (0 for _ in range(self.width))) for _ in range(self.depth)]

    def add(self, item, count=1):
        pass

    def query(self, item):
        pass

    def reset(self):
        pass

