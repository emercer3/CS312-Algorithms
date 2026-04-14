# See additional instructions for these tests in the instructions for the project
import math
import random
from time import time_ns
from tsp_solve import make_matrix, reduce_matrix, reduce_a_path, branch_and_bound
from tsp_core import generate_network, Timer

def test_reduced_cost_matrix_1():
    edges = [[math.inf, 7, 3, 12],
             [3, math.inf, 6, 14],
             [5, 8, math.inf, 6],
             [9, 3, 5, math.inf]]
    
    matrix = make_matrix(edges)
    original_edges_dict = {
    (0, 0): math.inf, (0, 1): 7,        (0, 2): 3,        (0, 3): 12,
    (1, 0): 3,        (1, 1): math.inf, (1, 2): 6,        (1, 3): 14,
    (2, 0): 5,        (2, 1): 8,        (2, 2): math.inf, (2, 3): 6,
    (3, 0): 9,        (3, 1): 3,        (3, 2): 5,        (3, 3): math.inf}

    assert matrix == original_edges_dict
    


def test_reduced_cost_matrix_2():
    edges = [[math.inf, 7, 3, 12],
             [3, math.inf, 6, 14],
             [5, 8, math.inf, 6],
             [9, 3, 5, math.inf]]
    
    matrix = make_matrix(edges)
    cost = reduce_matrix(edges, matrix)
    reduced_dict = {
    (0, 0): math.inf, (0, 1): 4,        (0, 2): 0,        (0, 3): 8,
    (1, 0): 0,        (1, 1): math.inf, (1, 2): 3,        (1, 3): 10,
    (2, 0): 0,        (2, 1): 3,        (2, 2): math.inf, (2, 3): 0,
    (3, 0): 6,        (3, 1): 0,        (3, 2): 2,        (3, 3): math.inf}

    assert matrix == reduced_dict
    assert cost == 15


def test_reduced_cost_seach_path():
    edges = [[math.inf, 7, 3, 12],
             [3, math.inf, 6, 14],
             [5, 8, math.inf, 6],
             [9, 3, 5, math.inf]]
    
    matrix = make_matrix(edges)
    old_cost = reduce_matrix(edges, matrix)
    new_matrix, cost = reduce_a_path(edges, matrix, 0, 1, old_cost)

    should_matrix = {
    (0, 0): math.inf, (0, 1): math.inf,        (0, 2): math.inf,        (0, 3): math.inf,
    (1, 0): math.inf, (1, 1): math.inf,        (1, 2): 0,               (1, 3): 7,
    (2, 0): 0,        (2, 1): math.inf,        (2, 2): math.inf,        (2, 3): 0,
    (3, 0): 4,        (3, 1): math.inf,        (3, 2): 0,               (3, 3): math.inf}
    new_cost = 24

    assert should_matrix == new_matrix
    assert new_cost == cost

    

def test_b_and_b_size_15():
    random.seed(time_ns())
    seed = random.randint(0, 5000)
    _, edges = generate_network(
        15,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=seed,
    )
    
    solutions = branch_and_bound(edges, Timer(120))


    assert 0 < len(solutions)