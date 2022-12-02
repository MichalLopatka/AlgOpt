import random
import numpy as np


class Individual:
    def __init__(self, loader):
        self.planes = loader.planes
        self.separation_matrix = loader.separation_matrix
        self.count = len(self.planes)
        self.T = np.zeros((self.count, 2))
        self.rows, self.cols = self.T.shape

    def random_initialize(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if y % 2 == 0:
                    self.T[x][y] = x
                else:
                    self.T[x][y] = random.randrange(
                        self.planes[x].earliest, self.planes[x].latest
                    )

        self.T = self.T[self.T[:, 1].argsort()]

    def greedy(self):
        # sort planes by appearance time
        for x in range(self.rows):
            self.T[x][0] = x
            self.T[x][1] = self.planes[x].target
        self.T = self.T[self.T[:, 1].argsort()]
        # main part
        for x in range(self.rows - 1):
            i = int(self.T[x][0])
            j = int(self.T[x + 1][0])
            # assume target time as result
            a = self.T[x][1]
            b = self.T[x + 1][1]
            # if separation is too small, add separation
            while b - a < self.separation_matrix[i][j]:
                b += 1
            self.T[x][1] = a
            self.T[x + 1][1] = b

    def greedy_modified(self, mode="target"):
        tempT = np.zeros((self.count, 4))
        rows, _ = tempT.shape
        for x in range(rows):
            tempT[x][0] = x
            tempT[x][1] = self.planes[x].target
            tempT[x][2] = self.planes[x].earliest
            tempT[x][3] = self.planes[x].latest
        if mode == "target":
            tempT = tempT[tempT[:, 1].argsort()]
        elif mode == "earliest":
            tempT = tempT[tempT[:, 2].argsort()]
        elif mode == "latest":
            tempT = tempT[tempT[:, 3].argsort()]
        for x in range(rows - 1):
            i = int(tempT[x][0])
            j = int(tempT[x + 1][0])
            a = tempT[x][1]
            b = tempT[x + 1][1]
            while b - a < self.separation_matrix[i][j]:
                b += 1
            tempT[x][1] = a
            tempT[x + 1][1] = b
        self.T = tempT[:, 0:2]

    def check_if_correct_time_frame(self):
        for x in range(self.rows):
            a = int(self.T[x][0])
            b = self.T[x][1]
            if b not in range(self.planes[a].earliest, self.planes[a].latest + 1):
                return False
        return True

    def check_if_correct_separation(self):
        for x in range(self.rows - 1):
            a = self.T[x + 1][1] - self.T[x][1]
            i = int(self.T[x][0])
            j = int(self.T[x + 1][0])
            b = self.separation_matrix[i][j]
            if a - b < 0:
                return False

        return True

    def fitness(self):
        penalty = 0
        for position in self.T:
            id, time = position
            plane = self.planes[int(id)]
            if time > plane.target:
                penalty += (time - plane.target) * plane.penalty_late
            elif time < plane.target:
                penalty += (plane.target - time) * plane.penalty_early
        return penalty
