import matplotlib.pyplot as plt

from utils import (generate_network, Timer,SolutionStats, Solver)
from tsp_plot import (plot_network, plot_tour, plot_solutions, plot_coverage,
                      plot_queue_size,
                      plot_solution_evolution,
                      plot_edge_probability)
from tsp_run import format_text_summary, format_plot_summary

def plot_node_expanded(solutions: dict[str, list[SolutionStats]], ax=None):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [st.n_nodes_expanded for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Number of Nodes Expanded')

def plot_node_pruned(solutions: dict[str, list[SolutionStats]], ax=None):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [st.n_nodes_pruned for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Number of Nodes Pruned')


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

    # 1) Queue Size
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_queue_size({name: stats}, ax=ax)
    ax.set_title("Queue Size")
    fig.savefig(f"{name}_queue_size.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 2) nodes expanded
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_node_expanded({name: stats}, ax=ax)
    ax.set_title("Node Expanded")
    fig.savefig(f"{name}_nodes_expanded.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 3) nodes pruned
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_node_pruned({name: stats}, ax=ax)
    ax.set_title("Node Pruned")
    fig.savefig(f"{name}_nodes_pruned.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 4) Coverage
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_coverage({name: stats}, ax=ax)
    ax.set_title("Coverage")
    fig.savefig(f"{name}_coverage.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == '__main__':
    from tsp_solve_backtracking import (random_tour, greedy_tour, backtracking, backtracking_bssf)

    main(
        12,
        # random_tour,
        # greedy_tour,
        backtracking_bssf,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=3,
        timeout=30
    )