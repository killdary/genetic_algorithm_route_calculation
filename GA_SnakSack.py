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



    '''metodo que gera uma populacao de rotas com os pesos selecionados'''
    def generate_population(self, number_population, inicial, max_weight, begin_deposite):
        '''
        metodo que gera uma população inicial para KSTSP

        :param number_population:
        :param inicial:
        :param max_weight:
        :return:
        '''

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

            flux_visited.insert(0, begin_deposite)
            flux_visited.append(begin_deposite)
            list_citys_flux.append(flux_visited)
            list_citys_flux_coust[i] = self.med_custo(flux_visited)

        return list_citys_flux, list_citys_flux_coust, list_citys_flux_value

    def crossover(self, best_individuals, worst_induviduasl, number_population):
        pass

    def mutation(self):
        pass

    def ga(self, size_generation, size_population, max_weight, towns_list, weight_list, begin_deposit):
        number_best_worst = 4

        mapa = np.loadtxt(towns_list)

        weights = np.loadtxt(weight_list)

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

            for i in range(number_best_worst):
                max_i = np.argmax(flux_visited_value)
                best_individuals.append(flux_visited[max_i])
                best_individuals_weight[i] = flux_visited_weight[max_i]
                best_individuals_value[i] = flux_visited_value[max_i]


                flux_visited.remove(max_i)
                flux_visited_weight = np.delete(flux_visited_weight, max_i)
                flux_visited_value = np.delete(flux_visited_value, max_i)

                min_i = np.argmin(flux_visited_value)
                worst_individuals.append(flux_visited[min_i])
                worst_individuals_weight[i] = flux_visited_weight[min_i]
                worst_individuals_value[i] = flux_visited_value[min_i]

                flux_visited.remove(min_i)
                flux_visited_weight = np.delete(flux_visited_weight, min_i)
                flux_visited_value = np.delete(flux_visited_value, min_i)


                pass

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

