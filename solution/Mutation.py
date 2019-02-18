import numpy as np

class Mutation:


    def __point_mutation(self, flux):
        self.I, self.J = np.random.randint(flux.size, size=2)

    def swap(self, flux):
        self.__point_mutation(flux)
        city_mutation = np.copy(flux)
        city_mutation[self.I], city_mutation[self.J] = city_mutation[self.J], city_mutation[self.I]
        return city_mutation

    def reverse(self, flux):
        self.__point_mutation(flux)
        city_mutation = np.copy(flux)
        city_mutation[self.I:self.J] = city_mutation[self.J:self.I:-1]
        return city_mutation

    def scramble(self, flux):
        self.__point_mutation(flux)
        city_mutation = np.copy(flux)
        np.random.shuffle(city_mutation[self.I:self.J])
        return city_mutation

    def insertion(self, flux):
        self.__point_mutation(flux)
        city_mutation = np.copy(flux)
        city_mutation[self.I:self.J] = np.roll(city_mutation[self.I:self.J], 1)
        return city_mutation

    def worst_gene_WGWRGM(self, City):
        pass

    def worst_gene_WGWWGM(self, City):
        pass

    def worst_gene_WGWNNM(self, City):
        pass