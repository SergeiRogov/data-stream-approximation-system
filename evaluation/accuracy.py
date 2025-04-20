"""
accuracy_evaluation.py

This module evaluates the accuracy of a Count-Min Sketch (CMS) instance
by comparing its estimates to a ground truth dataset.

Usage:
    - Ensure that the CMS instance and ground truth are properly initialized.
    - If evaluating mid-stream, pass copies of both the CMS and ground truth
      to maintain consistency.
"""
import numpy as np


def evaluate_accuracy(cms, ground_truth):
    """
    Evaluates the accuracy of a given Count-Min Sketch instance.

    If you use it mid-stream, be aware the CMS will keep evolving while the evaluation runs.
    Pass a copied CMS and ground_truth instances instead of the live ones.

    Args:
        cms: A CountMinSketch instance.
        ground_truth: A dictionary with ground truth counts.

    Returns:
        A dictionary containing the following:
            - 'avg_error': Average error
            - 'avg_error_percentage': Average error percentage
            - 'exact_match_percentage': Exact match percentage
            - 'overestimation_percentage': Overestimation percentage
            - 'percentiles': Dict with error percentiles (50th, 90th, 95th, 100th)
            - 'overestimated_items': List of (item, error), sorted by error desc
    """
    test_items = list(ground_truth.keys())
    dataset_length = len(test_items)

    if not dataset_length:
        return "\nNo items processed"

    errors = []
    overestimations = []
    correct_count = 0

    for item in test_items:
        error = cms.query(item) - ground_truth[item]
        errors.append(error)

        if error == 0:
            correct_count += 1
        elif error > 0:
            overestimations.append((item, error))

    avg_error = sum(errors) / dataset_length

    avg_error_percentage = sum(err / ground_truth[item] * 100 for item, err in zip(test_items, errors)) / dataset_length
    max_error_percentage = max(err / ground_truth[item] * 100 for item, err in zip(test_items, errors))

    exact_match_percentage = (correct_count / dataset_length) * 100
    overestimation_percentage = (len(overestimations) / dataset_length) * 100

    sorted_overestimations = sorted(overestimations, key=lambda x: x[1], reverse=True)
    percentiles = {}
    if overestimations:
        overestimation_errors = [error for _, error in sorted_overestimations]
        percentiles = {
            "50th": np.percentile(overestimation_errors, 50),
            "90th": np.percentile(overestimation_errors, 90),
            "95th": np.percentile(overestimation_errors, 95),
            "100th": np.percentile(overestimation_errors, 100)
        }

    return {
        'overestimation_percentage': overestimation_percentage,
        'exact_match_percentage': exact_match_percentage,
        'avg_error': avg_error,
        'avg_error_percentage': avg_error_percentage,
        'max_error_percentage': max_error_percentage,
        'percentiles': percentiles,
        'overestimated_items': sorted_overestimations
    }


def print_accuracy_evaluation(accuracy):
    overestimations = accuracy['overestimated_items']
    overestimation_percentage = accuracy['overestimation_percentage']
    exact_match_percentage = accuracy['exact_match_percentage']
    avg_error_percentage = accuracy['avg_error_percentage']
    avg_error = accuracy['avg_error']
    percentiles = accuracy['percentiles']

    print(f"Overestimations: {len(overestimations)} ({overestimation_percentage:.2f}%)")
    print(f"Exact Matches: {len([item for item, error in overestimations if error == 0])} ({exact_match_percentage:.2f}%)")
    print(f"Average Error Percentage: {avg_error_percentage:.2f}%")
    print(f"Average Error: {avg_error:.3f}")
    print(f"Max Error Percentage: {accuracy['max_error_percentage']:.2f}%")

    print("Percentiles:")
    for percentile, value in percentiles.items():
        print(f"{percentile}: {value}")

    max_items_to_display = 10
    print("\nSorted Overestimated Items:")
    for item, error in overestimations[:max_items_to_display]:
        print(f"{item}: {error}")
