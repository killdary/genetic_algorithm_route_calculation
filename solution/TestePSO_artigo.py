from GA_TOPMD import GaTopMd
from PSO_TOP import PSO
import gc
from datetime import datetime
import os
import re

paths = [

    'GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_40_1d.txt',

    'GATOPMD/mapas/artigo/mapa_4r_45_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_45_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_45_5d.txt',

    'GATOPMD/mapas/artigo/mapa_4r_50_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_50_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_50_5d.txt',

    'GATOPMD/mapas/artigo/mapa_4r_60_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_60_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_60_5d.txt',

    'GATOPMD/mapas/artigo/mapa_4r_70_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_70_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_70_5d.txt',

    'GATOPMD/mapas/artigo/mapa_4r_80_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_80_5d.txt',
    'GATOPMD/mapas/artigo/mapa_4r_80_5d.txt',

    # 'GATOPMD/mapas/artigo/mapa_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_40_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_50_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_60_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_50_7d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_60_7d.txt',

    # 'GATOPMD/mapas/artigo/mapa_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_70_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/mapa_5r_80_6d.txt',

    # 'GATOPMD/mapas/artigo/mapa_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_70_7d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/mapa_6r_80_7d.txt',

    # 'GATOPMD/mapas/artigo/mapa_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_60_8d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_70_8d.txt',
    #
    # 'GATOPMD/mapas/artigo/mapa_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/mapa_7r_80_8d.txt',

    # 'GATOPMD/mapas/artigo/mapa_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_70_9d.txt',

    # 'GATOPMD/mapas/artigo/mapa_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/mapa_8r_80_9d.txt',

]

prizes = [
    'GATOPMD/mapas/artigo/premio_4r_40_1d.txt',
    'GATOPMD/mapas/artigo/premio_4r_40_1d.txt',
    'GATOPMD/mapas/artigo/premio_4r_40_1d.txt',

    'GATOPMD/mapas/artigo/premio_4r_45_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_45_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_45_5d.txt',

    'GATOPMD/mapas/artigo/premio_4r_50_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_50_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_50_5d.txt',

    'GATOPMD/mapas/artigo/premio_4r_60_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_60_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_60_5d.txt',

    'GATOPMD/mapas/artigo/premio_4r_70_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_70_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_70_5d.txt',

    'GATOPMD/mapas/artigo/premio_4r_80_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_80_5d.txt',
    'GATOPMD/mapas/artigo/premio_4r_80_5d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_40_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_40_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_50_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_50_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_60_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_60_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_50_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_50_7d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_60_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_60_7d.txt',

    # 'GATOPMD/mapas/artigo/premio_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_70_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_70_6d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_80_6d.txt',
    # 'GATOPMD/mapas/artigo/premio_5r_80_6d.txt',

    # 'GATOPMD/mapas/artigo/premio_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_70_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_70_7d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_80_7d.txt',
    # 'GATOPMD/mapas/artigo/premio_6r_80_7d.txt',

    # 'GATOPMD/mapas/artigo/premio_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_60_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_60_8d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_70_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_70_8d.txt',
    #
    # 'GATOPMD/mapas/artigo/premio_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_80_8d.txt',
    # 'GATOPMD/mapas/artigo/premio_7r_80_8d.txt',

    # 'GATOPMD/mapas/artigo/premio_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_70_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_70_9d.txt',

    # 'GATOPMD/mapas/artigo/premio_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_80_9d.txt',
    # 'GATOPMD/mapas/artigo/premio_8r_80_9d.txt',

]

size_population = [.1,
                   .2,
                   .3,
                   .4,
                   .5,
                   .6,
                   .7,
                   .8,
                   .9,
                   10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
                   ]

costs = [
    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],

    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],

    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],

    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],

    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],

    [20, 23, 25, 30],
    [23, 25, 30],
    [20, 23, 25, 30],
    #
    # [18]*5,
    # [22]*4,
    # [18, 22, 24, 25, 28],
    # [22, 24, 25, 28],
    # [18, 22, 24, 25, 28],
    #
    # [19] * 5,
    # [23] * 4,
    # [19, 23, 25, 26, 29],
    # [23, 25, 26, 29],
    # [19, 23, 25, 26, 29],
    #
    # [20] * 5,
    # [22] * 4,
    # [20, 22, 25, 27, 30],
    # [22, 25, 27, 30],
    # [20, 22, 25, 27, 30],
    #
    # [18] * 6,
    # [20] * 5,
    # [18, 20, 22, 24, 25, 27],
    # [20, 22, 24, 25, 27],
    # [18, 20, 22, 24, 25, 27],
    #
    # [19] * 6,
    # [22] * 5,
    # [19, 22, 23, 24, 25, 28],
    # [22, 23, 24, 25, 28],
    # [19, 22, 23, 24, 25, 28],

    # [21] * 5,
    # [23] * 4,
    # [21, 23, 26, 27, 30],
    # [23, 26, 27, 30],
    # [21, 23, 26, 27, 30],
    #
    # [22] * 5,
    # [24] * 4,
    # [22, 24, 26, 28, 32],
    # [24, 26, 28, 32],
    # [22, 24, 26, 28, 32],
    #
    # [20] * 6,
    # [22] * 5,
    # [20, 22, 24, 25, 27, 30],
    # [22, 24, 25, 27, 30],
    # [20, 22, 24, 25, 27, 30],
    #
    # [21] * 6,
    # [23] * 5,
    # [21, 23, 24, 26, 29, 30],
    # [23, 24, 26, 29, 30],
    # [21, 23, 24, 26, 29, 30],

    # [18]*7,
    # [19]*6,
    # [18,19, 20, 22, 24 ,25, 27],
    # [19, 20, 22, 24 ,25, 27],
    # [18, 19, 20, 22, 24, 25, 27],

    # [19]*7,
    # [20]*6,
    # [19, 20, 21, 23, 24 ,25, 29],
    # [20, 21, 23, 24 ,25, 29],
    # [19, 20, 21, 23, 24 ,25, 29],

    # [19]*7,
    # [21]*6,
    # [19, 21, 23, 24, 25 ,26, 30],
    # [21, 23, 24, 25 ,26, 30],
    # [19, 21, 23, 24, 25 ,26, 30],

    # [15] * 8,
    # [17] * 7,
    # [15, 17, 19, 20, 21, 23, 25, 27],
    # [17 ,19, 20, 21, 23 ,25, 27],
    # [15, 17 ,19, 20, 21, 23 ,25, 27]

    # [15] * 8,
    # [19] * 7,
    # [15, 19 ,20, 21, 23, 24 ,25, 29],
    # [19 ,20, 21, 23, 24 ,25, 29],
    # [15, 19 ,20, 21, 23, 24 ,25, 29]
]

points_init = [
    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    [0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],

    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    #
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    #
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    #
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],

]

points_end = [
    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],

    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],

    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],

    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],

    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],

    [0, 0, 0, 0],
    [0, 0, 0],
    [1, 2, 3, 4],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [1, 2, 3, 4, 5],
    #
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [1, 2, 3, 4, 5],
    #
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [1, 2, 3, 4, 5],

    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6],
    #
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6],

    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6, 7],
    #
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6, 7],
    #
    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6, 7, 8],

    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0],
    # [1, 2, 3, 4, 5, 6, 7, 8],
]

deposits = [
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],

    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    #
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    #
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],
    # [0, 1, 2, 3, 4, 5],

    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],

    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],
    # [0, 1, 2, 3, 4, 5, 6],

    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],

    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],
    # [0, 1, 2, 3, 4, 5, 6, 7],

    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],

    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
    # [0, 1, 2, 3, 4, 5, 6, 7, 8],
]
number_executions = 30

main_path = './GATOPMD/Result/'
data = datetime.now()
execucao = str(data.strftime(("%d-%m-%Y_%H-%M-%S_execucao")))

result_folder = main_path + '' + execucao

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
            iterations=250,
            size_population=100,
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
        # bestElementsCosts, bestElements, bestElementGenaration, bestElementAlways, \
        # primeira_populacao, ultima_population= ga_execution.run()

        gbest, primeiro, ultimo = pso_execution.run()

        with open(folder_cenary + '/Results_Execution_melhor_elemento_custo_premio.csv', 'a+') as out:
            custo = 0
            for j in range(len(gbest.solution)):
                out.write(str(pso_execution.mensureCost(gbest.solution[j])) + ';')
                custo = custo + pso_execution.mensureCost(gbest.solution[j])
            out.write(str(custo) + ';')

            premio = 0
            for j in range(len(gbest.solution)):
                out.write(str(pso_execution.prizes.take(gbest.solution[j].astype(int)).sum()) + ';')
                premio = premio + pso_execution.prizes.take(gbest.solution[j].astype(int)).sum()
            out.write(str(premio) + '\n')

        with open(folder_cenary + '/Resultados_primeira_ultima_populacao'+name+'.txt', 'a+') as out:

            out.write('Execuçao: '+ str(numberExecution) +'\n')
            out.write('primeira populacao\n')
            for j in range(len(primeiro)):
                cost_total = 0
                fitness_total = 0
                for p in range(len(primeiro[j].solution)):
                    cost_total += pso_execution.mensureCost(primeiro[j].solution[p])
                    fitness_total += pso_execution.prizes.take(primeiro[j].solution[p].astype(int)).sum()
                    out.write(str(pso_execution.mensureCost(primeiro[j].solution[p])) + ';')
                    out.write(str(pso_execution.prizes.take(primeiro[j].solution[p].astype(int)).sum()) + ';')
                    out.write(str(primeiro[j].solution[p]) + '\n')

                out.write(str(cost_total) + ';')
                out.write(str(fitness_total) + '\n\n')

            out.write('última populacao\n')
            for j in range(len(ultimo)):
                cost_total = 0
                fitness_total = 0
                for p in range(len(ultimo[j].solution)):
                    cost_total += pso_execution.mensureCost(ultimo[j].solution[p])
                    fitness_total += pso_execution.prizes.take(ultimo[j].solution[p].astype(int)).sum()
                    out.write(str(pso_execution.mensureCost(ultimo[j].solution[p])) + ';')
                    out.write(str(pso_execution.prizes.take(ultimo[j].solution[p].astype(int)).sum()) + ';')
                    out.write(str(ultimo[j].solution[p]) + '\n')

                out.write(str(cost_total) + ';')
                out.write(str(fitness_total) + '\n\n')


            cost_total = 0
            fitness_total = 0
            out.write('Melhor Elemento populacao\n')
            for p in range(len(gbest.solution)):
                cost_total += pso_execution.mensureCost(gbest.solution[p])
                fitness_total += pso_execution.prizes.take(gbest.solution[p].astype(int)).sum()
                out.write(str(pso_execution.mensureCost(gbest.solution[p])) + ';')
                out.write(str(pso_execution.prizes.take(gbest.solution[p].astype(int)).sum()) + ';')
                out.write(str(gbest.solution[p]) + '\n')

            out.write(str(cost_total) + ';')
            out.write(str(fitness_total) + '\n\n\n')


        pso_execution.plota_rotas_TOP(cidades=pso_execution.map_points, rota=gbest.solution, file_plot=True,
                                     name_file_plot=folder_chart + '/Plot_Path_melhor_elemento_' + name + '_execution_' + str(
                                         numberExecution))

        print('####### Fim Execucao: ' + str(numberExecution))

    del pso_execution

    gc.collect()