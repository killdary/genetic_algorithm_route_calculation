#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:21:37 2018
@author: killdary
@version: 0.0.2
"""

import numpy as np

import matplotlib.pyplot as plt


class CalulateRoutesTSP:

    """
    Desenvolvimento do TSTSP para 'Prize Collect(PC)'
    methods -
        calculo do premio e selecao de cidades
        calculo penalidade
        calculo funcao objetivo
    """


    @staticmethod
    def plota_rotas(cidades, rota, size=8, font_size=20):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """
        pos_x = cidades[rota.astype(int), 0]
        pos_y = cidades[rota.astype(int), 1]

        cid_nome = range(len(pos_x))

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=40,
                   facecolor='w',
                   edgecolor='k')

        plt.plot(pos_x, pos_y, 'C3', lw=3)
        plt.scatter(pos_x, pos_y, s=120, marker="s")

        for i, txt in enumerate(cid_nome):
            plt.annotate(txt, (pos_x[i], pos_y[i]), fontsize=font_size)

        plt.title('Mapa GA')

    @staticmethod
    def _mede_custo(distancias, rota):
        """
        Method that calculates the distance of the points of the route from the distance matrix
        :param distancias: distance matrix
        :param rota:
        :return: cost of the route
        """
        dist_total = 0
        rota = rota.astype(int)

        cidade_atual = -1
        for cidade in rota:
            if cidade_atual >= 0:
                dist_total += distancias[cidade_atual, cidade]
            cidade_atual = cidade

        return dist_total

    @staticmethod
    def _matriz_distancia(cidades):
        """
        Method that calculate the distance matrix
        :param cidades: points or towns informed
        :return: numpy.matrix
        """
        qtd = cidades.shape[0]
        distancias = np.zeros([qtd, qtd])

        _temp_max = 0

        for i in range(qtd):
            for j in range(i, qtd):
                if i != j:
                    b = cidades[i, 0] - cidades[j, 0]
                    c = cidades[i, 1] - cidades[j, 1]
                    a = np.sqrt(np.square(b) + np.square(c))

                    distancias[i, j] = a
                    distancias[j, i] = a

                    if _temp_max < a:
                        _temp_max = a

        return distancias

    def min_rotas(self, distancias, new_pop, num):
        """
        :param distancias:
        :param new_pop:
        :param num:
        """
        rotas = np.array()
        min_pop = np.array()
        id_pop = np.array()

        for i, indiv in enumerate(new_pop):
            rotas = np.append(rotas, self._mede_custo(distancias, indiv))

        for i in range(num):
            min_pop = np.append(min_pop, rotas.min())
            id_min = rotas.argmin()
            id_pop = np.append(id_pop, id_min)

        for i, indiv in enumerate(new_pop):
            rotas = np.append(rotas, self._mede_custo(distancias, indiv))
            if len(min_pop) < num:
                min_pop = np.append(min_pop, ind)
                id_pop = np.id_pop(min_pop, i)
            else:
                for j in min_pop:
                    min_pop = np.append(min_pop, ind)
                    id_pop = np.id_pop(min_pop, i)

    @staticmethod
    def _generate_population(size_population, ancestral, first_gene):
        new_pop = np.zeros((size_population, ancestral.shape[0] + 2))

        for i in range(size_population):
            ind = np.copy(ancestral)
            np.random.shuffle(ind)

            new_pop[i] = np.concatenate([[first_gene], ind, [first_gene]])

        return new_pop

    def ga(self, generation, population, towns):
        """
        Calculation of the best route using Genetic Algorithm
        :param generation: number of the generations
        :param population: size of the population
        :param towns: file with the location of cities on a Cartesian plane
        :return: 2 values (cost best route, the sequence of towns of the route found)
        """
        #    Carrega os pontos do mapas que deverão ser gerados as rotas
        mapa = np.loadtxt(towns)
        self.mapa = mapa

        #    Calculo da matriz de distancias entre todos os pontos
        distancias = self._matriz_distancia(mapa)
        self._distancias = distancias

        #    Dados das gerações população e numero de pontos da rota
        geracoes = generation
        populacao = population
        populacao = 4 * ((populacao + 4) // 4)
        size = mapa.shape[0]
        new_pop = np.zeros((populacao, size + 1))
        custo_rotas = np.arange(populacao)

        #    Matriz que armazenará os 4 melhores individuos da população
        best_4_rotes = np.zeros((4, size + 1))
        best_4_cousts = np.zeros(4)

        #    A primeira população será totalmente aleatória
        inicial = np.random.permutation(size)
        primeiro_gene = inicial[0]
        inicial = np.delete([inicial], [0, 0])

        count_best = 0
        best_element = 0

        for i in range(populacao):
            ind = np.copy(inicial)
            np.random.shuffle(ind)

            ind = np.array(ind)
            new_pop[i] = np.concatenate([[primeiro_gene], ind, [primeiro_gene]])

            custo_rotas[i] = self._mede_custo(distancias, ind)

        #   Inicio das gerações, quando o for é iniciado será buscado os 4 melhores
        #   individuos da população, o restante dos individos serão descartados
        for ger in range(geracoes):
            temp_pop = np.copy(new_pop)
            temp_cust = np.copy(custo_rotas)

            #        Pegando os 4 melhores individuos da população
            for j in range(4):
                tmp_ind = np.argmin(temp_cust)

                #        if(best_4_cousts[best_4_cousts == temp_cust[tmp_ind]].shape[0] == 0):
                best_4_rotes[j] = np.copy(temp_pop[tmp_ind])
                best_4_cousts[j] = temp_cust[tmp_ind]

                temp_pop = np.delete(temp_pop, tmp_ind, axis=0)
                temp_cust = np.delete(temp_cust, tmp_ind)
            #        else:
            #            temp_pop = np.delete(temp_pop, tmp_ind, axis=0)
            #            temp_cust = np.delete(temp_cust, tmp_ind)

            #        Pontos de inserções de mutações, estes pontos deverão ser
            #        diferentes para que possa uma mudança de genes
            route_insert_points = np.random.randint(size - 1, size=2)

            while route_insert_points[0] == route_insert_points[1]:
                route_insert_points = np.random.randint(size - 1, size=2)
            #        Um pequeno tratamento para que os Elementos I e J sejam
            #         próximospois caso sejam próximos poderão gerar indivíduos identicos
            I = route_insert_points.min()
            J = route_insert_points.max()
            if I + 1 == J:
                if J == size - 2:
                    I = I - 1
                else:
                    J = J + 1

            #        mutacao = np.zeros((4,size))
            new_pop = np.zeros((populacao, size + 1))
            for j in range(4):
                init_end_point = best_4_rotes[j, 0]
                resultado = np.zeros((4, size + 1))

                mutacao = np.repeat([best_4_rotes[j, 1:-1]], 4, axis=0)
                #            elemento_mutacao = np.copy(best_4_rotes[j//4])

                if I == 0:
                    mutacao[1, :J] = mutacao[1, J - 1::-1]
                else:
                    mutacao[1, I:J] = mutacao[1, J - 1:I - 1:-1]

                mutacao[2, I:J] = np.roll(mutacao[2, I:J], 1)
                if np.array_equal(mutacao[1], mutacao[2]):
                    np.random.shuffle(mutacao[2])

                mutacao[3, I], mutacao[3, J] = mutacao[3, J], mutacao[3, I]

                for k in range(4):
                    resultado[k] = np.concatenate([[init_end_point], mutacao[k], [init_end_point]])

                indice = j * 4
                new_pop[indice:indice + 4] = resultado

            x = self._generate_population(populacao - 16, inicial, primeiro_gene)
            new_pop[16:] = x

            custo_rotas = np.zeros(populacao)
            for k in range(new_pop.shape[0]):
                custo_rotas[k] = self._mede_custo(distancias, new_pop[k])

            if best_element == best_4_cousts[0]:
                count_best += count_best
                if count_best == int(geracoes / 100):
                    break
            else:
                best_element = best_4_cousts[0]
                count_best = 0

        return best_4_cousts[0], best_4_rotes[0]

    def percorre_rota(self, rota, combustivel):
        rota = rota.astype(int)
        distancia_percorrida = 0
        combustivel_restante = combustivel
        caminho_percorrigo = [rota[0]]
        last_route = rota[0]
        for x in range(1, len(rota)):
            distancia_percorrida = distancia_percorrida + self._distancias[last_route, rota[x]]
            combustivel_restante -= self._distancias[rota[x - 1], rota[x]]
            caminho_percorrigo.append(rota[x])
            last_route = rota[x]
            if x != (len(rota) - 1) and combustivel_restante <= self._distancias[rota[x], rota[x + 1]]:
                distancia_percorrida += self._distancias[rota[x], rota[0]]
                combustivel_restante = combustivel
                caminho_percorrigo.append(rota[0])
                last_route = rota[0]
        #                distancia_percorrida += self._distancias[rota[0], rota[x]]
        #                combustivel_restante -= self._distancias[rota[0], rota[x]]
        #                caminho_percorrigo.append(rota[x])

        return distancia_percorrida, caminho_percorrigo

    def tanque_rota(self, rota, tank):
        route = rota.astype(int)
        point_recharge = route[0]
        travelled_distance = 0
        consum_fuel = float(tank)
        travelling = [point_recharge]
        last_town = point_recharge

        _temp_dist1 = 0
        _temp_dist2 = 0
        _temp_back = 0

        _temp_results = []

        town_number = 1
        size_route = route.size

        while (town_number < size_route):

            # for town_number in range(1, len(route)):
            _temp_dist1 = self._distancias[last_town, route[town_number]]
            _temp_dist2 = self._distancias[route[town_number], point_recharge]
            _temp_back = self._distancias[last_town, point_recharge]

            _temp_results.append([_temp_dist1, _temp_dist2, _temp_back, consum_fuel, tank])

            if town_number != len(route) - 1 and \
                consum_fuel >= (self._distancias[last_town, route[town_number]] +
                                self._distancias[route[town_number], point_recharge]):

                travelled_distance += self._distancias[last_town, route[town_number]]
                travelling.append(route[town_number])
                consum_fuel -= float(self._distancias[last_town, route[town_number]])
                last_town = route[town_number]
                town_number += 1

            elif last_town != point_recharge and \
                    consum_fuel >= self._distancias[last_town, point_recharge]:

                travelled_distance += self._distancias[last_town, point_recharge]
                travelling.append(point_recharge)
                consum_fuel = tank
                last_town = point_recharge


            else:
                print(_temp_dist1, _temp_dist2, _temp_back, consum_fuel)
                break

        np.savetxt('./limites.txt', np.asarray(_temp_results), delimiter=',', fmt='%.5f')

        return travelled_distance, travelling

if __name__ == "__main__":
    x = CalulateRoutesTSP()
    y, z = x.ga(generation=2500,
                population=50,
                towns='./pontos.txt')
    print(y, z)

    nova_rota = x.percorre_rota(z, 30)

    distancia_nova_rota, rota_recarga = x.tanque_rota(z, 30.0)

    print("Metodo ANtigo:")
    print(nova_rota)

    print("\nMetodo Novo:")
    print(distancia_nova_rota, rota_recarga)

    # x.plota_rotas(x.mapa,z)
    # x.plota_rotas(x.mapa,np.array(nova_rota[1], dtype=np.int32))
