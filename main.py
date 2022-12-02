from loader import Loader
from individual import Individual


def main():
    loader = Loader(path="data/airland1.txt")
    [print(x) for x in loader.planes]
    print(loader.separation_matrix)
    random_individual = Individual(loader)
    # random_individual.greedy()
    random_individual.greedy_modified(mode="target")
    print(random_individual.T)
    print(random_individual.fitness())
    print(random_individual.check_if_correct_separation())
    print(random_individual.check_if_correct_time_frame())


if __name__ == "__main__":
    main()
