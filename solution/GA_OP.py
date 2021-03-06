import numpy as np
import matplotlib.pyplot as plt
from Mutation import Mutation
from Crossover import Crossover
from Population import Population
from Selection import Selection
from FunctionObjective import FunctionObjective


class GA_TSPKP:

    def distance_matrix_calculate(self):
        """
        Method that calculate the distance matrix
        :param cidades: points or towns informed
        :return: numpy.matrix
        """
        qtd = self.mapa.shape[0]
        distancias = np.zeros([qtd, qtd])

        _temp_max = 0

        for i in range(qtd):
            for j in range(i, qtd):
                if i != j:
                    b = self.mapa[i, 0] - self.mapa[j, 0]
                    c = self.mapa[i, 1] - self.mapa[j, 1]
                    a = np.sqrt(np.square(b) + np.square(c))

                    distancias[i, j] = a
                    distancias[j, i] = a

                    if _temp_max < a:
                        _temp_max = a

        self.distancias = distancias

    '''funcao para remover valores repetidos da ordem da cidade'''
    @staticmethod
    def removed_citys_repeat(flux):
        citys_position = np.unique(flux, return_index=True)[1]
        citys_position.sort()
        new_citys = flux.take(citys_position)

        return new_citys

    def plota_rotas(self,cidades, rota, size=8, font_size=20):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """
        pos_x = cidades[rota.astype(int), 0]
        pos_y = cidades[rota.astype(int), 1]

        all_x = self.mapa[rota.astype(int), 0]
        all_y = self.mapa[rota.astype(int), 1]

        elements = self.mapa[:,0]
        x = self.mapa[:, 0]
        y = self.mapa[:,1]

        cid_nome = range(elements.size)

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=40,
                   facecolor='w',
                   edgecolor='k')

        plt.plot(pos_x, pos_y, 'C3', lw=3)
        plt.scatter(self.mapa[:, 0], self.mapa[:, 1], s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(txt ,  (x[i]-0.01, y[i]+0.3), fontsize=font_size)

        plt.title('Mapa GA')
        plt.show()

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            if key == 'genetarion':
                self.generation_size = value
            elif key == 'population':
                self.population_size = value
            elif key == 'limit_population':
                self.limit_population = value
            elif key == 'crossover_rate':
                self.crossover_rate = value
            elif key == 'mutation_rate':
                self.mutation_rate = value
            elif key == 'map_points':
                self.map_points = value
            elif key == 'max_coust':
                self.max_coust = value
            elif key == 'coust_rate':
                self.coust_rate = value
            elif key == 'prizes_rate':
                self.prizes_rate = value
            elif key == 'start_point':
                self.start_point = value
            elif key == 'end_point':
                self.end_point = value
            elif key == 'prizes':
                prizes = np.loadtxt(value)
                self.prizes = prizes[:, 1]
            elif key == 'initial_cromossome':
                self.initial_cromossome = value
                self.best_route = value
                self.receive_route = True
            elif key == 'number_agents':
                self.number_agents = value

        self.mapa = np.loadtxt(self.map_points)
        self.distance_matrix_calculate()

        self.FunctionObject = FunctionObjective(self.mapa, self.prizes)
        self.function_objective = self.FunctionObject.FO
        self.med_custo = self.FunctionObject.med_custo
        self.function_insert_remove = self.FunctionObject.coust_insert

        # todos os pontos de um mapa
        self.all_elements = np.arange(self.mapa.shape[0])

        if 'initial_cromossome' not in locals():
           self.initial_cromossome = np.arange(self.mapa.shape[0])
           self.receive_route = False

        if self.start_point != self.end_point:
            self.initial_cromossome = np.delete(self.initial_cromossome, [self.start_point, self.end_point])
        else:
            self.initial_cromossome = np.delete(self.initial_cromossome, [self.start_point])

        self.mutation_object = Mutation(self.max_coust, self.prizes)

        self.mutation = self.mutation_object.scramble

        self.crossover_class = Crossover()
        self.crossover = self.crossover_class.PMX

        self.Population = Population(self.start_point, self.end_point, self.med_custo, self.max_coust)

        self.Selection_object = Selection()
        self.selection = self.Selection_object.tournament

    def run(self):

        if not self.receive_route:
            # gerando uma população inicial
            population = self.Population.initialize_OP(self.initial_cromossome, self.population_size)

            # selecionando os 4melhores como os indivíduos iniciais
            best_elements = population[0:4]
            best_elements_coust = np.array([self.function_objective(element) for element in best_elements])

            best_count = 0
            best_always = np.copy( best_elements[0])
            best_coust = best_elements_coust[0]
            best_element_generation = list()
            for g in range(self.generation_size):

                print(g, best_coust, best_count)

                # calculo do custo
                cousts_population = [self.function_objective(value) for value in population]
                cousts_population = np.array(cousts_population)

                # selecionano os pais para cruzamento
                selected_parents_index = self.selection(self.population_size, cousts_population, 5)
                parents_select = [population[chromossome] for chromossome in selected_parents_index]

                # lista que terá a nova população
                new_population = list()

                for i in range(selected_parents_index.size):
                    #
                    select_2_parents = np.random.randint(selected_parents_index.size, size=2)

                    offspring_1,offspring_2 = self.crossover(parents_select[select_2_parents[0]],parents_select[select_2_parents[1]])

                    new_population.append(offspring_1)
                    new_population.append(offspring_2)

                # gerando lista de probabilidades para os novos indivíduos sofrerem mutações
                rand = np.random.uniform(0,1, len(new_population))

                for i in range(len(new_population)):
                    coust = self.med_custo(new_population[i])
                    if coust > self.max_coust:
                        new_population[i] = self.mutation_object.remove_pior_custo_2(new_population[i],
                                                                                     self.med_custo,
                                                                                     self.function_insert_remove)
                    if coust < self.max_coust:
                        new_population[i] = self.mutation_object.insert_individualin_cromossome_2(new_population[i],
                                                                                              self.all_elements,
                                                                                              self.med_custo,
                                                                                              self.function_insert_remove)

                    coust = self.med_custo(new_population[i])

                for i in range(rand.size):
                    if rand[i] >= self.mutation_rate:
                        if new_population[i].size > 3:
                            list_mut = list()
                            list_mut.append(self.mutation_object.swap(new_population[i]))
                            list_mut.append(self.mutation_object.insertion(new_population[i]))
                            list_mut.append(self.mutation_object.reverse(new_population[i]))
                            list_mut.append(self.mutation_object.scramble(new_population[i]))
                            list_mut.append(self.mutation_object.swap(new_population[i]))
                            list_mut.append(self.mutation_object.WGWRGM(new_population[i], self.med_custo))
                            list_mut.append(self.mutation_object.WGWWGM(new_population[i], self.med_custo))
                            list_mut.append(self.mutation_object.WGWNNM(new_population[i], self.med_custo))

                            cousts_mut = np.zeros(len(list_mut))

                            cousts_mut[0] = self.med_custo(list_mut[0])
                            cousts_mut[1] = self.med_custo(list_mut[1])
                            cousts_mut[2] = self.med_custo(list_mut[2])
                            cousts_mut[3] = self.med_custo(list_mut[3])
                            cousts_mut[4] = self.med_custo(list_mut[4])
                            cousts_mut[5] = self.med_custo(list_mut[5])
                            cousts_mut[6] = self.med_custo(list_mut[6])
                            cousts_mut[7] = self.med_custo(list_mut[7])

                            min_mut = np.argmin(cousts_mut)
                            new_population[i] = list_mut[min_mut]
                new_population = new_population + population

                fitness_values = np.zeros(len(new_population))
                cousts_values = np.zeros(len(new_population))

                for i in range(fitness_values.size):
                    fitness_values[i] = self.function_objective(new_population[i])
                    cousts_values[i] = self.med_custo(new_population[i])

                population_select = np.zeros(self.population_size)
                population = list()
                for i in range(self.population_size):
                    if len(new_population) == 0:
                        break
                    min_index = np.argmin(fitness_values)
                    if cousts_values[i] <= self.max_coust :
                        population_select[i] = min_index

                        exist_menor = [best for best in range(4) if fitness_values[min_index] < best_elements_coust[best]]

                        crhomossome = new_population[min_index]
                        if len(exist_menor) > 0:
                            flag_possui = [np.array_equal(element, crhomossome) for element in best_elements]
                            if True not in flag_possui:
                                best_tmp = best_elements
                                best_tmp.append(crhomossome)

                                new_cousts = np.array([self.function_objective(tmp) for tmp in best_tmp])
                                indexes_tmp = np.argsort(new_cousts)

                                best_elements_coust = new_cousts[indexes_tmp[0:4]]
                                best_elements = [best_tmp[best_index] for best_index in indexes_tmp]

                        population.append(new_population[min_index])
                    del new_population[min_index]
                    fitness_values = np.delete(fitness_values,[min_index])

                for i in range(len(population)):
                    if np.unique(population[i]).size < population[i].size - 1:
                        print('error')

                if best_elements_coust[0] < best_coust:
                    best_coust = best_elements_coust[0]
                    best_always = np.copy(best_elements[0])
                    best_count = 0

                elif best_elements_coust[0] == best_coust:
                    best_count += 1

                best_element_generation.append(best_elements_coust[0])

                if best_count >= self.limit_population:
                    break

            self.best_route = best_elements[0]



        print(best_element_generation)
        return best_elements_coust, best_elements


if __name__ == '__main__':
    ga = GA_TSPKP(
        genetarion = 1000,
        population = 100,
        limit_population = 30,
        crossover_rate = 100,
        mutation_rate = 0.8,
        coust_rate = 5,
        prizes_rate = 2,
        map_points = '../novas_cidades_5.txt',
        prizes = '../novos_premios_5.txt',
        # map_points = '../adilson_cidades.txt',
        # prizes = '../adilson_premios.txt',
        max_coust = 20,
        start_point = 0,
        end_point = 0,
        individual= 0)
    a , b = ga.run()

    for i in range(1):
        print('premios')
        print(ga.prizes.take(b[i]).sum())
        print('custo')
        print(ga.med_custo(b[i]))
        ga.plota_rotas(ga.mapa, b[i])
        # print(a[i])

    # input()