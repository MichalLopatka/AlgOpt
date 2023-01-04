from loader import Loader
from individual import Individual
from evolve import Evolve
from ants import Ants


def run_greedy():
    loader = Loader(path="data/airland13.txt")
    # [print(x) for x in loader.planes]
    # print(loader.separation_matrix)
    random_individual = Individual(loader)
    # random_individual.greedy()
    random_individual.greedy_modified(mode="target")
    # random_individual.greedy_randomized()
    # random_individual.greedy_randomized2()
    print(random_individual.T)
    print(random_individual.fitness())
    print(random_individual.check_if_correct_separation())
    print(random_individual.check_if_correct_time_frame())


def run_ev():
    loader = Loader(path="data/airland7.txt")
    # [print(x) for x in loader.planes]
    # print(loader.separation_matrix)
    ev = Evolve(loader)
    best = ev.alg_loop()
    print(best)


def run_ants():
    loader = Loader(path="data/airland5.txt")
    # [print(x) for x in loader.planes]
    # print(loader.separation_matrix)
    ev = Ants(loader)
    ev.loop()


def main():
    # run_ev()
    # run_greedy()
    run_ants()


if __name__ == "__main__":
    main()
