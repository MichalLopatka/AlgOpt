import numpy as np
import random
import numpy.random as npr


class Evolve:
    def __init__(self, loader, population_size: int = 200):
        self.planes = loader.planes
        self.length = len(self.planes)
        self.separation_matrix = loader.separation_matrix
        self.population_size = population_size
        self.population = self.create_population()

    def alg_loop(
        self, iterations: int = 100, tour_size: int = 20, px: float = 0.9, pm: float = 0.3
    ) -> tuple[int, list[int]]:
        t = 0
        population = self.population
        best = None
        best_fitness = 1000000
        while t < iterations:
            new_population = []
            while len(new_population) < self.population_size:
                chosen1 = self.tournament(population, tour_size)
                chosen2 = self.tournament(population, tour_size)
                if random.random() < px:
                    crossed1, crossed2 = self.pmx(chosen1, chosen2)
                else:
                    crossed1, crossed2 = chosen1, chosen2
                if random.random() < pm:
                    mutated1 = self.inverse(crossed1)
                    mutated2 = self.inverse(crossed2)
                    new_population.append(mutated1)
                    new_population.append(mutated2)

                else:
                    new_population.append(crossed1)
                    new_population.append(crossed2)
            t += 1
            population = new_population
            best = self.tournament(new_population, len(new_population))
            fitness = self.fitness(best)
            if fitness < best_fitness:
                best_fitness = fitness
            print(best)
            print(best_fitness)

        return self.fitness(best), best

    def create_population(self) -> list[int]:
        population = []
        for i in range(self.population_size):
            begin = self.semi_random_start()
            population.append(begin)
        return population

    def random_start(self, len):
        begin = list(range(0, len))
        random.shuffle(begin)
        return begin

    def semi_random_start(self):
        count = len(self.planes)
        T = np.zeros((count, 2))
        rows, _ = T.shape
        for x in range(rows):
            T[x][0] = x
            if(self.planes[x].target - self.planes[x].earliest == 0):
                T[x][1] = self.planes[x].earliest
            else:
                T[x][1] = random.randrange(
                    self.planes[x].earliest,
                    self.planes[x].target
                    + (self.planes[x].target - self.planes[x].earliest),
                )
        T = T[T[:, 1].argsort()]

        T = list(T[:, 0])
        T = [int(el) for el in T]
        # print(T)
        return list(T)

    def repair(self, T, rows):
        max_time = max(plane.latest for plane in self.planes)
        for x in range(rows - 1):
            i = int(T[x][0])
            j = int(T[x + 1][0])
            a = T[x][1]
            b = T[x + 1][1]
            while b - a < self.separation_matrix[i][j]:
                b += 1
            T[x][1] = a
            T[x + 1][1] = b
            if b > max_time:
                return T
        return T

    def fitness(self, route):
        T = np.zeros((self.length, 2))
        rows, _ = T.shape
        for i, el in enumerate(route):
            T[i, 0] = el
            T[i, 1] = random.randrange(self.planes[el].earliest, self.planes[el].target)
        T = self.repair(T, rows)
        penalty = 0
        for position in T:
            id, time = position
            plane = self.planes[int(id)]

            if time > plane.latest:
                penalty += 100000 * (time - plane.latest)

            if time < plane.earliest:
                penalty += 100000 * (plane.earliest - time)

            if time > plane.target:
                penalty += (time - plane.target) * plane.penalty_late
            elif time < plane.target:
                penalty += (plane.target - time) * plane.penalty_early

        return penalty

    def swap(self, order: list[int]):
        pos1, pos2 = random.sample(order, 2)
        order[pos1], order[pos2] = order[pos2], order[pos1]
        return order

    def inverse(self, order: list[int]):
        pos1 = random.randint(0, len(order) - 1)
        pos2 = random.randint(pos1 + 1, len(order))
        order[pos1:pos2] = order[pos1:pos2][::-1]
        return order

    def ox(self, order1: list[int], order2: list[int]) -> list[int]:
        left = random.randint(0, len(order1) - 1)
        right = random.randint(left + 1, len(order1))
        part1 = order1[left:right]
        new_order = [None] * len(order2)
        new_order[left:right] = part1
        order2 = [x for x in order2 if x not in part1]
        j = 0
        return_order = []
        for i in range(len(new_order)):
            if new_order[i] is None:
                return_order.append(order2[j])
                j += 1
            else:
                return_order.append(new_order[i])
        return return_order

    def pmx_looking(self, mapping_primary, mapping_secondary, value: int) -> int:
        while value in mapping_primary:
            value = mapping_secondary[mapping_primary.index(value)]
        return value

    def pmx(self, order1: list[int], order2: list[int]) -> tuple[list[int], list[int]]:
        left = random.randint(0, len(order1) - 1)
        right = random.randint(left + 1, len(order1))
        return_order1 = [-1] * len(order1)
        return_order2 = [-1] * len(order2)
        mapping1 = order1[left : right + 1]
        mapping2 = order2[left : right + 1]
        return_order1[left : right + 1] = order2[left : right + 1]
        return_order2[left : right + 1] = order1[left : right + 1]
        for i in range(len(order1)):
            if i >= left and i <= right:
                continue
            if order1[i] in mapping2:
                return_order1[i] = self.pmx_looking(mapping2, mapping1, order1[i])
            else:
                return_order1[i] = order1[i]
        for i in range(len(order2)):
            if i >= left and i <= right:
                continue
            if order2[i] in mapping1:
                return_order2[i] = self.pmx_looking(mapping1, mapping2, order2[i])
            else:
                return_order2[i] = order2[i]
        # print(return_order1, return_order2)
        # print(" ")
        return return_order1, return_order2

    def tournament(self, population: list[list[int]], sample_size: int) -> list[int]:
        sample = random.sample(population, sample_size)
        best = None
        for el in sample:
            if not best or self.fitness(el) < self.fitness(best):
                best = el
        return best

    # def roulette(self, population: list[list[int]]) -> list[int]:
    #     costs = [self.cost(pop) for pop in population]
    #     worst = self.cost(self.worst(population))
    #     diff = [(worst-c) for c in costs]
    #     # print(logs)
    #     max = sum([c for c in diff])
    #     # print(max)
    #     selection_probs = [c/max for c in diff]
    #     to_return = population[npr.choice(len(population), p=selection_probs)]
    #     # print(selection_probs)
    #     # print(to_return)
    #     return to_return
