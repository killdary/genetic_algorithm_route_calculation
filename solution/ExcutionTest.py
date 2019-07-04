from GA_TOPMD import GaTopMd
import gc

paths = [
    # 'GATOPMD/path_2.txt',
    # 'GATOPMD/path_2.txt',
    # 'GATOPMD/path_2.txt',
    # 'GATOPMD/path_2.txt',
    # 'GATOPMD/path_2.txt',
    # 'GATOPMD/path_3.txt',
    # 'GATOPMD/path_3.txt',
    # 'GATOPMD/path_3.txt',
    # 'GATOPMD/path_3.txt',
    # 'GATOPMD/path_3.txt',
    'GATOPMD/path_4.txt',
    'GATOPMD/path_4.txt',
    'GATOPMD/path_4.txt',
    'GATOPMD/path_4.txt',
    'GATOPMD/path_4.txt',
    'GATOPMD/path_4.txt'
]

prizes = [
    # 'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_3.txt',
    # 'GATOPMD/prize_3.txt',
    # 'GATOPMD/prize_3.txt',
    # 'GATOPMD/prize_3.txt',
    # 'GATOPMD/prize_3.txt',
    'GATOPMD/prize_4.txt',
    'GATOPMD/prize_4.txt',
    'GATOPMD/prize_4.txt',
    'GATOPMD/prize_4.txt',
    'GATOPMD/prize_4.txt',
    'GATOPMD/prize_4.txt'
]

size_population = [200,
                   200,
                   200,
                   200,
                   200,
                   # 300,
                   # 300,
                   # 300,
                   # 300,
                   # 300,
                   # 350,
                   # 350,
                   # 350,
                   # 350,
                   # 350
                   ]

costs=[
    # [30,30],
    # [15,10],
    # [20,15],
    # [10,10],
    # [20,20],
    # [25, 27, 27],
    # [20, 19, 18],
    # [20, 15, 25],
    # [5, 10, 12],
    # [10, 11, 12],
    [40, 40, 40],
    [25,27, 28, 30],
    [20,20, 20, 20],
    [15,5, 12, 20],
    [10,11, 12, 13],
    [20,5, 15, 25]
]

points_init = [
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    [0,1,2],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3]
]

points_end = [
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    # [0,1,2],
    [0,1,2],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3],
    [0,1,2,3]
]

number_executions = 5

for i in range(len(paths)):
    name = 'path_'+str(i+1)
    path_current = paths[i]
    prize_current = prizes[i]

    cost_current = costs[i]

    current_init = points_init[i]
    current_end = points_end[i]

    ga_execution = GaTopMd(
        generation = 1000,
        population = 300,
        limit_population = 50,
        crossover_rate = 0.8,
        mutation_rate = 0.8,
        cost_rate = 5,
        prizes_rate = 2,
        map_points = path_current,
        prizes = prize_current,
        max_cost= cost_current,
        start_point = current_init,
        end_point = current_end)

    with open('./GATOPMD/ResultWindows/Results_Execution.txt', 'a+') as out:
        out.write('Cenario: ' + path_current + '\n')

    print('Cenario: ' + path_current + '\n')
    for numberExecution in range(number_executions):
        print('####### Inicio Execucao: '+str(numberExecution))
        bestElementsCosts, bestElements, bestElementGenaration = ga_execution.run()

        with open('./GATOPMD/ResultWindows/Results_Execution_' + name + '.txt', 'a+') as out:
            out.write(' - Execucao ' + str(numberExecution) + '\n')
            out.write(' -- BestCostGenaration: ' + str(bestElementGenaration) + '\n')
            out.write(' -- BestCostElement: ' + str(bestElementsCosts) + '\n')
            out.write(' -- BestRoute: ' + str(bestElements[0]) + '\n')
            out.write(' -- Custo: \n')
            custo = 0
            for j in range(len(bestElements[i])):
                out.write(' ---------' + str(ga_execution.mensureCost(bestElements[i][j])) + '\n')
                custo = custo + ga_execution.mensureCost(bestElements[i][j])
            out.write(' ---- Total: '+str(custo)+'\n')

            out.write(' -- Premio: \n')
            premio = 0
            for j in range(len(bestElements[i])):
                out.write(' ---------' + str(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())+ '\n')
                premio = premio + ga_execution.prizes.take(bestElements[i][j].astype(int)).sum()
            out.write(' ---- Total: '+str(premio)+'\n')

        for i in range(1):
            print('custo')
            for j in range(len(bestElements[i])):
                print(ga_execution.mensureCost(bestElements[i][j]))
            print(' - ')
            for j in range(len(bestElements[i])):
                print(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())
            ga_execution.plota_rotas_TOP(cidades=ga_execution.map_points, rota = bestElements[i], file_plot=True,
                                          name_file_plot='./GATOPMD/ResultWindows/Plot_Path_'+ name+'_execution_'+ str(numberExecution))

        print('####### Fim Execucao: '+str(numberExecution))

    gc.collect()