#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 06 21:21:37 2019
@author: killdary
@version: 0.0.2
Backlog - product


tarefas a serem realixadas:
    criar funcao calculo de peso para se aproximar do limite da mochila
    criar funcao de cruzamento
    criar funcao de mutacao
    criar funcao de geracao de populacao
    
"""

import numpy as np
import matplotlib.pyplot as plt

class GA_SnakSack:



    def distance_matrix_calculate(self, mapa):
        """
        Method that calculate the distance matrix
        :param cidades: points or towns informed
        :return: numpy.matrix
        """
        qtd = mapa.shape[0]
        distancias = np.zeros([qtd, qtd])

        _temp_max = 0

        for i in range(qtd):
            for j in range(i, qtd):
                if i != j:
                    b = mapa[i, 0] - mapa[j, 0]
                    c = mapa[i, 1] - mapa[j, 1]
                    a = np.sqrt(np.square(b) + np.square(c))

                    distancias[i, j] = a
                    distancias[j, i] = a

                    if _temp_max < a:
                        _temp_max = a

        self.distancias = distancias


    '''metodo que mede o custo de uma rota em distancia'''
    def med_custo(self, citys):
        dist_total = 0
        rota = citys.astype(int)

        cidade_atual = -1
        for cidade in rota:
            if cidade_atual >= 0:
                dist_total += self.distancias[cidade_atual, cidade]
            cidade_atual = cidade

        return dist_total


    '''funcao para remover valores repetidos da ordem da cidade'''
    @staticmethod
    def removed_elements_repeat(array_citys):
        citys_position = np.unique(array_citys, return_index=True)[1]
        citys_position.sort()
        new_citys = array_citys.take(citys_position)

        return new_citys

    def correct_individual(self, flux_visited):
        #
        # if(flux_visited[0] == self.begin_deposit[0]):
        #     flux_visited = np.delete(flux_visited, 0)
        #
        # if(flux_visited[-1] == self.begin_deposit[0]):
        #     flux_visited = np.delete(flux_visited, -1)

        # talvez desnecessário
        flux_visited = np.copy(self.removed_elements_repeat(flux_visited))

        if(flux_visited[0] == self.begin_deposit[0]):
            flux_visited = np.delete(flux_visited, 0)

        individual = np.concatenate([self.begin_deposit, self.inicial_values])
        individual = np.delete(individual, flux_visited)
        individual = np.delete(individual, [0])

        count = 0
        while True:
            # weight_individual = self.weights.take(flux_visited).sum()
            coust_individual = self.med_custo(flux_visited)

            if coust_individual > self.max_coust:
                city_remove = np.random.randint(0, flux_visited.shape[0], 1)
                individual = np.append(individual, flux_visited[city_remove])
                flux_visited = np.delete(flux_visited, city_remove)
                count += 1

            elif count > 1 or individual.size ==0:
                break
            else:
                city_add = np.random.randint(0, individual.shape[0], 1)
                teste = individual[city_add]
                flux_visited = np.append(flux_visited, teste)
                individual = np.delete(individual, city_add)


        flux_value = self.prizes.take(flux_visited).sum()
        flux_visited = np.concatenate([self.begin_deposit, flux_visited, self.begin_deposit])
        flux_coust = self.med_custo(flux_visited)
        flux_weight = self.weights.take(flux_visited).sum()
        flux_function_value = flux_coust

        return flux_visited, flux_value, flux_coust, flux_weight, flux_function_value

    @staticmethod
    def generate_points_mutation_crossover(size):
        if size != 2:
            # inicializando as variaveis responsáveis pelos pontos de cruzamento
            route_insert_points = np.zeros(2)

            while route_insert_points[0] == route_insert_points[1]:
                route_insert_points = np.random.randint(size - 1, size=2)

            # Um pequeno tratamento para que os Elementos I e J nao sejam próximos
            # pois caso sejam próximos poderão gerar indivíduos identicos
            I = route_insert_points.min()
            J = route_insert_points.max()

            if I + 1 == J:
                if J == size - 2:
                    I = I - 1
                else:
                    J = J + 1
        else:
            I, J = 0 , 1

        return I, J

    '''metodo que gera uma populacao de rotas com os pesos selecionados'''
    def generate_population(self, number_population):
        '''
        metodo que gera uma população inicial para KSTSP

        :param number_population:
        :param inicial:
        :param max_weight:
        :return:
        '''

        begin_deposite = np.array([self.begin_deposit])

        # media de pesos das cidades
        mean_weight = self.weights.mean()

        mean_coust = self.distancias.mean()

        size = self.inicial_values.shape[0]

        # estabelecendo um número mínimo de cidades que se aproxime do peso
        # maximo suportado pela mochila
        # number_citys_select = int(round(self.max_weight / mean_weight))
        number_citys_select = int(round(self.max_coust / mean_coust))

        # gerando uma matriz de zeros para cidades visitadas e pouplação
        # population = np.zeros([number_population, size])
        visited_citys = np.zeros([number_population, size+1])

        list_citys_flux = list()
        list_citys_flux_coust = np.zeros(number_population)
        list_citys_flux_value = np.zeros(number_population)
        list_citys_flux_weigth = np.zeros(number_population)
        list_citys_flux_function_value = np.zeros(number_population)

        for i in range(number_population):
            individual = np.copy(self.inicial_values)

            flux_visited = np.random.choice(individual, number_citys_select)
            flux_visited = self.removed_elements_repeat(flux_visited)

            flux_visited, \
            temp_value, \
            temp_coust, \
            temp_weight, \
            temp_function_value = self.correct_individual(flux_visited)

            # individual = np.delete(inicial, flux_visited)
            # while True:
            #     weight_individual = self.weights.take(flux_visited).sum()
            #
            #     if weight_individual > max_weight:
            #         city_remove = np.random.randint(0,flux_visited.shape[0],1)
            #         individual = np.append(individual, flux_visited[city_remove])
            #         flux_visited = np.delete(flux_visited, city_remove)
            #
            #     else:
            #         break
            #
            # np.put(visited_citys[1, :], flux_visited, 1)

            list_citys_flux_value[i] = temp_value
            # flux_visited = np.concatenate([begin_deposite,flux_visited,begin_deposite])
            list_citys_flux.append(flux_visited)
            list_citys_flux_coust[i] = temp_coust
            list_citys_flux_weigth[i] = temp_weight
            list_citys_flux_function_value[i] = temp_function_value

        return list_citys_flux, \
               list_citys_flux_coust, \
               list_citys_flux_value, \
               list_citys_flux_weigth, \
               list_citys_flux_function_value

    '''
    Metodo para realizar o cruzamento entre os melhores individuos e um elemento aleatório dos piores individuos
    da população
    '''
    def crossover(self, best_individuals, worst_induviduasl, deposit):

        # deposit = np.array([deposit])

        # como os fluxos terão tamanhos variados sera pego maior valor entre os melhores e o piores para gerar a mutação
        max_size_best = np.amin(np.array([i.shape[0] for i in best_individuals]))
        max_size_worst = np.amin(np.array([i.shape[0] for i in worst_induviduasl]))

        size = max_size_best if max_size_best < max_size_worst else max_size_worst

        # inicializando as variaveis responsáveis pelos pontos de cruzamento
        route_insert_points = np.zeros(2)

        while route_insert_points[0] == route_insert_points[1]:
            route_insert_points = np.random.randint(size - 1, size=2)

        # Um pequeno tratamento para que os Elementos I e J nao sejam próximos
        # pois caso sejam próximos poderão gerar indivíduos identicos
        I = route_insert_points.min()
        J = route_insert_points.max()


        if I + 1 == J:
            if J == size - 2:
                I = I - 1
            else:
                J = J + 1

        result = list()

        # removendo o primeiro deposito das rotas, que esta no inicio e no fim
        best_individuals = [np.delete(element, [0, element.size-1]) for element in best_individuals]
        worst_induviduasl = [np.delete(element, [0, element.size-1]) for element in worst_induviduasl]

        for i in range(len(best_individuals)):
            individual = np.copy(best_individuals[i])
            individuals_rest = [np.copy(element) for element in best_individuals]
            individuals_rest.pop(i)

            element = np.random.randint(len(individuals_rest), size=1)[0]
            individual_cross = np.copy(individuals_rest[element])

            element_worst = np.random.randint(len(worst_induviduasl), size=1)[0]
            individual_worst = np.copy(worst_induviduasl[element_worst])

            # crossover one point
            kid_cross_1 = np.concatenate((individual[:J], individual_cross[J:]))
            kid_cross_1 = self.removed_elements_repeat(kid_cross_1)
            kid_cross_2 = np.concatenate((individual_cross[:J], individual[J:]))
            kid_cross_2 = self.removed_elements_repeat(kid_cross_2)

            # crossover two poitns
            kid_cross_3 = np.concatenate((individual_cross[:I], individual[I:J], individual_cross[J:]))
            kid_cross_3 = self.removed_elements_repeat(kid_cross_3)
            kid_cross_4 = np.concatenate((individual[:I], individual_cross[I:J], individual[J:]))
            kid_cross_4 = self.removed_elements_repeat(kid_cross_4)

            # partial sinusoidal crossover
            size_sinoidal = individual.size if individual.size < individual_cross.size else individual_cross.size

            kid_cross_5 = np.copy(individual)
            kid_cross_5[:size_sinoidal:2] = individual_cross[:size_sinoidal:2]
            kid_cross_5 = self.removed_elements_repeat(kid_cross_5)

            kid_cross_6 = np.copy(individual_cross)
            kid_cross_6[:size_sinoidal:2] = individual[:size_sinoidal:2]
            kid_cross_6 = self.removed_elements_repeat(kid_cross_6)

            # partial sinusoidal crossorver worst individual
            size_sinoidal = individual.size if individual.size < individual_worst.size else individual_worst.size

            kid_cross_7 = np.copy(individual)
            kid_cross_7[:size_sinoidal:2] = individual_worst[:size_sinoidal:2]
            kid_cross_7 = self.removed_elements_repeat(kid_cross_7)

            kid_cross_8 = np.copy(individual_worst)
            kid_cross_8[:size_sinoidal:2] = individual[:size_sinoidal:2]
            kid_cross_8 = self.removed_elements_repeat(kid_cross_8)

            result.append(kid_cross_1)
            result.append(kid_cross_2)
            result.append(kid_cross_3)
            result.append(kid_cross_4)
            result.append(kid_cross_5)
            result.append(kid_cross_6)
            result.append(kid_cross_7)
            result.append(kid_cross_8)

        return result


        # # a = [1, 2, 3, 1, 1, 3, 4, 3, 2]
        # # index_sets = [np.argwhere(i == a) for i in np.unique(a)]
        # pass

    def mutation(self, new_pop, best_individuals, size):
        all_individuals = list()
        #
        # for i in new_pop:
        #     x = np.delete(i,[0, -1])
        #     all_individuals.append(np.copy(x))

        result = list()

        for i in best_individuals:
            x = np.delete(i,[0, -1])
            all_individuals.append(np.copy(x))

            list_elements = np.repeat([x], 4, axis=0)

            I, J = self.generate_points_mutation_crossover(x.size)

            # Swap Mutation
            list_elements[0, I], list_elements[0,J] = list_elements[0,J], list_elements[0,I]

            # Reverse Mutation
            list_elements[1,I:J] = list_elements[1,J:I:-1]

            # Scramble Mutation
            np.random.shuffle(list_elements[2,I:J])

            # Insertion Mutation
            list_elements[3,I:J] = np.roll(list_elements[3,I:J], 1)



            result.append(np.concatenate([self.begin_deposit,list_elements[0], self.begin_deposit]))
            result.append(np.concatenate([self.begin_deposit,list_elements[1], self.begin_deposit]))
            result.append(np.concatenate([self.begin_deposit,list_elements[2], self.begin_deposit]))
            result.append(np.concatenate([self.begin_deposit,list_elements[3], self.begin_deposit]))





        # elements = np.random.choice(np.arange(len(all_individuals), np.random.randint(size)))
        elements = np.random.choice(np.arange(len(all_individuals)), (size - 16))


        for j in range(elements.size):
            i=np.copy(elements[j])
            individual = np.copy(all_individuals[i])
            mutation = np.random.randint(4, size=1)[0]

            I, J = self.generate_points_mutation_crossover(individual.size)

            # Swap Mutation
            if(mutation == 0):
                individual[I], individual[J] = individual[J], individual[I]

            # Reverse Mutation
            elif(mutation == 1):
                individual[I:J] = individual[J:I:-1]

            # Scramble Mutation
            elif(mutation == 2):
                np.random.shuffle(individual[I:J])

            # Insertion Mutation
            elif(mutation == 3):
                individual[I:J] = np.roll(individual[I:J], 1)



            result.append(np.concatenate([self.begin_deposit,np.copy(individual), self.begin_deposit]))

        return result


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
        plt.scatter(all_x, all_y, s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(txt, (all_x[i], all_y[i]), fontsize=font_size)

        plt.title('Mapa GA')
        plt.show()

    def function_objective(self,
                           number_best_worst,
                           best_individuals,
                           best_individuals_coust,
                           best_individuals_value,
                           best_individuals_weight,
                           best_individuals_function_value,
                           worst_individuals,
                           worst_individuals_coust,
                           worst_individuals_value,
                           worst_individuals_weight,
                           worst_individuals_function_value,
                           flux_visited,
                           flux_visited_coust,
                           flux_visited_value,
                           flux_visited_weight,
                           flux_visited_function_value):

        for i in range(number_best_worst):
            # pegando os elementos com o maior valor de prêmio
            max_i = np.argmax(flux_visited_function_value)

            if best_individuals_function_value[i] < flux_visited_function_value[max_i]:
                teste_flag = [np.array_equal(element, flux_visited[max_i]) for element in best_individuals]
                if True not in teste_flag:
                    best_individuals[i] = flux_visited[max_i]
                    best_individuals_coust[i] = flux_visited_coust[max_i]
                    best_individuals_value[i] = flux_visited_value[max_i]
                    best_individuals_weight[i] = flux_visited_weight[max_i]
                    best_individuals_function_value[i] = flux_visited_function_value[max_i]

                flux_visited.pop(max_i)
                flux_visited_coust = np.delete(flux_visited_coust, max_i)
                flux_visited_weight = np.delete(flux_visited_weight, max_i)
                flux_visited_value = np.delete(flux_visited_value, max_i)
                flux_visited_function_value = np.delete(flux_visited_function_value, max_i)

            # pegando os valores com os menores valores de prêmios
            min_i = np.argmin(flux_visited_function_value)

            if worst_individuals_function_value[i] == 0 or worst_individuals_function_value[i] > \
                    flux_visited_function_value[min_i]:

                teste_flag = [np.array_equal(element, flux_visited[max_i]) for element in worst_individuals]
                if True not in teste_flag:
                    worst_individuals[i] = flux_visited[min_i]
                    worst_individuals_coust[i] = flux_visited_coust[min_i]
                    worst_individuals_weight[i] = flux_visited_weight[min_i]
                    worst_individuals_value[i] = flux_visited_value[min_i]
                    worst_individuals_function_value[i] = flux_visited_function_value[min_i]

                flux_visited.pop(min_i)
                flux_visited_coust = np.delete(flux_visited_coust, min_i)
                flux_visited_weight = np.delete(flux_visited_weight, min_i)
                flux_visited_value = np.delete(flux_visited_value, min_i)
                flux_visited_function_value = np.delete(flux_visited_function_value, min_i)



        # for i in range(number_best_worst):
        #     x = np.copy(best_individuals[i])
        #     x_coust = self.med_custo(x)
        #     for j in range(1, x.size-1):
        #         x_copy = np.copy(x)
        #         x_copy[j-1], x_copy[j] =  x_copy[j],x_copy[j-1]
        #         x_copy_coust = self.med_custo(x_copy)
        #         if x_copy_coust < x_coust:
        #             x = np.copy(x_copy)
        #             x_coust = x_copy_coust
        #
        #     best_individuals[i] = np.copy(x)
        #     best_individuals_value[i] = self.prizes.take(x[1:-1]).sum()
        #     best_individuals_coust[i] = x_coust
        #     best_individuals_weight[i] = self.weights.take(x[1:-1]).sum()
        #     best_individuals_function_value[i] = (2*best_individuals_value[i]) - (best_individuals_coust[i]*3) - best_individuals_weight[i]


        return best_individuals,\
               best_individuals_coust,\
               best_individuals_value,\
               best_individuals_weight,\
               best_individuals_function_value,\
               worst_individuals,\
               worst_individuals_coust,\
               worst_individuals_value,\
               worst_individuals_weight,\
               worst_individuals_function_value

    def ga(self, size_generation, size_population, max_weight, max_coust, towns_list, weight_list, begin_deposit):
        number_best_worst = 4

        mapa = np.loadtxt(towns_list)

        weights = np.loadtxt(weight_list)

        self.max_weight = max_weight

        self.max_coust = max_coust

        self.mapa = mapa

        self.weights = weights[:, 0]

        x = self.weights.sum()

        self.prizes = weights[:, 1]

        self.distance_matrix_calculate(mapa)

        self.distance_values = self.distancias

        generation = size_generation
        population = size_population

        size = mapa.shape[0]
        self.size = size
        new_pop = np.zeros((population, size + 1))
        new_pop_visited = np.zeros((population, size + 1))

        inicial = np.arange(size)
        primeiro_gene = inicial[begin_deposit]
        inicial = np.delete([inicial], begin_deposit)

        self.inicial_values = inicial
        self.begin_deposit = np.array([begin_deposit])

        flux_visited, \
        flux_visited_coust, \
        flux_visited_value, \
        flux_visited_weight, \
        flux_visited_function_value = \
            self.generate_population(population)

        best_individuals_weight = np.copy(flux_visited_weight[0:number_best_worst])
        best_individuals_coust = np.copy(flux_visited_coust[0:number_best_worst])
        best_individuals_value = np.copy(flux_visited_value[0:number_best_worst])
        best_individuals_function_value = np.copy(flux_visited_function_value[0:number_best_worst])

        worst_individuals_weight = np.copy(flux_visited_weight[0:number_best_worst])
        worst_individuals_coust = np.copy(flux_visited_coust[0:number_best_worst])
        worst_individuals_value = np.copy(flux_visited_value[0:number_best_worst])
        worst_individuals_function_value = np.copy(flux_visited_function_value[0:number_best_worst])

        best_individuals = flux_visited[0:number_best_worst]
        worst_individuals = flux_visited[0:number_best_worst]

        best_value_ever = flux_visited_function_value[np.argmin(flux_visited_function_value)]
        count = 0
        for g in range(generation):

            if best_individuals_function_value[0] == best_value_ever:
                count += 1
            elif best_individuals_function_value[0] > best_value_ever:
                best_value_ever = best_individuals_function_value[0]
                count = 0

            if count == 400:
                break

            if g % 50 == 0 and g!= 0:
                self.plota_rotas(self.mapa, best_individuals[0])
                print(best_individuals_value[0])
                print(count)

            if g % 10 == 0:
                print(g)

            # seleção dos melhores e piores indivíduos

            best_individuals, \
            best_individuals_coust, \
            best_individuals_value, \
            best_individuals_weight, \
            best_individuals_function_value, \
            worst_individuals, \
            worst_individuals_coust, \
            worst_individuals_value, \
            worst_individuals_weight, \
            worst_individuals_function_value = self.function_objective(number_best_worst,
                                                                       best_individuals,
                                                                       best_individuals_coust,
                                                                       best_individuals_value,
                                                                       best_individuals_weight,
                                                                       best_individuals_function_value,
                                                                       worst_individuals,
                                                                       worst_individuals_coust,
                                                                       worst_individuals_value,
                                                                       worst_individuals_weight,
                                                                       worst_individuals_function_value,
                                                                       flux_visited,
                                                                       flux_visited_coust,
                                                                       flux_visited_value,
                                                                       flux_visited_weight,
                                                                       flux_visited_function_value)



            # for i in range(number_best_worst):
            #     # pegando os elementos com o maior valor de prêmio
            #     max_i = np.argmax(flux_visited_function_value)
            #
            #     if best_individuals_function_value[i] < flux_visited_function_value[max_i]:
            #         teste_flag = [np.array_equal(element, flux_visited[max_i]) for element in best_individuals]
            #         if True not in teste_flag:
            #             #     print('tem')
            #             # if not np.array_equal(best_individuals[i], flux_visited[max_i]):
            #             best_individuals[i] = flux_visited[max_i]
            #             best_individuals_coust[i] = flux_visited_coust[max_i]
            #             best_individuals_value[i] = flux_visited_value[max_i]
            #             best_individuals_weight[i] = flux_visited_weight[max_i]
            #             best_individuals_function_value[i] = flux_visited_function_value[max_i]
            #
            #         flux_visited.pop(max_i)
            #         flux_visited_coust = np.delete(flux_visited_coust, max_i)
            #         flux_visited_weight = np.delete(flux_visited_weight, max_i)
            #         flux_visited_value = np.delete(flux_visited_value, max_i)
            #         flux_visited_function_value = np.delete(flux_visited_function_value, max_i)
            #
            #     # pegando os valores com os menores valores de prêmios
            #     min_i = np.argmin(flux_visited_function_value)
            #
            #     if worst_individuals_function_value[i] == 0 or worst_individuals_function_value[i] > flux_visited_function_value[min_i]:
            #
            #         teste_flag = [np.array_equal(element, flux_visited[min_i]) for element in worst_individuals]
            #         if True not in teste_flag:
            #             # if not np.array_equal(worst_individuals[i], flux_visited[min_i]):
            #             worst_individuals[i] = flux_visited[min_i]
            #             worst_individuals_coust[i] = flux_visited_coust[min_i]
            #             worst_individuals_weight[i] = flux_visited_weight[min_i]
            #             worst_individuals_value[i] = flux_visited_value[min_i]
            #             worst_individuals_function_value[i] = flux_visited_function_value[min_i]
            #
            #         flux_visited.pop(min_i)
            #         flux_visited_coust = np.delete(flux_visited_coust, min_i)
            #         flux_visited_weight = np.delete(flux_visited_weight, min_i)
            #         flux_visited_value = np.delete(flux_visited_value, min_i)
            #         flux_visited_function_value = np.delete(flux_visited_function_value, min_i)


            pop = self.crossover(best_individuals, worst_individuals, begin_deposit)
            x=len(pop)
            pop = best_individuals + pop
            x=len(pop)

            pop_mutation = self.mutation(pop, best_individuals, x)

            rest_pop , x1, x2, x3, x4 = self.generate_population(population - (2*x))

            new_pop = pop + pop_mutation + rest_pop
            x = len(new_pop)

            flux_visited = list()
            flux_visited_value = np.zeros(population)
            flux_visited_weight = np.zeros(population)
            flux_visited_coust = np.zeros(population)
            flux_visited_function_value = np.zeros(population)
            for i in range(len(new_pop)):
                flux, flux_value, flux_coust, flux_weight, flux_function_value = self.correct_individual(new_pop[i])
                flux_visited.append(flux)
                flux_visited_value[i] = flux_value
                flux_visited_coust[i] = flux_coust
                flux_visited_weight[i] = flux_weight
                flux_visited_function_value[i] = flux_function_value

        best_individuals, \
        best_individuals_coust, \
        best_individuals_value, \
        best_individuals_weight, \
        best_individuals_function_value, \
        worst_individuals, \
        worst_individuals_coust, \
        worst_individuals_value, \
        worst_individuals_weight, \
        worst_individuals_function_value = self.function_objective(number_best_worst,
                                                                   best_individuals,
                                                                   best_individuals_coust,
                                                                   best_individuals_value,
                                                                   best_individuals_weight,
                                                                   best_individuals_function_value,
                                                                   worst_individuals,
                                                                   worst_individuals_coust,
                                                                   worst_individuals_value,
                                                                   worst_individuals_weight,
                                                                   worst_individuals_function_value,
                                                                   flux_visited,
                                                                   flux_visited_coust,
                                                                   flux_visited_value,
                                                                   flux_visited_weight,
                                                                   flux_visited_function_value)

        return best_individuals, best_individuals_value, best_individuals_coust, best_individuals_weight, best_individuals_function_value

if __name__ == '__main__':
    x = GA_SnakSack()

    a,b,c,d,e = x.ga(size_generation=2000,
         size_population=800,
         max_weight=100,
         max_coust=50,
         towns_list='./pontos.txt',
         weight_list='./prize_penalty.txt',
         begin_deposit=0)

    for i in range(len(a)):
        x.plota_rotas(x.mapa, a[i])
        print (b[i],c[i],d[i],e[i])

