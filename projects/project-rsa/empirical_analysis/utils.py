import os
import json
from time import time
from typing import Callable


def compute_average_runtimes(runtimes):
    groups = {}
    for size, runtime in runtimes:
        key = size
        if key not in groups:
            groups[key] = []
        groups[key].append(runtime)

    return [
        (
            size,
            round(sum(stats) / len(stats), 3),
        )
        for size, stats in groups.items()
    ]


def print_markdown_table(ave_runtimes, headers):
    header_widths = [len(header) for header in headers]

    rows = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("-" * len(header) for header in headers) + " |",
    ]

    rows += (
        "| "
        + " | ".join(f"{field:<{width}}" for field, width in zip(row, header_widths))
        + " |"
        for row in ave_runtimes
    )

    print("Copy this markdown table into your report:")
    print()
    print("\n".join(rows))


def measure_runtime(sizes: list[int], run: Callable[[int], None], fname_stem: str):
    runtimes = []
    try:
        for size in sizes:
            print("Running with size", size)
            for iteration in range(10):
                start = time()

                run(size)

                runtime = time() - start
                runtimes.append((size, runtime))

    except KeyboardInterrupt:
        print("Cancelling")

    ave_runtimes = compute_average_runtimes(runtimes)

    print()

    print_markdown_table(ave_runtimes, ["Size ", "Time (sec)"])

    # Print runtimes to a file
    this_folder = os.path.dirname(__file__)
    filename = fname_stem + "_runtimes.json"
    runtimes_file = os.path.join(this_folder, filename)
    with open(runtimes_file, "w") as file:
        json.dump(runtimes, file, indent=4)

    print()
    print(runtimes_file, "written")
