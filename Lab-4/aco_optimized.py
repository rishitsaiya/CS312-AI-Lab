
import random
import sys
import time

class AntColony(object):

    def __init__(self, DistanceBetCities, numAnts, maxIterations, alpha, beta, rho, Q):

        self.DistanceBetCities = DistanceBetCities
        self.numAnts = numAnts
        self.maxIterations = maxIterations

        self.Q = Q
        self.beta = beta
        self.rho = rho
        self.alpha = alpha
        
        self.KBest = int(0.1*NumOfCities+1)
        self.recursive = False

        # Self Variables

        self.N = len(DistanceBetCities)

        self.pheromones = [
            [0.1 for city in range(NumOfCities)] for selectedcity in range(NumOfCities)]
        self.bestCost = float('Inf')
        self.bestTour = range(NumOfCities)

    def optimise(self):

        while time.time()-start < 298:

            ants = []

            pheromonesDelta = [
                [0 for x in range(NumOfCities)] for y in range(NumOfCities)]

            for j in range(self.numAnts):
                ant = Ant(self.DistanceBetCities,
                          self.pheromones,
                          self.alpha, self.beta)

                ants.append(ant)

                if ant.pathCost(self.DistanceBetCities) < self.bestCost:
                    self.bestCost = ant.pathCost(self.DistanceBetCities)
                    self.bestTour = ant.currentPath
                    self.lastChange = time.time()
                    print("The tour length found is =", self.bestCost, sep=' ')
                    print(*self.bestTour, sep=" ")
                    print("......................................................................................................................................")

            ants.sort(key=lambda city: city.pathCost(self.DistanceBetCities))
            
            for chiti in ants[:self.KBest]:
                for i, v in enumerate(chiti.currentPath):
                    nextOne = chiti.currentPath[(i+1)%NumOfCities]
                    pheromonesDelta[v][nextOne] += self.Q/DistanceBetCities[v][nextOne]

            for i in range(NumOfCities):
                for j in range(NumOfCities):
                    self.pheromones[i][j] = (1-self.rho)*self.pheromones[i][j] + pheromonesDelta[i][j]

            if time.time()-self.lastChange > 300:
                break


class Ant(object):

    def __init__(self, DistanceBetCities, pheromones, alpha, beta):
        self.currentPath = []
        self.getPath(DistanceBetCities, pheromones, alpha, beta)

    def getPath(self, DistanceBetCities, pheromones, alpha, beta):

        initiate = random.randint(0, NumOfCities-1)
        validCities = list(range(0, NumOfCities))
        validCities.remove(initiate)

        self.currentPath.append(initiate)
        while(len(self.currentPath) < NumOfCities):

            lastCity = self.currentPath[-1]

            probability = [(pheromones[lastCity][nextPossibleCity]**alpha * (1/DistanceBetCities[lastCity][nextPossibleCity])**beta) for nextPossibleCity in validCities]

            probSet = [x/sum(probability) for x in probability]

            nextCity = random.choices(validCities, weights=probSet)[0]
            self.currentPath.append(nextCity)
            validCities.remove(nextCity)

    def pathCost(self, DistanceBetCities):
        fare = 0
        for i in range(len(self.currentPath)):
            fare += DistanceBetCities[self.currentPath[i]][self.currentPath[(i+1) % NumOfCities]]
        return fare


# %%

if __name__ == '__main__':

    start = time.time()
    # print(start)

    # Reading input from input file :

    data = open(sys.argv[1], "r").readlines()

    isEuclidean = False

    if(data[0] == "euclidean"):
        isEuclidean = True

    NumOfCities = int(data[1])

    CityCoordinates = []
    DistanceBetCities = []

    for i in range(NumOfCities):
        c = [float(x) for x in data[i+2].strip().split(' ')]
        CityCoordinates.append(c)
        d = [float(x) for x in data[NumOfCities+2+i].strip().split(' ')]
        DistanceBetCities.append(d)

    # print(CityCoordinates)
    # print(DistanceBetCities)

    if isEuclidean:
        aco = AntColony(DistanceBetCities, numAnts=int(NumOfCities),
                    maxIterations=200, alpha=3, beta=3, rho=0.1, Q=0.1)
    else:
        aco = AntColony(DistanceBetCities, numAnts=int(NumOfCities),
                    maxIterations=300, alpha=5, beta=5, rho=0.05, Q=0.05)

    aco.optimise()

    # print(time.time()-start)
