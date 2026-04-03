import json
import os
import sys
from time import time

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))
sys.path.append(os.path.join(this_folder, "..", ".."))

from main import generate_graph
from network_routing import (
    find_shortest_path_with_linear_pq,
    find_shortest_path_with_heap_pq,
)
from utils import compute_average_runtimes, print_markdown_table


def main(sizes, densities, n_reps):
    linear_runtimes = {}
    heap_runtimes = {}
    for density in densities:
        linear_runtimes[density] = []
        heap_runtimes[density] = []
    for density in densities:
        print()
        print('Running with density', density)
        try:
            for size in sizes:
                _, graph = generate_graph(312, size, density, 0.05, "uniform")

                print("Running with size", size, flush=True, end='')
                size_start = time()
                for iteration in range(n_reps):
                    print('.', end='', flush=True)
                    start = time()

                    find_shortest_path_with_linear_pq(graph, 0, size / 2)

                    runtime = time() - start
                    linear_runtimes[density].append((size, density, runtime))

                    start = time()

                    find_shortest_path_with_heap_pq(graph, 0, size / 2)

                    runtime = time() - start
                    heap_runtimes[density].append((size, density, runtime))
                print(time() - size_start, 'seconds elapsed', flush=True)

        except KeyboardInterrupt:
            print("Cancelling density " + str(density))

    l_low_runtimes, l_high_runtimes = linear_runtimes.values()
    h_low_runtimes, h_high_runtimes = heap_runtimes.values()

    ll_ave_runtimes = compute_average_runtimes(l_low_runtimes, densities[0])
    hl_ave_runtimes = compute_average_runtimes(h_low_runtimes, densities[0])

    lh_ave_runtimes = compute_average_runtimes(l_high_runtimes, densities[1])
    hh_ave_runtimes = compute_average_runtimes(h_high_runtimes, densities[1])

    l_size, l_density, l_runtime = zip(*ll_ave_runtimes)
    _, _, h_runtime = zip(*hl_ave_runtimes)

    low_combined = zip(l_size, l_density, h_runtime, l_runtime)

    l_size, l_density, l_runtime = zip(*lh_ave_runtimes)
    _, _, h_runtime = zip(*hh_ave_runtimes)

    high_combined = zip(l_size, l_density, h_runtime, l_runtime)

    print()

    print_markdown_table(
        low_combined, ["V   ", "Density", "heap time (sec)", "linear PQ time (sec)"]
    )

    print()

    print_markdown_table(
        high_combined, ["V   ", "Density", "heap time (sec)", "linear PQ time (sec)"]
    )

    # Print runtimes to a file
    this_folder = os.path.dirname(__file__)
    filename = "_stretch1_linear_runtimes.bk.json"
    runtimes_file = os.path.join(this_folder, filename)
    with open(runtimes_file, "w") as file:
        combined = [ll_ave_runtimes, lh_ave_runtimes]
        json.dump(combined, file, indent=4)

    print()
    print(runtimes_file, "written")

    this_folder = os.path.dirname(__file__)
    filename = "_stretch1_heap_runtimes.bk.json"
    runtimes_file = os.path.join(this_folder, filename)
    with open(runtimes_file, "w") as file:
        combined = [hl_ave_runtimes, hh_ave_runtimes]
        json.dump(combined, file, indent=4)

    print()
    print(runtimes_file, "written")


if __name__ == "__main__":
    # As these numbers get large, it may take a long time to run (more than 30 minutes total)
    # While long waits are inconvenient, running as large as you can will give you better data
    # If it is taking too long, you can omit the larger numbers
    # Or kill the process (ctrl + c) before it finishes-- your times calculated up to that point will be recorded
    # You can also try running fewer replicates per size/density combination
    # sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    sizes = [500, 1000, 2000, 4000, 8000, 10000, 12000, 14000, 16000]
    densities = [0.6, 1.0]
    n_reps = 3
    main(sizes, densities, n_reps)
