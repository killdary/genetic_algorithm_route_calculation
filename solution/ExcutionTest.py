from GA_TOPMD import GaTopMd
import gc
from datetime import datetime
import os
import re

paths = [
     # 'GATOPMD/path_2.txt',
     # 'GATOPMD/path_2.txt',
     # 'GATOPMD/path_2.txt',
     # 'GATOPMD/path_2.txt',
     # 'GATOPMD/path_2.txt',
     # 'GATOPMD/path_2.txt',
     # #
     # 'GATOPMD/path_3.txt',
     # 'GATOPMD/path_3.txt',
     # 'GATOPMD/path_3.txt',
     # 'GATOPMD/path_3.txt',
     # 'GATOPMD/path_3.txt',
     # 'GATOPMD/path_3.txt',

    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/mapas/novas_cidades_6.txt',
    # 'GATOPMD/path_4.txt',
    # 'GATOPMD/path_4.txt',
    # 'GATOPMD/path_4.txt',
    # 'GATOPMD/path_4.txt',
    # 'GATOPMD/path_4.txt',
    # 'GATOPMD/path_4.txt'

    # 'GATOPMD/mapas/artigo/mapa_4r_12_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_12_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_12_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_12_1d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_25_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_30_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_35_1d.txt',
    # 'GATOPMD/mapas/artigo/mapa_4r_35_1d.txt',
]

prizes = [
     # 'GATOPMD/prize_2.txt',
     # 'GATOPMD/prize_2.txt',
     # 'GATOPMD/prize_2.txt',
     # 'GATOPMD/prize_2.txt',
     # 'GATOPMD/prize_2.txt',
     # 'GATOPMD/prize_2.txt',
     #
     # 'GATOPMD/prize_3.txt',
     # 'GATOPMD/prize_3.txt',
     # 'GATOPMD/prize_3.txt',
     # 'GATOPMD/prize_3.txt',
     # 'GATOPMD/prize_3.txt',
     # 'GATOPMD/prize_3.txt',

    # 'GATOPMD/mapas/novos_premios_6.txt',
    # 'GATOPMD/mapas/novos_premios_6.txt',
    # 'GATOPMD/mapas/novos_premios_6.txt',
    # 'GATOPMD/mapas/novos_premios_6.txt',
    # 'GATOPMD/mapas/novos_premios_6.txt',
    # 'GATOPMD/mapas/novos_premios_6.txt',

    # 'GATOPMD/prize_4.txt',
    # 'GATOPMD/prize_4.txt',
    # 'GATOPMD/prize_4.txt',
    # 'GATOPMD/prize_4.txt',
    # 'GATOPMD/prize_4.txt',
    # 'GATOPMD/prize_4.txt'

    # 'GATOPMD/mapas/artigo/premio_12.txt',
    # 'GATOPMD/mapas/artigo/premio_12.txt',
    # 'GATOPMD/mapas/artigo/premio_12.txt',
    # 'GATOPMD/mapas/artigo/premio_12.txt',
    # 'GATOPMD/mapas/artigo/premio_4r_12_1d.txt',
    'GATOPMD/mapas/artigo/premio_4r_40_1d.txt',
    # 'GATOPMD/mapas/artigo/premio_4r_25_1d.txt',
    # 'GATOPMD/mapas/artigo/premio_4r_30_1d.txt',
    # 'GATOPMD/mapas/artigo/premio_4r_35_1d.txt',
    # 'GATOPMD/mapas/artigo/premio_4r_35_1d.txt',
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
    # [80],
    # [200],
    # [120],
    # [28,30],
    # [15,10],
    # [20,15],
    # [10,12],
    # [20,10],
    # #
    # [30, 40],
    # [30, 30, 30],
    # [20, 19, 18],
    # [20, 15, 25],
    # [5, 10, 12],
    # [10, 11, 12],
    # #
    # [130],
    # [50, 50],
    # [30,30,45],
    # [30,30,30,30],
    # [15,20,25,30],
    # [15,5, 12, 20],
    # [10,11, 12, 13],
    # [20,5, 15, 25]
    # [20,21,22,23,20,21,22,23],
    # [40,45],
    # [35,40],
    # [40,40,40],
    # [35,40,45,50],
    # [11,10,11,10]

    # [60],
    # [15,25,20],
    # [20,20,20,20],
    # [14,16,16,18],
    # [18,23,18,18],
    # [28,24,26,25],
    # [28,26,28,26],
    # [26,27,34,28],
    # [24,25,26,28],
    [35]*4,

]

points_init = [
     # [0],
     # [0,1],
     # [0,1],
     # [0,1],
     # [0,1],
     # [0,1],
     #
     # [1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],

     # [0,1,2],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3]
    # [0,0,0,0,0,0,0,0],
    # [0],
    # [0,0],
    # [0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],

    # [0,0,0,0],
    # # [0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],
    [0,0,0,0]

]

points_end = [
     # [0],
     # [0,1],
     # [0,1],
     # [0,1],
     # [0,1],
     # [0,1],
     #
     # [1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],
     # [0,1,2],

     # [0,1,2],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3],
     # [0,1,2,3]
    # [2,4,40,37],
    # [1,2,3,4],
    # [1,2,3,4],
    # [1,2,3,4],
    # [1,2,3,4],
    # [4,2,37,40],
    # [2,37],
    # [2,4,37],
    # [2,4,40,37],
    # [2,4,40,37],
    # [0],
    # [1,2,3],
    # [1,2,3,4],
    # [1,2,3,4],
    [1,2,3,4],
]


deposits = [
    # [0,1,2,3,4],
    # [0,1,2,3,4],
    # [0,1,2,3,4],
    # [0,1,2,3,4],
    # [0,1,2,3,4],
    # [0,1,2,3,4],
    # [0,4,2,37,40],
    # [0,1,2,3,4],
    [0,1,2,3,4],
]
number_executions = 15

main_path='./GATOPMD/Result/'
data = datetime.now()
execucao = str(data.strftime(("%d-%m-%Y_%H-%M-%S_execucao")))

result_folder = main_path+''+execucao
    
os.mkdir(result_folder)

print(os.getcwd())

for i in range(len(paths)):
    name = 'path_'+str(i+1)
    path_current = paths[i]
    prize_current = prizes[i]

    cost_current = costs[i]

    current_init = points_init[i]
    current_end = points_end[i]
    current_deposits = deposits[i]

    ga_execution = GaTopMd(
        generation = 1000,
        population = 210,
        limit_population = 25,
        crossover_rate = .8,
        mutation_rate = .3,
        cost_rate = 5,
        prizes_rate = 2,
        map_points = path_current,
        prizes = prize_current,
        max_cost= cost_current,
        start_point = current_init,
        end_point = current_end,
        depositos = current_deposits)
    
    folder_cenary = result_folder+'/results_'+re.findall('([\w]+)\.', path_current)[0]
    if not os.path.exists(folder_cenary):
        os.mkdir(folder_cenary)

    with open(folder_cenary+'/Results_Execution.txt', 'a+') as out:
        out.write('Cenario: ' + path_current + '\n')

    print('Cenario: ' + path_current + '\n')
    for numberExecution in range(number_executions):
        print('####### Inicio Execucao: '+str(numberExecution))
        bestElementsCosts, bestElements, bestElementGenaration, bestElementAlways = ga_execution.run()
        #
        # with open(folder_cenary+'/Results_Execution_' + name + '.txt', 'a+') as out:
        #     out.write(' - Execucao ' + str(numberExecution) + '\n')
        #     out.write(' -- BestCostGenaration: ' + str(bestElementGenaration) + '\n')
        #     out.write(' -- BestCostElement: ' + str(bestElementsCosts) + '\n')
        #     out.write(' -- BestRoute: ' + str(bestElements[0]) + '\n')
        #     out.write(' -- Custo: \n')
        #     custo = 0
        #     for j in range(len(bestElements[0])):
        #         out.write(' ---------' + str(ga_execution.mensureCost(bestElements[0][j])) + '\n')
        #         custo = custo + ga_execution.mensureCost(bestElements[0][j])
        #     out.write(' ---- Total: '+str(custo)+'\n')
        #
        #     out.write(' -- Premio: \n')
        #     premio = 0
        #     for j in range(len(bestElements[i])):
        #         out.write(' ---------' + str(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())+ '\n')
        #         premio = premio + ga_execution.prizes.take(bestElements[i][j].astype(int)).sum()
        #     out.write(' ---- Total: '+str(premio)+'\n')

        with open(folder_cenary+'/Results_Execution_melhor_elemento' + name + '.txt', 'a+') as out:
            out.write(' - Execucao ' + str(numberExecution) + '\n')
            out.write(' -- BestCostGenaration: ' + str(bestElementGenaration) + '\n')
            out.write(' -- BestCostElement: ' + str(bestElementsCosts) + '\n')
            out.write(' -- BestRoute: ' + str(bestElementAlways) + '\n')
            out.write(' -- Custo: \n')
            custo = 0
            for j in range(len(bestElementAlways)):
                out.write(' ---------' + str(ga_execution.mensureCost(bestElementAlways[j])) + '\n')
                custo = custo + ga_execution.mensureCost(bestElementAlways[j])
            out.write(' ---- Total: '+str(custo)+'\n')

            out.write(' -- Premio: \n')
            premio = 0
            for j in range(len(bestElementAlways)):
                out.write(' ---------' + str(ga_execution.prizes.take(bestElementAlways[j].astype(int)).sum())+ '\n')
                premio = premio + ga_execution.prizes.take(bestElementAlways[j].astype(int)).sum()
            out.write(' ---- Total: '+str(premio)+'\n')

        with open(folder_cenary+'/Results_Execution_melhor_elemento_custo_premio' + name + '.csv', 'a+') as out:
            valor = ga_execution.reply_method_top(ga_execution.FO,bestElementAlways).sum()
            custo = 0
            for j in range(len(bestElementAlways)):
                out.write(str(ga_execution.mensureCost(bestElementAlways[j])) + ';')
                custo = custo + ga_execution.mensureCost(bestElementAlways[j])
            out.write(str(custo)+';')

            premio = 0
            for j in range(len(bestElementAlways)):
                out.write(str(ga_execution.prizes.take(bestElementAlways[j].astype(int)).sum())+ ';')
                premio = premio + ga_execution.prizes.take(bestElementAlways[j].astype(int)).sum()
            out.write(str(premio)+'\n')

        #
        # for i in range(1):
        #     print('custo')
        #     for j in range(len(bestElements[i])):
        #         print(ga_execution.mensureCost(bestElements[i][j]))
        #     print(' - ')
        #     for j in range(len(bestElements[i])):
        #         print(ga_execution.prizes.take(bestElements[i][j].astype(int)).sum())
        #     ga_execution.plota_rotas_TOP(cidades=ga_execution.map_points, rota = bestElements[i], file_plot=True,
        #                                   name_file_plot=result_folder+'/Plot_Path_'+ name+'_execution_'+ str(numberExecution))

        for j in range(len(bestElementAlways)):
            print(ga_execution.mensureCost(bestElementAlways[j]))
        print(' - ')
        for j in range(len(bestElementAlways)):
            print(ga_execution.prizes.take(bestElementAlways[j].astype(int)).sum())
        ga_execution.plota_rotas_TOP(cidades=ga_execution.map_points, rota=bestElementAlways, file_plot=True,
                                     name_file_plot=folder_cenary + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         numberExecution))

        print('####### Fim Execucao: '+str(numberExecution))

    del ga_execution

    gc.collect()