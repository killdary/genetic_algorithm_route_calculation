from itertools import chain

import numpy as np


class Mutation:

    def __init__(self, med_custo, max_coust = 0, prizes = ''):
        self.max_coust = max_coust
        self.prizes = prizes
        self.med_custo = med_custo

    def __point_mutation(self, flux):
        size_min = flux.size

        if size_min == 2:
            self.I = 0
            self.J = 1
        else:
            route_insert_points = np.zeros(2)

            while route_insert_points[0] == route_insert_points[1]:
                route_insert_points = np.random.randint(size_min - 1, size=2)

            self.I = route_insert_points.min()
            self.J = route_insert_points.max()

    def __point_mutation_2(self,  parent_1, parent_2):
        size_min = parent_1.size if parent_1.size < parent_2.size else parent_2.size

        if size_min == 2:
            self.I = 0
            self.J = 1
        else:
            route_insert_points = np.zeros(2)

            while route_insert_points[0] == route_insert_points[1]:
                route_insert_points = np.random.randint(size_min - 1, size=2)

            self.I = route_insert_points.min()
            self.J = route_insert_points.max()

    def __trata_crhomossomo(self, crhormossomo):
        self.start = np.array([crhormossomo[0]])
        self.end = np.array([crhormossomo[crhormossomo.size-1]])
        result_crhomossome = np.delete(crhormossomo, [0, crhormossomo.size - 1])
        return result_crhomossome

    def __corrige_chromossomo(self, chromossomo):
        tes = np.concatenate([self.start, chromossomo, self.end])
        return np.concatenate([self.start, chromossomo, self.end])

    def swap(self, flux):
        city_mutation = self.__trata_crhomossomo(flux)
        self.__point_mutation(city_mutation)
        city_mutation[self.I], city_mutation[self.J] = city_mutation[self.J], city_mutation[self.I]
        city_mutation = self.__corrige_chromossomo(city_mutation)
        return city_mutation

    def reverse(self, flux):
        self.__point_mutation(flux)
        city_mutation = self.__trata_crhomossomo(flux)
        tmp = city_mutation[self.I:self.J]
        city_mutation[self.I:self.J] = tmp[::-1]
        city_mutation = self.__corrige_chromossomo(city_mutation)
        return city_mutation

    def scramble(self, flux):
        city_mutation = self.__trata_crhomossomo(flux)
        self.__point_mutation(city_mutation)
        np.random.shuffle(city_mutation[self.I:self.J])
        city_mutation = self.__corrige_chromossomo(city_mutation)
        return city_mutation

    def insertion(self, flux):
        city_mutation = self.__trata_crhomossomo(flux)
        self.__point_mutation(city_mutation)
        city_mutation[self.I:self.J] = np.roll(city_mutation[self.I:self.J], 1)
        city_mutation = self.__corrige_chromossomo(city_mutation)

        return city_mutation

    def WGWRGM(self, City):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        for i in range(0, City.size -2):
            value = self.med_custo(individual[i:i+2])
            if value < value_worst:
                value_worst = value
                index_worst = i

        index_random = np.random.choice(np.arange(individual.size),1)
        while index_random == index_worst:
            index_random = np.random.choice(np.arange(individual.size), 1)

        individual[index_worst], individual[index_random] = individual[index_random], individual[index_worst]
        individual = self.__corrige_chromossomo(individual)

        return individual

    def WGWWGM(self, City):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        # if individual.size > 3
        for i in range(0, individual.size):
            value = self.med_custo(individual[i:i + 2])
            if value > value_worst:
                index_worst2 = index_worst
                value_worst = value
                index_worst = i

        individual[index_worst], individual[index_worst2] = individual[index_worst2], individual[index_worst]

        individual = self.__corrige_chromossomo(individual)
        return individual

    def WGWNNM(self, City):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        if individual.size <= 2:
            individual[0], individual[1] = individual[1], individual[0]
        else:
            for i in range(1, individual.size - 2):
                value = self.med_custo(individual[i - 1:i]) + self.med_custo(individual[i:i + 2])
                if value > value_worst:
                    value_worst = value
                    index_worst = i

            minor = 100
            for i in np.arange(individual.size):
                if i != 0 and i != index_worst and i != (individual.size - 1):
                    value = self.med_custo(np.array([individual[index_worst], individual[i]]))
                    if minor > value:
                        minor = value
                        minor_i = i

            x = minor_i + (-1 if np.random.randint(2, size=1) == 0 else 1)
            # x = minor_i if x < individual.size else x - 2

            individual[index_worst], individual[x] = individual[x], individual[index_worst]

        individual = self.__corrige_chromossomo(individual)

        return individual

    def SWGLM(self, City):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        # if individual.size > 3
        for i in range(0, individual.size):
            value = self.med_custo(individual[i:i + 2])
            if value > value_worst:
                value_worst = value
                index_worst = i

        best_cost_individual = self.med_custo(individual)
        best_individual = individual
        for i in range(0, individual.size):
            if i != index_worst:
                teste_individual = np.copy(individual)
                teste_individual[i], teste_individual[index_worst] = teste_individual[index_worst], teste_individual[i]
                cost_test = self.med_custo(teste_individual)
                if cost_test < best_cost_individual:
                    best_cost_individual = cost_test
                    best_individual = teste_individual

        individual = self.__corrige_chromossomo(best_individual)
        # print('.', end='')
        return individual

    def insert_individualin_cromossome(self, City, chromossome, med_custo):

        citys_fall = np.delete(chromossome, City)
        chromossome_generate = self.__trata_crhomossomo(City)

        chromossome_generate_tmp = np.copy(chromossome_generate)

        while True:
            mede_custo_rota = med_custo(self.__corrige_chromossomo(chromossome_generate_tmp))
            if mede_custo_rota >= self.max_coust:
                break

            chromossome_generate = np.copy(chromossome_generate_tmp)

            if chromossome_generate.size < 2:
                city_add = 1
            else:
                city_add = np.random.randint(chromossome_generate.size - 1, size=1)

            if citys_fall.size > 1:
                city_rmv = np.random.randint(citys_fall.size - 1, size=1)
            else:
                city_rmv = 0
                break

            chromossome_generate_tmp = np.insert(chromossome_generate, city_add, citys_fall[city_rmv])
            citys_fall = np.delete(citys_fall, [city_rmv])

        chromossome_generate = self.__corrige_chromossomo(chromossome_generate)
        return chromossome_generate

    def insert_individualin_cromossome_2(self, City, chromossome, med_custo, function_aux):
        """

        :param City: all points oh the map
        :param chromossome: route
        :param med_custo: function with mensure of the couste
        :param function_aux: function with mensure the coust of the route, not only coust but prize too
        :return:
        """
        citys_fall = np.delete(chromossome, City)
        chromossome_generate = self.__trata_crhomossomo(City)

        idx_best = 0
        value_best = 0
        if citys_fall.size > 0:
            if citys_fall.size > 1:
                city_rmv = np.random.randint(citys_fall.size - 1, size=1)
            else:
                city_rmv = 0
            idx_best = -1
            value_best = -1
            element_insert = citys_fall[city_rmv]

            for i in range(chromossome_generate.size+1):
                tmp = np.insert(chromossome_generate, i, element_insert)
                tmp = self.__corrige_chromossomo(tmp)
                coust = med_custo(tmp)
                if coust <= self.max_coust:
                    value_function = function_aux(chromossome)
                    if value_function > value_best:
                        idx_best = i
                        value_best = value_function

            if idx_best != -1:
                chromossome_generate = np.insert(chromossome_generate, idx_best, element_insert)



        chromossome_generate = self.__corrige_chromossomo(chromossome_generate)
        return chromossome_generate


    def insert_individualin_cromossome_TOP(self, 
                                           chromossome, 
                                           all_elements_chromossome, 
                                           elements_chromossome, 
                                           med_custo, 
                                           function_aux,
                                           max_coust):
        """

        :param chromossome: all points oh the map
        :param all_elements_chromossome: elements of the team of routes
        :param elements_chromossome: route
        :param med_custo: function with mensure of the couste
        :param function_aux: function with mensure the coust of the route, not only coust but prize too
        :return:
        """
        citys_fall = np.setdiff1d(all_elements_chromossome, elements_chromossome)
        citys_fall = np.setdiff1d(citys_fall, chromossome)
        chromossome_generate = self.__trata_crhomossomo(chromossome)

        idx_best = 0
        value_best = 0
        if citys_fall.size > 0:
            if citys_fall.size > 1:
                city_rmv = np.random.randint(citys_fall.size - 1, size=1)
            else:
                city_rmv = 0
            idx_best = -1
            value_best = -1
            element_insert = citys_fall[city_rmv]

            for i in range(chromossome_generate.size+1):
                tmp = np.insert(chromossome_generate, i, element_insert)
                tmp = self.__corrige_chromossomo(tmp)
                coust = med_custo(tmp)
                if coust <= max_coust:
                    value_function = function_aux(tmp)
                    if value_function > value_best:
                        idx_best = i
                        value_best = value_function

            if idx_best != -1:
                chromossome_generate = np.insert(chromossome_generate, idx_best, element_insert)
                elements_chromossome = np.insert(elements_chromossome,0, element_insert)
                # elements_chromossome = np.concatenate([elements_chromossome, element_insert])



        chromossome_generate = self.__corrige_chromossomo(chromossome_generate)
        return chromossome_generate, elements_chromossome



    def remove_pior_custo(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = np.copy(City)
        while med_custo(individual) > self.max_coust:
            individual = self.__trata_crhomossomo(individual)
            for i in range(0, individual.size - 2):
                value = med_custo(individual[i:i + 2])
                if value < value_worst:
                    value_worst = value
                    index_worst = i
            individual = np.delete(individual,[index_worst])
            individual = self.__corrige_chromossomo(individual)

        return individual

    def remove_pior_custo_2(self, City, med_custo, function_aux, max_coust):

        individual = np.copy(City)

        coust = med_custo(City)
        if coust > max_coust:
            individual = self.__trata_crhomossomo(individual)

            idx_worst = -1
            value_worst = -1
            for i in range(individual.size):
                tmp = np.copy(individual)
                tmp = np.delete(tmp, [i])

                tmp_coust = function_aux(self.__corrige_chromossomo(tmp))

                if value_worst < tmp_coust:
                    idx_worst = i
                    value_worst = tmp_coust


            individual = np.delete(individual,[idx_worst])
            individual = self.__corrige_chromossomo(individual)

        return individual

    def remove_pior_custo_TOP(self, City, med_custo, function_aux):

        individual = np.copy(City)

        coust = med_custo(City)
        if coust > self.max_coust:
            individual = self.__trata_crhomossomo(individual)

            idx_worst = -1
            value_worst = -1
            for i in range(individual.size):
                tmp = np.copy(individual)
                tmp = np.delete(tmp, [i])

                tmp_coust = function_aux(self.__corrige_chromossomo(tmp))

                if value_worst < tmp_coust:
                    idx_worst = i
                    value_worst = tmp_coust


            individual = np.delete(individual,[idx_worst])
            individual = self.__corrige_chromossomo(individual)

        return individual

    def remove_random(self, City, med_custo):
        individual = np.copy(City)
        while med_custo(individual) > self.max_coust:
            individual = self.__trata_crhomossomo(individual)
            idx_random = np.random.randint(individual.size - 1, size=2)
            individual = np.delete(individual,[idx_random])
            individual = self.__corrige_chromossomo(individual)

        return individual

    def remove_pior_premio(self, City, med_custo):
        individual = np.copy(City)
        lst_prizes =  self.__trata_crhomossomo(City)
        prizes = self.prizes.take(lst_prizes)
        while med_custo(individual) > self.max_coust:
            individual = self.__trata_crhomossomo(individual)
            ind_min_prize = np.argmin(prizes)

            individual = np.delete(individual,[ind_min_prize])
            prizes = np.delete(prizes,[ind_min_prize])

            individual = self.__corrige_chromossomo(individual)

        return individual

    def insert_remove_points_TOP(self, 
                                 med_custo, 
                                 function_insert_remove, 
                                 all_elements, 
                                 chromossome):
        elements_chromossome = np.array([])

        for i in chromossome:
            tmp = self.__trata_crhomossomo(i)
            elements_chromossome = np.concatenate([elements_chromossome, tmp])

        for i in range(len(chromossome)):
            coust = med_custo(chromossome[i])

            if coust > self.max_coust[i]:
                chromossome[i] = self.remove_pior_custo_2(chromossome[i],
                                                             med_custo,
                                                             function_insert_remove,
                                                             self.max_coust[i])
            if coust < self.max_coust[i]:
                chromossome[i], elements_chromossome = self.insert_individualin_cromossome_TOP(chromossome[i],
                                                                         all_elements,
                                                                         elements_chromossome,
                                                                         med_custo,
                                                                         function_insert_remove,
                                                                         self.max_coust[i])
            # tmp = med_custo(chromossome[i])
            # if tmp > self.max_coust[i]:
            #     print(tmp, self.max_coust)


        return chromossome

    ''' Teste de metodo paenas pa inserção para melhorar a rota criada'''
    def insert_points_TOP(self,
                          med_custo,
                          function_insert_remove,
                          all_elements,
                          chromossome):

        elements_chromossome = np.array([])

        for i in chromossome:
            tmp = self.__trata_crhomossomo(i)
            elements_chromossome = np.concatenate([elements_chromossome, tmp])

        for i in range(len(chromossome)):
            coust = med_custo(chromossome[i])

            if coust < self.max_coust[i]:
                chromossome[i], elements_chromossome = self.insert_individualin_cromossome_TOP(chromossome[i],
                                                                                               all_elements,
                                                                                               elements_chromossome,
                                                                                               med_custo,
                                                                                               function_insert_remove,
                                                                                               self.max_coust[i])

        return chromossome

    def insert_points_TOP_2(self,
                          med_custo,
                          function_insert_remove,
                          all_elements,
                          chromossome):

        elements_chromossome = np.array([])
        resultado = [0]*len(chromossome)

        for i in chromossome:
            tmp = self.__trata_crhomossomo(i)
            elements_chromossome = np.concatenate([elements_chromossome, tmp])


        range_chormosome = np.arange(len(chromossome))
        np.random.shuffle(range_chormosome)

        for i in range_chormosome:
            coust = med_custo(chromossome[i])
            if coust < self.max_coust[i]:

                citys_fall = np.setdiff1d(all_elements, elements_chromossome)
                citys_fall = np.setdiff1d(citys_fall, chromossome[i])
                chromossome_generate = self.__trata_crhomossomo(chromossome[i])

                idx_best = 0
                value_best = 0
                if citys_fall.size > 0:
                    if citys_fall.size > 1:
                        city_rmv = np.random.randint(citys_fall.size - 1, size=1)
                    else:
                        city_rmv = 0
                    idx_best = np.random.randint(chromossome_generate.size - 1, size=1) if chromossome_generate.size > 2 else 0
                    element_insert = citys_fall[city_rmv]

                    chromossome_generate = np.insert(chromossome_generate, idx_best, element_insert)
                    elements_chromossome = np.insert(elements_chromossome, 0, element_insert)
                    # elements_chromossome = np.concatenate([elements_chromossome, element_insert])

                chromossome_generate = self.__corrige_chromossomo(chromossome_generate)

                resultado[i] = chromossome_generate
            else:
                resultado[i] = chromossome[i]

        return resultado




    def remove_points_TOP(self,
                          med_custo,
                          function_insert_remove,
                          all_elements,
                          chromossome):

        for i in range(len(chromossome)):
            coust = med_custo(chromossome[i])

            if coust > self.max_coust[i]:
                chromossome[i] = self.remove_pior_custo_2(chromossome[i],
                                                          med_custo,
                                                          function_insert_remove,
                                                          self.max_coust[i])

        return chromossome

    # def SWGLM(self, City, med_custo):
    #     value_worst = 0
    #     index_worst = 0
    #     individual = self.__trata_crhomossomo(City)

    def PMX_mutation(self, parent_1_tmp, parent_2_tmp, all_elements_1, all_elements_2):
        start_parent_1 = np.array([parent_1_tmp[0]])
        end_parent_1 = np.array([parent_1_tmp[-1]])
        start_parent_2 = np.array([parent_2_tmp[0]])
        end_parent_2 = np.array([parent_2_tmp[-1]])

        parent_1 = np.delete(parent_1_tmp, [0, parent_1_tmp.size - 1])
        parent_2 = np.delete(parent_2_tmp, [0, parent_2_tmp.size - 1])

        all_elemnts = np.unique(np.concatenate([parent_1, parent_2]))

        if parent_1.size > 1 and parent_2.size > 1:

            self.__point_mutation_2(parent_1, parent_2)
            offspring_1 = np.ones(parent_1.size).astype(int) * -1
            offspring_2 = np.ones(parent_2.size).astype(int) * -1
            offspring_1[self.I:self.J] = parent_2[self.I:self.J]
            offspring_2[self.I:self.J] = parent_1[self.I:self.J]

            for i in np.arange(offspring_1.size):
                if i < self.I or i >= self.J:
                    if parent_1[i] not in offspring_1:
                        offspring_1[i] = parent_1[i]

            for i in np.arange(offspring_2.size):
                if i < self.I or i > self.J:
                    if parent_2[i] not in offspring_2:
                        offspring_2[i] = parent_2[i]

            index_fall_1 = np.where(offspring_1 == -1)[0]
            index_fall_2 = np.where(offspring_2 == -1)[0]
            #
            # elements_1 = list()
            # for value in range(parent_1.size):
            #     if parent_1[value] not in offspring_1:
            #         elements_1.append(parent_1[value])


            # elements_1 = np.array(elements_1)

            # elements_2 = list()
            # for value in range(parent_2.size):
            #     if parent_2[value] not in offspring_2:
            #         elements_2.append(parent_2[value])
            #
            # elements_2 = np.array(elements_2)


            # elements_tmp = np.setdiff1d(parent_1, offspring_1)
            # elements_tmp2 = np.setdiff1d(parent_2, offspring_2)
            # test = np.setdiff1d(np.concatenate([elements_tmp, elements_tmp2]), offspring_1)
            # test2 = np.setdiff1d(all_elemnts, offspring_2)
            # test2 = np.setdiff1d(test2, offspring_1)

            # if (all_elements_1.size > 0):
            #     elements_1 = np.setdiff1d(elements_1, all_elements_1)
            #     test2 = np.setdiff1d(test2, all_elements_2)
            #     if elements_1.size < index_fall_1.size:
            #         index_fall_1 = index_fall_1[:elements_1.size]
            #     if test2.size < index_fall_2.size:
            #         index_fall_2 = index_fall_2[:test2.size]

            # offspring_1[index_fall_1] = np.array(elements_1[:index_fall_1.size])
            # offspring_1 = offspring_1[offspring_1 != -1]
            #
            # if test2.size == 0 or index_fall_2.size == 0:
            #     offspring_2 = offspring_2[offspring_2 != -1]
            # elif test2.size < index_fall_2.size:
            #     offspring_2[index_fall_2[:test2.size]] = np.array(test2)
            #     offspring_2 = offspring_2[offspring_2 !=-1]
            # else:
            #     offspring_2[index_fall_2] = np.array(test2[:index_fall_2.size])
            #     # offspring_2 = test2[test2 != -1]



            elements_1_teste = np.setdiff1d(all_elemnts, offspring_1)
            elements_2_teste = np.setdiff1d(all_elemnts, offspring_2)

            # offspring_1[offspring_1 == -1] = elements_1_teste[:offspring_1[offspring_1 == -1].size]

            if elements_1_teste.size == 0:
                offspring_1 = offspring_1[offspring_1 != -1]
            elif elements_1_teste.size < offspring_1[offspring_1 == -1].size:
                indixes = np.where(offspring_1 == -1)[0]
                offspring_1[indixes[:elements_1_teste.size]] = elements_1_teste
                offspring_1 = offspring_1[offspring_1 != -1]
            else:
                offspring_1[offspring_1 == -1] = elements_1_teste[:offspring_1[offspring_1 == -1].size]

            elements_2_teste = np.setdiff1d(elements_2_teste, offspring_1)

            if elements_2_teste.size == 0:
                offspring_2 = offspring_2[offspring_2 !=-1]
            elif elements_2_teste.size < offspring_2[offspring_2 == -1].size:
                indixes = np.where(offspring_2 == -1)[0]
                offspring_2[indixes[:elements_2_teste.size]] = elements_2_teste
                offspring_2 = offspring_2[offspring_2 !=-1]
            else:
                offspring_2[offspring_2 == -1] = elements_2_teste[:offspring_2[offspring_2 == -1].size]

            elements_1_teste = np.setdiff1d(all_elemnts, elements_1_teste)

            if True in np.isin(offspring_1, all_elements_1) or True in np.isin(offspring_2, all_elements_2):
                offspring_1 = np.setdiff1d(offspring_1, all_elements_1)
                offspring_2 = np.setdiff1d(offspring_2, all_elements_2)

        else:
            offspring_1 = parent_1
            offspring_2 = parent_2

        if np.intersect1d(offspring_1, offspring_2).size > 0:
            offspring_1 = offspring_1[np.isin(offspring_1, offspring_2, invert=True)]

        offspring_1 = np.concatenate([start_parent_1, offspring_1, end_parent_1])
        offspring_2 = np.concatenate([start_parent_2, offspring_2, end_parent_2])

        return offspring_1.astype(int), offspring_2.astype(int)