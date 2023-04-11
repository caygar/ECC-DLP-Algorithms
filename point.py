class Point:
    def __init__(self, x, y, a, b, p):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.p = p

    def reducemod(self, n):
        return n % self.p

    def equal(self, m, n):
        return self.reducemod(m - n) == 0

    def inverse(self, m):
        return pow(m, -1, self.p)

    def negate(self):
        return Point(self.x, -self.y, self.a, self.b, self.p)

    def __add__(self, other):
        if other.x == 0 and other.y == 0:
            return self

        if self.x == 0 and self.y == 0:
            return other

        if self.equal(self.x, other.x) and self.equal(self.y, -other.y):
            return Point(0, 0, self.a, self.b, self.p)

        if self.equal(self.x, other.x) and self.equal(self.y, self.y):
            u = self.reducemod((3 * self.x * self.x + self.a)
                               * self.inverse(2 * self.y))
        else:
            u = self.reducemod((self.y - other.y)
                               * self.inverse(self.x - other.x))

        v = self.reducemod(self.y - u * self.x)
        Rx = self.reducemod(u * u - self.x - other.x)
        Ry = self.reducemod(-u * Rx - v)

        return Point(Rx, Ry, self.a, self.b, self.p)

    def __sub__(self, other):
        return self + other.negate()

    def __mul__(self, n: int):
        bits = list(bin(n))[2:]
        R = Point(0, 0, self.a, self.b, self.p)
        T = self
        for bit in reversed(bits):
            if bit == '1':
                R = R + T
            T = T + T
        return R

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))
  
