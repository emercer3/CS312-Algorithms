from byu_pytest_utils import print_markdown_table
import json
import numpy as np
import matplotlib.pyplot as plt


def main():

    # Experiment with different stats!

    # stat = "score"
    stat = "time"
    # stat = "max_queue_size"
    # stat = "n_nodes_expanded"
    # stat = "n_nodes_pruned"
    # stat = "n_leaves_covered"
    # stat = "fraction_leaves_covered"

    with open("_stretch2_stats.json", "r") as f:
        stats_combined = json.load(f)

    reg_stats = stats_combined[0]
    smart_stats = stats_combined[1]

    reg_attr = [round(entry[stat], 3) for entry in reg_stats]
    smart_attr = [round(entry[stat], 3) for entry in smart_stats]
    print(reg_attr)

    combined = zip(list(range(1, 21)), reg_attr, smart_attr)

    print_markdown_table(combined, ["Run", "Score (Regular)", "Score (Smart)"])

    x = np.arange(1, 21)
    width = 0.35

    fig, ax = plt.subplots()

    ax.bar(x - width / 2, reg_attr, width, color="red", label="Regular B&B")
    ax.bar(x + width / 2, smart_attr, width, color="blue", label="Smart B&B")

    ax.legend()
    ax.set_xlabel("Runs")
    ax.set_xticks([])
    ax.set_ylabel("Time")
    ax.set_title("B&B Regular vs. Smart")

    plt.show()
    fig.savefig("reg_v_smart.svg")


if __name__ == "__main__":
    main()
