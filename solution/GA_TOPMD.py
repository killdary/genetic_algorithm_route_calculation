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
        self.max_cost = np.array(max_cost)
        self.start_point = start_point
        self.end_point = end_point

        self.number_agents = len(max_cost)

        self.distance = self.calculate_distances()
        self.functionObject = FunctionObjective(self.map_points, self.prizes)

        self.FO = self.functionObject.FO
        self.mensureCost = self.functionObject.med_custo
        self.methodInsertRemoveChromosome = self.functionObject.coust_insert

        self.allElementsMap = np.arange(self.map_points.shape[0])
        self.allElementsMap = self.allElementsMap[self.number_agents:]

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

    def plota_rotas_TOP(self, cidades, rota, size=12, font_size=20, file_plot=False, name_file_plot='plt'):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route300
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """

        pos_x = [cidades[val.astype(int), 0] for val in rota]
        pos_y = [cidades[val.astype(int), 1] for val in rota]

        elements = self.map_points[:, 0]
        x = self.map_points[:, 0]
        y = self.map_points[:, 1]

        cid_nome = range(elements.size)

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=80,
                   facecolor='w',
                   edgecolor='k')

        for i in range(len(rota)):
            plt.plot(pos_x[i],
                     pos_y[i],
                     'C' + str(i),
                     lw=5,
                     label='agente ' + str(i + 1))

        plt.rc('font', size=font_size)

        plt.legend(loc='center left')

        plt.scatter(self.map_points[:, 0], self.map_points[:, 1], s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(str(self.prizes[i]), (x[i] - 0.01, y[i] + 0.3), fontsize=font_size)

        #        plt.title('Mapa GA')
        if file_plot:
            plt.savefig(name_file_plot+'.png')
        else:
            plt.show()

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

    def reply_method_mutation_top(self, method, chromossome):
        size = len(chromossome)
        result = [0] * size
        for n in np.arange(size):
            if chromossome[n].size > 3:
                result[n] = method(chromossome[n])
            else:
                result[n] = chromossome[n]

        return chromossome

    def run(self):
        population = self.PopulationObject.initializeTopMd(self.initialChromossome,
                                                           self.populationSize,
                                                           self.number_agents)

        size_best_elements = 4
        bestElements = population[0:4]
        bestElementsCosts = np.array([self.reply_method_top(self.FO, element).sum() for element in bestElements])

        countGenaration = 0
        bestCost = bestElementsCosts[0]
        bestElementAlways = bestElements[0]
        bestElementGenaration = list()
        bestElementGenarationCost = list()

        for g in range(self.generationSize):

            print(g, bestCost, countGenaration)

            # completando populacao depois que apenas os melhores individuos restaram
            population += self.PopulationObject.initializeTopMd(self.initialChromossome,
                                                              self.populationSize - len(population),
                                                              self.number_agents)

            cost_population = [self.reply_method_top(self.FO, individual) for individual in population]
            cost_population = [costs.sum() for costs in cost_population]
            cost_population = np.array([costs.sum() for costs in cost_population])

            select_parents_index = self.selection(self.populationSize, cost_population, 5)
            parents_selected = [population[idx] for idx in select_parents_index]

            new_population = bestElements[:4]
            bestElementsTeste = bestElements

            # Realizando o cruzamento entre os genees
            for cross in range(select_parents_index.size):
                select_2_parents = np.random.randint(select_parents_index.size, size=2)

                # offspring1, offspring2 = self.crossover(parents_selected[select_2_parents[0]],
                #                                         parents_selected[select_2_parents[1]],
                #                                         function_objective=self.FO)

                offspring1, offspring2 = list(), list()
                all_elements_1, all_elements_2 = np.array([]), np.array([])
                for i in range(len(parents_selected[select_2_parents[0]])):
                    x,y = self.crossoverObject.PMX_3(parents_selected[select_2_parents[0]][i],
                                                     parents_selected[select_2_parents[1]][i],
                                                     all_elements_1, all_elements_2 )

                    all_elements_1 = np.unique(np.concatenate([all_elements_1, x[1:-1]]))
                    all_elements_2 = np.unique(np.concatenate([all_elements_2, y[1:-1]]))

                    offspring1.append(x)
                    offspring2.append(y)

                # for ii in range(len(offspring1)):
                #     for jj in range(len(offspring1)):
                #         if ii != jj:
                #             xxx = np.intersect1d(offspring1[ii], offspring1[jj])
                #             yyy = np.intersect1d(offspring2[ii], offspring2[jj])
                #
                #             if xxx.size > 1:
                #                 print('xxx')
                #                 print(offspring1)
                #                 # offspring1[jj] = offspring1[jj][np.isin(offspring1[jj],offspring1[ii], invert=True)]
                #             if yyy.size > 1:
                #                 print('yyy')
                #                 print(offspring2)
                #                 # offspring2[jj] = offspring2[jj][np.isin(offspring2[jj],offspring2[ii], invert=True)]


                # offspring3, offspring4 = self.crossoverObject.PMX_2(parents_selected[select_2_parents[0]],
                #                                                     parents_selected[select_2_parents[1]])


                new_population.append(offspring1)
                new_population.append(offspring2)


            # for i in range(len(new_population)):
            #    new_population[i] = self.reply_crossover_inner_agents(self.crossover_class.PMX, new_population[i])

            # gerando lista de probabilidades para os novos indivíduos sofrerem mutações
            rand = np.random.uniform(0,1, len(new_population))


            for i in range(len(new_population)):
                new_population[i] = self.mutationObject.insert_points_TOP_2(self.mensureCost,
                                                                         self.methodInsertRemoveChromosome,
                                                                         self.allElementsMap,
                                                                         new_population[i])

            fitness_values = np.zeros(len(new_population))
            cousts_values = np.zeros(len(new_population))

            for i in range(fitness_values.size):
                fitness_values[i] = self.reply_method_top(self.FO,new_population[i]).sum()
                cousts_values[i] =  self.reply_method_top(self.mensureCost,new_population[i]).sum()

            # aqui não foi atualizado####################
            population_mutation = list()
            for i in range(rand.size):
                if rand[i] <= self.mutation_rate:
                    list_mut = list()
                    list_mut.append(self.reply_method_mutation_top(self.mutationObject.swap,new_population[i]))
                    list_mut.append(self.reply_method_mutation_top(self.mutationObject.insertion,new_population[i]))
                    list_mut.append(self.reply_method_mutation_top(self.mutationObject.reverse,new_population[i]))
                    list_mut.append(self.reply_method_mutation_top(self.mutationObject.scramble,new_population[i]))
                    # list_mut.append(self.reply_method_mutation_top(self.mutationObject.swap,new_population[i]))

                    if self.number_agents > 1:
                        try:
                            ind = np.random.choice(range(self.number_agents), 2, replace=False)
                            elemento = [np.copy(chromossome) for chromossome in new_population[i]]
                            elemento[ind[0]], elemento[ind[1]] = self.mutationObject.PMX_mutation(
                                elemento[ind[0]], elemento[ind[1]], np.array([]), np.array([]))
                            list_mut.append(elemento)
                        except:
                            print(ind, elemento)
                            raise
                    else:
                        list_mut.append(self.reply_method_mutation_top(self.mutationObject.scramble, new_population[i]))



                    # if(countGenaration > self.limit_population * 0.6):
                    # list_mut.append(self.reply_method_mutation_top(self.mutationObject.WGWRGM,new_population[i]))
                    # list_mut.append(self.reply_method_mutation_top(self.mutationObject.WGWWGM,new_population[i]))
                    # list_mut.append(self.reply_method_mutation_top(self.mutationObject.WGWNNM,new_population[i]))


                    # cousts_mut = np.zeros(len(list_mut))
                    #
                    # cousts_mut[0] = sum(self.reply_method_top(self.mensureCost,list_mut[0]))
                    # cousts_mut[1] = sum(self.reply_method_top(self.mensureCost,list_mut[1]))
                    # cousts_mut[2] = sum(self.reply_method_top(self.mensureCost,list_mut[2]))
                    # cousts_mut[3] = sum(self.reply_method_top(self.mensureCost,list_mut[3]))
                    # cousts_mut[4] = sum(self.reply_method_top(self.mensureCost,list_mut[4]))
                    # cousts_mut[5] = sum(self.reply_method_top(self.mensureCost,list_mut[5]))
                    #
                    # # if(countGenaration > self.limit_population * 0.6):
                    # cousts_mut[6] = sum(self.reply_method_top(self.mensureCost,list_mut[6]))
                    # cousts_mut[7] = sum(self.reply_method_top(self.mensureCost,list_mut[7]))
                    # cousts_mut[8] = sum(self.reply_method_top(self.mensureCost,list_mut[8]))
                    #
                    # min_mut = np.argmin(cousts_mut)
                    # new_population[i] = list_mut[min_mut]
                    population_mutation = population_mutation + list_mut

                    # if self.number_agents > 1:
                    #     ind = np.random.choice(range(self.number_agents), 2)
                    #     elemento = [np.copy(chromossome) for chromossome in  new_population[i]]
                    #     elemento[ind[0]], elemento[ind[1]] = self.crossoverObject.PMX_2(
                    #         elemento[ind[0]], elemento[ind[1]],np.array([]), np.array([]))

                else:
                    population_mutation.append(new_population[i])


            for i in range(len(new_population)):
                new_population[i] = self.mutationObject.remove_points_TOP(self.mensureCost,
                                                                         self.methodInsertRemoveChromosome,
                                                                         self.allElementsMap,
                                                                         new_population[i])


            # new_population = new_population + population

            fitness_values = np.zeros(len(new_population))
            cousts_values = np.zeros(len(new_population))

            for i in range(fitness_values.size):
                fitness_values[i] = self.reply_method_top(self.FO, new_population[i]).sum()
                cousts_values[i] = self.reply_method_top(self.mensureCost, new_population[i]).sum()


            population_select = list()
            population = list()
            for i in range(int(self.populationSize * 0.8)):
                if len(new_population) == 0:
                    break
                min_index = np.argmin(fitness_values)
                # if cousts_values[i].sum() <= self.max_cost.sum():
                passa = list()
                custo = self.reply_method_top(self.mensureCost, new_population[min_index])
                for j in range(self.number_agents):
                    if custo[j] > self.max_cost[j]:
                        passa.append(False)

                if False not in passa:

                    exist_menor = [best for best in range(4) if
                                   fitness_values[min_index] < bestElementsCosts[best]]

                    crhomossome = new_population[min_index]

                    if len(exist_menor) > 0:
                        flag_possui = [np.array_equal(element, crhomossome) for element in bestElements]
                        if True not in flag_possui:

                            # beste_elements_new = list()
                            # best_costs_new = list()
                            # cost_chromosome = self.reply_method_top(self.FO, crhomossome).sum()
                            # add_elemente = False
                            # for element in range(size_best_elements):
                            #     if cost_chromosome < bestElementsCosts[element]:
                            #         beste_elements_new.append(crhomossome)
                            #         best_costs_new.append(cost_chromosome)
                            #
                            #         if element < size_best_elements -1:
                            #             for restante in range(element,size_best_elements-1):
                            #                 beste_elements_new.append(bestElements[restante])
                            #                 best_costs_new.append(bestElementsCosts[restante])
                            #         break
                            #     else:
                            #         beste_elements_new.append(bestElements[element])
                            #         best_costs_new.append(bestElementsCosts[element])
                            #
                            # bestElements = beste_elements_new
                            # bestElementsCosts = best_costs_new

                            best_elements_temporary = bestElements
                            best_elements_temporary.append(crhomossome)

                            new_cousts = np.array(
                                [self.reply_method_top(self.FO, tmp).sum() for tmp in best_elements_temporary])
                            indexes_best_individual = np.argsort(new_cousts)
                            indexes_best_individual = indexes_best_individual[0:size_best_elements]

                            bestElementsCosts = new_cousts[indexes_best_individual]
                            bestElements = [best_elements_temporary[best_index] for best_index in indexes_best_individual]
                    else:
                        if fitness_values[min_index] not in population_select:
                            population.append(new_population[min_index])
                            population_select.append(fitness_values[min_index])

                del new_population[min_index]
                fitness_values = np.delete(fitness_values, [min_index])


                # for i in range(len(population)):
                #     if np.unique(population[i]).size < population[i].size - 1:
                #         print('error')

            if bestElementsCosts[0] < bestCost:
                bestCost = bestElementsCosts[0]
                bestElementAlways = np.copy(bestElements[0])
                countGenaration = 0

                # bestElementTesteando = [np.copy(element) for element in bestElements]
                # bestElementTesteandoCost = np.copy(bestElementsCosts)

                bestElementGenaration.append(bestCost)
                # print(self.reply_method_top(self.mensureCost, bestElements[0]))

            # elif bestElementsCosts[0] == bestCost:
            #     countGenaration += 1

            else:
                countGenaration += 1
                population.append(bestElementAlways)
                # custos = self.reply_method_top(self.mensureCost, bestElements[0])
                # print(custos)
                # print([True for item in range(self.number_agents) if custos[item] > self.max_cost[item]])

                # bestElements = [np.copy(element) for element in bestElementTesteando]
                # bestElementsCosts = np.copy(bestElementTesteandoCost)

            bestElementGenarationCost.append(bestElementsCosts[0])

            population = population+bestElements
            if countGenaration >= self.limit_population:
                break

        self.bestRoute = bestElements[0]


        return bestElementsCosts, bestElements, bestElementGenaration, bestElementAlways



if __name__ == '__main__':
    ga = GaTopMd(
        generation = 1000,
        population = 175,
        limit_population = 25,
        crossover_rate = 0.3,
        mutation_rate = 0.6,
        cost_rate = 2,
        prizes_rate = 5,
        map_points = 'GATOPMD/mapas/novas_cidades_6.txt',
        prizes = 'GATOPMD/mapas/novos_premios_6.txt',
        max_cost=[25, 25 , 25, 25],
        start_point = [0,0,0,0],
        end_point = [2,4,40,37])
        # individual= 0)
    a, b, c, d = ga.run()

    for i in range(1):
        print('custo')
        for j in range(len(b[i])):
            print(ga.mensureCost(b[i][j]))
        print(' - ')
        for j in range(len(b[i])):
            print(ga.prizes.take(b[i][j].astype(int)).sum())
        ga.plota_rotas_TOP(ga.map_points, b[i])

        print(b[i])
        input()
        # print(a[i])