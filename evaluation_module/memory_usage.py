import sys


def evaluate_memory_usage(cms):
    """
    Evaluates the memory usage of the CountMinSketch instance by calculating
    the size of the CMS object in memory.

    Args:
        cms: The CountMinSketch instance to measure.

    Returns:
        The memory usage of the CMS in bytes.
    """
    cms_size = sys.getsizeof(cms)
    print(f"Memory usage of CMS: {cms_size} bytes")

    return cms_size
