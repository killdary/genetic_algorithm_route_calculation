import numpy as np


class Selection:
    def tournament(self, number_parents, population_cousts, k_parents_tournament):
        parents_selected = np.empty([number_parents])
        parents_selected[:] = np.nan

        indexes = np.arange(population_cousts.size)

        for i in range(number_parents):
            selected_parents = np.random.choice(indexes, k_parents_tournament, replace=False)
            elements = population_cousts[selected_parents]
            parent = np.argmin(population_cousts[selected_parents])
            parents_selected[i] = selected_parents[parent]

        return parents_selected.astype(int)

    def elitism(self, number_parents, population_cousts, x):
        parents_selected = np.empty([number_parents])
        parents_selected[:] = np.nan

        indexes = np.arange(population_cousts.size)

        for i in range(number_parents):
            parent = np.argmin(population_cousts)
            parents_selected[i] = population_cousts[parent]
            population_cousts = np.delete(population_cousts,[parent])

        return parents_selected.astype(int)

    def probabilidade(self, number_parents, population_cousts, z):
        x = np.copy(population_cousts)
        x.sort()
        y = int(number_parents/z)
        count = 0
        a = np.array([])
        for i in range(z):
            count_end = count + y
            if i < z-1:
                a = np.concatenate([a, x[count:count_end]])
            else:
                a = np.concatenate([a, x[count:-1]])
            count = count_end

        return np.array(a)
    #




if __name__ == '__main__':
    sel = Selection()
    cousts = np.random.choice(np.arange(-5,5),10)

    print(cousts)
    print(sel.tournament(10,cousts, 4))