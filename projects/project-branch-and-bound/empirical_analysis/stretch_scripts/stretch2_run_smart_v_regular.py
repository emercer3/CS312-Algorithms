from copy import deepcopy
from time import time_ns
import json
import os
import random
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, "..", ".."))

from tsp_core import generate_network, Timer
from tsp_solve import branch_and_bound, branch_and_bound_smart


def convert(solution_stat):
    converted = {
        "score": solution_stat.score,
        "time": solution_stat.time,
        "max_queue_size": solution_stat.max_queue_size,
        "n_nodes_expanded": solution_stat.n_nodes_expanded,
        "n_nodes_pruned": solution_stat.n_nodes_pruned,
        "n_leaves_covered": solution_stat.n_leaves_covered,
        "fraction_leaves_covered": solution_stat.fraction_leaves_covered,
    }
    return converted


def main(n, timeout: int, runs: int, **kwargs):

    random.seed(time_ns())

    reg_stats = []
    smart_stats = []

    for x in range(runs):
        print(f"Running iteration {x + 1}")

        seed = random.randint(0, 5000)
        _, edges = generate_network(n, seed=seed, **kwargs)

        timer = Timer(timeout)
        reg_final = branch_and_bound(deepcopy(edges), timer)[-1]
        timer = Timer(timeout)
        smart_final = branch_and_bound_smart(deepcopy(edges), timer)[-1]

        reg_stats.append(convert(reg_final))
        smart_stats.append(convert(smart_final))

    combined = [reg_stats, smart_stats]

    with open("_stretch2_stats.json", "w") as f:
        json.dump(combined, f, indent=4)


if __name__ == "__main__":

    # Adjust the timeout if needed

    main(15, timeout=5, runs=20, euclidean=True, reduction=0.2, normal=False)
