import json
import matplotlib.pyplot as plt
import os
import numpy as num


def compute_coefficient(observed_performance, theoretical_order):
    return [time / theoretical_order(n) for n, time in observed_performance]


def main():

    #filename = "_dvcq_convex_hull_runtimes.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))         #line 14 and 15 I added for devcontainer
    filename = os.path.join(script_dir, "_other_convex_hull_runtimes.json")

    with open(filename, "r") as f:
        runtimes = json.load(f)

    def theoretical_big_o(n):
        # FILL THIS IN with your theoretical time complexity
        return (num.log2(n)*n)

    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    # slice this list to use a subset for your estimate
    used_coeffs = coeffs[0:]

    coeff = sum(used_coeffs) / len(used_coeffs)
    print(coeff)

    plt.bar(range(len(coeffs)), coeffs)
    xlim = plt.xlim()
    plt.plot(xlim, [coeff, coeff], ls=":", c="k")
    plt.xlim(xlim)
    plt.title(f"coeff={coeff}")
    plt.savefig(os.path.join(script_dir, "coefficient_other_plot.png")) # I added to make work in devcontainer
    plt.show()


if __name__ == "__main__":
    main()
