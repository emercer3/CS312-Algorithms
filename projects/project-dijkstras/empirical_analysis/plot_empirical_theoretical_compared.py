import json
import matplotlib.pyplot as plt
import os
import numpy as n

def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary
    script_dir = os.path.dirname(os.path.abspath(__file__))         #line 14 and 15 I added for devcontainer
    filename = os.path.join(script_dir, "_heap_pq_runtimes.json")
    # filename = "_linear_pq_runtimes.json"
    # filename = '_heap_pq_runtimes.json'

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your theoretical time complexity
    def theoretical_big_o(v, e):
        return (v + e)*n.log2(v)

    # FILL THIS IN from result using compute_coefficient
    coeff = 4.474421771761552e-06

    vv, ee, times = zip(*runtimes)

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(vv, ee, times, marker="o")

    predicted_runtime = [coeff * theoretical_big_o(v, e) for v, e, t in runtimes]

    # Plot theoretical fit
    ax.plot(vv, ee, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    ax.legend(["Observed", "Theoretical O((V + E)log(V))"])
    ax.set_xlabel("|V|")
    ax.set_ylabel("|E|")
    ax.set_zlabel("Runtime")
    ax.set_title("Time for Dijkstras on Graph")

    # You are welcome to play with the view angle as you'd like
    # elev=0 with azim=0 and azim=90 might be interesting
    ax.view_init(elev=10, azim=-60)

    fig.show()
    fig.savefig("empirical_hpq.svg")


if __name__ == "__main__":
    main()
