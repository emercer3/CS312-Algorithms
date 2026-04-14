import math
import random
from queue import PriorityQueue
import itertools

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 20,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 4659,
    "timeout": 20,
}
# "n": 30,
#     "euclidean": True,
#     "reduction": 0.2,
#     "normal": False,
#     "seed": 312,
#     "timeout": 20,

# "n": 15,
#     "euclidean": True,
#     "reduction": 0.2,
#     "normal": False,
#     "seed": 4659,
#     "timeout": 20,

def make_matrix(edges: list[list[float]]) -> dict[float]:
    matrix = {}

    for j in range(len(edges)):
        for i in range(len(edges)):
            if i == j:
                matrix[j, i] = math.inf
            else:
                matrix[j, i] = edges[j][i]

    return matrix

def reduce_matrix(edges: list[list[float]], m: dict[float]) -> int:
    min_cost = 0
    min_row = math.inf
    row = 0
    col = 0
    finding = True

    while row < len(edges):
        if finding:
            if col == len(edges):
                finding = False
                col = 0
                continue
            if m[row, col] < min_row:
                min_row = m[row, col]
            col += 1
        else:
            if col == len(edges):
                finding = True
                row += 1
                col = 0
                if min_row != math.inf:
                    min_cost += min_row
                    min_row = math.inf
            elif min_row == math.inf:
                col +=1
                continue
            else:
                m[row, col] = m[row, col] - min_row
                col +=1

    min_col = math.inf
    row = 0
    col = 0
    finding = True

    while col < len(edges):
        if finding:
            if row == len(edges):
                finding = False
                row = 0
                continue
            if m[row, col] < min_col:
                min_col = m[row, col]
            row += 1
        else:
            if row == len(edges):
                finding = True
                col += 1
                row = 0
                if min_col != math.inf:
                    min_cost += min_col
                    min_col = math.inf
            elif min_col == math.inf:
                row +=1
                continue
            else:
                m[row, col] = m[row, col] - min_col
                row +=1
                
    return min_cost
            
def reduce_a_path(edges: list[list[float]], m: dict[float], wasat: int, tovisit: int, cur_cost: int) -> tuple[dict[float], int]:
    cur_cost += m[wasat, tovisit]
    m[tovisit, 0] = math.inf
    for row in range(len(edges)):
        for col in range(len(edges)):
            if row == wasat:
                m[row, col] = math.inf
            elif col == tovisit:
                m[row, col] = math.inf
    
    cur_cost += reduce_matrix(edges, m)
    return m, cur_cost

def sum_matrix(edges: list[list[float]], m: dict[float], lb : int) -> int:
    total = 0

    for j in range(len(edges)):
        for i in range(len(edges)):
            if i == j:
                continue
            elif m[j, i] != math.inf:
                total += m[j, i]

    return total






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

        stats.append(
            SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=1,
                n_nodes_expanded=n_nodes_expanded,
                n_nodes_pruned=n_nodes_pruned,
                n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered(),
            )
        )

    if not stats:
        return [
            SolutionStats(
                [],
                math.inf,
                timer.time(),
                1,
                n_nodes_expanded,
                n_nodes_pruned,
                cut_tree.n_leaves_cut(),
                cut_tree.fraction_leaves_covered(),
            )
        ]


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
    solutions = [greedy_tour(edges, Timer(1))[-1]]
    best = solutions[0].score
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
    Q = [(0, 0)]
    level = 0
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    maxqueue = 0
    cut_tree = CutTree(len(edges))

    # for i in range(len(edges)):
    #     Q.append((i, level))

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


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = [greedy_tour(edges, Timer(1))[-1]]
    best = solutions[0].score
    matrix = make_matrix(edges)
    cost = reduce_matrix(edges, matrix)
    cur = []
    Q = []
    level = 0
    orginal = matrix.copy()

    # for stretch 1 
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    maxqueue = 0
    cut_tree = CutTree(len(edges))

    Q.append((0, level, matrix.copy(), cost))

    while Q and not timer.time_out():
        if len(Q) > maxqueue:   # stretch 1
            maxqueue = len(Q)

        P, call, m, c = Q.pop(0)

        if call < len(cur):
            cur.pop()
            Q = [(P, call, m, c)] + Q
        elif c > best:
            n_nodes_pruned += 1 # stretch 1
            cut_tree.cut(cur + [P])
            continue
        elif P not in cur:
            n_nodes_expanded += 1   # stretch 1
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
                elif p in cur:
                    continue
                elif edges[P][p] == math.inf:
                    n_nodes_pruned += 1 # stretch 1
                    cut_tree.cut(cur + [p])
                    continue
                cur_m, cur_cost = reduce_a_path(edges, m.copy(), P, p, c)
                if cur_cost > best:
                    n_nodes_pruned += 1 # stretch 1
                    cut_tree.cut(cur + [p])
                    continue
                else:
                    toappend.append((p, call+1, cur_m, cur_cost))
                    
            Q = toappend + Q

    return solutions

# def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     solutions = [greedy_tour(edges, Timer(1))[-1]]
#     best = solutions[0].score
#     matrix = make_matrix(edges)
#     cost = reduce_matrix(edges, matrix)
#     cur = []
#     PQ = PriorityQueue()
#     level = 0
#     orginal = matrix.copy()
#     heigth = len(edges)
#     # for stretch 1 
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     maxqueue = 0
#     cut_tree = CutTree(len(edges))

#     PQ.put((sum_matrix(edges, matrix, cost), heigth, (0, level, matrix.copy(), cost, cur)))

#     while not PQ.empty() and not timer.time_out():

#         tlb, h ,(P, call, m, c, path) = PQ.get()

#         # if call < len(path):
#         #     cur.pop()
#         #     PQ.put((tlb, h, (P, call, m, c, path)))
#         if c > best:
#             n_nodes_pruned += 1 # stretch 1
#             cut_tree.cut(path + [P])
#             continue
#         elif P not in path:
#             n_nodes_expanded += 1   # stretch 1
#             new_path = path + [P]

#             for p in range(len(edges)):
#                 if len(new_path) == len(edges):
#                     if edges[P][new_path[0]] != math.inf:
#                         tour = Tour(new_path)
#                         cost = score_tour(tour, edges)
#                         if cost < best:
#                             solutions.append(SolutionStats(
#                             tour=tour,
#                             score=cost,
#                             time=timer.time(),
#                             max_queue_size=maxqueue,
#                             n_nodes_expanded=n_nodes_expanded,
#                             n_nodes_pruned=n_nodes_pruned,
#                             n_leaves_covered=cut_tree.n_leaves_cut(),
#                             fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
#                             best = cost
#                     break
#                 elif p in new_path:
#                     continue
#                 elif edges[P][p] == math.inf:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(new_path + [p])
#                     continue
#                 cur_m, cur_lb = reduce_a_path(edges, m.copy(), P, p, c)
#                 if cur_lb > best:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(new_path + [p])
#                     continue
#                 else:
#                     PQ.put((sum_matrix(edges, cur_m, cur_lb), h-1, (p, call+1, cur_m, cur_lb, new_path)))

#     return solutions




# def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     solutions = [greedy_tour(edges, Timer(1))[-1]]
#     best = solutions[0].score
#     matrix = make_matrix(edges)
#     cost = reduce_matrix(edges, matrix)
#     cur = []
#     PQ = PriorityQueue()
#     level = 0
#     orginal = matrix.copy()
#     heigth = len(edges)
#     # for stretch 1 
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     maxqueue = 0
#     cut_tree = CutTree(len(edges))
#     counter = itertools.count()

#     PQ.put((cost, heigth, counter, (0, level, matrix.copy(), cost)))

#     while not PQ.empty() and not timer.time_out():

#         lb, h, count, (P, call, m, c) = PQ.get()

#         if call < len(cur):
#             cur.pop()
#             PQ.put((lb, h, count, (P, call, m, c)))
#         elif c > best:
#             n_nodes_pruned += 1 # stretch 1
#             cut_tree.cut(cur + [P])
#             continue
#         elif P not in cur:
#             n_nodes_expanded += 1   # stretch 1
#             toappend = []
#             cur.append(P)

#             for p in range(len(edges)):
#                 if len(cur) == len(edges):
#                     if edges[P][cur[0]] != math.inf:
#                         tour = Tour(cur)
#                         cost = score_tour(tour, edges)
#                         if cost < best:
#                             solutions.append(SolutionStats(
#                             tour=tour,
#                             score=cost,
#                             time=timer.time(),
#                             max_queue_size=maxqueue,
#                             n_nodes_expanded=n_nodes_expanded,
#                             n_nodes_pruned=n_nodes_pruned,
#                             n_leaves_covered=cut_tree.n_leaves_cut(),
#                             fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
#                             best = cost
#                         cur.pop()
#                     break
#                 elif p in cur:
#                     continue
#                 elif edges[P][p] == math.inf:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(cur + [p])
#                     continue
#                 cur_m, cur_lb = reduce_a_path(edges, m.copy(), P, p, c)
#                 if cur_lb > best:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(cur + [p])
#                     continue
#                 else:
#                     PQ.put((cur_lb, h-1, next(counter), (p, call+1, cur_m, cur_lb)))

#     return solutions

# def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     solutions = [greedy_tour(edges, Timer(1))[-1]]
#     best = solutions[0].score
#     matrix = make_matrix(edges)
#     cost = reduce_matrix(edges, matrix)
#     cur = []
#     PQ = PriorityQueue()
#     level = 0
#     orginal = matrix.copy()
#     heigth = len(edges)
#     # for stretch 1 
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     maxqueue = 0
#     cut_tree = CutTree(len(edges))

#     PQ.put((heigth*cost, (0, level, matrix.copy(), cost, cur, heigth)))

#     while not PQ.empty() and not timer.time_out():

#         priority, (P, call, m, c, path, h) = PQ.get()

#         if call < len(path):
#             path.pop()
#             PQ.put((priority, (P, call, m, c, path, h)))
#         elif c > best:
#             n_nodes_pruned += 1 # stretch 1
#             cut_tree.cut(path + [P])
#             continue
#         elif P not in cur:
#             n_nodes_expanded += 1   # stretch 1
#             path.append(P)

#             for p in range(len(edges)):
#                 if len(path) == len(edges):
#                     if edges[P][path[0]] != math.inf:
#                         tour = Tour(path)
#                         cost = score_tour(tour, edges)
#                         if cost < best:
#                             solutions.append(SolutionStats(
#                             tour=tour,
#                             score=cost,
#                             time=timer.time(),
#                             max_queue_size=maxqueue,
#                             n_nodes_expanded=n_nodes_expanded,
#                             n_nodes_pruned=n_nodes_pruned,
#                             n_leaves_covered=cut_tree.n_leaves_cut(),
#                             fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
#                             best = cost
#                         path.pop() # not needed i don't think
#                     break
#                 elif p in path:
#                     continue
#                 elif edges[P][p] == math.inf:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(path + [p])
#                     continue
#                 cur_m, cur_lb = reduce_a_path(edges, m.copy(), P, p, c)
#                 if cur_lb > best:
#                     n_nodes_pruned += 1 # stretch 1
#                     cut_tree.cut(path + [p])
#                     continue
#                 else:
#                     PQ.put((h-1* cur_lb, (p, call+1, cur_m, cur_lb, path, h-1)))

#     return solutions


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = [greedy_tour(edges, Timer(1))[-1]]
    best = solutions[0].score
    matrix = make_matrix(edges)
    cost = reduce_matrix(edges, matrix)
    cur = []
    PQ = PriorityQueue()
    level = 0
    orginal = matrix.copy()
    heigth = len(edges)
    # for stretch 1 
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    maxqueue = 0
    cut_tree = CutTree(len(edges))

    PQ.put((heigth, cost, (0, level, matrix.copy(), cost)))

    while not PQ.empty() and not timer.time_out():

        h, lb, (P, call, m, c) = PQ.get()

        if call < len(cur):
            cur.pop()
            PQ.put((h, lb, (P, call, m, c)))
        elif c > best:
            n_nodes_pruned += 1 # stretch 1
            cut_tree.cut(cur + [P])
            continue
        elif P not in cur:
            n_nodes_expanded += 1   # stretch 1
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
                elif p in cur:
                    continue
                elif edges[P][p] == math.inf:
                    n_nodes_pruned += 1 # stretch 1
                    cut_tree.cut(cur + [p])
                    continue
                cur_m, cur_lb = reduce_a_path(edges, m.copy(), P, p, c)
                if cur_lb > best:
                    n_nodes_pruned += 1 # stretch 1
                    cut_tree.cut(cur + [p])
                    continue
                else:
                    PQ.put((h-1, cur_lb, (p, call+1, cur_m, cur_lb)))

    return solutions