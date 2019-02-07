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

    def generate_population(self, population, inicial):
        for i in range(population):
            individual = np.copy(inicial)
            np.random.shuffle(individual)



            pass
        pass

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

        return distancias


    def mutation(self):
        pass

    def ga(self, size_generation, size_population, max_weight, towns_list, weight_list):

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

        inicial = np.random.permutation(size)
        primeiro_gene = inicial[0]
        inicial = np.delete([inicial], [0, 0])

        for g in range(population):

            pass

        pass
