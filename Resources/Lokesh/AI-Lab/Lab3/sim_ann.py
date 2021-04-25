import math
import random
# import matplotlib.pyplot as plt

euc = True
file_name = input()
data = open(file_name)
data = data.read()
data = data.split("\n")

if data[0] != "euclidean":
    euc = False
n = int(data[1])

class cities:
    index = int(0)
    x = int(0)
    y = int(0)
    distance = []

city = []

for i in range(0,n):
    temp = cities()
    row = data[i + 2].split()
    temp.x = float(row[0])
    temp.y = float(row[1])
    temp.index = int(i)
    temp.distance = data[i + n + 2].split()
    city.append(temp)

def prob(E,T):
    return( 1 / ( 1 + ( math.exp( (-1)*(E)/(T) ) ) ) )

def path_length(ls):
    ret = float(0)
    for i in range(1,n):
        ret = ret + float(city[ls[i]].distance[ls[i-1]])
    ret = ret + float(city[ls[0]].distance[ls[len(ls)-1]])
    return ret

def graph(ls):
    x = []
    y = []
    for i in range(0,len(ls)):
        x.append(city[ls[i]].x)
        y.append(city[ls[i]].y)
    x.append(x[0])
    y.append(y[0])
    plt.plot(x,y,marker='o', markerfacecolor='blue', markersize=5)
    plt.pause(0.00001)
    plt.draw()
    plt.clf()

T = n

path = list(range(0,n))

# print(path,"\t",path_length(path),"\n\n")

br = 0
while(T > 0.09):
    pre_pl = path_length(path)

    # graph(path)

    # randomly swapping two cities
    time = 0 
    final = n*10
    if n > 100:
        final = n
    for sth in range(0,final):   # can replce final with n*n for best result (but time consuming)
        temp_path = path.copy()

        start,end = random.randrange(1,n,1),random.randrange(1,n,1)
        temp_path[start],temp_path[end] = temp_path[end],temp_path[start]
        
        cost = (path_length(temp_path) - path_length(path))

        if(random.random() > prob(cost,T)): # allow probabiliticly
            path = temp_path
            time = time + 1

        # if(time == 1):
        #     break
            
    if(pre_pl == path_length(path)):
        br = br + 1
    else:
        br = 0
    if(br > 10):
        break

    # print(T,"\t",path_length(path))

    T = T - 1

print(path_length(path))
for i in path:
    print(i,end=' ')
print()

# print(path,"\t",path_length(path))
