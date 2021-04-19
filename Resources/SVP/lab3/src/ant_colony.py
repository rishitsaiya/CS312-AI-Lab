import sys
import random

class AntColony(object):

    def __init__(self, distances, n_ants, max_iterations, alpha, beta, rho, Q):
        self.distances = distances
        self.n_ants = n_ants
        self.max_iterations = max_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        
        # Self Variables
        self.N = len(distances)
        self.pheromones = [[0.1 for x in range(N)] for y in range(N)]
        self.best_cost = float('Inf')
        self.best_tour = range(N)

    
    def optimize(self):
        for i in range(self.max_iterations):
            
            # Simulate N ants
            for j in range(self.n_ants):
                ant = Ant(self.distances, self.pheromones, self.alpha, self.beta)
                
                # Check if best tour
                if ant.cost_of_tour(self.distances) < self.best_cost:
                    self.best_cost = ant.cost_of_tour(self.distances)
                    self.best_tour = ant.path
                    print(*self.best_tour, sep=" ")
                    print(self.best_cost)

                # Calc pheromones delta
                pheromones_delta = [[0 for x in range(N)] for y in range(N)]
                for i, u in enumerate(ant.path):
                    v = ant.path[(i+1)%N]
                    pheromones_delta[u][v] += self.Q/distances[u][v]
                
            # Update pheromones
            for u in range(N):
                for v in range(N):
                    self.pheromones[u][v] = (1-self.rho)*self.pheromones[u][v] + pheromones_delta[u][v]
        

class Ant(object):

    def __init__(self, distances, pheromones, alpha, beta):
        self.N = len(distances)
        self.path = []
        self.simulate(distances, pheromones, alpha, beta)

    def cost_of_tour(self, distances):
        cost = 0
        for i in range(len(self.path)):
            cost += distances[self.path[i]][self.path[(i+1)%N]]
        return cost

    def simulate(self, distances, pheromones, alpha, beta):
        start = random.randint(0, N-1)
        allowed = list(range(0, N))
        allowed.remove(start)

        self.path.append(start)
        while(len(self.path) != N):
            u = self.path[-1]
            prob = [(pheromones[u][v]**alpha  * (1/distances[u][v])**beta) for v in allowed]
            sigma = sum(prob)
            prob = [x/sigma for x in prob]

            # Roullete wheel
            next_city = random.choices(allowed, weights=prob)[0]
            # print(allowed)
            allowed.remove(next_city)
            self.path.append(next_city)    


if __name__ == '__main__':

    inputfile = open(sys.argv[1], "r")
    lines = inputfile.readlines()
    
    # input 
    isEuclidean = lines[0]
    N = int(lines[1])

    coordinates = []
    for i in range(2, N+2):
        c = [float(x) for x in lines[i].rstrip().split(' ')]
        coordinates.append(c)
    # print(coordinates)

    distances = []
    for i in range(N+2, 2*N + 2):
        d = [float(x) for x in lines[i].rstrip().split(' ')]
        distances.append(d)
    # print(distances)

    aco = AntColony(distances, n_ants=100, max_iterations=50, alpha=8, beta=8, rho=0.2, Q=0.1)
    aco.optimize()


    