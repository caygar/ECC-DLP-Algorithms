from point import Point


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int) -> None:
        # discriminant must be not be 0, i.e. must be non-singular
        if (a ** 3) * 4 + (b ** 2) * 27 == 0:
            raise ValueError

        self.a: int = a
        self.b: int = b
        self.p: int = p

    def check_on_field(self, x, y):
        lfs = y**2
        rfs = x**3 + self.a * x + self.b
        return (lfs - rfs) % self.p == 0

    def calculate_num_points(self):
        count = 1
        for y in range(self.p):
            for x in range(self.p):
                if (x**3 + self.a * x + self.b - y**2) % self.p == 0:
                    count += 1
        return count

    def subgroup_order(self, x, y):
        P = self(x, y)
        n = 1
        while not (P.x == 0 and P.y == 0):
            P = P + self(x, y)
            n += 1
        return n

    def __call__(self, x, y):
        return Point(x, y, self.a, self.b, self.p)

    
