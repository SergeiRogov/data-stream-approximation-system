import random
import time


class RandomStreamSimulator:
    """
    A class to simulate a simple data stream by generating items at a controlled rate.

    This class mimics real-time streaming data by yielding randomly selected items
    from a predefined list with a specified time delay between each item.
    """
    def __init__(self, sleep_time=0.01, stream_size=1000, item_list=None):
        """
        Initialize the StreamSimulator.

        Args:
            sleep_time: Time delay between each item being added to simulate the stream.
            stream_size: The number of items in the simulated stream.
            item_list: A list of items that can be randomly chosen in the stream.
        """
        self.stream_size = stream_size
        self.item_list = item_list if item_list else ["apple", "banana", "cherry",
                                                      "ginger", "strawberry", "fig",
                                                      "grape", "pineapple", "kiwi"]
        self.sleep_time = sleep_time

    def generate_random_stream(self):
        """
        Generate a random data stream of predefined size.
        Returns:
            A list of randomly selected items from the item list.
        """
        return [random.choice(self.item_list) for _ in range(self.stream_size)]

    def simulate_random_stream(self):
        """
        Simulate a real-time data stream by yielding one item at a time.
        Yields:
            One item at a time from the generated stream.
        """
        data_stream = self.generate_random_stream()
        for item in data_stream:
            yield item
            time.sleep(self.sleep_time)
