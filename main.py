from loader import Loader
from individual import Individual
from evolve import Evolve


def run_greedy():
    loader = Loader(path="data/airland1.txt")
    [print(x) for x in loader.planes]
    print(loader.separation_matrix)
    random_individual = Individual(loader)
    # random_individual.greedy()
    # random_individual.greedy_modified(mode="target")
    random_individual.greedy_randomized()
    print(random_individual.T)
    print(random_individual.fitness())
    print(random_individual.check_if_correct_separation())
    print(random_individual.check_if_correct_time_frame())


def run_ev():
    loader = Loader(path="data/airland1.txt")
    [print(x) for x in loader.planes]
    print(loader.separation_matrix)
    ev = Evolve(loader)
    ev.alg_loop()


def main():
    #run_ev()
    run_greedy()


if __name__ == "__main__":
    main()
