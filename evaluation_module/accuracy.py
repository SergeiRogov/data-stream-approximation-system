"""
accuracy_evaluation.py

This module evaluates the accuracy of a Count-Min Sketch (CMS) instance
by comparing its estimates to a ground truth dataset.

Usage:
    - Ensure that the CMS instance and ground truth are properly initialized.
    - If evaluating mid-stream, pass copies of both the CMS and ground truth
      to maintain consistency.
"""
import random


def evaluate_accuracy(cms, ground_truth, test_samples_num=1000):
    """
    Evaluates the accuracy of a given Count-Min Sketch instance.

    If you use it mid-stream, be aware the CMS will keep evolving while the evaluation runs.
    Pass a copied CMS and ground_truth instances instead of the live ones.

    Args:
        cms: A CountMinSketch instance.
        ground_truth: A dictionary with ground truth counts.
        test_samples_num: Number of items to sample for accuracy testing.

    Returns:
        A dictionary containing the following:
            - 'avg_error': Average error
            - 'avg_error_percentage': Average error percentage
            - 'max_error': Maximum error
            - 'max_error_percentage': Maximum error percentage
            - 'exact_match_percentage': Exact match percentage
    """
    test_items = random.sample(list(ground_truth.keys()), min(test_samples_num, len(ground_truth)))
    errors = [cms.query(item) - ground_truth[item] for item in test_items]
    correct_count = sum(1 for err in errors if err == 0)

    avg_error = sum(errors) / len(errors)
    max_error = max(errors)

    # maximum error and maximum error percentage could be associated with different items

    avg_error_percentage = sum(err / ground_truth[item] * 100 for item, err in zip(test_items, errors)) / len(test_items)
    max_error_percentage = max(err / ground_truth[item] * 100 for item, err in zip(test_items, errors))

    exact_match_percentage = (correct_count / len(test_items)) * 100

    print(f"Average Error: {avg_error:.3f}")
    print(f"Average Error Percentage: {avg_error_percentage:.2f}%")
    print(f"Max Error: {max_error}")
    print(f"Max Error Percentage: {max_error_percentage:.2f}%")
    print(f"Exact Match Percentage: {exact_match_percentage:.2f}%")

    return {
        'avg_error': avg_error,
        'avg_error_percentage': avg_error_percentage,
        'max_error': max_error,
        'max_error_percentage': max_error_percentage,
        'exact_match_percentage': exact_match_percentage
    }
