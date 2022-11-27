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
    def __init__(self, loader):
        count = len(loader.planes)
        self.T = np.zeros((count, 2))
        row, col = self.T.shape

        while True:
            for x in range(row):
                for y in range(col):
                    if (y % 2 == 0):
                        self.T[x][y] = x
                    else:
                        self.T[x][y] = random.randrange(loader.planes[x].earliest, loader.planes[x].latest)

            self.T = self.T[self.T[:, 1].argsort()]
            if(self.check_if_correct(loader)):
                # print(self.T)
                break

    def check_if_correct(self, loader):
        row, col = self.T.shape
        for x in range(row - 1):
            a = (self.T[x+1][1] - self.T[x][1])
            i = int(self.T[x][0])
            j = int(self.T[x+1][0])
            b = (loader.separation_matrix[i][j])
            if(a - b < 0):
                return False

        return True


@dataclass()
class Population:
    population: list[Individual]
