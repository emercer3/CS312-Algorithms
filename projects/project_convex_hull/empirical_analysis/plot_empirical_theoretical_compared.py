import json
import matplotlib.pyplot as plt
import os
import numpy as num

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))         #line 14 and 15 I added for devcontainer
    filename = os.path.join(script_dir, "_dvcq_convex_hull_runtimes.json")

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your theoretical time complexity
    def theoretical_big_o(n):
        return (num.log2(n)*n**.9)

    # FILL THIS IN from result using compute_coefficient
    coeff = 0.00031372594818718886

    nn, times = zip(*runtimes)

    # Plot empirical values
    fig = plt.figure()
    plt.scatter(nn, times, marker="o")

    predicted_runtime = [coeff * theoretical_big_o(n) for n, _ in runtimes]

    # Plot theoretical fit
    plt.plot(nn, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    plt.legend(["Observed", "Theoretical O(n^.9*log(n))"])
    plt.xlabel("n")
    plt.ylabel("runtime")
    plt.title("Time for DVCQ Convex Hull on Graph")
    fig.show()
    fig.savefig("empirical.svg")


if __name__ == "__main__":
    main()
