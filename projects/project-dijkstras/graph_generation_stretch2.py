from road_graph import generate_road_graph
from road_plotting import plot_road_graph

from network_routing import find_shortest_path_with_heap_pq



def run_case(n, max_neighbors, seed, outfile, title):
    graph, positions = generate_road_graph(
        n=n,
        max_neighbors=max_neighbors,
        seed=seed
    )

    source = 0
    target = n - 1

    path, cost = find_shortest_path_with_heap_pq(graph, source, target)

    print(f"{title}")
    print(f"  Nodes: {n}")
    print(f"  Path length: {len(path)}")
    print(f"  Cost: {cost:.2f}\n")

    plot_road_graph(
        graph,
        positions,
        path,
        title=title,
        outfile=outfile
    )


def main():
    # -------------------------
    # Small graph
    # -------------------------
    run_case(
        n=50,
        max_neighbors=4,
        seed=1,
        outfile="road_graph_small.svg",
        title="Small Road Network (n = 50)"
    )

    # -------------------------
    # Medium graph
    # -------------------------
    run_case(
        n=150,
        max_neighbors=5,
        seed=2,
        outfile="road_graph_medium.svg",
        title="Medium Road Network (n = 150)"
    )

    # -------------------------
    # Large graph
    # -------------------------
    run_case(
        n=400,
        max_neighbors=6,
        seed=3,
        outfile="road_graph_large.svg",
        title="Large Road Network (n = 400)"
    )


if __name__ == "__main__":
    main()
