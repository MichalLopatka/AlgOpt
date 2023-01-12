import numpy as np
import random
import numpy.random as npr


class Ants:
    def __init__(self, loader, a=1, b1=2, b2=4, Q=5, p=2, ants=200, iters=30, pheromone_ants=10):
        self.planes = loader.planes
        self.length = len(self.planes)
        self.separation_matrix = loader.separation_matrix
        self.pheromones = np.ones(shape=(self.length, self.length))
        self.a = a
        self.b1 = b1
        self.b2 = b2
        self.Q = Q
        self.p = p
        self.ants = ants
        self.iters = iters
        self.pheromone_ants = pheromone_ants

    def loop(self):
        global_best = np.inf
        global_route = None
        for _ in range(self.iters):
            best_route = None
            best_cost = np.inf
            best_n = np.empty((0,len(self.planes) +1), int)
            for _ in range(self.ants):
                candidates = self.generate_candidate_list_semi_random()
                route = []
                while candidates:
                    if((0 in candidates) and self.planes[0].earliest == self.planes[0].latest):
                        chosen = 0
                    else:
                        chosen = self.select_plane(candidates, route)
                    candidates.remove(chosen)
                    route.append(chosen)
                fitness = self.fitness(route)
                if fitness < best_cost:
                    best_cost = fitness
                    best_route = route
                actual = np.concatenate((fitness, route), axis=None)
                best_n = np.vstack([best_n, actual])
                best_n = best_n[best_n[:, 0].argsort()]
            #print(best_n[:, 0])
            #self.update_pheromones(best_route, best_cost)
            for x in range(self.pheromone_ants):
                self.update_pheromones(best_n[x][1:].astype(int), best_n[x][0].astype(int))
            # print(best_cost, best_route)
            if best_cost < global_best:
                global_best = best_cost
                global_route = best_route
            print(global_best, global_route)


    def generate_candidate_list(self):
        begin = list(range(0, self.length))
        random.shuffle(begin)
        return begin

    def generate_candidate_list_semi_random(self):
        count = len(self.planes)
        T = np.zeros((count, 2))
        rows, _ = T.shape
        for x in range(rows):
            T[x][0] = x
            if(self.planes[x].latest - self.planes[x].earliest == 0):
                T[x][1] = self.planes[x].earliest
            elif(self.planes[x].target - self.planes[x].earliest ==0):
                T[x][1] = random.randrange(
                    self.planes[x].earliest,
                    self.planes[x].latest
                )
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

    def probability(self, pheromone, priority, penalty):
        prob = (
            float(pheromone) ** self.a * (1 / (priority + 1)) ** self.b1
            + (1 / (penalty + 1)) ** self.b2
        )

        return prob

    def probability2(self, priority, penalty):
        prob = (
            (1 / (priority + 1)) ** self.b1
            + (1 / (penalty + 1)) ** self.b2
        )

        return prob

    def assess_priority(self, candidates):
        T = np.zeros((len(candidates), 2))
        for i, el in enumerate(candidates):
            T[i, 0] = int(el)
            T[i, 1] = self.planes[el].target
        T = T[T[:, 1].argsort()]
        T = list(T[:, 0])
        T = [int(x) for x in T]
        return T

    def select_plane(self, candidates, route):
        try:
            last = route[-1]
            priorities = self.assess_priority(candidates)
            probs = [
                self.probability(
                    self.pheromones[last, x],
                    priorities.index(x),
                    self.count_penalty(route, x),
                )
                for x in candidates
            ]
            probs_sum = sum(probs)
            probabilities = [x / probs_sum for x in probs]
            chosen = int(
                np.random.choice(candidates, p=probabilities, replace=False, size=1)
            )
        except (IndexError, TypeError):
            priorities = self.assess_priority(candidates)
            probs = [
                self.probability2(
                    priorities.index(x),
                    self.count_penalty(route, x),
                )
                for x in candidates
            ]
            probs_sum = sum(probs)
            probabilities = [x / probs_sum for x in probs]
            chosen = int(np.random.choice(candidates, replace=False, size=1))
        return chosen

    def update_pheromones(self, best_route, best_penalty):
        for i in range(self.pheromones.shape[0]):
            for j in range(self.pheromones.shape[1]):
                self.pheromones[i, j] = self.p * self.pheromones[i, j]

        for x in range(len(best_route) - 1):
            self.pheromones[best_route[x], best_route[x + 1]] += self.Q / best_penalty

    def count_penalty(self, route, new):
        route = np.append(route, new)
        route = [int(x) for x in route]
        T = np.zeros((len(route), 2))
        rows, _ = T.shape
        for i, el in enumerate(route):
            # print(el)
            T[i, 0] = el
            T[i, 1] = self.planes[el].target
        T = self.repair(T, rows)
        penalty = 0
        position = T[-1]
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
            T[i, 1] = self.planes[el].target
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
