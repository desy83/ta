import random
from copy import copy
import math

class PerlinNoise(object):
    p = []

    def __init__(self, seed):
        self.p = [i for i in xrange(0, 256)]
        random.seed(seed)
        random.shuffle(self.p)

        for entry in copy(self.p):
            self.p.append(entry)

    def noise(self, x, y, z):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        Z = int(math.floor(z)) & 255


        x -= math.floor(x)
        y -= math.floor(y)
        z -= math.floor(z)

        u = self.fade(x)
        v = self.fade(y)
        w = self.fade(z)

        A = self.p[X] + Y;
        AA = self.p[A] + Z;
        AB = self.p[A + 1] + Z;
        B = self.p[X + 1] + Y;
        BA = self.p[B] + Z;
        BB = self.p[B + 1] + Z;

        res = self.lerp(w, self.lerp(v, self.lerp(u, self.grad(self.p[AA], x, y, z), self.grad(self.p[BA], x-1, y, z)), self.lerp(u, self.grad(self.p[AB], x, y-1, z), self.grad(self.p[BB], x-1, y-1, z))), self.lerp(v, self.lerp(u, self.grad(self.p[AA+1], x, y, z-1), self.grad(self.p[BA+1], x-1, y, z-1)), self.lerp(u, self.grad(self.p[AB+1], x, y-1, z-1), self.grad(self.p[BB+1], x-1, y-1, z-1))))
        return (res + 1.0) / 2.0

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        return a + t * (b - a)

    def grad(self, ha, x, y, z):
        h = ha & 15
        if h < 8:
            u = x
        else:
            u = y
        if h < 4:
            v = y
        else:
            if h == 12 or h == 14:
                v = x
            else:
                v = z

        tmp1 = u if (h & 1) == 0 else -u
        tmp2 = v if (h & 2) == 0 else -v
        return tmp1 + tmp2
