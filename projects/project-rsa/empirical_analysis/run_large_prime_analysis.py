import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from prime_number_generation import generate_large_prime

from utils import measure_runtime


def main(sizes):
    measure_runtime(sizes, generate_large_prime, "_primes")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    sizes = [64, 128, 256, 512, 1024, 2048]

    sys.setrecursionlimit(sizes[-1] * 2)

    main(sizes)
