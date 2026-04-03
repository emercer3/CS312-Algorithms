# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point, plot_points

def slope(c1, c2) -> float:                     # O(1)
    return (c1[1] - c2[1]) / (c1[0] - c2[0])


def find_upper_tangent(L: list[tuple[float, float]], R: list[tuple[float, float]]) -> tuple[float, float]:  # O(n)
    lind = 0
    rind = 0

    for i in range(0, len(R)):      # O(n)
        if R[i][0] < R[rind][0]:
            rind = i

    cur = slope(L[lind], R[rind])
    done = False

    while not done:
        done = True

        while cur > slope(L[(lind+1) % len(L)], R[rind]):   # left upper
            lind = (lind+1) % len(L)
            cur = slope(L[lind], R[rind])
            done = False

        while cur < slope(L[lind], R[(rind-1) % len(R)]):  # right upper
            rind = (rind-1) % len(R)
            cur = slope(L[lind], R[rind])
            done = False

    return (L[lind], R[rind])


def find_lower_tangent(L: list[tuple[float, float]], R: list[tuple[float, float]]) -> tuple[float, float]:  # O(n)
    lind = 0
    rind = 0

    for i in range(0, len(R)):
        if R[i][0] < R[rind][0]:
            rind = i

    cur = slope(L[lind], R[rind])
    done = False

    while not done:
        done = True

        while cur < slope(L[lind-1], R[rind]):
            lind = (lind-1) % len(L)
            cur = slope(L[lind], R[rind])
            done = False

        while cur > slope(L[lind], R[(rind+1) % len(R)]):
            rind = (rind+1) % len(R)
            cur = slope(L[lind], R[rind])
            done = False

    return (L[lind], R[rind])


def combine(L: list[tuple[float, float]], R: list[tuple[float, float]]) -> list[tuple[float, float]]:   # O(n)
    Luptan, Ruptan = find_upper_tangent(L, R)   # O(n)
    Llowtan, Rlowtan = find_lower_tangent(L, R) # O(n)
    
    Luind = L.index(Luptan)     # O(n)
    Llind = L.index(Llowtan)    # O(n) 
    Ruind = R.index(Ruptan)     # O(n)
    Rlind = R.index(Rlowtan)    # O(n)

    new_hull = []

    i = Rlind
    new_hull.append(R[i])
    while i != Ruind:           # O(n)
        i = (i + 1) % len(R)
        new_hull.append(R[i])
    
    i = Luind
    new_hull.append(L[i])
    while i != Llind:           # O(n)
        i = (i + 1) % len(L)
        new_hull.append(L[i])

    rightmost = max(range(len(new_hull)), key=lambda i: new_hull[i][0])
        
    return new_hull[rightmost:] + new_hull[:rightmost]


def orientation(a, b, c):       # O(1)
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def base_assortment(points):    # O(1)
    if len(points) == 1:
        return points

    if len(points) == 2:
        # rightmost first
        if points[0][0] > points[1][0]:
            return [points[0], points[1]]
        else:
            return [points[1], points[0]]

    # 3 points (sorted by x)
    a, b, c = points

    turn = orientation(a, b, c) # O(1)

    if turn > 0:
        # CCW: a → b → c
        return [c, a, b]  # rotate
    else:
        # CW or collinear
        return [c, b, a]


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]: # O(n*log(n))
    size = len(points) 

    if size < 4:
        return base_assortment(points)  # O(1)

    L = points[:(len(points)//2)]
    R = points[(len(points)//2):]

    L_hull = compute_hull(L)    # both are half the original so over all will be log(n)
    R_hull = compute_hull(R)

    return combine(L_hull, R_hull)  # O(n)


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:  # O(n*log(n))
    """Return the subset of provided points that define the convex hull"""
    points.sort()       # O(nlog(n))
    return compute_hull(points)     # O(n*log(n))


def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull
       using Graham's Scan (O(n log n))"""
    
    if len(points) <= 1:
        return points.copy()

    # Step 1: Find pivot (lowest y, then lowest x)
    pivot = min(points, key=lambda p: (p[1], p[0]))

    # Step 2: Sort by polar angle relative to pivot
    def polar_angle(p):
        return (p[0] - pivot[0], p[1] - pivot[1])

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    sorted_pts = sorted(points, key=lambda p: (
        -((p[0] - pivot[0]) / ((p[0] - pivot[0])**2 + (p[1] - pivot[1])**2 + 1e-12)),
        (p[0] - pivot[0])**2 + (p[1] - pivot[1])**2
    ))

    # A simpler and safer angle sort:
    from math import atan2
    sorted_pts = sorted(points, key=lambda p: (
        atan2(p[1] - pivot[1], p[0] - pivot[0]),
        (p[0] - pivot[0])**2 + (p[1] - pivot[1])**2
    ))

    # Step 3: Build hull using stack
    hull = []
    for p in sorted_pts:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull
