from evaluation_module.memory_usage import evaluate_memory_usage
from evaluation_module.query_speed import evaluate_query_speed
from input_stream_module.dataset_stream_simulator import DatasetStreamSimulator
from input_stream_module.random_stream_simulator import RandomStreamSimulator
from summarization_algorithms.count_min_sketch import CountMinSketch
from evaluation_module.accuracy import evaluate_accuracy
import copy


def evaluate(cms, ground_truth):
    print("\n------------------------------------------------------------")
    print(f"Evaluating accuracy after ({cms.totalCount} items processed)")
    print("------------------------------------------------------------")
    evaluate_accuracy(cms, ground_truth)
    evaluate_query_speed(cms, ground_truth)
    evaluate_memory_usage(cms)


if __name__ == '__main__':

    WIDTH = 10000
    DEPTH = 5
    SLEEP_TIME = 0.001

    # stream_simulator = RandomStreamSimulator(stream_size=STREAM_SIZE, sleep_time=SLEEP_TIME)
    stream_simulator = DatasetStreamSimulator(dataset_path="../datasets/FIFA.csv", field_name="Tweet", sleep_time=SLEEP_TIME)
    cms = CountMinSketch(width=WIDTH, depth=DEPTH)

    ground_truth = {}
    eval_every_n_items = 5000
    for item in stream_simulator.simulate_dataset_stream():
        cms.add(item)
        ground_truth[item] = ground_truth.get(item, 0) + 1

        if cms.totalCount % eval_every_n_items == 0:
            evaluate(copy.deepcopy(cms), copy.deepcopy(ground_truth))

    evaluate(cms, ground_truth)
