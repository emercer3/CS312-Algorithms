from byu_pytest_utils import compute_coefficient
import os

def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    script_dir = os.path.dirname(os.path.abspath(__file__))         #line 14 and 15 I added for devcontainer
    # runtime file is produced at the project root; resolve relative to repo root
    filename = os.path.abspath(os.path.join(script_dir, "..", "_banded_align_runtimes.json"))
    #filename = "_unbanded_align_runtimes.json"
    # filename = "_banded_align_runtimes.json"

    def theoretical_big_o(n):
        # FILL THIS IN with your theoretical time complexity
        return n

    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = None
    # plt.savefig(os.path.join(script_dir, "coefficient_other_plot.png")) # I added to make work in devcontainer
    compute_coefficient(filename, theoretical_big_o, start, end)


if __name__ == "__main__":
    main()
