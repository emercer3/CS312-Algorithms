import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from network_routing import find_shortest_path_with_heap_pq

from utils import measure_runtime


def main(sizes):
    measure_runtime(sizes, 0.2, find_shortest_path_with_heap_pq, "_heap_pq")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    main(sizes)
