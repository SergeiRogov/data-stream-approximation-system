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


def evaluate_accuracy(cms, ground_truth, test_samples=100):
    """
    Evaluates the accuracy of a given Count-Min Sketch instance.

    If you use it mid-stream, be aware the CMS will keep evolving while the evaluation runs.
    Pass a copied CMS and ground_truth instances instead of the live ones.

    Args:
        cms: A CountMinSketch instance.
        ground_truth: A dictionary with ground truth counts.
        test_samples: Number of items to sample for accuracy testing.

    Returns:
        Average error, max error, and the percentage of exact estimates.
    """
    test_items = random.sample(list(ground_truth.keys()), min(test_samples, len(ground_truth)))
    errors = [cms.query(item) - ground_truth[item] for item in test_items]
    correct_count = sum(1 for err in errors if err == 0)

    avg_error = sum(errors) / len(errors)
    max_error = max(errors)
    exact_match_percentage = (correct_count / len(test_items)) * 100

    print(f"Average Error: {avg_error:.3f}, "
          f"Max Error: {max_error}, "
          f"Exact Matches: {correct_count}/{len(test_items)} ({exact_match_percentage:.2f}%)")

    return avg_error, max_error, exact_match_percentage
