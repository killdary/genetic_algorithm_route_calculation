from GA_TOPMD import GaTopMd


paths = [
    'GATOPMD/path_2.txt',
    # 'GATOPMD/path_3.txt',
    # 'GATOPMD/path_4.txt'
]

prizes = [
    'GATOPMD/prize_2.txt',
    # 'GATOPMD/prize_3.txt',
    # 'GATOPMD/prize_4.txt'
]

costs=[
    [20,20],
    # [25,30, 35],
    # [25,30, 35, 40]
]

points_init = [
    [0,1],
    # [0,1,2],
    # [0,1,2,3]
]

points_end = [
    [0,1],
    # [0,1,2],
    # [0,1,2,3]
]

number_executions = 10

for i in range(len(paths)):
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

    with open('./GATOPMD/Result/Results_Execution.txt', 'a+') as out:
        out.write('Cenario: ' + path_current + '\n')

    for numberExecution in range(number_executions):
        print('####### Inicio Execucao: '+str(numberExecution))
        bestElementsCosts, bestElements, bestElementGenaration = ga_execution.run()

        with open('./GATOPMD/Result/Results_Execution.txt', 'a+') as out:
            out.write(' - Execucao ' + str(numberExecution) + '\n')
            out.write(' - BestCostGenaration: ' + str(bestElementGenaration) + '\n')
            out.write(' - BestCostElement: ' + str(bestElementsCosts) + '\n')
            out.write(' - BestRoute: ' + str(bestElements) + '\n')
            out.write(' - Premio: \n')
            for j in range(len(bestElements[i])):
                out.write(' ---------' + str(ga_execution.mensureCost(bestElements[i][j])) + '\n')

            out.write(' - Custo: \n')
            for j in range(len(bestElements[i])):
                out.write(' ---------' + str(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())+ '\n')

        for i in range(1):
            print('custo')
            for j in range(len(bestElements[i])):
                print(ga_execution.mensureCost(bestElements[i][j]))
            print(' - ')
            for j in range(len(bestElements[i])):
                print(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())
            ga_execution.plota_rotas_TOP(cidades=ga_execution.map_points, rota = bestElements[i], file_plot=True,
                                          name_file_plot='./GATOPMD/Result/PlotExecution_' + str(numberExecution))

        print('####### Fim Execucao: '+str(numberExecution))