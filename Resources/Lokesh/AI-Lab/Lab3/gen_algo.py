import math
import random
import copy
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

def GENETIC_ALGO(k_weakest,generations,popu_size):
    k_weakest = int(k_weakest*n)

    solution = []
    population = []

    path = list(range(0,n))
    upper_bound = 5 * path_length(path)

    # generate 'popu_size' candidates 
    for i in range(0,popu_size):
        temp = path.copy()
        random.shuffle(temp)
        population.append(temp)
    
    prev_best = path_length(population[0])

    # sort population based on path length in ascending order
    population.sort(key=lambda x : path_length(x))

    now_best = path_length(population[0])
    solution = (population[0])

    # print("0\t",now_best)

    for gen in range(0,generations):        
        # calculate fitness of each member of population
        fitness = []
        for item in population:
            # less path length = more fit
            fitness.append(upper_bound - path_length(item))

        # generating new population with probability proportional to fitness
        selected = random.choices(population,fitness,k=popu_size)

        # CROSSOVER
        offsprings = CROSSOVER_OX(selected,popu_size)

        # sort offsprings based on path length in ascending order
        offsprings.sort(key=lambda x : path_length(x))

        # MUTATION
        for i in range(0,int(popu_size/10)):
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
            # print(gen+1,"\t",now_best)
    return solution

k_replace = 0.7
generations_run = n*10                # n*n for best result
population_size = int(n/10)             # n/2 for best result
print("k_replace = ",str(k_replace))
print("generations_run = ",generations_run)
print("population_size = ",population_size)
print()

optimal_path = GENETIC_ALGO(k_replace,generations_run,population_size)

print(path_length(optimal_path))
for i in optimal_path:
    print(i,end=' ')
print()


# print(optimal_path)