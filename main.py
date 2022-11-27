import random

from loader import Loader
from models import Individual
from utils import fitness

def main():
    loader = Loader(path="data/airland1.txt")
    [print(x) for x in loader.planes]
    print(loader.separation_matrix)
    random_individual = Individual(loader)
    print(random_individual.T)
    print(fitness(random_individual.T, loader.planes))


if __name__ == "__main__":
    main()
