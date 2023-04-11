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
    E, P, Q, q, d = read_test("test1.txt")
    start = time()
    print(naive_bsgs(P.x, P.y, Q.x, Q.y, E, q=q) == d)
    end = time()
    print(end - start)

    start = time()
    print(polhig_hellman(P.x, P.y, Q.x, Q.y, E, q=q) == d)
    end = time()
    print(end - start)


if __name__ == '__main__':
    main()
