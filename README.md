## Calculo de Rotas para o Problema de Orientação de Equipes com Múltiplas Restrições de Locomoção e Mudança de Base
Este projeto foi desenvolvido em python para o cálculo de rotas para múltiplos agentes com restrições de locomoção e mudança de base. Este problema foi criado com a junção do Problema de Orientação de Equipes e o Problema daMochila Múltipla

#### Feature

* Recebe um .txtcom a localização das cidaddes em um plano cartesiano 2D.
* Calcula a rota para os agentes
* Cria um gráfico da rota criada

#### Pré Requisitos

* Numpy
* Matplotlib

#### Uso
```python
    from solution.AG_routes import CalulateRoutesTSP
    route = CalulateRoutesTSP()
    
    # return 2 values (cost best route, the sequence of towns of the route found)
    print(route.GA(generation=1000,
                    population=100,
                    limit_population=20,
                    crossover_rate= .6,
                    mutation_rate=.8,
                    cost_rate=2,
                    prizes_rate=5,
                    map_points=path_current,
                    prizes=prize_current,
                    max_cost=cost_current,
                    start_point=current_init,
                    end_point=current_end,
                    depositos=current_deposits)))
```
