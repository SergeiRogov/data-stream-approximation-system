from input_stream_module.stream_simulator import StreamSimulator
from summarization_algorithms.count_min_sketch import CountMinSketch
from evaluation_module.accuracy import evaluate_accuracy
import copy

if __name__ == '__main__':

    STREAM_SIZE = 4000
    WIDTH = 10
    DEPTH = 3
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
            evaluate_accuracy(copy.deepcopy(cms), copy.deepcopy(ground_truth))

    print(f"\nFinal evaluation after full stream processing... ({cms.totalCount} items processed)")
    evaluate_accuracy(cms, ground_truth, STREAM_SIZE)
