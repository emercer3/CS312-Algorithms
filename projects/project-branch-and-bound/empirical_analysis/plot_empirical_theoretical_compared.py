import json
import matplotlib.pyplot as plt


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_b_and_b_runtimes.json"

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your theoretical time complexity
    def theoretical_big_o(n):
        return 2.5**n

    # FILL THIS IN from result using compute_coefficient
    coeff = 9.699481027925547e-06

    NN, times = zip(*runtimes)
    nn = [n[0] for n in NN]

    # Plot empirical values
    fig = plt.figure()
    plt.scatter(nn, times, marker="o")
    predicted_runtime = [coeff * theoretical_big_o(*n) for n, _ in runtimes]

    # Plot theoretical fit
    plt.plot(nn, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    plt.legend(["Observed", "Theoretical O(2.5^n)"])
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("Branch and Bound")

    fig.show()
    fig.savefig("empirical.svg")


if __name__ == "__main__":
    main()
