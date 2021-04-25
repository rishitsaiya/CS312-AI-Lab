import copy
import time
class state:
    h_value = 0
    poles = [[],[],[]]
    parent = 0
    ten = 0
    def __eq__(self,other):
        return self.poles == other.poles
    def disp(self):
        i = 0
        for pole in self.poles:
            print(i," --> ",pole)
            i = i + 1
        print() 

start = state()
discs = int(input())
ls = []
for i in range(0,discs):
    ls.append(discs - i)
start.poles = [ls,[],[]]
start.disp()

goal = state()
goal.poles = [[],[],ls]
goal.disp()

hue = -1

def movegen(STATE):
    ls = []
    for i in range(0,3):
        for j in range(0,3):
            if(i != j):               # from pole i to pole j
                node = state()
                node.h_value = STATE.h_value
                node.poles = copy.deepcopy(STATE.poles)
                if(len(node.poles[i]) != 0):   # source i.e., pole[i] is not empty
                    if((len(node.poles[j]) == 0) or (node.poles[j][-1] > node.poles[i][-1])):   # check for valid state
                        temp = node.poles[i][-1] 
                        node.poles[i].pop()
                        node.poles[j].append(temp)
                        if(hue == 1):
                            node.h_value = heuristic_1(node)
                        if(hue == 2):
                            node.h_value = heuristic_2(node)
                        if(hue == 3):
                            node.h_value = heuristic_3(node)
                        ls.append(node)
    return ls

def goaltest(TEST):
    if TEST.poles == goal.poles:
        return True
    return False

h1_offset = 3 * ((discs)*(discs + 1)) / 2
h2_offset = 3 * ((discs)*(discs + 1)) / 2
h3_offset = ((discs) * (11 - 2*(discs) ) * (discs + 1)) / 2

# print(h3_offset)

def heuristic_1(node):
    value = 0
    for i in range(0,3):
        for j in range(0,len(node.poles[i])):
            value = value + ((i + 1) * node.poles[i][j])
    return h1_offset - value

def heuristic_2(node):
    value = 0
    for i in range(0,3):
        for j in range(0,len(node.poles[i])):
            value = value + ((i + 1) * node.poles[i][j])
    return value

def heuristic_3(node):
    node.h_value = 0
    for i in range(0,3):
        for j in range(len(node.poles[i])):
            if i % 2 == 0:
                if discs % 2 == 0:
                    if (j == 0 and node.poles[i][j] % 2 == 0) or (j != 0 and (node.poles[i][j-1] - node.poles[i][j]) % 2 != 0):
                        # print("A ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value + (i+1)*node.poles[i][j]*(j+1)
                    else:
                        # print("B ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value - (i+1)*node.poles[i][j]*(j+1)
                else:
                    if (j == 0 and node.poles[i][j] % 2 != 0) or (j != 0 and (node.poles[i][j-1] - node.poles[i][j]) % 2 != 0):
                        # print("C ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value + (i+1)*node.poles[i][j]*(j+1)
                    else:
                        # print("D ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value - (i+1)*node.poles[i][j]*(j+1)
            else:
                if discs % 2 == 0:
                    if (j == 0 and node.poles[i][j] % 2 != 0) or (j != 0 and (node.poles[i][j-1] - node.poles[i][j]) % 2 != 0):
                        # print("E ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value + (i+1)*node.poles[i][j]*(j+1)
                    else:
                        # print("F ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value - (i+1)*node.poles[i][j]*(j+1)
                else:
                    if (j == 0 and node.poles[i][j] % 2 == 0) or (j != 0 and (node.poles[i][j-1] - node.poles[i][j]) % 2 != 0):
                        # print("G ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value + (i+1)*node.poles[i][j]*(j+1)
                    else:
                        # print("H ", i+1, node.poles[i][j], j+1)
                        node.h_value = node.h_value - (i+1)*node.poles[i][j]*(j+1)
            # print(node.h_value)
    d = discs
    # print(node.poles)
    for j in range(len(node.poles[0])):
        if d == node.poles[0][j]:
            # print("j: ", node.poles[0][j])
            node.h_value = node.h_value - node.poles[0][j]*(j+1)
            d = d - 1
    node.h_value = h3_offset - node.h_value
    return node.h_value








# BFS

print("BEST FIRST SEARCH\n")
print("Function\tStates\tPath Length")
now = time.time()
for q in range(0,4):
    hue = q

    OPEN = []
    CLOSED = []

    OPEN.append(start)
    states = 1
    path = []
    while(len(OPEN) != 0):
        temp = OPEN[0]
        CLOSED.append(temp)
        if(goaltest(temp)):
            break
        del OPEN[0]
        states = states + 1
        neighbours = movegen(temp)
        new_list = list(item for item in neighbours if (item not in CLOSED) and (item not in OPEN))
        for item in new_list:
            item.parent = len(CLOSED) - 1
        OPEN.extend(new_list)
        OPEN.sort(key=lambda x: x.h_value)

    path = []
    path.append(CLOSED[-2])

    while(path[-1] != start):
        path.append(CLOSED[path[-1].parent])
        
    path.reverse()
    path.append(goal)

    if(hue == 0):
        print("No Heuristic\t",states,"\t",len(path),time.time() - now)
    else:
        print("Heuristic ",hue,"\t",states,"\t",len(path),time.time() - now)

    # for item in path:
    #     item.disp()

print("\n")









# Hill Climb

print("HILL CLIMB")

now = time.time()

states = 1
hue = 3

node = start
node.h_value = heuristic_3(node)
print(node.h_value)

path = []
path.append(node)

neighbours = movegen(node)
neighbours.sort(key=lambda x: x.h_value)

# print("-------")
# for item in neighbours:
#     print(item.h_value)
#     item.disp()
# print("-------")

new_node = neighbours[0]
path.append(new_node)

print(node.h_value," ",new_node.h_value)
new_node.disp()

while(node.h_value > new_node.h_value):
        node = new_node
        states = states + 1
        if(goaltest(node)):
            break

        neighbours = movegen(node)
        neighbours.sort(key=lambda x: x.h_value)
        
        new_node = neighbours[0]
        path.append(new_node)
        print(node.h_value," ",new_node.h_value)
        new_node.disp()

print("States ",states,"\tPath Length ",len(path),"\tTime",time.time() - now,"\n\n")

# for item in path:
#     item.disp()











# Tabu Search

print("TABU")

hue = 3
saturation = False
for t in range(discs*6,1,-1):
    tenure = t
    states = 0

    searchable = []
    restricted = []

    node = start
    states = states + 1
    # node.disp()
    restricted.append(node)

    neighbours = movegen(node)
    neighbours.sort(key=lambda x: x.h_value)

    searchable = neighbours

    node = searchable[0]
    states = states + 1

    original = time.time()

    while(not goaltest(node) ):
        if(time.time() - original > 1):
            saturation = True
            break
        # node.disp()
        neighbours = movegen(node)
        neighbours.sort(key=lambda x: x.h_value)

        node.ten = tenure
        restricted.append(node)

        del searchable[0]

        for item in restricted:
            item.ten = item.ten - 1
            if(item in neighbours):
                neighbours.remove(item)
            if(item.ten == 0):
                restricted.remove(item)

        for item in searchable:
            if item not in neighbours:
                neighbours.append(item)

        searchable = neighbours
        
        if(len(searchable) == 0):
            break
        node = searchable[0]
        states = states + 1
    if saturation:
        break

    print(tenure," ",states)



# Beam Search

