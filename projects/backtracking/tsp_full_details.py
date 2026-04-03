import matplotlib.pyplot as plt

from utils import (generate_network, Timer, Solver)
from tsp_plot import (plot_network, plot_tour, plot_solutions, plot_coverage,
                      plot_queue_size,
                      plot_solution_evolution,
                      plot_edge_probability)
from tsp_run import format_text_summary, format_plot_summary


def main(n, find_tour: Solver, timeout=60, **kwargs):
    # Generate network
    print(f'Generating network of size {n} with args: {kwargs}')
    locations, edges = generate_network(n, **kwargs)

    # Solve
    timer = Timer(timeout)
    stats = find_tour(edges, timer)
    name = find_tour.__name__
    print(format_text_summary(name, stats[-1]))
    print(f'Total solutions found: {len(stats)}')

    draw_edges = n <= 10

    # 1) Network + Tour
    fig, ax = plt.subplots(figsize=(8, 8))
    plot_network(locations, edges, edge_alpha=0.5 if draw_edges else 0.1, ax=ax)
    if stats[-1].tour:
        plot_tour(locations, stats[-1].tour, ax=ax)

    summary = format_plot_summary(name, stats[-1])
    ax.set_title(f"Network + Tour\n{summary}")
    fig.savefig(f"{name}_network_tour.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 2) Solutions Found Over Time
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_solutions({name: stats}, ax)
    ax.set_title("Solutions Found")
    fig.savefig(f"{name}_solutions.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 3) Coverage
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_coverage({name: stats}, ax=ax)
    ax.set_title("Coverage")
    fig.savefig(f"{name}_coverage.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 4) Queue Size
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_queue_size({name: stats}, ax=ax)
    ax.set_title("Queue Size")
    fig.savefig(f"{name}_queue_size.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 5) Edge Probability
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_edge_probability({name: stats}, edges, ax=ax)
    ax.set_title("Edge Probability")
    fig.savefig(f"{name}_edge_probability.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 6) Solution Evolution
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_solution_evolution([st.tour for st in stats], ax=ax)
    ax.set_title("Solution Evolution")
    fig.savefig(f"{name}_solution_evolution.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # # Report and Plot
    # n_plots = 7

    # fig, axs = plt.subplots(n_plots, 1, figsize=(8, 8 * n_plots))
    # if n_plots > 1:
    #     axs = axs.flatten()
    # else:
    #     axs = [axs]

    # draw_edges = n <= 10

    # # Plot network and solution
    # ax = axs[0]
    # plot_network(locations, edges, edge_alpha=0.5 if draw_edges else 0.1, ax=ax)
    # if stats[-1].tour:  # i.e. if there was a solution
    #     plot_tour(locations, stats[-1].tour, ax=ax)
    # summary = format_plot_summary(name, stats[-1])
    # ax.set_title(summary)

    # # Plot stats
    # plot_solutions({name: stats}, axs[1])

    # plot_coverage({name: stats}, ax=axs[3])
    # plot_queue_size({name: stats}, ax=axs[4])
    # plot_edge_probability({name: stats}, edges, ax=axs[5])
    # plot_solution_evolution([st.tour for st in stats], ax=axs[6])
    # fig.savefig(f"{name}_n{n}.png", dpi=300, bbox_inches="tight")
    # plt.show()


if __name__ == '__main__':
    from tsp_solve_backtracking import (random_tour, greedy_tour, backtracking, backtracking_bssf)

    main(
        12,
        random_tour,
        # greedy_tour,
        # backtracking_bssf,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=3,
        timeout=30
    )
