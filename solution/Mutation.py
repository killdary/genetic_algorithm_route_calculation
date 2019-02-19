import numpy as np

class Mutation:


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
        return np.delete(crhormossomo, [0, crhormossomo.size-1])

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


    def SWGLM(self, City, med_custo):
        value_worst = 0
        index_worst = 0
        individual = self.__trata_crhomossomo(City)