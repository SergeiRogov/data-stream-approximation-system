import csv
import time


class DatasetStreamSimulator:
    """
    A class to simulate a real-time data stream from a CSV dataset.
    """
    def __init__(self, dataset_path, field_name, sleep_time=0.01):
        """
        Initialize the stream simulator.

        Args:
            dataset_path: Path to the dataset file (CSV).
            field_name: The field to extract from the CSV file (like "Tweet").
            sleep_time: Time delay between yielding each item.
        """
        self.dataset_path = dataset_path
        self.field_name = field_name
        self.sleep_time = sleep_time

    def simulate_dataset_stream(self):
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
