import numpy as np
from models import Plane


class Loader:
    def __init__(self, path="data/airland1.txt"):
        self.planes = self.process_planes(path)
        self.separation_matrix = self.get_separation_matrix()

    def load_file(self, path: str):
        with open(path, encoding="utf8") as f:
            numbers = f.read()
            numbers = " ".join(numbers.split())
            numbers = numbers.split(" ")
        return [self.num(x) for x in numbers]

    def process_planes(self, path: str):
        numbers = self.load_file(path)
        planes = []
        self.count, self.freeze_time = numbers[0], numbers[1]
        for p in range(2, (self.count + 6) * self.count + 2, self.count + 6):
            appearance, earliest, target, latest, penalty_early, penalty_late = numbers[
                p : p + 6
            ]
            separations = numbers[p + 6 : p + 6 + self.count]
            planes.append(
                Plane(
                    appearance,
                    earliest,
                    target,
                    latest,
                    penalty_early,
                    penalty_late,
                    separations,
                )
            )
        return planes

    def get_separation_matrix(self):
        rows = [np.array(p.separations) for p in self.planes]
        matrix = np.stack(rows)
        return matrix

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)
