import sys


def evaluate_memory_usage(cms):
    """
    Evaluates the memory usage of the CountMinSketch instance, including its internal structures.

    Args:
        cms: The CountMinSketch instance to measure.

    Returns:
        The total memory usage of the CMS in bytes.
    """
    total_size = sys.getsizeof(cms)
    total_size += sys.getsizeof(cms.hash_tables)

    for table in cms.hash_tables:
        total_size += sys.getsizeof(table) + table.itemsize * len(table)

    return total_size


def print_memory_usage(total_size):
    print(f"Total CMS memory usage: {total_size} bytes")
