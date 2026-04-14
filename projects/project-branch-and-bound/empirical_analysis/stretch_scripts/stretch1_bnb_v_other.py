from copy import deepcopy
import matplotlib.pyplot as plt
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, "..", ".."))

from tsp_core import generate_network, Timer, Solver


def main(n, b_and_b: Solver, other_tour: Solver, timeout: int, **kwargs):

    # Generate
    print(f"Generating network of size {n} with args: {kwargs}")
    _, edges = generate_network(n, **kwargs)

    # Solve

    other_times = []
    other_coverage = []

    b_and_b_times = []
    b_and_b_coverage = []

    print("Running backtracking solver...")
    timer = Timer(timeout)
    other_stats = other_tour(deepcopy(edges), timer)
    print("Running branch and bound...")
    timer = Timer(timeout)
    b_and_b_stats = b_and_b(deepcopy(edges), timer)

    for result in other_stats:
        other_times.append(result.time)
        other_coverage.append(round(result.fraction_leaves_covered * 100, 4))

    for result in b_and_b_stats:
        b_and_b_times.append(result.time)
        b_and_b_coverage.append(round(result.fraction_leaves_covered * 100, 4))

    fig = plt.figure()

    plt.scatter(other_times, other_coverage, marker="o", c="k")
    plt.plot(other_times, other_coverage, c="k", lw=2, label="BSSF_backtracking")

    plt.scatter(b_and_b_times, b_and_b_coverage, marker="o", c="r")
    plt.plot(b_and_b_times, b_and_b_coverage, c="r", lw=2, label="Branch and Bound")

    plt.legend()
    plt.xlabel("Solution time (sec)")
    plt.ylabel("Fraction of leaves covered (%)")
    plt.title("TSP Solvers Compared -- Fraction of Leaves")

    fig.show()
    fig.savefig("time_vs_solution.svg")

    plt.show()


if __name__ == "__main__":
    from tsp_solve import (
        random_tour,
        greedy_tour,
        backtracking,
        branch_and_bound,
        backtracking_bssf,
    )

    # Uncomment one of your tours from project backtracking to compare B&B to

    main(
        12,
        branch_and_bound,
        # random_tour,
        # greedy_tour,
        # backtracking,
        backtracking_bssf,
        timeout=60,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )
