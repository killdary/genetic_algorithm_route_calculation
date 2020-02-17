import numpy as np
import matplotlib.pyplot as plt
from Mutation import Mutation
from FunctionObjective import FunctionObjective
from Crossover import Crossover
from Population import Population
from Selection import Selection
import copy, sys, random
from operator import attrgetter


def calculate_distances(map_points):
    size = map_points.shape[0]
    distances = np.zeros([size, size])

    temp_max = 0

    for i in range(size):
        for j in range(size):
            if i != j:
                b = map_points[i, 0] - map_points[j, 0]
                c = map_points[i, 1] - map_points[j, 1]
                a = np.sqrt(np.square(b) + np.square(c))

                distances[i, j] = a
                distances[j, i] = a

                if temp_max < a:
                    temp_max = a

    return distances


def reply_method_mutation_top(method, chromossome, sizeMut=0):
    size = len(chromossome)
    size_mut_genes = sizeMut
    if sizeMut == 0:
        size_mut_genes = size

    result = [0] * size

    rand = np.arange(size)
    np.random.shuffle(rand)
    rand = rand[:size_mut_genes]

    for n in np.arange(size):
        if n in rand:
            if chromossome[n].size > 3:
                result[n] = method(chromossome[n])
            else:
                result[n] = chromossome[n]
        else:
            result[n] = chromossome[n]

    return result


class Particle:
    position: list
    number_robots: int
    cost: np.array([])
    fitness: np.array([])
    finess_total: float

    def __init__(self,route, mensure_function, fitness_function):

        self.solution = route
        x = mensure_function(route[0])

        self.pbest = route

        self.number_robots = len(route)
        self.mensure_function = mensure_function
        self.fitness_function = fitness_function
        self.best_part_pos = [0.0] * self.number_robots

        self.cost = np.array([0]*self.number_robots)
        self.fitness = np.array([0]*self.number_robots)
        self.velocity = [0.0] * self.number_robots
        self.calcCostPath()


    def calcCostPath(self):
        for i in range(self.number_robots):
            self.cost[i] = self.mensure_function(self.pbest[i]).sum()
            self.velocity[i] = self.cost[i]
            self.fitness[i] = self.fitness_function(self.pbest[i]).sum()

        self.finess_total = self.fitness.sum()


    # set pbest
    def setPBest(self, new_pbest):
        self.pbest = new_pbest

    # returns the pbest
    def getPBest(self):
        return self.pbest

    # set the new velocity (sequence of swap operators)
    def setVelocity(self, new_velocity):
        self.velocity = new_velocity

    # returns the velocity (sequence of swap operators)
    def getVelocity(self):
        return self.velocity

    # set solution
    def setCurrentSolution(self, solution):
        self.solution = solution

    # gets solution
    def getCurrentSolution(self):
        return self.solution

    # set cost pbest solution
    def setCostPBest(self, cost):
        self.cost_pbest_solution = cost

    # gets cost pbest solution
    def getCostPBest(self):
        return self.cost_pbest_solution

    # set cost current solution
    def setCostCurrentSolution(self, cost):
        self.cost_current_solution = cost

    # gets cost current solution
    def getCostCurrentSolution(self):
        return self.cost_current_solution

    # removes all elements of the list velocity
    def clearVelocity(self):
        self.velocity = [0]*self.number_robots


class PSO:
    def __init__(self, map_points, iterations, size_population, beta, alfa,
                 cost_rate, prizes_rate, prizes, max_cost,
                 start_point, end_point, depositos=[]):
        self.map_points = np.loadtxt(map_points)
        self.iterations = iterations
        self.size_population = size_population
        self.beta = beta
        self.alfa = alfa
        self.cost_rate = np.array(cost_rate)
        self.prizes_rate = prizes_rate
        self.prizes = np.loadtxt(prizes)[:, 1]
        self.max_cost = np.array(max_cost)
        self.start_point = start_point
        self.end_point = end_point
        self.depositos = depositos

        self.particles = []

        self.number_agents = len(max_cost)

        self.distance = calculate_distances(self.map_points)
        self.functionObject = FunctionObjective(self.map_points, self.prizes)

        self.FO = self.functionObject.FO
        self.mensureCost = self.functionObject.med_custo
        self.methodInsertRemoveChromosome = self.functionObject.coust_insert

        self.allElementsMap = np.arange(self.map_points.shape[0])
        self.allElementsMap = self.allElementsMap[self.number_agents:]

        # removendo depositos
        deposits = [x for x in self.start_point]
        deposits += [x for x in self.end_point if x not in deposits]
        deposits = np.unique(np.array(deposits))
        self.initialChromossome = np.arange(self.map_points.shape[0])
        self.initialChromossome = np.delete(self.initialChromossome, self.depositos)

        self.allElementsMap = np.copy(self.initialChromossome)

        self.mutationObject = Mutation(self.mensureCost, self.max_cost, self.prizes)
        self.mutation = self.mutationObject.scramble

        self.crossoverObject = Crossover()
        self.crossover = self.crossoverObject.cross_TOPMD

        self.PopulationObject = Population(self.start_point, self.end_point, self.mensureCost, self.max_cost,
                                           self.distance)

        self.SelectionObject = Selection()
        self.selection = self.SelectionObject.tournament


        solutions = self.PopulationObject.initializeTopMdGreed2(self.initialChromossome,
                                                                     self.size_population, self.number_agents, 1)

        for s in solutions:
            particle = Particle(route=s, mensure_function=self.mensureCost, fitness_function=self.FO)
            self.particles.append(particle)

    def plota_rotas_TOP(self, cidades, rota, size=12, font_size=20, file_plot=False, name_file_plot='plt'):
        """
        Method to create a chart with the best routes found
        :param cidades: all points of the route300
        :param rota: the sequence with the best route
        :param size: size of the chart
        :param font_size: size of the label of the points
        """

        pos_x = [cidades[val.astype(int), 0] for val in rota]
        pos_y = [cidades[val.astype(int), 1] for val in rota]

        elements = self.map_points[:, 0]
        x = self.map_points[:, 0]
        y = self.map_points[:, 1]

        # cid_nome = range(elements.size)
        cid_nome = self.allElementsMap

        plt.figure(num=None,
                   figsize=(size, size),
                   dpi=80,
                   facecolor='w',
                   edgecolor='k')

        for i in range(len(rota)):
            plt.plot(pos_x[i],
                     pos_y[i],
                     'C' + str(i),
                     lw=5,
                     label='robot ' + str(i + 1),
                     zorder=1)

        plt.rc('font', size=font_size)

        plt.xlabel("X")
        plt.ylabel("Y")

        plt.scatter(self.map_points[cid_nome, 0], self.map_points[cid_nome, 1], s=120, marker="s", zorder=2)

        plt.scatter(self.map_points[self.depositos,0], self.map_points[self.depositos,1], s=150,marker='^', zorder=3, c='black')

        plt.legend(loc='lower left',bbox_to_anchor=(0,1.02,1,0.2),ncol=4, mode='expand')

        # for i, txt in enumerate(cid_nome):
        for i in cid_nome:
            plt.annotate(str(self.prizes[i]), (x[i] - 0.01, y[i] + 0.3), fontsize=font_size)

        # for i, txt in enumerate(cid_nome):
        #     plt.annotate(txt, (x[i] - 0.01, y[i] + 0.3), fontsize=font_size)

        # for i in self.start_point:
        #     plt.annotate('dep.', (x[i] - 0.01, y[i] + 0.3), fontsize=font_size)

        for i in self.depositos:
            plt.annotate('base', (x[i] - 0.01, y[i] + 0.3), fontsize=font_size)

        #        plt.title('Mapa GA')
        # plt.margins(0.05)
        if file_plot:
            plt.savefig(name_file_plot+'.png')
        else:
            plt.show()

    def setGBest(self, new_gbest):
        self.gbest = new_gbest

    # returns gbest (best particle of the population)
    def getGBest(self):
        return self.gbest

    def run(self):

        self.gbest = min(self.particles,  key=attrgetter('finess_total'))
        self.primeiro = self.particles
        for t in range(self.iterations):

            if t%10 == 0:
                print('interation : %d | gbest cost: %f | fitness: %f' % (t, self.gbest.cost.sum(), self.gbest.finess_total))
                print(self.gbest.cost, self.gbest.fitness)

            self.pbest = min(self.particles,  key=attrgetter('finess_total'))

            for ind_p in range(len(self.particles)):
                self.particles[ind_p].clearVelocity()  # cleans the speed of the particle
                temp_velocity = []
                solution_gbest = copy.copy(self.gbest.getPBest())  # gets solution of the gbest
                solution_pbest = self.particles[ind_p].getPBest()[:]  # copy of the pbest solution
                solution_particle = self.particles[ind_p].getCurrentSolution()[
                                    :]  # gets copy of the current solution of the particle

                particle_tmp = self.particles[ind_p]

                self.particles[ind_p].setCurrentSolution = self.mutationObject.insert_points_TOP_2(self.mensureCost,
                                                                         self.methodInsertRemoveChromosome,
                                                                         self.allElementsMap,
                                                                          particle_tmp.getCurrentSolution(),1)
                self.particles[ind_p].calcCostPath()

                # route1, route2 = self.crossoverObject.cross_slice(self.particles[ind_p].getCurrentSolution(),
                #                                                   self.gbest.getCurrentSolution(),
                #                                         self.mensureCost,
                #                                         self.start_point,
                #                                         self.end_point)

                offspring1, offspring2 = list(), list()
                all_elements_1, all_elements_2 = np.array([]), np.array([])
                for i in range(self.particles[ind_p].number_robots):
                    x, y = self.crossoverObject.PMX_3(self.particles[ind_p].getCurrentSolution()[i],
                                                      self.pbest.getCurrentSolution()[i],
                                                      all_elements_1, all_elements_2)

                    all_elements_1 = np.unique(np.concatenate([all_elements_1, x[1:-1]]))
                    all_elements_2 = np.unique(np.concatenate([all_elements_2, y[1:-1]]))

                    offspring1.append(x)
                    offspring2.append(y)

                    route1 = offspring1
                    route2 = offspring2

                route1 = reply_method_mutation_top(self.mutationObject.swap,route1)
                route2 = reply_method_mutation_top(self.mutationObject.swap,route2)

                route1 = reply_method_mutation_top(self.mutationObject.SWGLM,route1)
                route2 = reply_method_mutation_top(self.mutationObject.SWGLM,route2)


                route1 = self.mutationObject.remove_points_TOP(self.mensureCost,
                                                                         self.FO,
                                                                         self.allElementsMap,
                                                                         route1)
                route2 = self.mutationObject.remove_points_TOP(self.mensureCost,
                                                                         self.FO,
                                                                         self.allElementsMap,
                                                                         route2)

                particle_tmp_1 = Particle(route=route1, mensure_function=self.mensureCost, fitness_function=self.FO)
                particle_tmp_2 = Particle(route=route2, mensure_function=self.mensureCost, fitness_function=self.FO)


                flag_1 =  [True for ind in range(particle_tmp_1.number_robots) if particle_tmp_1.cost[ind] > self.max_cost[ind]]
                flag_2 =  [True for ind in range(particle_tmp_2.number_robots) if particle_tmp_2.cost[ind] > self.max_cost[ind]]

                best_particle = None

                if True not in flag_1 and True not in flag_2:
                    best_particle = particle_tmp_2
                    if particle_tmp_1.finess_total < particle_tmp_2.finess_total:
                        best_particle = particle_tmp_1
                elif True not in flag_1:
                    best_particle = particle_tmp_1
                elif True not in flag_2:
                    best_particle = particle_tmp_2

                if best_particle:
                    flag = [True for ind in range(best_particle.number_robots) if best_particle.cost[ind] > self.max_cost[ind]]
                    if self.gbest.finess_total > best_particle.finess_total:
                        if True not in flag:
                            self.gbest = best_particle

                    if best_particle.finess_total < self.particles[ind_p].finess_total:
                        self.particles[ind_p] = best_particle

        self.ultimo = self.particles
        return self.gbest, self.primeiro, self.ultimo

if __name__ == '__main__':
    p = PSO(
        map_points='GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',
        iterations=300,
        size_population=100,
        beta=.3,
        alfa=.8,
        cost_rate=2,
        prizes_rate=5,
        prizes='GATOPMD/mapas/artigo/premio_4r_40_1d.txt',
        # max_cost= [25, 27, 29, 31],
        max_cost=[20, 23, 25, 30],
        start_point=[0, 0, 0, 0,],
        end_point=[0, 0, 0, 0],
        depositos=[0, 1, 2, 3, 4])

    particle = p.run()

    print('gbest cost: %f | fitness: %f' % (particle.cost.sum(), particle.finess_total))
    print(particle.cost, particle.fitness)

    x = 0
    for j in range(len(particle.solution)):
        x = x + p.prizes.take(particle.solution[j].astype(int)).sum()
        print(p.prizes.take(particle.solution[j].astype(int)).sum())

    print(x)
    for i in particle.solution:
        print(i)

    p.plota_rotas_TOP(p.map_points, particle.solution)