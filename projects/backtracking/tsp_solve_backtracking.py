import math
import random
from collections import deque

from utils import Tour, SolutionStats, Timer, score_tour, Solver
from cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = []
    started = 0
    ind = started
    visited = []
    best = math.inf

    while not timer.time_out():
        if started == len(edges):
            break
        visited.append(ind)
        if len(visited) == len(edges):
            tour = Tour(visited)
            cost = score_tour(tour, edges)
            if cost < best:
                solutions.append(SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=0,
                n_nodes_expanded=0,
                n_nodes_pruned=0,
                n_leaves_covered=0,
                fraction_leaves_covered=0))
                best = cost
            else:
                visited = []
                started += 1
                ind = started
                continue
        else:
            min = math.inf

            for i in range(len(edges[ind])):
                if i in visited:
                    continue
                if edges[ind][i] == math.inf:
                    continue
                elif edges[ind][i] < min:
                    newindex = i
                    min = edges[ind][i]

            if min == math.inf:
                visited = []
                started += 1
                ind = started
                continue
            else:
                ind = newindex
    
    if len(solutions) == 0:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            0,
            0,
            0,
            0)]
    else:
        return solutions


def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = []
    best = math.inf
    cur = []
    Q = []
    level = 0

    for i in range(len(edges)):
        Q.append((i, level))

    while Q and not timer.time_out():
        P, call = Q.pop(0)

        if call < len(cur):
            cur.pop()
            Q = [(P, call)] + Q
        elif P not in cur:
            toappend = []
            cur.append(P)

            for p in range(len(edges)):
                if len(cur) == len(edges):
                    if edges[P][cur[0]] != math.inf:
                        tour = Tour(cur)
                        cost = score_tour(tour, edges)
                        if cost < best:
                            solutions.append(SolutionStats(
                            tour=tour,
                            score=cost,
                            time=timer.time(),
                            max_queue_size=0,
                            n_nodes_expanded=0,
                            n_nodes_pruned=0,
                            n_leaves_covered=0,
                            fraction_leaves_covered=0))
                            best = cost
                        cur.pop()
                    break
                elif p in cur:
                    continue
                elif edges[P][p] == math.inf:
                    continue
                else:
                    toappend.append((p, call+1))
                    
            Q = toappend + Q

    return solutions

def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = [greedy_tour(edges, Timer(1))[-1]]
    best = solutions[0].score
    cur = []
    Q = []
    level = 0
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    maxqueue = 0
    cut_tree = CutTree(len(edges))

    for i in range(len(edges)):
        Q.append((i, level))

    while Q and not timer.time_out():
        if len(Q) > maxqueue:
            maxqueue = len(Q)

        P, call = Q.pop(0)

        if call < len(cur):
            cur.pop()
            Q = [(P, call)] + Q
        elif P not in cur:
            n_nodes_expanded += 1
            toappend = []
            cur.append(P)

            for p in range(len(edges)):
                if len(cur) == len(edges):
                    if edges[P][cur[0]] != math.inf:
                        tour = Tour(cur)
                        cost = score_tour(tour, edges)
                        if cost < best:
                            solutions.append(SolutionStats(
                            tour=tour,
                            score=cost,
                            time=timer.time(),
                            max_queue_size=maxqueue,
                            n_nodes_expanded=n_nodes_expanded,
                            n_nodes_pruned=n_nodes_pruned,
                            n_leaves_covered=cut_tree.n_leaves_cut(),
                            fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
                            best = cost
                        cur.pop()
                    break
                elif score_tour(Tour(cur + [p]), edges) > best:
                    n_nodes_pruned += 1
                    cut_tree.cut(cur + [p])
                    continue
                elif p in cur:
                    continue
                elif edges[P][p] == math.inf:
                    n_nodes_pruned += 1
                    cut_tree.cut(cur + [p])
                    continue
                else:
                    toappend.append((p, call+1))
                    
            Q = toappend + Q

    return solutions