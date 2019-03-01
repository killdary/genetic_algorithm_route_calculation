import numpy as np

class Mutation:

    def __init__(self, max_coust = 0, prizes = ''):
        self.max_coust = max_coust
        self.prizes = prizes

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

    def WGWRGM(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        for i in range(0, City.size -2):
            value = med_custo(individual[i:i+2])
            if value < value_worst:
                value_worst = value
                index_worst = i

        index_random = np.random.choice(np.arange(individual.size),1)
        while index_random == index_worst:
            index_random = np.random.choice(np.arange(individual.size), 1)

        individual[index_worst], individual[index_random] = individual[index_random], individual[index_worst]
        individual = self.__corrige_chromossomo(individual)

        return individual

    def WGWWGM(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        # if individual.size > 3
        for i in range(0, individual.size):
            value = med_custo(individual[i:i + 2])
            if value > value_worst:
                index_worst2 = index_worst
                value_worst = value
                index_worst = i

        individual[index_worst], individual[index_worst2] = individual[index_worst2], individual[index_worst]

        individual = self.__corrige_chromossomo(individual)
        return individual

    def WGWNNM(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)
        if individual.size <= 2:
            individual[0], individual[1] = individual[1], individual[0]
        else:
            for i in range(1, individual.size - 2):
                value = med_custo(individual[i - 1:i]) + med_custo(individual[i:i + 2])
                if value > value_worst:
                    value_worst = value
                    index_worst = i

            minor = 100
            for i in np.arange(individual.size):
                if i != 0 and i != index_worst and i != (individual.size - 1):
                    value = med_custo(np.array([individual[index_worst], individual[i]]))
                    if minor > value:
                        minor = value
                        minor_i = i

            x = minor_i + (-1 if np.random.randint(2, size=1) == 0 else 1)
            # x = minor_i if x < individual.size else x - 2

            individual[index_worst], individual[x] = individual[x], individual[index_worst]

        individual = self.__corrige_chromossomo(individual)

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


    def remove_pior_custo_2(self, City, med_custo, function_aux):

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


    def SWGLM(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)