import sys
import random
from utils import Point

A = 100
def randomPoint():
    p = A * random.random() 
    q = A * random.random()
    return Point(round(p), round(q))

N = int(sys.argv[1])
print(N)
P = []
for i in range(N):
    P.append(randomPoint())
    print(P[-1].x, P[-1].y)

edges = [[-1 for j in range(N)] for i in range(N)]

for _ in range(N//3):
    for u in range(1, N):
        # at the end of every iteration we have a tree
        # for the new vertex u, we connect it to what is left behind
        v = 0
        if u != 1:
            v = random.randint(max(0, u-3), u-1)
        w = round(P[u].distance(P[v]) * (1 + random.random() )**2)
        edges[u][v] = w
        edges[v][u] = w

for i in range(N):
    print(*edges[i], sep=", ")


        

