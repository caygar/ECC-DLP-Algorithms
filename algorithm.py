"""
crt(a,m): An implementation of the chinese remainder theorem. A mathematical theorem that states that given a system
          of linear congruences with pairwise relatively prime moduli, there exists a unique solution that can be computed
          using the product of the moduli and their inverses.
          
          Takes in two lists as input, and returns an integer representing the unique solution to the system of linear congruences modulo the product
          of the moduli.
          
naive_bsgs(x1,y1,x2,y2,E,q):  An implementation of the Baby-step Giant-step algorithm, which computes the discrete logarithm of a point
                              Q (coordinates are given with x2, y2) with respect to a point P (coordinates are given with x1, y1) on the elliptic curve E.
                              
                              The algorithm works by first computing a series of 'baby steps' that are multiples of P up to a certain limit (which is the
                              supgroup_order in our implementation), and then computing a series of 'giant steps' that are multiples of Q down to that same limit.
                              
                              If both steps converge, we have found the discrete logarithm. If not, the algorithm repeats until it either finds the logarithm, or exceeds
                              the search limit. In that case, the function returns None.
                              

polhig_hellman(x1,y1,x2,y2,E,q):  An implementation of the Polhig Hellman algorithm, which computes the discrete logarithm of a point (h) with respect to another point
                                  (g, in this case). Firstly it factors the order of the subgroup, then calculates the discrete logarithm mod each prime factor using
                                  the Baby-step Giant-step algorithm we implemented previously. Lastly, uses our implementation of the Chinese Remainder Theorem to
                                  combine the solutions for each prime factor and return the overall solution.

"""


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
