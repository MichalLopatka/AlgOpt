import random

from loader import Loader
from models import Individual


def main():
    loader = Loader(path="data/airland1.txt")
    print(loader.planes[2])
    print(loader.separation_matrix)

    random_individual = Individual(loader)


if __name__ == "__main__":
    main()
