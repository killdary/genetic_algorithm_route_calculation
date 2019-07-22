import numpy as np




class Crossover:

    def __point_mutation(self,  parent_1, parent_2):
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




    @staticmethod
    def removed_citys_repeat(flux):
        citys_position = np.unique(flux, return_index=True)[1]
        citys_position.sort()
        new_citys = flux.take(citys_position)

        return new_citys


    def one_point(self, City1, City2):
        pass


    def two_point(self, parent_1, parent_2):
        start = np.array([parent_1[0]])
        end = np.array([parent_1[-1]])

        parent_tmp_1 = np.delete(parent_1, [0, parent_1.size - 1])
        parent_tmp_2 = np.delete(parent_2, [0, parent_2.size - 1])



        pass

    def PMX(self, parent_1_tmp, parent_2_tmp):
        start = np.array([parent_1_tmp[0]])
        end = np.array([parent_1_tmp[-1]])

        parent_1 = np.delete(parent_1_tmp, [0, parent_1_tmp.size-1])
        parent_2 = np.delete(parent_2_tmp, [0, parent_2_tmp.size-1])

        all_elemnts = np.unique(np.concatenate([parent_1, parent_2]))

        if parent_1.size > 1 and parent_2.size > 1:

            self.__point_mutation(parent_1, parent_2)
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
            elements_1 = list()
            for value in range(parent_1.size):
                if parent_1[value] not in offspring_1:
                    elements_1.append(parent_1[value])

            elements_2 = list()
            for value in range(parent_2.size):
                if parent_2[value] not in offspring_2:
                    elements_2.append(parent_2[value])

            elements_tmp = np.setdiff1d(parent_1, offspring_1)
            elements_tmp2 = np.setdiff1d(parent_2, offspring_2)
            test = np.setdiff1d(np.concatenate([elements_tmp, elements_tmp2]), offspring_1)
            test2 = np.setdiff1d(all_elemnts, offspring_2)

            # elements_1 = [parent_1[value] for value in np.arange(parent_1.size) if parent_1[value] not in offspring_1]
            # elements_2 = [parent_2[value] for value in np.arange(parent_2.size) if parent_2[value] not in offspring_2]

            offspring_1[index_fall_1] = np.array(elements_1[:index_fall_1.size])
            offspring_2[index_fall_2] = np.array(test2[:index_fall_2.size])

        else:
            offspring_1 = parent_1
            offspring_2 = parent_2

        offspring_1 = np.concatenate([start, offspring_1, end])
        offspring_2 = np.concatenate([start, offspring_2, end])

        return offspring_1.astype(int), offspring_2.astype(int)

    def PMX_2(self, parent_1_tmp, parent_2_tmp, all_elements_1, all_elements_2):

        start_parent_1 = np.array([parent_1_tmp[0]])
        end_parent_1 = np.array([parent_1_tmp[-1]])
        start_parent_2 = np.array([parent_2_tmp[0]])
        end_parent_2 = np.array([parent_2_tmp[-1]])

        parent_1 = np.delete(parent_1_tmp, [0, parent_1_tmp.size - 1])
        parent_2 = np.delete(parent_2_tmp, [0, parent_2_tmp.size - 1])

        all_elemnts = np.unique(np.concatenate([parent_1, parent_2]))

        if parent_1.size > 1 and parent_2.size > 1:

            self.__point_mutation(parent_1, parent_2)
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
            elements_1 = list()
            for value in range(parent_1.size):
                if parent_1[value] not in offspring_1:
                    elements_1.append(parent_1[value])

            elements_1 = np.array(elements_1)

            elements_2 = list()
            for value in range(parent_2.size):
                if parent_2[value] not in offspring_2:
                    elements_2.append(parent_2[value])

            elements_tmp = np.setdiff1d(parent_1, offspring_1)
            elements_tmp2 = np.setdiff1d(parent_2, offspring_2)
            test = np.setdiff1d(np.concatenate([elements_tmp, elements_tmp2]), offspring_1)
            test2 = np.setdiff1d(all_elemnts, offspring_2)

            if(all_elements_1.size > 0):
                elements_1 = np.setdiff1d(elements_1,all_elements_1)
                test2 = np.setdiff1d(test2, all_elements_2)
                if elements_1.size < index_fall_1.size:
                    index_fall_1 = index_fall_1[:elements_1.size]
                if test2.size < index_fall_2.size:
                    index_fall_2 = index_fall_2[:test2.size]

            offspring_1[index_fall_1] = np.array(elements_1[:index_fall_1.size])
            offspring_1 = offspring_1[offspring_1 != -1]

            offspring_2[index_fall_2] = np.array(test2[:index_fall_2.size])
            offspring_2 = test2[test2 != -1]

            if True in np.isin(offspring_1, all_elements_1) or \
                    True in np.isin(offspring_2, all_elements_2):
                offspring_1 = np.setdiff1d(offspring_1,all_elements_1)
                offspring_2 = np.setdiff1d(offspring_2,all_elements_2)





        else:
            offspring_1 = parent_1
            offspring_2 = parent_2

        offspring_1 = np.concatenate([start_parent_1, offspring_1, end_parent_1])
        offspring_2 = np.concatenate([start_parent_2, offspring_2, end_parent_2])

        return offspring_1.astype(int), offspring_2.astype(int)

    def PMX_3(self, parent_1_tmp, parent_2_tmp, all_elements_1, all_elements_2):

        start_parent_1 = np.array([parent_1_tmp[0]])
        end_parent_1 = np.array([parent_1_tmp[-1]])
        start_parent_2 = np.array([parent_2_tmp[0]])
        end_parent_2 = np.array([parent_2_tmp[-1]])

        parent_1 = np.delete(parent_1_tmp, [0, parent_1_tmp.size - 1])
        parent_2 = np.delete(parent_2_tmp, [0, parent_2_tmp.size - 1])

        all_elemnts = np.unique(np.concatenate([parent_1, parent_2]))

        if parent_1.size > 1 and parent_2.size > 1:

            self.__point_mutation(parent_1, parent_2)
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


            elements_1_teste = np.setdiff1d(all_elemnts, all_elements_1)
            elements_1_teste = np.setdiff1d(elements_1_teste, offspring_1)


            if elements_1_teste.size == 0:
                offspring_1 = offspring_1[offspring_1 !=-1]
            elif elements_1_teste.size < offspring_1[offspring_1 == -1].size:
                try:
                    indixes = np.where(offspring_1 == -1)[0]
                    offspring_1[indixes[:elements_1_teste.size]] = elements_1_teste
                    offspring_1 = offspring_1[offspring_1 !=-1]
                except:
                    print(indixes, elements_1_teste, offspring_1)
                    raise
            else:
                offspring_1[offspring_1 == -1] = elements_1_teste[:offspring_1[offspring_1 == -1].size]

            elements_2_teste = np.setdiff1d(all_elemnts, all_elements_2)
            elements_2_teste = np.setdiff1d(elements_2_teste, offspring_2)

            if elements_2_teste.size == 0:
                offspring_2 = offspring_2[offspring_2 !=-1]
            elif elements_2_teste.size < offspring_2[offspring_2 == -1].size:
                try:
                    indixes = np.where(offspring_2 == -1)[0]
                    offspring_2[indixes[:elements_2_teste.size]] = elements_2_teste
                    offspring_2 = offspring_2[offspring_2 != -1]
                except:
                    print(indixes, elements_2_teste, offspring_2)
                    raise
            else:
                offspring_2[offspring_2 == -1] = elements_2_teste[:offspring_2[offspring_2 == -1].size]

        else:
            offspring_1 = parent_1
            offspring_2 = parent_2

        if np.intersect1d(all_elements_1, offspring_1).size > 0:
            offspring_1 = offspring_1[np.isin(offspring_1, all_elements_1, invert=True)]

        if np.intersect1d(all_elements_2, offspring_2).size > 0:
            offspring_2 = offspring_2[np.isin(offspring_2, all_elements_2, invert=True)]

        offspring_1 = np.concatenate([start_parent_1, offspring_1, end_parent_1])
        offspring_2 = np.concatenate([start_parent_2, offspring_2, end_parent_2])

        return offspring_1.astype(int), offspring_2.astype(int)


    def OX(self, parent_1, parent_2):

        start = np.array([parent_1[0]])
        end = np.array([parent_1[-1]])

        if parent_1.size > parent_2.size:
            parent_tmp_1 = np.delete(parent_2, [0, parent_2.size-1])
            parent_tmp_2 = np.delete(parent_1, [0, parent_1.size-1])
        else:
            parent_tmp_1 = np.delete(parent_1, [0, parent_1.size-1])
            parent_tmp_2 = np.delete(parent_2, [0, parent_2.size-1])

        self.__point_mutation(parent_tmp_1, parent_tmp_2)

        offspring_1 = np.ones(parent_tmp_2.size).astype(int) * np.nan
        offspring_2 = np.ones(parent_tmp_1.size).astype(int) * np.nan

        offspring_1[self.I:self.J] = parent_tmp_1[self.I:self.J]
        offspring_2[self.I:self.J] = parent_tmp_2[self.I:self.J]

        copy_ordend_parent_1 = np.ones(parent_tmp_1.size)
        copy_ordend_parent_1 = np.concatenate([parent_tmp_1[self.J:],parent_tmp_1[:self.J]])
        copy_ordend_parent_2 = np.ones(parent_tmp_2.size)
        copy_ordend_parent_2 = np.concatenate([parent_tmp_2[self.J:],parent_tmp_2[:self.J]])

        index_parent_2 = np.array(list(range(self.J, parent_tmp_2.size)) + list(range(self.J)))

        index_parent_1 = np.array(list(range(self.J, parent_tmp_1.size)) + list(range(self.J)))

        all = np.concatenate([parent_tmp_1, parent_tmp_2])
        all = self.removed_citys_repeat(all)

        x_teste = np.isin(parent_tmp_2, offspring_1, invert=True)


        j = 0
        for i in index_parent_2:
            if j >= (copy_ordend_parent_2.size - 1):
                break
            while copy_ordend_parent_2[j] in offspring_1:
                if j >= (copy_ordend_parent_2.size - 1):
                    break
                j += 1

            if i < self.I or i >= self.J:
                offspring_1[i] = copy_ordend_parent_2[j]
                j += 1

        j = 0
        for i in index_parent_1:
            if j >= (copy_ordend_parent_1.size - 1):
                break
            while copy_ordend_parent_1[j] in offspring_2:
                if j >= (copy_ordend_parent_2.size - 1):
                    break
                j += 1

            if i < self.I or i >= self.J:
                offspring_2[i] = copy_ordend_parent_1[j]
                j += 1

        elements_fault1 = np.isin(parent_tmp_2,offspring_1, invert=True)
        elements_fault = parent_tmp_2[elements_fault1]
        # elements_fault = np.isin(elements_fault,offspring_2, invert=True)
        # elements_fault = all[elements_fault]

        idx = np.isnan(offspring_1)
        offspring_1[idx] = elements_fault[:np.sum(idx)]


        elements_fault1 = np.isin(parent_tmp_1,offspring_2, invert=True)
        elements_fault = parent_tmp_1[elements_fault1]
        idx = np.isnan(offspring_2)
        offspring_2[idx] = elements_fault[:np.sum(idx)]



        offspring_1 = np.concatenate([start, offspring_1, end])
        offspring_2 = np.concatenate([start, offspring_2, end])
        #
        # x =  np.isnan(offspring_1).any()
        # if x:
        #     print('aqui')
        #
        # x =  np.isnan(offspring_2).any()
        # if x:
        #     print('aqui')


        return offspring_1.astype(int), offspring_2.astype(int)

    def cross_TOP(self, parent_1, parent_2, function_objective):
        start = np.array([parent_1[0][0]])
        end = np.array([parent_1[0][-1]])

        cousts_route_1 = np.array([function_objective(value) for value in parent_1])
        cousts_route_2 = np.array([function_objective(value) for value in parent_2])

        parent_1_tmp = [ np.delete(value,[0, value.size-1]) for value in parent_1]
        parent_2_tmp = [ np.delete(value,[0, value.size-1]) for value in parent_2]


        ind_min_coust_1 = np.argmin(cousts_route_1)
        ind_min_coust_2 = np.argmin(cousts_route_2)

        ind_max_coust_1 = np.argmax(cousts_route_1)
        ind_max_coust_2 = np.argmax(cousts_route_2)

        offspring_1 = [val for val in parent_1_tmp]

        tmp = parent_2_tmp[ind_min_coust_2]
        for x in offspring_1:
            c = np.isin(tmp, x, invert=True)
            tmp = tmp[c]

        offspring_1.append(tmp)

        offspring_1 = [np.concatenate([start, val, end]) for val in offspring_1]
        cousts_route_1 = np.array([function_objective(value) for value in offspring_1])

        indexes_tmp = np.argsort(cousts_route_1)
        size = len(parent_1)
        offspring_1 = [ offspring_1[val] for val in indexes_tmp[:size]]

        # offspring_1 = [np.copy(parent_1_tmp[ind_min_coust_1])]
        #
        # for n in np.arange(len(parent_2_tmp)):
        #     if n!= ind_max_coust_2:
        #         tmp = parent_2_tmp[n]
        #         for x in offspring_1:
        #             c = np.isin(tmp, x, invert=True)
        #             tmp = tmp[c]
        #
        #         # contais_2 = np.isin(parent_1_tmp[n], offspring_2[0], invert=True)
        #         offspring_1.append(tmp)
        #
        # offspring_1 = [np.concatenate([start, val, end]) for val in offspring_1]

        offspring_2 = [val for val in parent_2_tmp]

        tmp = parent_1_tmp[ind_min_coust_1]
        for x in offspring_2:
            c = np.isin(tmp, x, invert=True)
            tmp = tmp[c]

        offspring_2.append(tmp)

        offspring_2 = [np.concatenate([start, val, end]) for val in offspring_2]
        cousts_route_2 = np.array([function_objective(value) for value in offspring_2])

        indexes_tmp = np.argsort(cousts_route_2)

        offspring_2 = [ offspring_2[val] for val in indexes_tmp[:size]]

        # offspring_2 = [np.copy(parent_2_tmp[ind_min_coust_2])]
        #
        # for n in np.arange(len(parent_1_tmp)):
        #     if n!= ind_max_coust_1:
        #         tmp = parent_1_tmp[n]
        #         for x in offspring_2:
        #             c = np.isin(tmp, x, invert=True)
        #             tmp = tmp[c]
        #
        #         # contais_2 = np.isin(parent_1_tmp[n], offspring_2[0], invert=True)
        #         offspring_2.append(tmp)
        #
        # offspring_2 = [np.concatenate([start, val, end]) for val in offspring_2]

        return offspring_1, offspring_2

    def cross_TOPMD(self, parent_1, parent_2, function_objective):
        start = np.array([deposit_start[0] for deposit_start in parent_1])
        end = np.array([deposit_start[-1] for deposit_start in parent_1])

        cousts_route_1 = np.array([function_objective(value) for value in parent_1])
        cousts_route_2 = np.array([function_objective(value) for value in parent_2])

        parent_1_tmp = [np.delete(value, [0, value.size - 1]) for value in parent_1]
        parent_2_tmp = [np.delete(value, [0, value.size - 1]) for value in parent_2]

        ind_min_coust_1 = np.argmin(cousts_route_1)
        ind_min_coust_2 = np.argmin(cousts_route_2)


        ind_max_coust_1 = np.argmax(cousts_route_1)
        ind_max_coust_2 = np.argmax(cousts_route_2)

        offspring_1 = [val for val in parent_1_tmp]

        tmp = parent_2_tmp[ind_min_coust_2]
        for x in offspring_1:
            c = np.isin(tmp, x, invert=True)
            tmp = tmp[c]

        offspring_1[ind_max_coust_1] = np.copy(tmp)

        offspring_1 = [np.concatenate([[start[idx]], offspring_1[idx], [end[idx]]]) for idx in range(len(offspring_1))]
        cousts_route_1 = np.array([function_objective(value) for value in offspring_1])

        offspring_2 = [val for val in parent_2_tmp]

        tmp = parent_1_tmp[ind_min_coust_1]
        for x in offspring_2:
            c = np.isin(tmp, x, invert=True)
            tmp = tmp[c]

        offspring_2[ind_max_coust_2] = np.copy(tmp)

        offspring_2 = [np.concatenate([[start[idx]], offspring_2[idx], [end[idx]]]) for idx in range(len(offspring_2))]
        cousts_route_2 = np.array([function_objective(value) for value in offspring_2])

        return offspring_1, offspring_2

    def cross_teste(self, parent_1, parent_2, function_objective):
        costs_p1 = [function_objective(i) for i in parent_1]
        costs_p2 = [function_objective(i) for i in parent_2]

        ind_min_1 = np.argmin(costs_p1)
        # ind_min_2 = np.argmin(costs_p2)

        point = ind_min_1

        all_elements_1 = np.array(parent_1[ind_min_1][1:-1])
        all_elements_2 = np.array(parent_2[ind_min_1][1:-1])
        for i in range(len(parent_1)):
            if i != point:
                ind = np.isin(all_elements_1, parent_1[i], invert=True)
                parent_1[i] = parent_1[i][ind]
                all_elements_1 = np.unique(np.concatenate([all_elements_1, parent_1[i][1:-1]]))


                ind = np.isin(all_elements_2, parent_2[i], invert=True)
                parent_2[i] = parent_2[i][ind]
                all_elements_2 = np.unique(np.concatenate([all_elements_2, parent_2[i][1:-1]]))

        return  parent_1, parent_2



if __name__ == '__main__':
    start = np.array([0])
    end = np.array([30])
    tmp1 = np.random.choice(np.arange(1,21),20, replace=False)
    tmp2 = np.random.choice(np.arange(1,21),20, replace=False)
    parent_1 = np.concatenate([start,tmp1,end])
    parent_2 = np.concatenate([start,tmp2,end])

    corssover = Crossover()

    x,y = corssover.OX(parent_1, parent_2)

    print(parent_1, parent_2)
    print(x,y)
    print(corssover.I, corssover.J)