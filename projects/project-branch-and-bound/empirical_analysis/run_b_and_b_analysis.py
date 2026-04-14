import itertools
import json
import os
import random
import sys

from time import time_ns

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from tsp_solve import branch_and_bound
from tsp_core import generate_network, Timer

from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def _preprocessing(size):
    random.seed(time_ns())
    seed = random.randint(0, 5000)
    _, edges = generate_network(
        size,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=seed,
    )

    return edges


def _b_and_b(*edges):
    timer = Timer(120)
    edges = list(edges)
    branch_and_bound(edges, timer)


def main(input):
    measure_runtime(
        _b_and_b,
        input,
        preprocessing=_preprocessing,
    )

    with open("_b_and_b_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes)


if __name__ == "__main__":
    sizes = [5, 10, 12, 15, 17, 19]

    iterations = 5
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))

    main(input_tuples)
