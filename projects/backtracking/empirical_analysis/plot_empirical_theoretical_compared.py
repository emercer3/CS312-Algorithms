import json
import matplotlib.pyplot as plt
import math

def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    # filename = "_greedy_runtimes.json"
    filename = "_backtracking_runtimes.json"

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your theoretical time complexity
    def theoretical_big_o(n, _):
        return math.factorial(n)

    # FILL THIS IN from result using compute_coefficient
    coeff = 2.6451957454284926e-06

    NN, times = zip(*runtimes)
    nn = [n[0] for n in NN]

    # Plot empirical values
    fig = plt.figure()
    plt.scatter(nn, times, marker="o")
    predicted_runtime = [coeff * theoretical_big_o(*n) for n, _ in runtimes]

    # Plot theoretical fit
    plt.plot(nn, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    plt.legend(["Observed", "Theoretical O(n!)"])
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("back")

    fig.show()
    fig.savefig("empirical_b.svg")


if __name__ == "__main__":
    main()
