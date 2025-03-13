from evaluation_module.memory_usage import evaluate_memory_usage
from evaluation_module.query_speed import evaluate_query_speed
from input_stream_module.stream_simulator import StreamSimulator
from summarization_algorithms.count_min_sketch import CountMinSketch
from evaluation_module.accuracy import evaluate_accuracy
import copy


def evaluate(cms, ground_truth):

    print(f"\nAccuracy:")
    evaluate_accuracy(cms, ground_truth)

    print(f"\nAverage Query Speed:")
    evaluate_query_speed(cms, ground_truth)

    print(f"\nMemory Usage:")
    evaluate_memory_usage(cms)


if __name__ == '__main__':

    STREAM_SIZE = 6000
    WIDTH = 15
    DEPTH = 5
    SLEEP_TIME = 0.001

    stream_simulator = StreamSimulator(stream_size=STREAM_SIZE, sleep_time=SLEEP_TIME)
    cms = CountMinSketch(width=WIDTH, depth=DEPTH)

    ground_truth = {}
    MIDWAY_THRESHOLD = STREAM_SIZE // 2

    for item in stream_simulator.simulate_stream():
        cms.add(item)
        ground_truth[item] = ground_truth.get(item, 0) + 1

        if cms.totalCount == MIDWAY_THRESHOLD:
            print(f"\nEvaluating accuracy halfway through the stream... ({cms.totalCount} items processed)")
            evaluate(copy.deepcopy(cms), copy.deepcopy(ground_truth))

    print(f"\nFinal evaluation after full stream processing... ({cms.totalCount} items processed)")
    evaluate(cms, ground_truth)
