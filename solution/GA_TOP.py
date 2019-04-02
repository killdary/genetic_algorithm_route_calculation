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

    def plota_rotas(self, cidades, rota, size=8, font_size=20):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """
        pos_x = cidades[rota.astype(int), 0]
        pos_y = cidades[rota.astype(int), 1]

        # all_x = self.mapa[rota.astype(int), 0]
        # all_y = self.mapa[rota.astype(int), 1]

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

    def plota_rotas_TOP(self, cidades, rota, size=8, font_size=20):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """

        pos_x = [cidades[val.astype(int), 0] for val in rota]
        pos_y = [cidades[val.astype(int), 1] for val in rota]

        elements = self.mapa[:,0]
        x = self.mapa[:, 0]
        y = self.mapa[:, 1]

        cid_nome = range(elements.size)

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=40,
                   facecolor='w',
                   edgecolor='k')

        for i in range(len(rota)):
            plt.plot(pos_x[i], pos_y[i], 'C3', lw=3)

        plt.scatter(self.mapa[:, 0], self.mapa[:, 1], s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(txt ,  (x[i]-0.01, y[i]+0.3), fontsize=font_size)

        plt.title('Mapa GA')
        plt.show()


    '''metodo auxilixar para replicar o metodo sempre que possivel'''
    def reply_method_TOP(self, method, chromossome):
        size = len(chromossome)
        result = np.zeros(size)
        for n in np.arange(size):
            result[n] = method(chromossome[n])

        return result

    def reply_method_mutation_TOP(self, method, chromossome):
        size = len(chromossome)
        result = [0] * size
        for n in np.arange(size):
            if chromossome[n].size > 3:
                result[n] = method(chromossome[n])
            else:
                result[n] = chromossome[n]

        return chromossome

    def reply_crossover_inner_agents(self, method, chromossome):
        size = len(chromossome)
        number_cross = int(size/2)
        ids = np.random.choice(size,size, replace=False)
        new_chromossome = list()
        for i in range(0,size-1, 2):
            x,y = method(chromossome[ids[i]], chromossome[ids[i+1]])
            new_chromossome.append(x)
            new_chromossome.append(y)

        new_chromossome.append(chromossome[ids[-1]])


        if True in np.isin(new_chromossome[0][1:-2], new_chromossome[1][1:-2]):
            print('error')
        if True in np.isin(new_chromossome[0][1:-2], new_chromossome[2][1:-2]):
            print('error')
        if True in np.isin(new_chromossome[2][1:-2], new_chromossome[1][1:-2]):
            print('error')


        return  new_chromossome



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

        self.mutation_object = Mutation( self.med_custo, self.max_coust, self.prizes)

        self.mutation = self.mutation_object.scramble

        self.crossover_class = Crossover()
        self.crossover = self.crossover_class.cross_TOP

        self.Population = Population(self.start_point, self.end_point, self.med_custo, self.max_coust)

        self.Selection_object = Selection()
        self.selection = self.Selection_object.tournament

    def run(self):

        if not self.receive_route:
            # gerando uma população inicial
            population = self.Population.initialize_TOP(self.initial_cromossome, self.population_size, self.number_agents)

            # selecionando os 4melhores como os indivíduos iniciais
            best_elements = population[0:4]
            best_elements_coust = np.array([self.reply_method_TOP(self.function_objective, element).sum()
                                                                    for element in best_elements])
            # best_elements_coust = self.reply_method_TOP(self.function_objective, best_elements)

            best_count = 0
            best_always = np.copy( best_elements[0])
            best_coust = best_elements_coust[0]
            best_element_generation = list()
            for g in range(self.generation_size):

                print(g, best_coust, best_count)

                # calculo do custo
                cousts_population = [self.reply_method_TOP(self.function_objective, value) for value in population]
                '''ealizando a soma do custo de todos os crhomossomos'''
                cousts_population = [value.sum() for value in cousts_population]

                cousts_population = np.array(cousts_population)

                # selecionano os pais para cruzamento
                selected_parents_index = self.selection(self.population_size, cousts_population, 5)
                parents_select = [population[chromossome] for chromossome in selected_parents_index]

                # lista que terá a nova população
                new_population = list()

                for i in range(selected_parents_index.size):
                    #
                    select_2_parents = np.random.randint(selected_parents_index.size, size=2)

                    offspring_1,offspring_2 = self.crossover(parents_select[select_2_parents[0]],parents_select[select_2_parents[1]], function_objective=self.function_objective)

                    new_population.append(offspring_1)
                    new_population.append(offspring_2)

                # for i in range(len(new_population)):
                #     new_population[i] = self.reply_crossover_inner_agents(self.crossover_class.PMX, new_population[i])


                # gerando lista de probabilidades para os novos indivíduos sofrerem mutações
                rand = np.random.uniform(0,1, len(new_population))


                for i in range(len(new_population)):
                    new_population[i] = self.mutation_object.insert_remove_points_TOP(self.med_custo,
                                                                                       self.function_insert_remove,
                                                                                       self.all_elements,
                                                                                       new_population[i])



                # aqui não foi atualizado####################
                for i in range(rand.size):
                    if rand[i] >= self.mutation_rate:
                        list_mut = list()
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.swap,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.insertion,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.reverse,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.scramble,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.swap,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.WGWRGM,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.WGWWGM,new_population[i]))
                        list_mut.append(self.reply_method_mutation_TOP(self.mutation_object.WGWNNM,new_population[i]))

                        cousts_mut = np.zeros(len(list_mut))

                        cousts_mut[0] = sum(self.reply_method_TOP(self.med_custo,list_mut[0]))
                        cousts_mut[1] = sum(self.reply_method_TOP(self.med_custo,list_mut[1]))
                        cousts_mut[2] = sum(self.reply_method_TOP(self.med_custo,list_mut[2]))
                        cousts_mut[3] = sum(self.reply_method_TOP(self.med_custo,list_mut[3]))
                        cousts_mut[4] = sum(self.reply_method_TOP(self.med_custo,list_mut[4]))
                        cousts_mut[5] = sum(self.reply_method_TOP(self.med_custo,list_mut[5]))
                        cousts_mut[6] = sum(self.reply_method_TOP(self.med_custo,list_mut[6]))
                        cousts_mut[7] = sum(self.reply_method_TOP(self.med_custo,list_mut[7]))

                        min_mut = np.argmin(cousts_mut)
                        new_population[i] = list_mut[min_mut]
                new_population = new_population + population


                fitness_values = np.zeros(len(new_population))
                cousts_values = np.zeros(len(new_population))

                for i in range(fitness_values.size):
                    fitness_values[i] = self.reply_method_TOP(self.function_objective,new_population[i]).sum()
                    cousts_values[i] =  self.reply_method_TOP(self.med_custo,new_population[i]).sum()

                population_select = np.zeros(self.population_size)
                population = list()
                for i in range(self.population_size):
                    if len(new_population) == 0:
                        break
                    min_index = np.argmin(fitness_values)
                    if cousts_values[i] <= self.max_coust*self.number_agents:
                        population_select[i] = min_index

                        exist_menor = [best for best in range(4) if fitness_values[min_index] < best_elements_coust[best]]

                        crhomossome = new_population[min_index]
                        if len(exist_menor) > 0:
                            flag_possui = [np.array_equal(element, crhomossome) for element in best_elements]
                            if True not in flag_possui:
                                best_tmp = best_elements
                                best_tmp.append(crhomossome)

                                new_cousts = np.array([self.reply_method_TOP(self.function_objective, tmp).sum() for tmp in best_tmp])
                                indexes_tmp = np.argsort(new_cousts)

                                best_elements_coust = new_cousts[indexes_tmp[0:4]]
                                best_elements = [best_tmp[best_index] for best_index in indexes_tmp]

                        population.append(new_population[min_index])
                    del new_population[min_index]
                    fitness_values = np.delete(fitness_values,[min_index])

                # for i in range(len(population)):
                #     if np.unique(population[i]).size < population[i].size - 1:
                #         print('error')

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
        map_points = '../novas_cidades_4.txt',
        prizes = '../novos_premios_4.txt',
        # map_points = '../adilson_cidades.txt',
        # prizes = '../adilson_premios.txt',
        number_agents = 1,
        max_coust = 30,
        start_point = 21,
        end_point = 21,
        individual= 0)
    a , b = ga.run()

    for i in range(1):
        print('custo')
        for j in range(len(b[i])):
            print(ga.med_custo(b[i][j]))
        ga.plota_rotas_TOP(ga.mapa, b[i])

        x = np.isin(b[0][1:-2], b[1][1:-2])
        y = np.isin(b[0][1:-2], b[2][1:-2])
        z = np.isin(b[2][1:-2], b[1][1:-2])

        print(b[i])
        print('premios')
        for j in range(len(b[i])):
            print(ga.prizes.take(b[i][j]).sum())
        # print(a[i])

    input()