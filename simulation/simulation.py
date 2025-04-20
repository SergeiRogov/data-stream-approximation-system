import json
import os
import datetime
from evaluation.memory_usage import evaluate_memory_usage
from evaluation.query_speed import evaluate_query_speed
from input_stream.dataset_stream_simulator import DatasetStreamSimulator
from summarization_algorithms.count_min_sketch import CountMinSketch
from evaluation.accuracy import evaluate_accuracy
import copy
from visualization.visualization import visualize


def evaluate(cms, ground_truth):
    print("\n------------------------------------------------------------")
    print(f"Evaluating accuracy after ({cms.totalCount} items processed)")
    print("------------------------------------------------------------")
    accuracy = evaluate_accuracy(cms, ground_truth)
    query_speed = evaluate_query_speed(cms, ground_truth)
    memory_usage = evaluate_memory_usage(cms)
    load_factor = cms.get_load_factor()

    return accuracy, query_speed, memory_usage, load_factor


def record_metrics(results_file, items_processed, accuracy, query_speed, memory_usage, load_factor):
    result = {
        "processed_items": int(items_processed),
        "avg_error": float(accuracy["avg_error"]),
        "overestimation_percentage": float(accuracy["overestimation_percentage"]),
        "query_speed": float(query_speed),
        "memory_usage": float(memory_usage),
        "load_factor": float(load_factor),
        "percentiles": {
            "50th": float(accuracy["percentiles"].get("50th", 0.0)),
            "90th": float(accuracy["percentiles"].get("90th", 0.0)),
            "95th": float(accuracy["percentiles"].get("95th", 0.0)),
            "100th": float(accuracy["percentiles"].get("100th", 0.0)),
        }
    }
    try:
        with open(results_file, "r") as f:
            existing_results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = []
    existing_results.append(result)
    with open(results_file, "w") as f:
        json.dump(existing_results, f, indent=4)


if __name__ == '__main__':

    WIDTH = 10000
    DEPTH = 5
    SLEEP_TIME = 0.00001

    DATASET_PATH = "../datasets/FIFA.csv"
    FIELD = "Tweet"

    stream_simulator = DatasetStreamSimulator(dataset_path=DATASET_PATH, field_name=FIELD, sleep_time=SLEEP_TIME)
    cms = CountMinSketch(width=WIDTH, depth=DEPTH)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ALGORITHM_NAME = cms.__class__.__name__
    DATASET_NAME = os.path.splitext(os.path.basename(DATASET_PATH))[0]
    RESULTS_DIR = f"../experiments/{DATASET_NAME}/{ALGORITHM_NAME}"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    RESULTS_FILE = f"{RESULTS_DIR}/w{cms.width}_d{cms.depth}_{timestamp}.json"
    PLOTS_DIR = f"../visualization/plots/{DATASET_NAME}/{ALGORITHM_NAME}"
    os.makedirs(PLOTS_DIR, exist_ok=True)

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w") as f:
            json.dump([], f)

    ground_truth = {}

    eval_every_n_items = 5_000
    visualize_every_n_items = 200_000

    for item in stream_simulator.simulate_stream():
        cms.add(item)
        ground_truth[item] = ground_truth.get(item, 0) + 1

        if cms.totalCount % eval_every_n_items == 0:
            accuracy, query_speed, memory_usage, load_factor = evaluate(copy.deepcopy(cms), copy.deepcopy(ground_truth))
            record_metrics(RESULTS_FILE, cms.totalCount, accuracy, query_speed, memory_usage, load_factor)

        if cms.totalCount % visualize_every_n_items == 0:
            visualize(RESULTS_FILE, PLOTS_DIR)

    accuracy, query_speed, memory_usage, load_factor = evaluate(cms, ground_truth)
    record_metrics(RESULTS_FILE, cms.totalCount, accuracy, query_speed, memory_usage, load_factor)
    visualize(RESULTS_FILE, PLOTS_DIR)
