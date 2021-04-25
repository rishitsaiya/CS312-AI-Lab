import math
import random
import sys

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

# Creating cities from the graph given
for i in range(0,n):
    temp = cities()
    row = data[i + 2].split()
    temp.x = float(row[0])
    temp.y = float(row[1])
    temp.index = int(i)
    temp.distance = data[i + n + 2].split()
    city.append(temp)
    
class ants:
    index = int(0)
    cities = []

ant = []

A = 15

if n < A:
    A = n

# Creating ants for each cities
for i in range(A):
    temp = ants()
    temp.index = i
    t = []
    t.append(i)
    temp.cities = t
    ant.append(temp)

eta = []

# Defining Visibility Matrix
for i in range(n):
    temp = []
    for j in range(n):
        if i == j:
            temp.append(sys.float_info.max)
        else:
            temp.append(1/float(city[i].distance[j]))
    eta.append(temp)

tou = []

# Defining Pheremone Matrix
for i in range(n):
    temp = []
    for j in range(n):
        if i == j:
            temp.append(1)
        else:
            temp.append(sys.float_info.min)
    tou.append(temp)

alpha = 1
beta = 1
prob = []
cum_prob = []

# A function to calculate the initial probability matrix for each iteration
def probab(prob, cum_prob, k):
    sum = 0
    for s in range(n):
        if s not in ant[k].cities:
            for i in range(n):
                if i != s:
                    # Denominator sum for all allowed cities for ant k
                    sum = sum + pow(tou[i][s],alpha)*pow(eta[i][s],beta)
    temp = []
    for i in range(n):
        t = []
        for j in range(n):
            if i != j and j not in ant[k].cities:
                num = pow(tou[i][j],alpha)*pow(eta[i][j],beta)
                # Probability for each ant k to travel in edge i-j
                p = num/sum
                t.append(p)
            else:
                t.append(0)
        temp.append(t)
    prob.append(temp)

    # Calculating the cumulative probability matrix
    temp = []
    for i in range(n):
        t = []
        sum = 0
        for j in range(n):
            sum = sum + prob[k][i][j]
            t.append(sum)
        temp.append(t)
    cum_prob.append(temp)

# Creating Initial Probability Matrix
for k in range(A):
    probab(prob, cum_prob, k)

# A Function to update probabilities after each city is travelled by an ant
def Update_prob(prob, cum_prob, k):
    sum = 0
    for s in range(n):
        if s not in ant[k].cities:
            for i in range(n):
                if i != s:
                    sum = sum + pow(tou[i][s],alpha)*pow(eta[i][s],beta)
    for i in range(n):
        for j in range(n):
            if i != j and j not in ant[k].cities:
                num = pow(tou[i][j],alpha)*pow(eta[i][j],beta)
                p = num/sum
                prob[k][i][j] = p
            else:
                prob[k][i][j] = 0

    for i in range(n):
        sum = 0
        for j in range(n):
            sum = sum + prob[k][i][j]
            cum_prob[k][i][j] = sum

roh = 0.5
Q = 1

# A function to update pheremones after each iteration
def update_tou(path, path_length, tou):
    del_tou_each = []
    for k in range(A):
        temp = []
        for i in range(n):
            t = []
            for j in range(n):
                delta = 0
                for x in range(n):
                    # If path available, delta is inverse of the tour length else 0
                    if i == path[k][x] and j == path[k][x+1]:
                        delta = Q/path_length[k]
                        break
                    else:
                        delta = 0
                t.append(delta)
            temp.append(t)
        del_tou_each.append(temp)
    del_tou = []
    for i in range(n):
        temp = []
        for j in range(n):
            sum = 0
            for k in range(A):
                # Delta Tau for all ants in edge i-j
                sum = sum + del_tou_each[k][i][j]
            temp.append(sum)
        del_tou.append(temp)
    for i in range(n):
        for j in range(n):
            # Update Tau
            tou[i][j] = tou[i][j]*(1-roh) + del_tou[i][j]
    
# Fucntion to reset Cities travelled by ants after each iteration
def reset_ant_cities():
    for k in range(A):
        ant[k].cities = [k]

Pat = []
Pat_len = []
# Iterations
for iti in range(A):
    # print("Iteration: ", iti)
    path = []
    path_length = []
    # For each Ants
    for k in range(A):
        temp = []
        length = 0
        # While it completes a tour
        while(True):
            i = ant[k].index
            temp.append(i)
            # Random Probability to choose a path
            rand = random.uniform(0,max(cum_prob[k][i]))
            for j in range(n):
                next = k
                # Choose a path with Rand probability if it is not travelled earlier
                if j not in ant[k].cities and rand < cum_prob[k][i][j]:
                    next = j
                    break
            ant[k].cities.append(next)
            ant[k].index = next
            length = length + float(city[i].distance[next])
            if next == k:
                temp.append(next)
                break
            Update_prob(prob, cum_prob, k)
        # print("City: ", temp[0], end =" ")
        # print("\tLength: ", length)
        path.append(temp)
        path_length.append(length)
    # Update Pheremones after a tour is completed
    update_tou(path,path_length,tou)

    # Take the minimum from that Iteration
    minimum = path_length.index(min(path_length))

    Pat.append(path[minimum])
    Pat_len.append(path_length[minimum])
    # print("Start City", path[minimum][0], end =" ")
    # print("\tBest Length: ", path_length[minimum])

    # Reset Ant Cities for next Iteration
    reset_ant_cities()
    
    # Reset Probability Matrix
    prob.clear()
    cum_prob.clear()
    for k in range(A):
        probab(prob, cum_prob, k)

mini = Pat_len.index(min(Pat_len))

print(Pat_len[mini])
for i in range(len(Pat[mini])):
    print(Pat[mini][i], end=" ")
print()