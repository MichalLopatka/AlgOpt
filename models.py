import random
from dataclasses import dataclass
import numpy as np


@dataclass()
class Plane:
    appearance: int
    earliest: int
    target: int
    latest: int
    penalty_early: float
    penalty_late: float
    separations: list[int]


class Individual:
    def __init__(self):
        self.T

    def random_initialize(self, loader):
        count = len(loader.planes)
        self.T = np.zeros((count, 2))
        row, col = self.T.shape

        for x in range(row):
            for y in range(col):
                if (y % 2 == 0):
                    self.T[x][y] = x
                else:
                    self.T[x][y] = random.randrange(loader.planes[x].earliest, loader.planes[x].latest)

        self.T = self.T[self.T[:, 1].argsort()]

    def greedy(self, loader):
        count = len(loader.planes)
        self.T = np.zeros((count, 2))
        row, col = self.T.shape
        # sort planes by appearance time
        for x in range(row):
            self.T[x][0] = x
            self.T[x][1] = loader.planes[x].target
        self.T = self.T[self.T[:, 1].argsort()]
        # main part
        for x in range(row - 1):
            i = int(self.T[x][0])
            j = int(self.T[x + 1][0])
            # assume target time as result
            a = self.T[x][1]
            b = self.T[x+1][1]
            # if separation is too small, add separation
            while(b-a < loader.separation_matrix[i][j]):
                b += 1
            self.T[x][1] = a
            self.T[x+1][1] = b

    def check_if_correct_time_frame(self, loader):
        row, col = self.T.shape
        for x in range(row):
            a = int(self.T[x][0])
            b = self.T[x][1]
            if b not in range(loader.planes[a].earliest, loader.planes[a].latest+1):
                return False
        return True

    def check_if_correct_separation(self, loader):
        row, col = self.T.shape
        for x in range(row - 1):
            a = (self.T[x + 1][1] - self.T[x][1])
            i = int(self.T[x][0])
            j = int(self.T[x + 1][0])
            b = (loader.separation_matrix[i][j])
            if (a - b < 0):
                return False

        return True


@dataclass()
class Population:
    population: list[Individual]
