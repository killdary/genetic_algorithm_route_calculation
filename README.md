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
    from AG_routes import CalulateRoutesTSP
    route = CalulateRoutesTSP()
    
    # return 2 values (cost best route, the sequence of towns of the route found)
    print(route.GA(generation=2500,
                   population=50,
                   towns='./pontos.txt'))
```
