#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed May 23 21:21:37 2018
@author: killdary
@version: 0.0.2
Backlog - product
    - TSP Janela de Tempo
    - Adaptar TSPLIB para o software e calcular eficiencia
    - Aplicar em Simulador VRep
    - Aplica em Robo Real
    - escrever a discertacao
Em Andamento
    - TSP Prize Collecting
        * Gerar Aleatoria cidades Visitadas
            * quando selecionar cidades diferentes, melhor alternativa seria gerar cidades
              a cada nova rodada de individuos
        * Calcular Premios Coletados
        * Calcular Penalizacoes Sofridas
        * Submeter cidades visitadas a mutacao do algoritmo
        * Criar Funcao Objetivo
        * Mapear Restricoes Formulacao mAtematica

Urgente Vandilberto
    - TSP skapsack problem
        *


Realizados
    - Calculo da menor Rota usando GA
    - Gerar Grafico com Rota
"""

import numpy as np

import matplotlib.pyplot as plt


class CalulateRoutesTSP:
    # TSP Prize Collecting

    """
    Desenvolvimento do TSP para 'Prize Collect(PC)'
    methods -
        amarrar uma cidade como sendo o deposito
        calculo do premio e selecao de cidades
        calculo penalidade
        calculo funcao objetivo
    """

    @staticmethod
    def prize_calculation(prize_min, lst_prizes_true):
        """
        metodo para o calculo fluxo de cidades, premio e cidades visitadas
        :param prize_min: valor minimo para o premio
        :param lst_prizes_true: lista de premios de cada cidade
        :return:  fluxo de cidades, premio e cidades visitadas
        """
        # pegando o numero de cidade
        lst_prizes = np.asarray(lst_prizes_true)
        size = lst_prizes.shape[0]

        # media dos premios das cidades
        mean_prize = lst_prizes.mean()

        # range das cidades a serem visitadas, essas cidades devem vir sem a cidade deposito
        # lista de cidades
        citys = np.arange(0, size)

        # numero de cidades a serem selecionadas para se aproximar da rota
        # total de cidades dividido pela média dos premios retorna um número aproximado
        # de cidades a serem visitadas para atingir o prêmio mínimo
        number_city_select = int(round(len(citys) / mean_prize))

        # fluxo de cidade que serão visitadas selecionadas aleatoriamente
        flux_citys = np.random.choice(citys, number_city_select)
        citys = np.delete(citys, flux_citys)

        while True:
            # eh realizado um calculo dos premios em cima das cidades visitadas
            prize = lst_prizes.take(flux_citys).sum()

            # Caso p premio ainda seja menor que o premio minimo eh selecionada mais uma cidade
            # aleatoria para compor as cidades visitadas
            if prize < prize_min:
                new_city = np.random.choice(citys, 1)
                flux_citys = np.append(flux_citys, new_city)
                citys = np.delete(citys, new_city)

            # Caso o premio seja maior ou igual ao premio minimo o while eh encerrado
            elif prize_min <= prize:
                break

        # Depois de selecionar as cidades visitadas é gerado um vetor de zerose nas posicoes correspondetes
        # as cidades visitadas é colocado um valor 1, isso é realizado pelo metodo put do numpy
        citys_visited = np.zeros(size)
        np.put(citys_visited, flux_citys, 1)

        # flux_citys = np.append(flux_citys, np.zeros(size-flux_citys.shape[0]))

        # resumidadmente o fluxo de cidades sao as cidades visitadas, prize sao os premios e a citys_visited
        # é um vetor de zeros com as cidades visitadas marcadas com o valor 1
        return flux_citys, prize, citys_visited

    """ metodo que realiza o calculo da penalidade de uma rota
        para realizar o calculo é necessario passar o array com o status de visita de todas
        as cidades        
    """

    def penalty_calculation(self, citys_visited, penaltys):
        '''
        Metodo responsavel por calcular as penalidades por nao visitar determinadas cidades
        :param citys_visited: vetor de zeros com as posicoes das cidades visitadas trocado seu valor por 1
        :param penaltys: vetor com as penalidades das cidades nao visitadas
        :return:
        '''
        # selecinada as cidades que tem o valor igual a 0, ou seja, nao visitadas
        city_not_visited = np.where(citys_visited == 0)
        # soma das penalidades das cidades nao visitadas
        sum_penalty = penaltys.take(city_not_visited).sum()
        return sum_penalty

    ''' funcao objetivo
    '''

    def goal_function_price_collecting(self, score_distance, score_penalty):
        '''
        Funcao objetivo basta somar a soma das distancias com a soma das penalidades
        :param score_distance: valor da distancia total percorrida por um caixeiro
        :param score_penalty: valor da soma de todas as penalidades das cidades nao visitadas
        :return: valor do score do TSPPC
        '''
        return score_distance + score_penalty

    @staticmethod
    def penalty_prize_calculation(citys_status_visit, prize_min, prizes, penaltys):
        counts_try = 0

        size = citys_status_visit.shape[0]
        citys = np.arange(0, size)

        citys_visited = np.where(citys_status_visit == 1)[0]
        citys = np.delete(citys, citys_visited)

        while True:
            sum_prize = prizes.take(citys_visited).sum()

            if sum_prize < prize_min:
                new_city = np.random.choice(citys, 1)
                citys_visited = np.append(citys_visited, new_city)
                citys_status_visit[new_city] = 1
                citys = np.delete(citys, new_city)


            # Caso o premio seja maior ou igual ao premio minimo o while eh encerrado
            elif prize_min <= sum_prize:
                if counts_try > 2:
                    break
                else:
                    new_city = np.random.choice(citys_visited, 1)
                    citys_status_visit[new_city] = 0
                    citys = np.append(citys, new_city)
                    citys_visited = np.delete(citys_visited, new_city)
                    counts_try = counts_try + 1

        city_not_visited = np.where(citys_status_visit == 0)
        sum_penalty = penaltys.take(city_not_visited).sum()

        return citys_status_visit, sum_prize, sum_penalty

    """ a funcao crossover_prizes tem como objetivo executar  cruzamento dos melhores indivíduos 
        da popula para gerar escolhas de visitas que reduzam as penalidades"""
    def crossover_prizes(self, best_individual, size_population):
        size = best_individual.shape[0]

        # inicializando as variaveis responsáveis pelos pontos de cruzamento
        route_insert_points = np.zeros(2)

        while route_insert_points[0] == route_insert_points[1]:
            route_insert_points = np.random.randint(size_population - 1, size=2)

        # Um pequeno tratamento para que os Elementos I e J nao sejam próximos
        # pois caso sejam próximos poderão gerar indivíduos identicos
        I = route_insert_points.min()
        J = route_insert_points.max()
        if I + 1 == J:
            if J == size - 2:
                I = I - 1
            else:
                J = J + 1

        for i in range(size):
            main_indivvidual = best_individual[i]
            remaining_individual = np.delete(best_individual[i])

            # um array de 7 posicoes e criado pra armazenar o os elementos gerados
            # e o individuo principal do cruzamento
            result_crossover = np.repeat(np.expand_dims(main_indivvidual, axis=0), 7, axis=0)

            # primeira mutacao -> cruzamento de 1 ponto
            result_crossover[0,0:I] = remaining_individual[0,0:I]
            result_crossover[1,I:] = remaining_individual[0,I:]
            result_crossover[2,I:J] = remaining_individual[0,I:]
            result_crossover[2,I:J] = remaining_individual[0,I:]


            pass

        pass

    '''endregion'''

    '''
    Metodos gerais da biblioteca:
        _mede_custo: medir custo da rota em distancia
        _matriz_distancia: criar a matriz de distancia euclidiana das cidades
        plota_rotas: criar o grafico da rota 
    '''

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
        # distancia_percorrida += self._distancias[rota[0], rota[x]]
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

    '''mutação, esta região gerará mutações para consumo iterno'''

    @staticmethod
    def _generate_points(size):
        route_insert_points = np.random.randint(size - 1, size=2)

        while route_insert_points[0] == route_insert_points[1]:
            route_insert_points = np.random.randint(size - 1, size=2)
        # Um pequeno tratamento para que os Elementos I e J sejam
        #         próximospois caso sejam próximos poderão gerar indivíduos identicos
        I = route_insert_points.min()
        J = route_insert_points.max()
        if I + 1 == J:
            if J == size - 2:
                I = I - 1
            else:
                J = J + 1
        return I, J

    '''
        
    '''

    """
    Metodo principal da Classe que gera as rotas o GA em si
    """

    def ga(self, generation, population, towns, type='classic', prize_min=0, prizes=''):
        """
        Calculation of the best route using Genetic Algorithm
        :param prize_min:
        :param type:
        :param generation: number of the generations
        :param population: size of the population
        :param towns: file with the location of cities on a Cartesian plane
        :return: 2 values (cost best route, the sequence of towns of the route found)
        """
        # Carrega os pontos do mapas que deverão ser gerados as rotas
        mapa = np.loadtxt(towns)

        # Flag responsavel por habiliar a coleta de Premio TSP PC
        flag_prize_collection = False

        if type == 'prize_colect':
            flag_prize_collection = True
            prize_penalty = np.loadtxt(prizes)
            lst_prizes = prize_penalty[:, 0]
            lst_penalty = prize_penalty[:, 1]

        # Jogando o mapa como um recurso global da classe
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

        # gerando e buscando dados necessários para o TSPPC
        if flag_prize_collection:
            # gerando premio e rotas iniciais
            premio_rotas = np.zeros(populacao)
            penalidade_rotas = np.zeros(populacao)

            # fluxo de visitasdas cidades da rota
            fluxo_visitas = list()

            cidades_visitadas = np.zeros((populacao, size))

            best_4_cidades_visitadas = np.zeros((4, size))
            best_4_penalty = np.zeros(4)
            best_4_prize = np.zeros(4)

        # Matriz qprize_penprize_minaltyue armazenará os 4 melhores individuos da população
        best_4_rotes = np.zeros((4, size + 1))
        best_4_cousts = np.zeros(4)

        #    A primeira população será totalmente aleatória
        inicial = np.random.permutation(size)
        primeiro_gene = inicial[0]
        inicial = np.delete([inicial], [0, 0])

        count_best = 0
        best_element = 0

        # percoreendo a população e gerando os primiros indivíduos
        # a nova populacao eh da nao apenas para a rota mas tambem para penalidades
        for i in range(populacao):
            ind = np.copy(inicial)
            np.random.shuffle(ind)

            ind = np.array(ind)
            new_pop[i] = np.concatenate([[primeiro_gene], ind, [primeiro_gene]])

            custo_rotas[i] = self._mede_custo(distancias, ind)

            # gerando as primeiras visitas as cidades e medindo suas penalidades
            if flag_prize_collection:
                fluxo, premio_rotas[i], cidades_visitadas[i] = self.prize_calculation(prize_min, lst_prizes)
                penalidade_rotas[i] = self.penalty_calculation(cidades_visitadas[i], lst_penalty)
                fluxo_visitas.append(fluxo)

        # Inicio das gerações, quando o for é iniciado será buscado os 4 melhores
        #   individuos da população, o restante dos individos serão descartados
        #### Update
        # Neste ponto tambem sera armazenao as 3 menores penalidades geradas anteriormente
        # Para cada novo individuo gerado gerar uma nova rota de visitas e depois aplicar
        # o mesmo vetor de mutacao nos quatro individuos

        for ger in range(geracoes):
            temp_pop = np.copy(new_pop)
            temp_cust = np.copy(custo_rotas)

            if flag_prize_collection:
                temp_penalidade_rotas = np.copy(penalidade_rotas)
                temp_cidades_visitadas = np.copy(cidades_visitadas)
                temp_premio_rotas = np.copy(premio_rotas)

            # Pegando os 4 melhores individuos da população
            for j in range(4):
                tmp_ind = np.argmin(temp_cust)

                #        if(best_4_cousts[best_4_cousts == temp_cust[tmp_ind]].shape[0] == 0):
                best_4_rotes[j] = np.copy(temp_pop[tmp_ind])
                best_4_cousts[j] = temp_cust[tmp_ind]

                # deletar valores repetidos
                indices_valores_custos = np.where(temp_cust == best_4_cousts[j])

                temp_pop = np.delete(temp_pop, indices_valores_custos, axis=0)
                temp_cust = np.delete(temp_cust, indices_valores_custos)

                # coletar as 4 rotas com as menores penalidades
                if flag_prize_collection:
                    temp_ind_penalty = np.argmin(temp_penalidade_rotas)

                    best_4_penalty[j] = temp_penalidade_rotas[temp_ind_penalty]
                    best_4_prize[j] = temp_premio_rotas[temp_ind_penalty]
                    best_4_cidades_visitadas[j] = np.copy(temp_cidades_visitadas[temp_ind_penalty])

                    # deletar valores repetidos
                    indices_valores_repetidos = np.where(temp_penalidade_rotas == best_4_penalty[j])

                    temp_penalidade_rotas = np.delete(temp_penalidade_rotas, indices_valores_repetidos)
                    temp_premio_rotas = np.delete(temp_premio_rotas, indices_valores_repetidos)
                    temp_cidades_visitadas = np.delete(temp_cidades_visitadas, indices_valores_repetidos, axis=0)

            # else:
            #            temp_pop = np.delete(temp_pop, tmp_ind, axis=0)
            #            temp_cust = np.delete(temp_cust, tmp_ind)

            #        Pontos de inserções de mutações, estes pontos deverão ser
            #        diferentes para que possa uma mudança de genes
            route_insert_points = np.random.randint(size - 1, size=2)

            while route_insert_points[0] == route_insert_points[1]:
                route_insert_points = np.random.randint(size - 1, size=2)
            # Um pequeno tratamento para que os Elementos I e J sejam
            #         próximospois caso sejam próximos poderão gerar indivíduos identicos
            I = route_insert_points.min()
            J = route_insert_points.max()
            if I + 1 == J:
                if J == size - 2:
                    I = I - 1
                else:
                    J = J + 1

            # mutacao = np.zeros((4,size))
            new_pop = np.zeros((populacao, size + 1))
            for j in range(4):
                init_end_point = best_4_rotes[j, 0]
                resultado = np.zeros((4, size + 1))

                # aqui é pego o segundo elemento e o penultimo, pois o primeiro elemento e o último serão iguais
                # e serão criado  cópias onde tres sofreão mutações
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

                # a cada rodada serah colocado na nova população, no a nova população sempre iniciará com 16 elementos
                # 4 ,elhosres resultados e 12 mutações decorridas deles
                new_pop[indice:indice + 4] = resultado

                # aqui se tem inicio a geração das mutações dos premios e das penalidades
                if flag_prize_collection:
                    mutacao_cidades_visitadas = np.repeat([best_4_cidades_visitadas[j]], 4, axis=0)

                    if I == 0:
                        mutacao_cidades_visitadas[1, :J] = mutacao_cidades_visitadas[1, J - 1::-1]
                    else:
                        mutacao_cidades_visitadas[1, I:J] = mutacao_cidades_visitadas[1, J - 1:I - 1:-1]

                    mutacao_cidades_visitadas[2, I:J] = np.roll(mutacao_cidades_visitadas[2, I:J], 1)

                    if np.array_equal(mutacao_cidades_visitadas[1], mutacao_cidades_visitadas[2]):
                        np.random.shuffle(mutacao_cidades_visitadas[2])

                    mutacao_cidades_visitadas[3, I], mutacao_cidades_visitadas[3, J] = mutacao_cidades_visitadas[3, J], \
                                                                                       mutacao_cidades_visitadas[3, I]

                    # mutacao_cidades_visitadas[3, 0:25], \
                    # mutacao_cidades_visitadas[3, 25:] = \
                    #     mutacao_cidades_visitadas[3, 25:], \
                    #     mutacao_cidades_visitadas[3, 0:25]

                    cidades_visitadas[indice:indice + 4] = mutacao_cidades_visitadas

            x = self._generate_population(populacao - 16, inicial, primeiro_gene)
            new_pop[16:] = x

            if flag_prize_collection:
                for pr in range(16, populacao):
                    fluxo, premio_rotas[pr], cidades_visitadas[pr] = self.prize_calculation(prize_min, lst_prizes)
                    penalidade_rotas[pr] = self.penalty_calculation(cidades_visitadas[pr], lst_penalty)
                # fluxo_visitas.append(fluxo)

                penalidade_rotas[16:] = np.zeros(penalidade_rotas[16:].shape[0])
                for k in range(populacao):
                    cidades_visitadas[k], premio_rotas[k], penalidade_rotas[k] = self.penalty_prize_calculation(
                        cidades_visitadas[k], prize_min, lst_prizes, lst_penalty)

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

        if flag_prize_collection:
            return best_4_cousts[0], best_4_rotes[0], best_4_penalty[0], best_4_cidades_visitadas[0]
        else:
            return best_4_cousts[0], best_4_rotes[0]


if __name__ == "__main__":
    x = CalulateRoutesTSP()
    a, b, c, d = x.ga(generation=2500,
                      population=50,
                      towns='./pontos.txt',
                      type='prize_colect',
                      prize_min=150,
                      prizes='./prize_penalty.txt')
    print(a, b, c, d)


    #
    # nova_rota = x.percorre_rota(z, 30)
    #
    # distancia_nova_rota, rota_recarga = x.tanque_rota(z, 30.0)
    #
    # print("Metodo ANtigo:")
    # print(nova_rota)
    #
    # print("\nMetodo Novo:")
    # print(distancia_nova_rota, rota_recarga)

    # x.plota_rotas(x.mapa,z)
    # x.plota_rotas(x.mapa,np.array(nova_rota[1], dtype=np.int32))