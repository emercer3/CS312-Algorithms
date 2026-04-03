import os
import sys
import json

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from generate_keypair import generate_key_pairs

from utils import measure_runtime


def main(sizes):
    keypairs = []

    def run_key_pair_gen(size):
        N, e, d = generate_key_pairs(size)
        keypairs.append((size, N, e, d))

    measure_runtime(sizes, run_key_pair_gen, "_keypairs")

    # Print keypairs to a file
    keypair_file = os.path.join(this_folder, "_keypairs.json")
    with open(keypair_file, "w") as file:
        json.dump(keypairs, file, indent=4)

    print(keypair_file, "written")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    sizes = [64, 128, 256, 512, 1024, 2048]

    sys.setrecursionlimit(sizes[-1] * 2)

    main(sizes)
