#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:21:37 2018

@author: killdary

"""

import numpy as np
import matplotlib.pyplot as plt
import datetime


def plota_rotas(cidades, rota):
    x = cidades[rota.astype(int), 0]
    y = cidades[rota.astype(int), 1]
    
    cid_nome = range(len(x))
    
    plt.figure(num=None, figsize=(9, 9), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(x, y, 'C3', lw=3)
    plt.scatter(x, y, s=120, marker="s")
    
    for i, txt in enumerate(cid_nome):
        plt.annotate(txt, (x[i],y[i]),fontsize=18)
    plt.title('Mapa GA')

def mede_custo(distancias, rota):
    dist_total = 0
    rota = rota.astype(int)
    
    cidade_atual = -1
    for cidade in rota:
        if cidade_atual >= 0:
            dist_total += distancias[cidade_atual, cidade]
        cidade_atual = cidade
        
    return dist_total

def matriz_distancia(cidades):
    qtd = cidades.shape[0]    
    distancias = np.zeros([qtd,qtd])
    
    for i in range(qtd):
        for j in range(i,qtd):
            if i != j:
                b = cidades[i,0] - cidades[j,0]
                c = cidades[i,1] - cidades[j,1]
                a = np.sqrt(np.square(b) + np.square(c))
                
                distancias[i,j] = a
                distancias[j,i] = a
    return distancias

def min_rotas(distancias, new_pop, num):
    rotas = np.array()
    min_pop = np.array()
    id_pop = np.array()
    
    for i, indiv in enumerate(new_pop):
        rotas = np.append(rotas , mede_custo(distancias,indiv))
    
    for i in range(num):
        min_pop = np.append(min_pop, rotas.min())
        id_min = rotas.argmin()
        id_pop = np.append(id_pop, id_min)
        
    
    for i, indiv in enumerate(new_pop):
        rotas = np.append(rotas , mede_custo(distancias,indiv))
        if len(mini_pop) < num:
            min_pop = np.append(min_pop, ind)
            id_pop = np.id_pop(min_pop, i)
        else:
            for j in min_pop:
                min_pop = np.append(min_pop, ind)
                id_pop = np.id_pop(min_pop, i)
                

def mutation(rotas, ga=True):
    size_samples = size_population/rotas

    for i in range(0,size_samples):
        sample = rotas[i,1:-1]
        if i%2 == 0:
            new_ind = np.random.permutation(sample)
            

def generate_population(size_population, ancestral, first_gene):   
    new_pop = np.zeros((size_population, ancestral.shape[0]+2))
    
    for i in range(size_population):
        ind = np.copy(ancestral)
        np.random.shuffle(ind)
          
        new_pop[i] = np.concatenate([[first_gene], ind, [first_gene]])
    
    return new_pop
        

print(datetime.datetime.now())
#def GA():
    
#    Carrega os pontos do mapas que deverão ser gerados as rotas    
mapa = np.loadtxt('./pontos.txt')
#mapa = np.array([[8,6],[4,2],[1,7],[5,9],[3,3],[15,11],[5,5],[10,6],[12,12],[1,12]])

#    Calculo da matriz de distancias entre todos os pontos
distancias = matriz_distancia(mapa)

#    Dados das gerações população e numero de pontos da rota
geracoes = 2500
populacao = 50
populacao = 4*((populacao+4)//4)
size = mapa.shape[0]
new_pop = np.zeros((populacao, size+1))
custo_rotas = np.arange(populacao)

#    Matriz que armazenará os 4 melhores individuos da população
best_4_rotes = np.zeros((4,size+1))
best_4_cousts = np.zeros(4)


#    A primeira população será totalmente aleatória

inicial = np.random.permutation(size)
primeiro_gene = inicial[0]
inicial = np.delete([inicial],[0,0])

count_best = 0
best_element = 0

for i in range(populacao):
    ind = np.copy(inicial)
    np.random.shuffle(ind)
      
    ind = np.array(ind)
    new_pop[i] = np.concatenate([[primeiro_gene], ind, [primeiro_gene]])
    
    custo_rotas[i] = mede_custo(distancias, ind)

#    Inicio das gerações, quando o for é iniciado será buscado os 4 melhores individuos 
#        da população, o restante dos individos serão descartados
for ger in range(geracoes):
    temp_pop = np.copy(new_pop)
    temp_cust = np.copy(custo_rotas)
#        Pegando os 4 melhores individuos da população
    for j in range(4):
        tmp_ind = np.argmin(temp_cust)
        
#        if(best_4_cousts[best_4_cousts == temp_cust[tmp_ind]].shape[0] == 0):
        best_4_rotes[j] = np.copy(temp_pop[tmp_ind])
        best_4_cousts[j] = temp_cust[tmp_ind]
        
        temp_pop = np.delete(temp_pop, tmp_ind, axis=0)
        temp_cust = np.delete(temp_cust, tmp_ind)
#        else:
#            temp_pop = np.delete(temp_pop, tmp_ind, axis=0)
#            temp_cust = np.delete(temp_cust, tmp_ind)
            
            
        
#        Pontos de inserções de mutações, estes pontos deverão ser diferentes para que possa
#            uma mudança de genes
    routeInsertPoints = np.random.randint(size-1, size=2)

    while routeInsertPoints[0] == routeInsertPoints[1]:
        routeInsertPoints = np.random.randint(size-1, size=2)
#        Um pequeno tratamento para que os Elementos I e J sejam próximos
#        pois caso sejam próximos poderão gerar indivíduos identicos
    I = routeInsertPoints.min()
    J = routeInsertPoints.max()
    if I+1 == J:
        if J == size-2:
            I = I-1
        else:
            J=J+1
    
#        mutacao = np.zeros((4,size))
    new_pop = np.zeros((populacao, size+1))
    for j in range(4):            
        init_end_point = best_4_rotes[j,0]
        resultado = np.zeros((4,size+1))
        
        mutacao = np.repeat([best_4_rotes[j,1:-1]],4, axis=0)
#            elemento_mutacao = np.copy(best_4_rotes[j//4])
        
        if I == 0:
            mutacao[1,:J] = mutacao[1,J-1::-1]
        else:
            mutacao[1,I:J] = mutacao[1,J-1:I-1:-1]
                
        mutacao[2, I:J] = np.roll(mutacao[2,I:J],1)
        if np.array_equal(mutacao[1], mutacao[2]):
            np.random.shuffle( mutacao[2])
            
        mutacao[3, I], mutacao[3, J] = mutacao[3, J], mutacao[3, I]
        
        for k in range(4):
            resultado[k] = np.concatenate([[init_end_point], mutacao[k],[init_end_point]])
        

        indice = j*4
        new_pop[indice:indice+4] = resultado
        
        
    x = generate_population(populacao - 16,inicial,primeiro_gene)
    new_pop[16:] = x
    
    custo_rotas = np.zeros(populacao)
    for k in range(new_pop.shape[0]):
        custo_rotas[k] = mede_custo(distancias, new_pop[k])
        
    if(best_element == best_4_cousts[0]):
        count_best += count_best
        if count_best == int(geracoes/100):
            break
    else:
        best_element = best_4_cousts[0]
        count_best = 0
    


plota_rotas(mapa, best_4_rotes[0])

#GA()
        
    
    
    