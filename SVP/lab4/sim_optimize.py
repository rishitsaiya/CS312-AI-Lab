import sys
import random
import numpy as np


class SimulatedAnnealing(object):
    def __init__(self, filename=None):
        if not filename:
            return
        with open(filename, "r") as file:
            lines = file.readlines()
        
        isEuclidean = lines[0]
        self.N = int(lines[1])

        for i in range(2, self.N+2):
            c = [float(x) for x in lines[i].rstrip().split(' ')]

        distances = []
        for i in range(self.N+2, 2*self.N + 2):
            d = [float(x) for x in lines[i].rstrip().split(' ')]
            distances.append(d)
        self.distances = np.array(distances)

    def heuristic(self, tour):
        return sum(self.distances[tour[i-1]][tour[i]] for i in range(len(tour)))
        
    def greedyOptim(self, r):
        tours = []
        for start in range(self.N):
            sol = []
            openSet = set( range(self.N) )
            u = start
            for _ in range(self.N):
                v = min(openSet, key=lambda x: self.distances[u][x])
                sol.append(v)
                openSet.remove(v)
                u = v
            tours.append(sol)
        if r == 1:
            return min(tours, key=lambda x: self.heuristic(x))
        
        tours.sort(key=lambda x: self.heuristic(x))
        return tours[:r]

    def optimize(self, filename, iter=200):
        self.__init__(filename)
        node = self.greedyOptim(1)
        self.bestTour = node
        self.bestCost = self.heuristic(node)
        print(self.bestCost)

        for k in range(1, iter+ 1):
            temp = 200
            while True:
                newNode = node.copy()
                i = random.randint(0, self.N-1)
                j = random.randint(0, self.N-1)
                newNode[i], newNode[j] = newNode[j], newNode[i]

                deltaH = self.heuristic(node) - self.heuristic(newNode)

                if deltaH > 0: # found a better node so update best and break
                    node = newNode
                    newCost = self.heuristic(node) 
                    if newCost < self.bestCost:
                        self.bestCost = newCost
                        self.bestTour = node.copy()
                        print(self.bestCost)
                    break

                else:
                    power = deltaH/( k * temp)
                    p = 1 / ( 1 + np.exp( power) )
                    # print(power)
                    if random.random() < p:
                        del(node)
                        node = newNode
                
                temp = 0.99*temp
                # print("temperature:", temp)

optimizer = SimulatedAnnealing()
optimizer.optimize(sys.argv[1], int(10e7) )
