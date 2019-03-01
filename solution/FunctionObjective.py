import numpy as np


class FunctionObjective:
    def __init__(self, map_points, prizes):
        self.map_points = map_points
        self.prizes = prizes

        self.distance_matrix_calculate()

    def distance_matrix_calculate(self):
        qtd = self.map_points.shape[0]
        distancias = np.zeros([qtd, qtd])

        _temp_max = 0

        for i in range(qtd):
            for j in range(i, qtd):
                if i != j:
                    b = self.map_points[i, 0] - self.map_points[j, 0]
                    c = self.map_points[i, 1] - self.map_points[j, 1]
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

    def FO(self, chromosome):
        prizes_total = self.prizes.take(chromosome).sum()
        coust_total = self.med_custo(chromosome)
        return ((prizes_total * 3) - coust_total) * -1

    def coust_insert(self, chromosome):
        prizes_total = self.prizes.take(chromosome).sum()
        coust_total = self.med_custo(chromosome)
        return ((prizes_total ** 2)/ coust_total)


