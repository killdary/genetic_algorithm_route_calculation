import numpy as np
import matplotlib.pyplot as plt
from Mutation import Mutation
from FunctionObjective import FunctionObjective
from Crossover import Crossover
from Population import Population
from Selection import Selection


class GaTopMd:
    generationSize: int
    populationSize: int
    limit_population: int
    crossover_rate: float
    mutation_rate: float
    cost_rate: int
    prizes_rate: int
    map_points: np.array
    prizes: np.array
    max_cost: np.array
    start_point: list
    end_point: list

    distance = np.array

    def __init__(self, generation, population, limit_population, crossover_rate,
                 mutation_rate, cost_rate, prizes_rate, map_points,
                 prizes, max_cost, start_point, end_point):

        self.generationSize = generation
        self.populationSize = population
        self.limit_population = limit_population
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.cost_rate = np.array(cost_rate)
        self.prizes_rate = prizes_rate
        self.map_points = np.loadtxt(map_points)
        self.prizes = np.loadtxt(prizes)[:, 1]
        self.max_cost = max_cost
        self.start_point = start_point
        self.end_point = end_point

        self.number_agents = len(max_cost)

        self.distance = self.calculate_distances()
        self.functionObject = FunctionObjective(self.map_points, self.prizes)

        self.FO = self.functionObject.FO
        self.mensureCost = self.functionObject.med_custo
        self.methodInsertRemoveChromossome = self.functionObject.coust_insert

        self.allElementsMap = np.arange(self.map_points.shape[0])

        # removendo depositos
        deposits = [x for x in self.start_point]
        deposits = [x for x in self.end_point if x in deposits]
        self.initialChromossome = np.arange(self.map_points.shape[0])
        self.initialChromossome = np.delete(self.initialChromossome, [deposits])

        self.mutationObject = Mutation(self.mensureCost, self.max_cost, self.prizes)
        self.mutation = self.mutationObject.scramble

        self.crossoverObject = Crossover()
        self.crossover = self.crossoverObject.cross_TOPMD

        self.PopulationObject = Population(self.start_point, self.end_point, self.mensureCost, self.max_cost)

        self.SelectionObject = Selection()
        self.selection = self.SelectionObject.tournament

    def calculate_distances(self):
        size = self.map_points.shape[0]
        distances = np.zeros([size, size])

        temp_max = 0

        for i in range(size):
            for j in range(size):
                if i != j:
                    b = self.map_points[i, 0] - self.map_points[j, 0]
                    c = self.map_points[i, 1] - self.map_points[j, 1]
                    a = np.sqrt(np.square(b) + np.square(c))

                    distances[i, j] = a
                    distances[j, i] = a

                    if temp_max < a:
                        temp_max = a

        return distances

    @staticmethod
    def reply_method_top(method, chromossome):
        size = len(chromossome)
        result = np.zeros(size)
        for n in np.arange(size):
            result[n] = method(chromossome[n])

        return result

    def run(self):
        population = self.PopulationObject.initializeTopMd(self.initialChromossome,
                                                           self.populationSize,
                                                           self.number_agents)

        bestElements = population[0:4]
        bestElementsCosts = np.array([self.reply_method_top(self.FO, element).sum() for element in bestElements])

        countGenaration = 0
        bestElementGenaration = np.copy(bestElements[0])
        bestElementGenarationCost = np.copy(bestElementsCosts[0])

        for g in range(self.generationSize):

            print(g, countGenaration, bestElementGenarationCost)

            # completando populacao depois que apenas os melhores individuos restaram
            population += self.PopulationObject.initialize_TOP(self.initialChromossome,
                                                              self.populationSize - len(population),
                                                              self.number_agents)

            cost_population = [self.reply_method_top(self.FO, individual) for individual in population]
            cost_population = [costs.sum() for costs in cost_population]
            cost_population = np.array([costs.sum() for costs in cost_population])

            select_parents_index = self.selection(self.populationSize, cost_population, 5)
            parents_selected = [population[idx] for idx in select_parents_index]

            new_population = list()

            # Realizando o cruzamento entre os genees
            for cross in range(select_parents_index.size):
                select_2_parents = np.random.randint(select_parents_index.size, size=2)

                offspring1, offspring2 = self.crossover(parents_selected[select_2_parents[0]],
                                                        parents_selected[select_2_parents[1]],
                                                        function_objective=self.FO)

                new_population.append(offspring1)
                new_population.append(offspring2)


if __name__ == '__main__':
    ga = GaTopMd(
        generation = 1000,
        population = 500,
        limit_population = 50,
        crossover_rate = 80,
        mutation_rate = 0.8,
        cost_rate = 5,
        prizes_rate = 2,
        map_points = '../rota_team_17.txt',
        prizes = '../rota_team_17_p.txt',
        # map_points = '../adilson_cidades.txt',
        # prizes = '../adilson_premios.txt',
        max_cost=[10, 8],
        start_point = [0, 1],
        end_point = [0, 1])
        # individual= 0)
    ga.run()