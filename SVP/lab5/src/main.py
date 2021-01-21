import sys
from queue import PriorityQueue
from utils import Point
import numpy as np

class Astar(object):
    def __init__(self):
        self.N = 0
        self.V = []
        self.E = []
        self.closed = set([])

    def goalTest(self, u):
        return u == self.N - 1
    
    def moveGen(self, u):
        return zip(range(self.N), self.E[u])

    def f(self, u):
        return self.g(u) + self.h2(u)

    def g(self, u):
        return self.V[u].value

    
    def h1(self, u):
        return 10*self.V[u].distance(self.V[-1])

    def h2 (self, u):
        return np.exp(- self.V[u].distance(self.V[-1]) )

    def h3(self, u):
        return self.V[u].distance(self.V[-1])


    def takeInput(self, filename):
        with open(filename, "r") as file:
            self.N = int( next(file).rstrip() )
            readLine = lambda x: list(map(int, x.rstrip().split()))
            self.V = [ Point( *readLine(next(file)) ) for i in range(self.N) ]
            self.E = [ readLine(next(file)) for i in range(self.N) ]


    def reconstructPath(self):
        v = self.N - 1
        path = []
        while v is not None:
            path.append(v)
            v = self.V[v].parent
        path.reverse()
        cost = sum(self.E[path[i-1]][path[i]] for i in range(1, len(path)))
        return cost, path

    
    def propagateImprovement(self, u):
        for v, w in self.moveGen(u):
            if w != 0: 
                newVal = self.g(u) + w
                if newVal < self.g(v):
                    self.V[v].parent = u
                    self.V[v].value = newVal
                    if(v in self.closed):
                        self.propagateImprovement(v)
    

    def getShortestPath(self):
        """
            calculate the shortest path from vertex 0 and N-1
            returns cost, path

            g(u): path length from 0 to u
            h1(u): euclidean distance from u to goal
            f(u) = g(u) + h1(u), used as p in priority queue

        """
        Q = PriorityQueue() # implemented with lazy update
        self.V[0].value = 0
        Q.put( (self.f(0), 0) )

        
        self.closed = set([0])
        
        while not Q.empty():
            f, u = Q.get()
            
            if self.goalTest(u):
                return self.reconstructPath()
            
            self.closed.add(u)

            for v, w in self.moveGen(u):
                if w != 0 and v not in self.closed:
                    # add to queue only if this reduces the path length
                    newValue = self.g(u) + w
                    
                    if newValue < self.g(v):
                        self.V[v].value = newValue
                        self.V[v].parent = u
                        Q.put( (self.f(v), v) )
                
                if w != 0 and v in self.closed:
                    newValue = self.g(u) + w

                    if newValue < self.g(v):
                        self.V[v].parent = u
                        self.V[v].value = newValue
                        self.propagateImprovement(v)


    def testPrint(self, filename):
        self.takeInput(filename)
        cost, path = self.getShortestPath()
        print(cost)
        print(*path, sep=" ")


A = Astar()
A.testPrint(sys.argv[1])