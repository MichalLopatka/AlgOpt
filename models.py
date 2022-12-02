from individual import Individual
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


@dataclass()
class Population:
    population: list[Individual]
