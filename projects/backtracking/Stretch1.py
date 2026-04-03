import matplotlib.pyplot as plt
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from tsp_solve_backtracking import (
    backtracking,
    backtracking_bssf,
    greedy_tour,
    random_tour,
)

from utils import generate_network, Timer

def main():
    backtracking_times = []
    backtracking_scores = []

    bssf_times = []
    bssf_scores = []

    _, edges = generate_network(15, euclidean=True, reduction=0, normal=False, seed=312)

    print(f"Begin backtracking")
    timer = Timer(30)
    backtracking_results = backtracking(edges, timer)

    print(f"Begin BSSF")
    timer = Timer(30)
    bssf_results = backtracking_bssf(edges, timer)

    for result in backtracking_results:
        backtracking_times.append(result.time)
        backtracking_scores.append(result.score)

    for result in bssf_results:
        bssf_times.append(result.time)
        bssf_scores.append(result.score)

    print(f"backtracing best score: {backtracking_scores} in time of {backtracking_times}")
    print(f"BSSF best score: {bssf_scores} in time of {bssf_times}")

if __name__ == "__main__":
    main()
