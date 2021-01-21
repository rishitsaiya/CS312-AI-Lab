import sys
import random
import numpy as np


class GeneticAlgorithm(object):
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
            return max(tours, key=lambda x: self.heuristic(x))
        
        tours.sort(key=lambda x: self.heuristic(x))
        return tours[:r]

    def crossover(self, A, B): # cyclic crossover
        child = [-1] * self.N
        index = 0
        while child[index] != -1:
            child[index] = A[index]
            index = A.index( B[index] )
        for i in range(self.N):
            if child[i] != -1:
                child[i] = B[i]
        return child

    def optimize(self, filename, iter=200):
        self.__init__(filename)
        population = self.greedyOptim(self.N)

        P = len(population)
        self.bestTour = population[0]
        self.bestCost = self.heuristic(population[0])
        print(self.bestCost)

        for i in range(iter):
            prob = np.array([ 1/self.heuristic(tour) for tour in population])
            prob = prob/prob.sum()
            selected = random.choices(population, weights=prob, k=P)
            random.shuffle(selected)
            children = []
            for j in range(P//2):
                children.append( self.crossover(selected[j], selected[P//2+j]) )
                children.append( self.crossover(selected[P//2+j], selected[j]) )
        
            population = population + children

            if random.random() < 0.05:
                index = random.randint(0, P-1)
                mutated = population[index]
                i = random.randint(0, self.N-1)
                j = random.randint(0, self.N-1)
                mutated[i], mutated[j] = mutated[j], mutated[i]
            
            population.sort(key=lambda x: self.heuristic(x))           
            population = population[:P]

            newCost = self.heuristic(population[0]) 
            if newCost < self.bestCost:
                self.bestCost = newCost
                self.bestTour = population[0].copy()
                print(self.bestCost)
        

        
        
        

optimizer = GeneticAlgorithm()
optimizer.optimize(sys.argv[1], int(10e7) )
