## Calulate Routes Traveling Salesman Problem
This project aims to develop a python module that performs the route calculations of
the Traveling Salesman Problem(TSP). The initial version focuses only on the symmetric TSP.

#### Feature

* Receives a .txt file with the location of cities on a cartesian plane
* Calculate the route for the TSP
* Creates a graph with the route found

#### Prerequisites

* Numpy
* Matplotlib

#### Usage
```python
    from AG_routes import CalulateRoutesTSP
    route = CalulateRoutesTSP()
    
    # return 2 values (cost best route, the sequence of towns of the route found)
    print(route.GA(generation=2500,
                   population=50,
                   towns='./pontos.txt'))
```