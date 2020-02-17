from GA_TOPMD import GaTopMd
from PSO_TOP import PSO
import gc
from datetime import datetime
import os
import re
import numpy as np

paths = [

    'GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',

]

prizes = [
    'GATOPMD/mapas/artigo/premio_4r_40_1d.txt',
]

size_population = [.1,
                   ]

costs = [
    [20, 23, 25, 30],
]

points_init = [
    [0, 0, 0, 0],

]

points_end = [
    [0, 0, 0, 0],
]

deposits = [
    [0, 1, 2, 3, 4],
]
number_executions = 30

main_path = './GATOPMD/Result/'
data = datetime.now()
execucao = str(data.strftime(("%d-%m-%Y_%H-%M-%S_execucao")))

result_folder = main_path + '' + 'grafico'

os.mkdir(result_folder)

print(os.getcwd())

for i in range(len(paths)):
    name = 'path_' + str(i + 1)
    path_current = paths[i]
    prize_current = prizes[i]

    cost_current = costs[i]

    current_init = points_init[i]
    current_end = points_end[i]
    current_deposits = deposits[i]
    population_current = size_population[i]

    # ga_execution = GaTopMd(
    #     generation=1000,
    #     population=100,
    #     limit_population=20,
    #     crossover_rate= .6,
    #     mutation_rate=.8,
    #     cost_rate=2,
    #     prizes_rate=5,
    #     map_points=path_current,
    #     prizes=prize_current,
    #     max_cost=cost_current,
    #     start_point=current_init,
    #     end_point=current_end,
    #     depositos=current_deposits)


    folder_cenary = result_folder + '/results_' + re.findall('([\w]+)\.', path_current)[0]
    folder_chart = folder_cenary+'/charts'+name
    if not os.path.exists(folder_cenary):
        os.mkdir(folder_cenary)

    if not os.path.exists(folder_chart):
        os.mkdir(folder_chart)

    with open(folder_cenary + '/Results_Execution.txt', 'a+') as out:
        out.write('Cenario: ' + path_current + '\n')

    print('Cenario: ' + path_current + '\n')

    with open(folder_cenary + '/Results_Execution_melhor_elemento_custo_premio.csv', 'a+') as out:
        out.write(name + '\n')

    for numberExecution in range(number_executions):

        pso_execution = PSO(
            iterations=1,
            size_population=1,
            beta=.3,
            alfa=.8,
            cost_rate=2,
            prizes_rate=5,
            map_points=path_current,
            prizes=prize_current,
            max_cost=cost_current,
            start_point=current_init,
            end_point=current_end,
            depositos=current_deposits)

        print('####### Inicio Execucao: ' + str(numberExecution))

        gbest, primeiro, ultimo = pso_execution.run()









        mapaa = list()
        mapaa.append(np.fromstring('0, 19, 18, 12, 11, 7, 8, 13, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 20, 14, 9, 5, 15, 16, 21, 24, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 28, 29, 27, 34, 33, 37, 41, 38, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 25, 31, 32, 26, 40, 39, 43, 44, 36, 30, 0', dtype=int, sep=','))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         1))

        mapaa = list()
        mapaa.append(np.fromstring('0, 35, 38, 41, 37, 34, 27, 29, 28, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 13, 8, 7, 11, 6, 12, 23, 18, 19, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 30, 36, 44, 43, 39, 40, 26, 32, 31, 25, 0', dtype=int, sep=','))
        mapaa.append(np.fromstring('', dtype=int, sep=','))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         2))

        mapaa = list()
        mapaa.append(np.fromstring('0, 23, 18, 19, 13, 8, 7, 11, 12, 6, 1', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 20, 14, 9, 5, 15, 16, 21, 17, 10, 2', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 28, 35, 42, 41, 38, 34, 29, 27, 33, 37, 3', dtype=int, sep=','))
        mapaa.append(np.fromstring('0, 25, 24, 26, 32, 31, 30, 36, 44, 43, 39, 40, 4', dtype=int, sep=','))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         3))


        mapaa = list()
        mapaa.append(np.fromstring('0 14  9  5 15 20  0', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 13  7 11  6 12 18 19  0', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 28 29 34 38 41 37 33 27  0', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 30 31 43 39 40 26 25 24  0', dtype=int, sep=' '))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         4))


        mapaa = list()
        mapaa.append(np.fromstring('0 13  7 11  6 12 18 19  0', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 28 29 34 38 41 37 33 27  0', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 30 44 43 39 40 26 31 25  0', dtype=int, sep=' '))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         5))



        mapaa = list()
        mapaa.append(np.fromstring('0 23 18 19 13  8  7 11 12  6  1', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 24 20 14 15  9  5 10  2', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 28 29 27 34 38 42 41 37  3', dtype=int, sep=' '))
        mapaa.append(np.fromstring('0 25 26 31 30 36 43 39 40  4', dtype=int, sep=' '))

        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=mapaa, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         6))

        print('####### Fim Execucao: ' + str(numberExecution))

    del pso_execution

    gc.collect()