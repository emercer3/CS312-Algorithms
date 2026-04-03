import matplotlib.pyplot as plt


def plot_road_graph(
    graph,
    positions,
    path=None,
    title="Road Network with Shortest Path",
    outfile=None
):
    plt.figure(figsize=(10, 10))

    # Draw roads
    for u in graph:
        x1, y1 = positions[u]
        for v in graph[u]:
            x2, y2 = positions[v]
            plt.plot([x1, x2], [y1, y2], linewidth=0.5)

    # Draw cities
    xs = [positions[i][0] for i in positions]
    ys = [positions[i][1] for i in positions]
    plt.scatter(xs, ys, s=10)

    # Highlight shortest path
    if path and len(path) > 1:
        px = [positions[i][0] for i in path]
        py = [positions[i][1] for i in path]
        plt.plot(px, py, linewidth=3, label="Shortest Path")
        plt.legend()

    plt.title(title)
    plt.axis("off")

    if outfile:
        plt.savefig(outfile, format="svg", bbox_inches="tight")

    plt.show()
    plt.close()
