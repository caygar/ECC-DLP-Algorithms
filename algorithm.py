from elliptic import EllipticCurve
from math import ceil, sqrt
from sympy import factorint


def crt(a, m):
    k = len(a)
    prod = 1
    for i in range(k):
        prod = prod * a[i]

    result = 0

    for i in range(k):
        pp = prod // a[i]
        result = result + m[i] * pow(pp, -1, a[i]) * pp

    return result % prod


def naive_bsgs(x1: int, y1: int,
               x2: int, y2: int,
               E: EllipticCurve,
               q: int = -1):
    P = E(x1, y1)
    Q = E(x2, y2)
    q = E.subgroup_order(x1, y1) if q == -1 else q

    m = ceil(sqrt(q))
    baby_step = {P*j: j for j in range(m)}
    for i in range(m):
        temp = Q - P * (i*m)
        if temp in baby_step:
            return i*m + baby_step[temp]
    return None


def polhig_hellman(x1: int, y1: int,
                   x2: int, y2: int,
                   E: EllipticCurve,
                   q=-1) -> int:
    g = E(x1, y1)
    h = E(x2, y2)
    q = E.subgroup_order(x1, y1) if q == -1 else q

    # Step 1: Factor the order of the group
    factors = factorint(q)

    # Step 2: Compute discrete logarithm mod each prime factor
    r = []
    m = [p**e for p, e, in factors.items()]

    for p, e in factors.items():
        g_i = g * (q // (p ** e))
        h_i = h * (q // (p ** e))
        x_i = naive_bsgs(g_i.x, g_i.y, h_i.x, h_i.y, E, q=q)
        r.append(x_i)
    return crt(m, r)
