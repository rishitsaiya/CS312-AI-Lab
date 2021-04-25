import math
import random
import copy
import time
# import matplotlib.pyplot as plt

now = time.time()

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

def prob(E,T):
    return( 1 / ( 1 + ( math.exp( (-1)*(E)/(T) ) ) ) )

for i in range(0,n):
    temp = cities()
    row = data[i + 2].split()
    temp.x = float(row[0])
    temp.y = float(row[1])
    temp.index = int(i)
    temp.distance = data[i + n + 2].split()
    city.append(temp)

def path_length(ls):
    ret = float(0)
    for i in range(1,n):
        ret = ret + float(city[ls[i]].distance[ls[i-1]])
    ret = ret + float(city[ls[0]].distance[ls[len(ls)-1]])
    return ret

def CROSSOVER_SELF_TRY(parent_gen,popu_size):
    child_gen = []
    for i in range(0,int(popu_size/2)):
        p1 = parent_gen[i]
        p2 = parent_gen[popu_size - 1 - i]

        c1 = p1.copy()
        temp = p2[int(n/2):]

        for item in temp:
            if item in c1:
                c1.remove(item)
        c1.extend(temp)

        c2 = p2.copy()
        temp = p1[int(n/2):]

        for item in temp:
            if item in c2:
                c2.remove(item)
        c2.extend(temp)

        child_gen.append(c1)
        child_gen.append(c2)
    return child_gen

def CROSSOVER_PMX(parent_gen,popu_size):
    child_gen = []
    for i in range(0,int(len(parent_gen)/2)):
        p1 = parent_gen[i]
        p2 = parent_gen[len(parent_gen) - 1 - i]

        start = random.randrange(0,n-1,1)
        end = random.randrange(start+1,n,1)

        c1 = [-1] * n
        c2 = [-1] * n

        for ind in range(start,end + 1):
            c1[ind] = p1[ind]
            c2[ind] = p2[ind]

        for ind in range(0,n):
            if p2[ind] not in c1:
                c1[ind] = p2[ind]
            if p1[ind] not in c2:
                c2[ind] = p1[ind]

        for item in p2:
            if(item not in c1):
                c1[c1.index(-1)] = item
        for item in p1:
            if(item not in c2):
                c2[c2.index(-1)] = item

        child_gen.append(c1)
        child_gen.append(c2)
            
    return child_gen

def CROSSOVER_OX(parent_gen,popu_size):
    child_gen = []
    for i in range(0,int(len(parent_gen)/2)):
        p1 = parent_gen[i]
        p2 = parent_gen[len(parent_gen) - 1 - i]

        start = random.randrange(0,n-1,1)
        end = random.randrange(start+1,n,1)

        c1 = p1[start:end]
        c2 = p2[start:end]

        for ind in range(0,n):
            if p2[ind] not in c1:
                c1.append(p2[ind])
            if p1[ind] not in c2:
                c2.append(p1[ind])

        child_gen.append(c1)
        child_gen.append(c2)
            
    return child_gen

def CROSSOVER_CX(parent_gen,popu_size):
    child_gen = []
    for i in range(0,int(popu_size/2)):
        p1 = parent_gen[i]
        p2 = parent_gen[popu_size - 1 - i]

        c1 = p1.copy()
        c2 = p2.copy()

        index = []

        index.append(0)
        
        breaker = 0
        while (breaker != len(index)):
            breaker = len(index)
            point = c1.index(c2[index[-1]])
            if(point not in index):
                index.append(point)

        temp = list(range(0,n))
        for item in index:
            temp.remove(item)

        for item in temp:
            c1[item],c2[item] = c2[item],c1[item]

        child_gen.append(c1)
        child_gen.append(c2)
            
    return child_gen

def GENETIC_ALGO(k_weakest,generations,popu_size,ph,upb):
    k_weakest = int(k_weakest*n)

    solution = []
    population = ph.copy()
    
    prev_best = path_length(population[0])

    upper_bound = upb

    # sort population based on path length in ascending order
    # population.sort(key=lambda x : path_length(x))

    now_best = path_length(population[0])
    solution = (population[0])

    # print("0\t",now_best)

    for gen in range(0,generations): 
        # calculate fitness of each member of population
        fitness = []
        for item in population:
            # less path length = more fit
            fitness.append(-1*path_length(item))

        # generating new population with probability proportional to fitness
        selected = random.choices(population,fitness,k=popu_size)

        # CROSSOVER
        offsprings = CROSSOVER_OX(selected,popu_size)

        # sort offsprings based on path length in ascending order
        offsprings.sort(key=lambda x : path_length(x))

        # MUTATION
        for i in range(0,int(math.sqrt(popu_size))):
            temp = random.randrange(1,popu_size-2,1)

            start = random.randrange(0,n-1,1)
            end = random.randrange(start,n,1)
            offsprings[temp][start:end] = offsprings[temp][start:end][::-1]

        prev_best = path_length(population[0])
        population[k_weakest:] = offsprings[:k_weakest]

        population.sort(key=lambda x : path_length(x))

        now_best = path_length(population[0])

        if(prev_best > now_best):
            solution = population[0]
            # file = open("result.txt","w")
            for i in solution:
                # file.write(str(i) + ' ')
                print(i,end=' ')
            # file.close()
            print()
            # print(gen+1,"\t",now_best)
    return solution

path = list(range(0,n))
diffi = []

upb = 2 * path_length(path)

for i in range(0,n):
    temp_path = path.copy()
    random.shuffle(temp_path)

    temp_len = path_length(temp_path)

    upb = max(upb,temp_len)
    diff = path_length(temp_path) - path_length(path)

    if diff < 0:
        diff = -1* diff

    diffi.append(diff)

diff = float(0)

for i in range(0,n):
    diff = diff + diffi[i]

diff = diff / n

T = diff / 7
T_not = T

# print(path,"\t",path_length(path),"\n\n")

br = 0

solution = []
solution.append(path)

old_pl = path_length(path)
new_pl = path_length(solution[-1])
run = 0
while(T > 0.09):
    run = run + 1
    pre_pl = path_length(path)

    # graph(path)

    # randomly swapping two cities
    time = 0 
    final = 10*n
    if n > 100:
        final = n*2
    for sth in range(0,final):   # can replce final with n*n for best result (but time consuming)
        temp_path = path.copy()

        start,end = random.randrange(0,n,1),random.randrange(1,n,1)
        temp_path[start:end] = temp_path[start:end][::-1]
        # temp_path[start],temp_path[end] = temp_path[end],temp_path[start]

        new_pl = path_length(temp_path)

        if(new_pl < old_pl):
            # print(new_pl)
            solution.append(temp_path)
            # file = open("result.txt","w")
            for i in solution[-1]:
                # file.write(str(i) + ' ')
                print(i,end=' ')
            # file.close()
            print()
            old_pl = new_pl
        
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
    if(br > 5):
        break

    # print(T,"\t",path_length(path))
    if n > 100 and n < 500:
        T = T_not * math.exp(-0.005* run)
    if n < 101:
        T = T_not * math.exp(-0.003* run)
    if n > 499:
        T = T_not * math.exp(-0.009* run)

if n < 101:
    k_replace = 0.8
    generations_run = n*n                # n*n for best result
    population_size = int(4*n)             # n/2 for best result
if n > 101 and n < 301:
    k_replace = 0.9
    generations_run = n*n                # n*n for best result
    population_size = int(2*n)             # n/2 for best result
if n > 301:
    k_replace = 0.95
    generations_run = n*n                # n*n for best result
    population_size = int(n)             # n/2 for best result

# print(path_length(solution[-1]))
# print("k_replace = ",str(k_replace))
# print("generations_run = ",generations_run)
# print("population_size = ",population_size)
# print()

solution.reverse()

optimal_path = GENETIC_ALGO(k_replace,generations_run,population_size,solution[:population_size],upb)

# print(path_length(optimal_path))
# for i in optimal_path:
#     print(i,end=' ')
# print()