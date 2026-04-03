import json
import matplotlib.pyplot as plt
import os


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary
    script_dir = os.path.dirname(os.path.abspath(__file__))         #line 14 and 15 I added for devcontainer
    filename = os.path.join(script_dir, "_banded_align_runtimes.json")
    #filename = "_unbanded_align_runtimes.json"
    # filename = "_banded_align_runtimes.json"

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your theoretical time complexity
    def theoretical_big_o(n):
        return n

    # FILL THIS IN from result using compute_coefficient
    coeff = 6.416116734345754e-06

    nn, times = zip(*runtimes)

    # Plot empirical values
    fig = plt.figure()
    plt.scatter(nn, times, marker="o")

    predicted_runtime = [coeff * theoretical_big_o(*n) for n, _ in runtimes]

    # Plot theoretical fit
    plt.plot(nn, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    plt.legend(["Observed", "Theoretical O(n)"])
    plt.xlabel("n")
    plt.ylabel("Runtime")
    plt.title("Time for banded Align")

    fig.show()
    fig.savefig("empirical_bounded.svg")


if __name__ == "__main__":
    main()
