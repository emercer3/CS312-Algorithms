import random
import sys
from time import time

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)


def explore(g : GRAPH, n : str, dictlist : dict[str, list[int]], counter : int, visited : list[str]) -> tuple[list[str], dict[str, list[int]], int]:    # O(v + e)
    pre = counter                   # pre visit
    dictlist[n] = [pre, 0]
    visited.append(n)

    for branch in g[n]:                             # O(e)
        if branch not in visited:
            visited, dictlist, counter = explore(g, branch, dictlist, counter+1, visited)   # O(v)

    counter+= 1
    dictlist[n][1] = counter        # post visit
    return visited, dictlist, counter


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:        # O(V + E)
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    DFSorders = []
    visited = []
    counter = 0

    for n in graph:                     # O(v)
        if n not in visited:
            counter+= 1
            visited, final, counter = explore(graph, n, {}, counter, visited)   # O(v + e)
            DFSorders.append(final)

    return DFSorders


def reverse_graph(graph: GRAPH) -> GRAPH:       # O(V + E)
    new_graph = {}

    for node in graph:                              # O(v)
        new_graph[node] = []
        for branch in graph[node]:                  # O(e)
            if branch not in new_graph:
                new_graph[branch] = [node]
            else:
                new_graph[branch].append(node)

    return new_graph


def get_post_order(graph: GRAPH, prepost: list[dict[str, list[int]]]) -> dict[str, list[str]]:  # O(v^2)
    trees = {}
    new_ordered_graph = {}

    for tree in prepost:    # O(v)
        trees.update(tree)

    for i in range(2*(len(trees)+1), 0, -1):    # O(2*v)
        for node in trees:                      # O(v)
            if trees[node][1] == i:
                new_ordered_graph[node] = graph[node]
    
    return new_ordered_graph

            
def sink_to_source(prepost: list[dict[str, list[int]]]) -> list[set[str]]:  # O(v)
    final = []

    for tree in prepost:    # O(v)
        set = []
        for node in tree:
            set.append(node)
        final.append(set)

    return final

            

def find_sccs(graph: GRAPH) -> list[set[str]]:  # O(V^2)
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    reversed_graph = reverse_graph(graph)   # O(V+E)
    order = prepost(reversed_graph)         # O(V+E)
    new_ordered_graph = get_post_order(graph, order)    # O(v^2)
    scc = prepost(new_ordered_graph)        # O(V+E)
    return sink_to_source(scc)          # O(v)


def helper(node: str, branch: str, trees: list[dict[str, list[int]]]) -> :
    return 0


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    for node in graph:
        for branch in graph[node]:
            for n in trees:
                for b in trees:
                    if node in n and branch in b:
                        if n[node][0] < b[branch][0] < b[branch][1] < n[node][1]:
                            classification['tree/forward'].add((node, branch))
                        elif b[branch][0] < n[node][0] < n[node][1] < b[branch][1]:
                            classification['back'].add((node, branch))
                        elif b[branch][0] < b[branch][1] < n[node][0] < n[node][1]:
                            classification['cross'].add((node, branch))

    return classification


