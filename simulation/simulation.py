import json
import os
import datetime
from evaluation.memory_usage import evaluate_memory_usage
from evaluation.avg_query_time import evaluate_avg_query_time
from evaluation.accuracy import evaluate_accuracy
from ground_truth.decaying_truth import DecayingTruth
from ground_truth.truth import Truth
from visualization.visualization import visualize
import copy


def evaluate(cms, ground_truth):
    print(f"{cms.totalCount} items processed. Evaluating...")
    accuracy = evaluate_accuracy(cms, ground_truth)
    avg_query_time = evaluate_avg_query_time(cms, ground_truth)
    memory_usage = evaluate_memory_usage(cms)
    load_factor = cms.get_load_factor()

    return accuracy, avg_query_time, memory_usage, load_factor


def record_metrics(results_file, items_processed, accuracy, avg_query_time, memory_usage, load_factor):
    result = {
        "processed_items": int(items_processed),
        "avg_error": float(accuracy["avg_error"]),
        "overestimation_percentage": float(accuracy["overestimation_percentage"]),
        "underestimation_percentage": float(accuracy["underestimation_percentage"]),
        "exact_match_percentage": float(accuracy["exact_match_percentage"]),
        "avg_query_time": float(avg_query_time),
        "memory_usage": float(memory_usage),
        "load_factor": float(load_factor),
        "percentiles": {
            "overestimation": {
                "50th": float(accuracy.get("overestimation_percentiles", {}).get("50th", 0.0)),
                "90th": float(accuracy.get("overestimation_percentiles", {}).get("90th", 0.0)),
                "95th": float(accuracy.get("overestimation_percentiles", {}).get("95th", 0.0)),
                "100th": float(accuracy.get("overestimation_percentiles", {}).get("100th", 0.0)),
            },
            "underestimation": {
                "50th": float(accuracy.get("underestimation_percentiles", {}).get("50th", 0.0)),
                "90th": float(accuracy.get("underestimation_percentiles", {}).get("90th", 0.0)),
                "95th": float(accuracy.get("underestimation_percentiles", {}).get("95th", 0.0)),
                "100th": float(accuracy.get("underestimation_percentiles", {}).get("100th", 0.0)),
            },
            "combined": {
                "50th": float(accuracy.get("combined_percentiles", {}).get("50th", 0.0)),
                "90th": float(accuracy.get("combined_percentiles", {}).get("90th", 0.0)),
                "95th": float(accuracy.get("combined_percentiles", {}).get("95th", 0.0)),
                "100th": float(accuracy.get("combined_percentiles", {}).get("100th", 0.0)),
            }
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


def get_algorithm(algorithm, width, depth, alpha=0.1):
    if algorithm == "ConservativeCountMinSketch":
        from summarization_algorithms.conservative_count_min_sketch import ConservativeCountMinSketch
        cms = ConservativeCountMinSketch(width=width, depth=depth)
    elif algorithm == "CountMeanMinSketch":
        from summarization_algorithms.count_mean_min_sketch import CountMeanMinSketch
        cms = CountMeanMinSketch(width=width, depth=depth)
    elif algorithm == "CountSketch":
        from summarization_algorithms.count_sketch import CountSketch
        cms = CountSketch(width=width, depth=depth)
    elif algorithm == "DecayCMS":
        from summarization_algorithms.decay_cms import DecayCMS
        cms = DecayCMS(width=width, depth=depth, alpha=alpha)
    else:  # CountMinSketch
        from summarization_algorithms.count_min_sketch import CountMinSketch
        cms = CountMinSketch(width=width, depth=depth)
    return cms


def process_config(config):
    if config["stream_type"] == "random":
        config["dataset_name"] = "synthetic"
    else:
        import os
        config["dataset_name"] = os.path.splitext(os.path.basename(config["dataset_path"]))[0]
    return config


def get_truth_class(config):
    if config["algorithm"] == "DecayCMS":
        return DecayingTruth(alpha=config["alpha"])
    return Truth()


def get_stream_simulator(config):
    if config["stream_type"] == "dataset":
        from input_stream.dataset_stream_simulator import DatasetStreamSimulator
        return DatasetStreamSimulator(
            dataset_path=config["dataset_path"],
            field_name=config["field"],
            sleep_time=config["sleep_time"]
        )
    elif config["stream_type"] == "random":
        from input_stream.random_stream_simulator import RandomStreamSimulator
        return RandomStreamSimulator(sleep_time=config["sleep_time"])
    else:
        raise ValueError(f"Unknown stream source: {config['stream_type']}")


def eval_and_record(cms, ground_truth, file_path):
    accuracy, query_speed, memory_usage, load_factor = evaluate(copy.deepcopy(cms), ground_truth.get_all())
    record_metrics(file_path, cms.totalCount, accuracy, query_speed, memory_usage, load_factor)


if __name__ == '__main__':

    with open("../config.json", "r") as f:
        CONFIG = json.load(f)

    CONFIG = process_config(CONFIG)

    WIDTH = CONFIG["width"]
    DEPTH = CONFIG["depth"]
    ALGORITHM = CONFIG["algorithm"]
    ALPHA = CONFIG.get("alpha", 0.1)
    EVAL_INTERVAL = CONFIG["eval_interval"]
    VIS_INTERVAL = CONFIG["vis_interval"]
    DATASET_NAME = CONFIG["dataset_name"]

    stream_simulator = get_stream_simulator(CONFIG)
    cms = get_algorithm(ALGORITHM, WIDTH, DEPTH, ALPHA)
    ground_truth = get_truth_class(CONFIG)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    RESULTS_DIR = f"../experiments/{DATASET_NAME}/{ALGORITHM}/w{cms.width}_d{cms.depth}/{timestamp}"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")
    PLOTS_DIR = RESULTS_DIR

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w") as f:
            json.dump([], f)

    for item in stream_simulator.simulate_stream():
        cms.add(item)
        ground_truth.add(item)

        if cms.totalCount % EVAL_INTERVAL == 0:
            eval_and_record(cms, ground_truth, RESULTS_FILE)

        if cms.totalCount % VIS_INTERVAL == 0:
            visualize(RESULTS_FILE, PLOTS_DIR)

    eval_and_record(cms, ground_truth, RESULTS_FILE)
    visualize(RESULTS_FILE, PLOTS_DIR)
