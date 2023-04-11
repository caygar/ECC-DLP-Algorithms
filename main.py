"""
Using out prewritten test files, we test the runtime of our algorithms.
"""

from elliptic import EllipticCurve
from time import time
from algorithm import naive_bsgs, polhig_hellman


def read_test(filename: str):
    with open(filename, 'r') as f:
        a = int(f.readline())
        b = int(f.readline())
        p = int(f.readline())
        q = int(f.readline())
        Px = int(f.readline())
        Py = int(f.readline())
        d = int(f.readline())
        f.close()

    E = EllipticCurve(a, b, p)
    P = E(Px, Py)
    Q = P * d
    return E, P, Q, q, d


def main():
    for i in range(1,4):
        print(f"TEST {i}#")
        E, P, Q, q, d = read_test(f"test{i}.txt")
        start = time()
        print(f"Baby-step Giant-step #{i}")
        print(naive_bsgs(P.x, P.y, Q.x, Q.y, E, q=q) == d)
        end = time()
        print(end - start)
        print("=====================")

        print(f"Polhig Hellman #{i}")
        start = time()
        print(polhig_hellman(P.x, P.y, Q.x, Q.y, E, q=q) == d)
        end = time()
        print(end - start)
        print("=====================")


if __name__ == '__main__':
    main()
