import csv
import time
from input_stream.stream_simulator_base import StreamSimulator


class DatasetStreamSimulator(StreamSimulator):
    """
    Simulates a real-time data stream from a CSV dataset.
    """
    def __init__(self, dataset_path, field_name, sleep_time=0.01):
        super().__init__(sleep_time)
        self.dataset_path = dataset_path
        self.field_name = field_name

    def simulate_stream(self):
        """
        Simulate a real-time data stream by yielding one item at a time from the specified field.
        """
        with open(self.dataset_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = row.get(self.field_name)
                if data:
                    for word in data.split():
                        yield word
                        time.sleep(self.sleep_time)
