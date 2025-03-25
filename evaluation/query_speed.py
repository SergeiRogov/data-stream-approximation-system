import random
import time


def evaluate_query_speed(cms, ground_truth, test_samples_num=1000):
    """
    Evaluates the speed of the query method of CountMinSketch.

    Args:
        cms: The CountMinSketch instance to test.
        ground_truth: A dictionary containing the actual counts of items.
        test_samples_num: The number of random items to query.

    Returns:
        Average query time per item.
    """
    test_items = random.sample(list(ground_truth.keys()), min(test_samples_num, len(ground_truth)))

    start_time = time.time()
    for item in test_items:
        cms.query(item)
    end_time = time.time()

    avg_query_time = (end_time - start_time) / test_samples_num
    print(f"Average query time per item: {avg_query_time:.12f} seconds")

    return avg_query_time
