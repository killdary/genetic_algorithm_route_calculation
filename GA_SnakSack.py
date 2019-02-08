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

    def correct_individual(self, number_citys_select):
        individual = np.copy(self.inicial_values)
        individual = np.delete(individual, number_citys_select)

        flux_visited = np.random.choice(individual, number_citys_select)
        individual = np.delete(self.inicial_values, flux_visited)

        flux_visited = self.removed_elements_repeat(flux_visited)

        while True:
            weight_individual = self.weights.take(flux_visited).sum()

            if weight_individual > self.max_weight:
                city_remove = np.random.randint(0, flux_visited.shape[0], 1)
                individual = np.append(individual, flux_visited[city_remove])
                flux_visited = np.delete(flux_visited, city_remove)

            else:
                break

        flux_value = self.prizes.take(flux_visited).sum()
        flux_visited = np.concatenate([self.begin_deposit, flux_visited, self.begin_deposit])
        flux_coust = self.med_custo(flux_visited)

        return flux_visited, flux_coust, flux_value

    @staticmethod
    def generate_points_mutation_crossover(size):
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

        return I, J


    '''metodo que gera uma populacao de rotas com os pesos selecionados'''
    def generate_population(self, number_population, inicial, max_weight, begin_deposite):
        '''
        metodo que gera uma população inicial para KSTSP

        :param number_population:
        :param inicial:
        :param max_weight:
        :return:
        '''

        begin_deposite = np.array([begin_deposite])

        # media de pesos das cidades
        mean_weight = self.weights.mean()

        size = inicial.shape[0]

        # estabelecendo um número mínimo de cidades que se aproxime do peso
        # maximo suportado pela mochila
        number_citys_select = int(round(size / mean_weight))

        # gerando uma matriz de zeros para cidades visitadas e pouplação
        # population = np.zeros([number_population, size])
        visited_citys = np.zeros([number_population, size+1])

        list_citys_flux = list()
        list_citys_flux_coust = np.zeros(number_population)
        list_citys_flux_value = np.zeros(number_population)

        for i in range(number_population):
            individual = np.copy(inicial)

            flux_visited = np.random.choice(individual, number_citys_select)
            individual = np.delete(inicial, flux_visited)

            flux_visited = self.removed_elements_repeat(flux_visited)

            while True:
                weight_individual = self.weights.take(flux_visited).sum()

                if weight_individual > max_weight:
                    city_remove = np.random.randint(0,flux_visited.shape[0],1)
                    individual = np.append(individual, flux_visited[city_remove])
                    flux_visited = np.delete(flux_visited, city_remove)

                else:
                    break

            np.put(visited_citys[1, :], flux_visited, 1)

            list_citys_flux_value[i] = self.prizes.take(flux_visited).sum()


            flux_visited = np.concatenate([begin_deposite,flux_visited,begin_deposite])
            list_citys_flux.append(flux_visited)
            list_citys_flux_coust[i] = self.med_custo(flux_visited)

        return list_citys_flux, list_citys_flux_coust, list_citys_flux_value

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

        for i in new_pop:
            all_individuals.append(np.copy(i))

        for i in best_individuals:
            all_individuals.append(np.copy(i))

        # elements = np.random.choice(np.arange(len(all_individuals), np.random.randint(size)))
        elements = np.random.choice(np.arange(len(all_individuals)), size)

        result = list()

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

            result.append(np.copy(individual))
        
        return result

    def ga(self, size_generation, size_population, max_weight, towns_list, weight_list, begin_deposit):
        number_best_worst = 4

        mapa = np.loadtxt(towns_list)

        weights = np.loadtxt(weight_list)

        self.max_weight = max_weight

        self.mapa = mapa

        self.weights = weights[:, 0]

        self.prizes = weights[:, 1]

        self.distance_values = self.distance_matrix_calculate(mapa)

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
        self.begin_deposit = begin_deposit

        flux_visited, flux_visited_weight, flux_visited_value = self.generate_population(population,
                                                                                         inicial,
                                                                                         max_weight,
                                                                                         begin_deposit)
        best_individuals = list()
        best_individuals_weight = np.zeros(number_best_worst)
        best_individuals_value = np.zeros(number_best_worst)

        worst_individuals = list()
        worst_individuals_weight = np.zeros(number_best_worst)
        worst_individuals_value = np.zeros(number_best_worst)

        for g in range(population):
            # seleção dos melhores e piores indivíduos
            for i in range(number_best_worst):
                # pegando os elementos com o maior valor de prêmio
                max_i = np.argmax(flux_visited_value)
                best_individuals.append(flux_visited[max_i])
                best_individuals_weight[i] = flux_visited_weight[max_i]
                best_individuals_value[i] = flux_visited_value[max_i]


                flux_visited.pop(max_i)
                flux_visited_weight = np.delete(flux_visited_weight, max_i)
                flux_visited_value = np.delete(flux_visited_value, max_i)

                # pegando os valores com os menores valores de prêmios
                min_i = np.argmin(flux_visited_value)
                worst_individuals.append(flux_visited[min_i])
                worst_individuals_weight[i] = flux_visited_weight[min_i]
                worst_individuals_value[i] = flux_visited_value[min_i]

                flux_visited.pop(min_i)
                flux_visited_weight = np.delete(flux_visited_weight, min_i)
                flux_visited_value = np.delete(flux_visited_value, min_i)


            pop = self.crossover(best_individuals, worst_individuals, begin_deposit)

            pop_mutation = self.mutation(pop, best_individuals, 20)

            pass

        pass

if __name__ == '__main__':
    x = GA_SnakSack()

    x.ga(size_generation=2500,
         size_population=50,
         max_weight=150,
         towns_list='./pontos.txt',
         weight_list='./prize_penalty.txt',
         begin_deposit=0)

