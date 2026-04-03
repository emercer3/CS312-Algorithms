import json
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

    datasets = [
        (
            "_heap_pq_runtimes.json",
            "_linear_pq_runtimes.json",
            "Sparse Graphs"
        ),
        (
            "_heap_medium_pq_runtimes.json",
            "_linear_medium_pq_runtimes.json",
            "Medium Density Graphs"
        ),
        (
            "_heap_large_pq_runtimes.json",
            "_linear_large_pq_runtimes.json",
            "Dense Graphs"
        ),
    ]

    fig = plt.figure(figsize=(18, 6))

    for idx, (heap_file, linear_file, title) in enumerate(datasets, start=1):
        heap_data = load_data(os.path.join(base_dir, heap_file))
        linear_data = load_data(os.path.join(base_dir, linear_file))

        vh, eh, th = zip(*heap_data)
        vl, el, tl = zip(*linear_data)

        ax = fig.add_subplot(1, 3, idx, projection="3d")

        ax.scatter(vh, eh, th, marker="o", label="Heap PQ")
        ax.scatter(vl, el, tl, marker="^", label="Linear PQ")

        ax.set_xlabel("|V|")
        ax.set_ylabel("|E|")
        ax.set_zlabel("Runtime")
        ax.set_title(title)
        ax.view_init(elev=10, azim=-60)

        if idx == 1:
            ax.legend()

    fig.suptitle("Dijkstra Runtime Comparison: Density vs Input Size vs PQ Implementation")
    plt.tight_layout()
    plt.savefig("dijkstra_pq_comparison.svg")
    plt.show()


if __name__ == "__main__":
    main()
