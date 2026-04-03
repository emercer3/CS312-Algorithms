import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from scc import prepost

from utils import measure_runtime


def main(densities, sizes):
    measure_runtime(densities, sizes, prepost, "_prepost")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    sizes = [10, 50, 100, 500, 2000, 4000, 8000]
    #densities = [0.25, 0.5, 1.0, 2.0, 3.0]
    densities = [0.25, 0.5, 1.0, 2.0, 3.0]
    main(densities, sizes)
