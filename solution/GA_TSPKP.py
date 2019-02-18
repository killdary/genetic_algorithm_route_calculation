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
        return self.med_custo(cromossome)

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

        cid_nome = range(len(pos_x))

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



    def __init__(self,
                genetarion,
                population,
                limit_population,
                crossover_rate,
                mutation_rate,
                map_points,
                prizes,
                max_coust,
                start_point,
                end_point):

        # as variáveis 
        self.genetarion_size = genetarion
        self.population_size = population
        self.limit_population = limit_population
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.map_points = map_points
        self.max_coust = max_coust
        self.start_point = np.array([start_point])
        self.end_point = np.array([end_point])

        self.mapa = np.loadtxt(map_points)

        self.prizes = np.loadtxt(prizes)

        self.distance_matrix_calculate()

        self.mutation_object = Mutation()

        self.mutation = self.mutation_object.scramble

        self.crossover_class = Crossover()
        self.crossover = self.crossover_class.PMX

        self.Population = Population(self.start_point, self.end_point, self.med_custo, max_coust)

        self.initial_cromossome = np.arange(self.mapa.shape[0])

        if start_point != end_point:
            self.initial_cromossome = np.delete(self.initial_cromossome, [start_point, end_point])
        else:
            self.initial_cromossome = np.delete(self.initial_cromossome, [start_point])


        self.Selection_object = Selection()
        self.selection = self.Selection_object.tournament

    def run(self):

        population = self.Population.initialize(self.initial_cromossome, self.population_size)
        best_elements = population[0:4]
        best_elements_coust = np.array([self.function_objective(element) for element in best_elements])

        best_count = 0
        best_always = np.copy( best_elements[0])
        best_coust = best_elements_coust[0]
        best_element_generation = list()
        for g in range(self.genetarion_size):

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


            for i in range(len(new_population)):
                if not np.unique(self.initial_cromossome).size == new_population[i].size - 2:
                    print('error')

            for i in range(rand.size):
                if rand[i] >= self.mutation_rate:
                    mut_1 = self.mutation_object.swap(new_population[i])
                    mut_2 = self.mutation_object.insertion(new_population[i])
                    mut_3 = self.mutation_object.WGWRGM(new_population[i], self.function_objective)
                    mut_4 = self.mutation_object.WGWWGM(new_population[i], self.function_objective)
                    mut_5 = self.mutation_object.WGWNNM(new_population[i], self.function_objective)

                    if not np.unique(self.initial_cromossome).size == mut_1.size - 2:
                        print('error')
                    if not np.unique(self.initial_cromossome).size == mut_2.size - 2:
                        print('error')
                    if not np.unique(self.initial_cromossome).size == mut_3.size - 2:
                        print('error')
                    if not np.unique(self.initial_cromossome).size == mut_4.size - 2:
                        print('error')

                    coust_mut_1 = self.function_objective(mut_1)
                    coust_mut_2 = self.function_objective(mut_2)
                    coust_mut_3 = self.function_objective(mut_3)
                    coust_mut_4 = self.function_objective(mut_4)
                    coust_mut_5 = self.function_objective(mut_5)

                    if coust_mut_1 > coust_mut_2 and coust_mut_1 > coust_mut_3  and coust_mut_1 >  coust_mut_4 and coust_mut_1 >  coust_mut_5:
                        new_population[i] = mut_1
                    elif coust_mut_2 >  coust_mut_3 and coust_mut_2 > coust_mut_4 and coust_mut_2 > coust_mut_5:
                        new_population[i] = mut_2
                    elif coust_mut_3 >  coust_mut_4:
                        new_population[i] = mut_3
                    else:
                        new_population[i] = mut_4


            for i in range(len(new_population)):
                if not np.unique(self.initial_cromossome).size == new_population[i].size - 2:
                    print('error')

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

        print(best_element_generation)
        return best_elements_coust, best_elements





if __name__ == '__main__':
    ga = GA_TSPKP(
        genetarion = 1000,
        population = 300,
        limit_population = 100,
        crossover_rate = 100,
        mutation_rate = 0.8,
        map_points = '../novas_cidades_2.txt',
        prizes = '../novos_premios_2.txt',
        max_coust = 0,
        start_point = 0,
        end_point = 0)
    a , b = ga.run()

    for i in range(4):
        ga.plota_rotas(ga.mapa, b[i])
        print(a[i])

    input()