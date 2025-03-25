import random
import time
from input_stream.stream_simulator_base import StreamSimulator


class RandomStreamSimulator(StreamSimulator):
    """
    Simulates a simple data stream by generating items at a controlled rate.
    """

    def __init__(self, sleep_time=0.01, stream_size=1000, item_list=None):
        super().__init__(sleep_time)
        self.stream_size = stream_size
        self.item_list = item_list if item_list else ["apple", "banana", "cherry",
                                                      "ginger", "strawberry", "fig",
                                                      "grape", "pineapple", "kiwi"]

    def generate_random_stream(self):
        """
        Generate a random data stream of predefined size.
        Returns:
            A list of randomly selected items from the item list.
        """
        return [random.choice(self.item_list) for _ in range(self.stream_size)]

    def simulate_stream(self):
        """
        Simulate a real-time data stream by yielding one item at a time.
        Yields:
            One item at a time from the generated stream.
        """
        data_stream = self.generate_random_stream()
        for item in data_stream:
            yield item
            time.sleep(self.sleep_time)
