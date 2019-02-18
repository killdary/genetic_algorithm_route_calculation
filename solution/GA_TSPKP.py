import numpy as np
from Mutation import Mutation
from Crossover import Crossover
from Population import Population


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

    def seletion(self, pop):
        pass



    def mutation(self, type, city):
        pass


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

        self.gene_mutation = Mutation()

        # self.crossover = Crossover()

        self.Population = Population(self.start_point, self.end_point, self.med_custo, max_coust)

        self.initial_cromossome = np.arange(self.mapa.shape[0])

        self.initial_cromossome = np.delete(self.initial_cromossome, [start_point, end_point])



        self.pop_init = self.Population.initialize(self.initial_cromossome, self.population_size)



    def run(self):

        population = self.pop_init
        for g in range(self.genetarion_size):

            cousts_population = [self.function_objective(value) for value in population]
            cousts_population = np.array(cousts_population)

            pass
        pass


if __name__ == '__main__':
    ga = GA_TSPKP(
        genetarion = 100,
        population = 100,
        limit_population = 100,
        crossover_rate = 100,
        mutation_rate = 100,
        map_points = '../novas_cidades.txt',
        prizes = '../novos_premios.txt',
        max_coust = 10,
        start_point = 0,
        end_point = 5)
    ga.run()