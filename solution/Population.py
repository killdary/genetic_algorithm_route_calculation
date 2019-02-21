import numpy as np


class Population:
    def __init__(self, start_city, end_city, function_mensure_coust, max_coust):
        self.start = np.array([start_city])
        self.end = np.array([end_city])
        self.function_mensure_coust = function_mensure_coust
        self.max_coust = max_coust



    def initialize(self, initial, size):
        genes_elements = np.copy(initial)

        population_init = list()

        for i in range(size):
            individual = np.random.choice(genes_elements, genes_elements.size, replace=False)
            #
            # if self.max_coust > 0:
            #     while True:
            #         coust = self.function_mensure_coust(np.concatenate([self.start, individual, self.end]))
            #
            #         if coust > self.max_coust:
            #             city_remove = np.random.randint(0, individual.shape[0], 1)
            #             individual = np.delete(individual, city_remove)
            #         else:
            #             break

            individual = np.concatenate([self.start,individual, self.end])
            population_init.append(individual)

        return population_init

    def initialize_with_coust(self, initial, size, distancias):
        mean_distances = np.matrix(distancias).mean()
        number_selection = round(self.max_coust/mean_distances)

        genes_elements = np.copy(initial)

        population_init = list()

        for i in range(size):
            individual = np.random.choice(genes_elements, number_selection - 2, replace=False)

            individual = np.concatenate([self.start, individual, self.end])
            population_init.append(individual)

        return population_init



if __name__ == '__main__':
    start = np.array([0])
    end = np.array([15])
    pop = Population(start, end)
    init = np.arange(1,10)
    cromossomes = np.concatenate([start, init ,end])


    population = pop.initialize(cromossomes,10)

    print(population)


