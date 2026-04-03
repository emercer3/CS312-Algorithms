import random
import math


def generate_road_graph(
    n: int,
    max_neighbors: int = 4,
    width: int = 1000,
    height: int = 1000,
    seed: int | None = None
):
    if seed is not None:
        random.seed(seed)

    # City locations
    positions = {
        i: (random.uniform(0, width), random.uniform(0, height))
        for i in range(n)
    }

    graph = {i: {} for i in range(n)}

    def dist(a, b):
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        return math.hypot(x1 - x2, y1 - y2)

    # Connect nearby cities
    for i in range(n):
        neighbors = sorted(
            (j for j in range(n) if j != i),
            key=lambda j: dist(i, j)
        )
        for j in neighbors[:max_neighbors]:
            d = dist(i, j)
            graph[i][j] = d
            graph[j][i] = d

    # Ensure connectivity
    visited = set()

    def dfs(u):
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v)

    dfs(0)
    for i in range(n):
        if i not in visited:
            j = min(visited, key=lambda v: dist(i, v))
            d = dist(i, j)
            graph[i][j] = d
            graph[j][i] = d
            dfs(i)

    return graph, positions
