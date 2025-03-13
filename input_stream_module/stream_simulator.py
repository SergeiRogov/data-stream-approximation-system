import random
import time


class StreamSimulator:
    """
    A class to simulate a simple data stream by generating items at a controlled rate.

    This class mimics real-time streaming data by yielding randomly selected items
    from a predefined list with a specified time delay between each item.
    """
    def __init__(self, stream_size=1000, item_list=None, sleep_time=0.01):
        """
        Initialize the StreamSimulator.

        Args:
            stream_size: The number of items in the simulated stream.
            item_list: A list of items that can be randomly chosen in the stream.
            sleep_time: Time delay between each item being added to simulate the stream.
        """
        self.stream_size = stream_size
        self.item_list = item_list if item_list else ["apple", "banana", "cherry",
                                                      "ginger", "strawberry", "fig",
                                                      "grape", "pineapple", "kiwi"]
        self.sleep_time = sleep_time

    def generate_data_stream(self):
        """
        Generate a random data stream of predefined size.
        """
        return [random.choice(self.item_list) for _ in range(self.stream_size)]

    def simulate_stream(self):
        """
        Simulate a real-time data stream by yielding one item at a time.
        """
        data_stream = self.generate_data_stream()

        for item in data_stream:

            yield item
            time.sleep(self.sleep_time)
