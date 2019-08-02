import numpy as np


class Population:
    def __init__(self, start_city, end_city, function_mensure_coust, max_coust, distance):
        self.start = np.array(start_city)
        self.end = np.array(end_city)
        self.function_mensure_coust = function_mensure_coust
        self.max_coust = max_coust
        self.distance = distance



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


    def initialize_OP(self, initial, size):
        """
        funcao responsavel por iniciar uma populacao para o orieteering problem
        :param initial:
        :param size:
        :return:
        """
        new_population = list()
        for i in range(size):
            cromossome_default = np.copy(initial)
            chromossome_generate = np.copy(cromossome_default)
            np.random.shuffle(chromossome_generate)


            while True:
                mede_custo_rota = self.function_mensure_coust(np.concatenate([self.start, chromossome_generate, self.end]))
                if mede_custo_rota <= self.max_coust:
                    break
                if chromossome_generate.size -1 == 0:
                    chromossome_generate = np.copy(cromossome_default)
                    np.random.shuffle(chromossome_generate)

                city_rmv = np.random.randint(chromossome_generate.size -1, size=1)
                chromossome_generate = np.delete(chromossome_generate, [city_rmv])

            new_population.append(np.concatenate([self.start, chromossome_generate, self.end]))

        return new_population

    '''observar a forma de geracao da população para melhoria dos métodos anteriores'''
    def initialize_TOP(self, initial, size, number_agents=3):
        new_population = list()
        range_agents = range(number_agents)
        for n in range(size):
            all_points = np.copy(initial)

            # points = np.random.choice(all_points, number_agents, replace=False)

            # all_points = np.setdiff1d(all_points, points)

            chromossome = list()
            for n_ag in range_agents:
                chromossome.append(np.array([]))

            for n_ag in range_agents:
                max_coust = self.max_coust[n_ag]
                while True:
                    point_add = np.random.choice(np.arange(all_points.size), 1)
                    tmp_agent = np.concatenate([chromossome[n_ag], all_points[point_add]])
                    x = self.start
                    x = self.end
                    coust_route = self.function_mensure_coust(np.concatenate([[self.start], tmp_agent, [self.end]]))

                    if coust_route > max_coust:
                        break
                    if coust_route <= max_coust:
                        chromossome[n_ag] = tmp_agent
                        all_points = np.setdiff1d(all_points, tmp_agent)

                coust_route =  self.function_mensure_coust(np.concatenate([[self.start], chromossome[n_ag], [self.end]]))
                chromossome[n_ag] = np.concatenate([[self.start], chromossome[n_ag], [self.end]])


            new_population.append(chromossome)

        return new_population

    def initializeTopMd(self, initial, size, numberAgents):
        newPopulation = list()
        listAgents = range(numberAgents)
        for n in range(size):
            all_points = np.copy(initial)

            chromossome = list()
            for n_ag in listAgents:
                chromossome.append(np.array([]))
                max_cost = self.max_coust[n_ag]
                while True:
                    point_add = np.random.choice(np.arange(all_points.size), 1)
                    tmp_agent = np.concatenate([chromossome[n_ag], all_points[point_add]])
                    coust_route = self.function_mensure_coust(np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))

                    if coust_route > max_cost * 5:
                        break
                    if coust_route <= max_cost * 5:
                        chromossome[n_ag] = tmp_agent
                        all_points = np.setdiff1d(all_points, tmp_agent)
                    if all_points.size > 0:
                        break

                coust_route = self.function_mensure_coust(np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))
                chromossome[n_ag] = np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]])

            elements_chromossome = np.array([])

            for i in chromossome:
                elements_chromossome = np.concatenate([elements_chromossome, i[1:-1]])

            if elements_chromossome.size > np.unique(elements_chromossome).size:
                print('aqui')
            newPopulation.append(chromossome)

        return newPopulation


    def initializeTopMd2(self, initial, size, numberAgents):
        newPopulation = list()
        listAgents = range(numberAgents)
        for n in range(size):
            all_points = np.copy(initial)

            chromossome = list()
            for n_ag in listAgents:
                chromossome.append(np.array([]))
                max_cost = self.max_coust[n_ag]
                while True:
                    point_add = np.random.choice(np.arange(all_points.size), 1)
                    tmp_agent = np.concatenate([chromossome[n_ag], all_points[point_add]])
                    coust_route = self.function_mensure_coust(np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))

                    if coust_route > max_cost:
                        break
                    if coust_route <= max_cost:
                        chromossome[n_ag] = tmp_agent
                        all_points = np.setdiff1d(all_points, tmp_agent)
                    if all_points.size > 0:
                        break

                coust_route = self.function_mensure_coust(np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))
                chromossome[n_ag] = np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]])

            elements_chromossome = np.array([])

            for i in chromossome:
                elements_chromossome = np.concatenate([elements_chromossome, i[1:-1]])

            if elements_chromossome.size > np.unique(elements_chromossome).size:
                print('aqui')
            newPopulation.append(chromossome)

        return newPopulation

    def testeinit(self, initial, size, numberAgents):
        new_population = list()
        # size = initial.size
        slice = int(initial.size/numberAgents)
        for n in range(size):
            all_points = np.copy(initial)
            np.random.shuffle(all_points)
            agent = list()
            count = 0
            end = slice
            for i in range(numberAgents):
                if i < numberAgents-1:
                    x = np.copy(all_points[count:end])
                    agent.append(np.concatenate([[self.start[i]],x, [self.end[i]]]))
                    count = end
                    end = slice +end
                else:
                    x = np.copy(all_points[count:-1])
                    agent.append(np.concatenate([[self.start[i]],x, [self.end[i]]]))

            new_population.append(agent)

        return new_population

    def initializeTopMdGreed(self, initial, size, numberAgents, biggest=5):
        new_population = list()
        list_agents = range(numberAgents)

        for n in range(size):
            all_points = np.copy(initial)

            chromossome = list()
            for n_ag in list_agents:
                chromossome.append(np.array([]))
                max_cost = self.max_coust[n_ag]
                while True:
                    key = np.random.choice(range(numberAgents), 1, replace=False)
                    list_dist_key = self.distance[key,all_points]
                    # ind_minor = np.argmin(list_dist_key)
                    key = [np.argmin(list_dist_key)]


                    point_add = key

                    tmp_agent = np.concatenate([chromossome[n_ag], all_points[point_add]])
                    coust_route = self.function_mensure_coust(
                        np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))

                    if coust_route > max_cost *biggest:
                        break
                    if coust_route <= max_cost*biggest:
                        chromossome[n_ag] = tmp_agent
                        all_points = np.setdiff1d(all_points, tmp_agent)
                    if all_points.size == 0:
                        break

                chromossome[n_ag] = np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]])

            new_population.append(chromossome)

        return new_population

    def initializeTopMdGreed2(self, initial, size, numberAgents, biggest=5):
        new_population = list()
        list_agents = range(numberAgents)

        for n in range(size):
            all_points = np.copy(initial)
            all_elements_cromossomo = np.array([])

            chromossome = list()
            for n_ag in list_agents:
                chromossome.append(np.array([]))
                max_cost = self.max_coust[n_ag]

                ind = np.arange(all_points.size)
                np.random.shuffle(ind)

                key = all_points[ind[0]]
                chromossome[n_ag] = np.array([key])
                ind_remove = np.isin(all_points,chromossome[n_ag], invert=True)
                all_points =all_points[ind_remove]
                all_elements_cromossomo = np.concatenate([all_elements_cromossomo, chromossome[n_ag]])
                all_elements_cromossomo = np.unique(all_elements_cromossomo)

                while True:
                    last = chromossome[n_ag][-1]
                    indices_vizinho = np.isin(all_points,[last], invert=True)
                    vizinhos = all_points[indices_vizinho]
                    list_dist_key = self.distance[last][vizinhos]
                    # ind_minor = np.argmin(list_dist_key)
                    if list_dist_key.size == 0:
                        break
                    key = [np.argmin(list_dist_key)]

                    point_add = key

                    tmp_agent = np.concatenate([chromossome[n_ag], all_points[point_add]])
                    coust_route = self.function_mensure_coust(
                        np.concatenate([[self.start[n_ag]], tmp_agent, [self.end[n_ag]]]))

                    if coust_route > max_cost * biggest:
                        break
                    if coust_route <= max_cost * biggest:
                        chromossome[n_ag] = tmp_agent
                        ind_remove = np.isin(all_points,chromossome[n_ag], invert=True)
                        all_points =all_points[ind_remove]
                        all_elements_cromossomo = np.concatenate([all_elements_cromossomo, chromossome[n_ag]])
                        all_elements_cromossomo = np.unique(all_elements_cromossomo)
                    if all_points.size == 0:
                        break

                chromossome[n_ag] = np.concatenate([[self.start[n_ag]], chromossome[n_ag], [self.end[n_ag]]])

            if 0 not in chromossome[0]:
                print('falha')

            new_population.append(chromossome)

        return new_population

if __name__ == '__main__':
    start = np.array([0])
    end = np.array([15])
    pop = Population(start, end)
    init = np.arange(1,10)

    cromossomes = np.concatenate([start, init ,end])




    population = pop.initialize(cromossomes,10)

    print(population)


