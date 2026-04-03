import math as m


def align(seq1: str, seq2: str, match_award=-3, indel_penalty=5, sub_penalty=1, banded_width=-1, gap="-") -> tuple[float, str | None, str | None]:
    if banded_width == -1:
        return align_unbanded(seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width, gap)
    

    seq1length = len(seq1)
    seq2length = len(seq2)
    if (len(seq1) < len(seq2)):
        smaller = len(seq1)
        larger = len(seq2)
    else:
        smaller = len(seq2)
        larger = len(seq1)

    if (larger - smaller) > banded_width:
        return (m.inf, None, None)
        
    path = {}
    

    for j in range(seq1length+1):
        i_start = max(0, j-banded_width)
        i_end = min(seq2length, j+banded_width)

        for i in range(i_start, i_end+1):
            if i == 0 and j == 0:
                path[(i, j)] = (0, (0, 0))
                continue

            diag = path.get((i-1, j-1), (m.inf, None))[0]
            left = path.get((i-1, j), (m.inf, None))[0]
            up = path.get((i, j-1), (m.inf, None))[0]


            if i > 0 and j > 0:
                if seq2[i-1] == seq1[j-1]:
                    diag += match_award
                else:
                    diag += sub_penalty

            if left != m.inf:
                left += indel_penalty
            if up != m.inf:
                up += indel_penalty

            path[(i, j)] = find_min(i, j, diag, left, up)


    shortest_path = path[(seq2length, seq1length)][0]
    s1, s2 = get_path(path, seq2, seq1, seq2length, seq1length, gap)

    return shortest_path, s1, s2


def find_min(i: int, j: int, diagonal: int, left: int, up: int) -> tuple[int, tuple[int, int]]:
    """tie breaking diagonal, left, top"""
    best = min(diagonal, left, up)

    if best == diagonal:
        return (diagonal, (i-1, j-1))
    elif best == left:
        return (left, (i-1, j))
    else:
        return (up, (i, j-1))
    
def get_path(path: dict, s2: str, s1: str, i: int, j: int, gap: str) -> tuple[str, str]:
    final1 = ""
    final2 = ""

    while True:
        previ, prevj = path[(i, j)][1]

        if i == 0 and j == 0:
            break

        elif i-1 == previ and j-1 == prevj: # diagonal match
            final2 = s2[previ] + final2
            final1 = s1[prevj] + final1
            i = i-1
            j = j-1
        elif i-1 == previ and j == prevj: # left
            final1 = gap + final1
            final2 = s2[previ] + final2
            i = i-1
        elif i == previ and j-1 == prevj: # up
            final1 = s1[prevj] + final1
            final2 = gap + final2
            j = j-1

    return (final1, final2)
    
def align_unbanded(seq1: str, seq2: str, match_award=-3, indel_penalty=5, sub_penalty=1, banded_width=-1, gap="-") -> tuple[float, str | None, str | None]:
    """
    Align seq1 against seq2 using Needleman-Wunsch
    Put seq1 on left (j) and seq2 on top (i)
    => matrix[i][j]
    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
    :param gap: the character to use to represent gaps in the alignment strings
    """
    seq1length = len(seq1)
    seq2length = len(seq2)

    path = {}

    for j in range(seq1length+1):
        for i in range(seq2length+1):
            if i == 0 and j == 0:
                path[(i, j)] = (0, (0, 0))
            elif i == 0: # moving down
                path[(i, j)] = (path[(i, j-1)][0] + indel_penalty, (i, j-1))
            elif j == 0: # moving right
                path[(i, j)] = (path[(i-1, j)][0] + indel_penalty, (i-1, j))
            else:
                if seq2[i-1] == seq1[j-1]:
                    sub_values = path[(i-1, j-1)][0] + match_award
                else:
                    sub_values = path[(i-1, j-1)][0] + sub_penalty
                path[(i, j)] = find_min(i, j, sub_values, path[(i-1, j)][0] + indel_penalty, path[(i, j-1)][0] + indel_penalty)

    shortest_path = path[(seq2length, seq1length)][0]
    s1, s2 = get_path(path, seq2, seq1, seq2length, seq1length, gap)

    return shortest_path, s1, s2


def local_align(seq1: str, seq2: str, match_award=-3, indel_penalty=5, sub_penalty=3, banded_width=-1, gap="-") -> tuple[float, str | None, str | None]:
    path, s1, s2 = local_align_unbanded(seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width, gap)
    return path, s1, s2

def local_align_unbanded(seq1: str, seq2: str, match_award=-3, indel_penalty=5, sub_penalty=3, banded_width=-1, gap="-") -> tuple[float, str | None, str | None]:
    """
    Align seq1 against seq2 using Needleman-Wunsch
    Put seq1 on left (j) and seq2 on top (i)
    => matrix[i][j]
    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
    :param gap: the character to use to represent gaps in the alignment strings
    """
    seq1length = len(seq1)
    seq2length = len(seq2)

    path = {}

    for j in range(seq1length+1):
        for i in range(seq2length+1):
            if i == 0 and j == 0:
                path[(i, j)] = (0, (0, 0))
            elif i == 0: # moving down
                path[(i, j)] = (0, (i, j-1))
            elif j == 0: # moving right
                path[(i, j)] = (0, (i-1, j))
            else:
                if seq2[i-1] == seq1[j-1]:
                    sub_values = path[(i-1, j-1)][0] + match_award
                else:
                    sub_values = path[(i-1, j-1)][0] + sub_penalty

                path[(i, j)] = find_min_local(i, j, sub_values, path[(i-1, j)][0] + indel_penalty, path[(i, j-1)][0] + indel_penalty)

    shortest_path = min(path, key=lambda k: path[k][0])
    s1, s2 = get_path_local(path, seq1, seq2, shortest_path, gap)

    return path[shortest_path][0], s1, s2


def find_best(path, seq1length, seq2length):

    min_score = min((val[0] for val in path.values()), default=0)

    best_cell = None

    for j in range(seq1length+1):
        for i in range(seq2length+1):

            if path[(i, j)][0] == min_score:
                best_cell = (i, j)
                break

        if best_cell:
            break

    return best_cell, min_score


def get_path_local(path, s1: str, s2: str, cords: tuple[int, int], gap) -> tuple[str, str]:
    final1 = ""
    final2 = ""
    i, j = cords

    while path[(i, j)][0] != 0:
        previ, prevj = path[(i, j)][1]

        if i-1 == previ and j-1 == prevj: # diagonal match
            final2 = s2[previ] + final2
            final1 = s1[prevj] + final1
            i = i-1
            j = j-1
        elif i-1 == previ and j == prevj: # left
            final1 = gap + final1
            final2 = s2[previ] + final2
            i = i-1
        elif i == previ and j-1 == prevj: # up
            final1 = s1[prevj] + final1
            final2 = gap + final2
            j = j-1

    return (final1, final2)


def find_min_local(i: int, j: int, diagonal: int, left: int, up: int) -> tuple[int, tuple[int, int]]:
    """tie breaking diagonal, left, top"""

    best = min(diagonal, left, up)

    if best > 0:
        return (0, None)

    elif best == diagonal:
        return (diagonal, (i-1, j-1))

    elif best == left:
        return (left, (i-1, j))

    else:
        return (up, (i, j-1))