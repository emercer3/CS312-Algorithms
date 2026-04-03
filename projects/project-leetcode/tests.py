def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    length = len(candidates)
    tree = {}
    pos = []

    for i in candidates:
        node = [candidates[i]]
        tree[node] = candidates[i]

    maketree(tree, target, candidates[0], pos)

    return pos

def sum(l : List[int]) -> int:
    sum = 0
    for i in l:
        sum += i
    return sum


def maketree(tree, tar, node, cur, pos):
    if tree[node] > tar:
        tree.delete(node)
    elif tree[node] == tar:
        pos.append(node.append(cur))
    else:
        tree[node] = sum(node)
        node.append(cur)

    for i in candidates:
        maketree(tree)

def main():
    combinationSum([2, 3, 5], 8)
