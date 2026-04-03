import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from convex_hull import compute_hull_other

from utils import measure_runtime


def main(sizes):
    measure_runtime(sizes, compute_hull_other, "_other_convex_hull")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    sizes = [10, 100, 1000, 10000, 20000, 40000, 50000]
    main(sizes)
