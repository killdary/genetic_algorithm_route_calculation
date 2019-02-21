import numpy as np
import matplotlib.pyplot as plt
from Mutation import Mutation
from Crossover import Crossover
from Population import Population
from Selection import Selection


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

    def med_custo(self, flux):
        dist_total = 0
        rota = flux.astype(int)

        cidade_atual = -1
        for cidade in rota:
            if cidade_atual >= 0:
                dist_total += self.distancias[cidade_atual, cidade]
            cidade_atual = cidade

        return dist_total

    def function_objective(self, cromossome):
        coust = self.med_custo(cromossome)
        prizes = self.prizes.take(cromossome).sum()
        return (self.prizes_rate * prizes) - (self.coust_rate * coust)

    '''funcao para remover valores repetidos da ordem da cidade'''
    @staticmethod
    def removed_citys_repeat(flux):
        citys_position = np.unique(flux, return_index=True)[1]
        citys_position.sort()
        new_citys = flux.take(citys_position)

        return new_citys

    # def correct_individual(self, flux):
    #     flux_wrong = np.delete(flux, [0, -1])
    #
    #     flux_wrong = np.copy(self.removed_citys_repeat(flux_wrong))
    #
    #     city_s
    #
    #
    #     while True:
    #         coust_flux_wrong = self.mede_custo(np.concatenate([self.start_point, flux_wrong, self.end_point]))
    #
    #         if coust_flux_wrong > self.max_coust:
    #             city_remove = np.random.randint(flux_wrong.size, 1)


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

        cid_nome = range(len(all_x))

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=40,
                   facecolor='w',
                   edgecolor='k')

        plt.plot(pos_x, pos_y, 'C3', lw=3)
        plt.scatter(self.mapa[:, 0], self.mapa[:, 1], s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(txt, (all_x[i], all_y[i]), fontsize=font_size)

        plt.title('Mapa GA')
        plt.show()



    # def __init__(self,
    #             genetarion,
    #             population,
    #             limit_population,
    #             crossover_rate,
    #             mutation_rate,
    #             map_points,
    #             prizes,
    #             max_coust,
    #             start_point,
    #             end_point):

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

        # as variáveis
        # self.generation_size = genetarion
        # self.population_size = population
        # self.limit_population = limit_population
        # self.crossover_rate = crossover_rate
        # self.mutation_rate = mutation_rate
        # self.map_points = map_points
        # self.max_coust = max_coust
        # self.start_point = np.array([start_point])
        # self.end_point = np.array([end_point])
        # self.prizes = np.loadtxt(prizes)

        self.mapa = np.loadtxt(self.map_points)
        self.distance_matrix_calculate()

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
            population = self.Population.initialize(self.initial_cromossome, self.population_size)
            best_elements = population[0:4]
            best_elements_coust = np.array([self.function_objective(element) for element in best_elements])

            best_count = 0
            best_always = np.copy( best_elements[0])
            best_coust = best_elements_coust[0]
            best_element_generation = list()
            for g in range(self.generation_size):

                print(g, best_coust, best_count)

                cousts_population = [self.function_objective(value) for value in population]
                cousts_population = np.array(cousts_population)

                selected_parents_index = self.selection(self.population_size, cousts_population, 5)

                parents_select = [population[chromossome] for chromossome in selected_parents_index]

                new_population = list()

                for i in range(selected_parents_index.size):
                    select_2_parents = np.random.randint(selected_parents_index.size, size=2)

                    offspring_1,offspring_2 = self.crossover(parents_select[select_2_parents[0]],parents_select[select_2_parents[1]])

                    new_population.append(offspring_1)
                    new_population.append(offspring_2)

                rand = np.random.uniform(0,1, len(new_population))

                for i in range(rand.size):
                    if rand[i] >= self.mutation_rate:
                        if new_population[i].size > 3:
                            list_mut = list()
                            list_mut.append(self.mutation_object.swap(new_population[i]))
                            list_mut.append(self.mutation_object.insertion(new_population[i]))
                            list_mut.append(self.mutation_object.reverse(new_population[i]))
                            list_mut.append(self.mutation_object.scramble(new_population[i]))
                            list_mut.append(self.mutation_object.swap(new_population[i]))
                            list_mut.append(self.mutation_object.WGWRGM(new_population[i], self.function_objective))
                            list_mut.append(self.mutation_object.WGWWGM(new_population[i], self.function_objective))
                            list_mut.append(self.mutation_object.WGWNNM(new_population[i], self.function_objective))

                            cousts_mut = np.zeros(8)

                            cousts_mut[0] = self.function_objective(list_mut[0])
                            cousts_mut[1] = self.function_objective(list_mut[1])
                            cousts_mut[2] = self.function_objective(list_mut[2])
                            cousts_mut[3] = self.function_objective(list_mut[3])
                            cousts_mut[4] = self.function_objective(list_mut[4])
                            cousts_mut[5] = self.function_objective(list_mut[5])
                            cousts_mut[6] = self.function_objective(list_mut[6])
                            cousts_mut[7] = self.function_objective(list_mut[7])
                            min_mut = np.argmin(cousts_mut)
                            new_population[i] = list_mut[min_mut]

                new_population = new_population + population

                fitness_values = np.zeros(len(new_population))

                for i in range(fitness_values.size):
                    fitness_values[i] = self.function_objective(new_population[i])

                population_select = np.zeros(self.population_size)
                population = list()
                for i in range(self.population_size):
                    min_index = np.argmin(fitness_values)
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

        if self.max_coust > 0:
            new_population = list()
            for i in range(10):
                cousts_mut = np.zeros(2)
                list_mut = list()
                list_mut.append(self.mutation_object.remove_random(self.best_route, self.function_objective))
                list_mut.append(self.mutation_object.remove_pior_premio(self.best_route, self.function_objective))
                cousts_mut[0] = self.function_objective(list_mut[0])
                cousts_mut[1] = self.function_objective(list_mut[1])

                index_min = np.argmin(cousts_mut)
                new_population.append(list_mut[index_min])


        print(best_element_generation)
        return best_elements_coust, new_population





if __name__ == '__main__':
    ga = GA_TSPKP(
        genetarion = 10,
        population = 50,
        limit_population = 75,
        crossover_rate = 100,
        mutation_rate = 0.8,
        coust_rate = 3,
        prizes_rate = 2,
        map_points = '../novas_cidades.txt',
        prizes = '../novos_premios.txt',
        max_coust = 15,
        start_point = 0,
        end_point = 0,
        individual= 0)
    a , b = ga.run()

    for i in range(10):
        ga.plota_rotas(ga.mapa, b[i])
        print(a[i])

    input()