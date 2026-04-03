def find_shortest_path_with_heap_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    prev = {}
    dist = {}
    queue = [(source, 0)]
    node_to_queue = {source: 0}
    i = 1

    for n in graph:
        dist[n] = float("inf")
        prev[n] = "null"

        if n != source:
            queue.append((n, float("inf")))
            node_to_queue[n] = i
            i += 1

    dist[source] = 0

    while len(queue) != 0:
        u, udist = deleteminheap(queue, node_to_queue)

        for v in graph[u]:
            if v in node_to_queue:
                i = node_to_queue[v]
                vn, vd = queue[i]
                if vd > udist + graph[u][v]:
                    newvdist = udist + graph[u][v]
                    prev[v] = u
                    queue[i] = (vn, newvdist)
                    dist[v] = newvdist
                    bubbleup(queue, i, node_to_queue)

    path = get_path(prev, source, target, [])
    path.reverse()
    return (path, dist[target])


def bubbleup(q : list, i : int, ntq : dict):
    cn, cd = q[i]

    while True:
        if i != 0 and cd < q[(i-1)//2][1]:
            ntq[q[(i-1)//2][0]] = i
            ntq[q[i][0]] = (i-1)//2
            q[(i-1)//2], q[i] = q[i], q[(i-1)//2]
            i = (i-1)//2
        else:
            break


def bubbledown(q : list, i : int, ntq : dict):
    cn, cd = q[i]

    while True:
        if (2*i+2) <= len(q)-1:
            if (2*i+2) <= len(q)-1 and cd > q[2*i+2][1] and q[2*i+2][1] < q[2*i+1][1]:
                ntq[q[2*i+2][0]] = i
                ntq[q[i][0]] = 2*i+2
                q[2*i+2], q[i] = q[i], q[2*i+2]
                i = 2*i+2
            elif (2*i+1) <= len(q)-1 and cd > q[2*i+1][1]:
                ntq[q[2*i+1][0]] = i
                ntq[q[i][0]] = 2*i+1
                q[2*i+1], q[i] = q[i], q[2*i+1]
                i = 2*i+1
            else:
                break
        elif (2*i+1) <= len(q)-1:
            if (2*i+1) <= len(q)-1 and cd > q[2*i+1][1]:
                ntq[q[2*i+1][0]] = i
                ntq[q[i][0]] = 2*i+1
                q[2*i+1], q[i] = q[i], q[2*i+1]
                i = 2*i+1
            else:
                break
        else: 
            break
        
def resortheap(q : list, i : int, ntq : dict):
    cn, cd = q[i]

    while True:
        if i != 0 and cd < q[(i-1)//2][1]:
            ntq[q[(i-1)//2][0]] = i
            ntq[q[i][0]] = (i-1)//2
            q[(i-1)//2], q[i] = q[i], q[(i-1)//2]
            i = (i-1)//2
        elif (2*i+2) <= len(q)-1:
            if (2*i+2) <= len(q)-1 and cd > q[2*i+2][1] and q[2*i+2][1] < q[2*i+1][1]:
                ntq[q[2*i+2][0]] = i
                ntq[q[i][0]] = 2*i+2
                q[2*i+2], q[i] = q[i], q[2*i+2]
                i = 2*i+2
            elif (2*i+1) <= len(q)-1 and cd > q[2*i+1][1]:
                ntq[q[2*i+1][0]] = i
                ntq[q[i][0]] = 2*i+1
                q[2*i+1], q[i] = q[i], q[2*i+1]
                i = 2*i+1
            else:
                break
        elif (2*i+1) <= len(q)-1:
            if (2*i+1) <= len(q)-1 and cd > q[2*i+1][1]:
                ntq[q[2*i+1][0]] = i
                ntq[q[i][0]] = 2*i+1
                q[2*i+1], q[i] = q[i], q[2*i+1]
                i = 2*i+1
            else:
                break
        else: 
            break
    return


def deleteminheap(q : list, ntq : dict) -> tuple[int, int]:
    node, min = q[0] 

    if len(q) == 1:
        q.pop()
        ntq.__delitem__(node)
        return node, min
    
    ntq.__delitem__(node)
    newhead, newdist = q[len(q)-1]
    ntq[newhead] = 0
    q.pop()
    q[0] = (newhead, newdist)
    max = len(q)-1

    bubbledown(q, 0, ntq)

    return node, min



def find_shortest_path_with_linear_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    prev = {}
    dist = {}
    queue = {}

    for n in graph:
        dist[n] = float("inf")
        queue[n] = float("inf")
        prev[n] = "null"
    
    queue[source] = 0
    dist[source] = 0

    while not is_empty(queue):
        u = deletemin(queue)
        if u == None:
            break

        for v in graph[u]:
            if v not in queue:
                continue
            elif queue[v] > dist[u] + graph[u][v]:
                queue[v] = dist[u] + graph[u][v]
                prev[v] = u
                dist[v] = dist[u] + graph[u][v]

    path = get_path(prev, source, target, [])
    path.reverse()
    return (path, dist[target])



def is_empty(q : dict) -> bool:
    return len(q) == 0

def deletemin(q: dict) -> int | None:
    min = [float("inf"), None]

    for node in q:
        if q[node] < min[0]:
            min[0] = q[node]
            min[1] = node

    if min[1] is None:
        return None
    q.__delitem__(min[1])
    return min[1]
    
def decreasekey(q : dict, node : int, distance : int):
    q[node] = distance

def dis(q : dict, node):
    return q[node]

def get_path(p : dict, s : int, t : int, path : list):
    path.append(t)
    if s == t:
        return path
    elif p[t] == "null":
        return []
    return get_path(p, s, p[t], path)