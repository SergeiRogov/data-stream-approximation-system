"""
Count-Min Sketch Base Class

This file contains the abstract base class for Count-Min Sketch (CMS) implementations.

Subclasses must implement the `add`, `query`, and `reset` methods.
Subclasses may implement the`__init__` method if needed.
"""
import abc


class CountMinSketchBase(abc.ABC):
    """
    Abstract base class for Count-Min Sketch implementations.
    Defines the core structure and methods of Count-Min Sketches.
    """
    def __init__(self, width, depth, seed=42, *args, **kwargs):
        """
        Initialize sketch with width, depth, and seed.
        Subclasses may require additional parameters.
        """
        self.width = width
        self.depth = depth
        self.seed = seed
        self.n = 0

        pass  # Allow subclasses to handle additional parameters as necessary

    @abc.abstractmethod
    def add(self, item, count=1):
        """
        Add an item to the sketch.
        """
        pass

    @abc.abstractmethod
    def query(self, item):
        """
        Query the count of an item.
        """
        pass

    @abc.abstractmethod
    def reset(self):
        """
        Reset the sketch.
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(width={self.width}, depth={self.depth})"

    def __getitem__(self, x):
        """
        A convenience method to call `query`.
        """
        return self.query(x)

    def __len__(self):
        """
        Return number of distinct items counted.
        """
        return self.n
