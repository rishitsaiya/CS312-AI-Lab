import copy
import random
class state:
    childs = []
    poles = [[],[],[]]
    parent = -1
    index = -1
    g = 0
    h = 0
    f = 0
    def __eq__(self,other):
        if(self.poles[0] == other.poles[0] and self.poles[1] == other.poles[1] and self.poles[2] == other.poles[2]):
            return True
        return False

state_set = []

def display(state):
    i = 0
    # print('Cost: ', state.cost)
    for pole in state.poles:
        print(i," -> ",pole)
        i = i + 1
    print()

def deepcopy(a):
    node = state()
    node.childs = copy.deepcopy(a.childs)
    node.poles = copy.deepcopy(a.poles)
    return node

def movegen(state):
    ls = []
    for i in range(0,3):
        for j in range(0,3):
            if(i != j):
                if(len(state.poles[i]) != 0):
                    if(len(state.poles[j]) == 0 or ((len(state.poles[j]) != 0) and (state.poles[j][-1] > state.poles[i][-1]))):
                        new = deepcopy(state)
                        new.poles[j].append(state.poles[i][-1])
                        del new.poles[i][-1]
                        if new not in state_set:
                            new.index = len(state_set)
                            state_set.append(new)
                        ls.append(state_set.index(new))
    return ls

def reconstruct_path(index):
    ls = [index]
    temp = index
    while(state_set[temp].parent != state_set[temp].index):
        # print(temp)
        temp = state_set[temp].parent
        ls.append(temp)
    ls.reverse()
    return ls

def cost(state):
    cost = discs*discs
    for i in range(0,3):
        for j in state.poles[i]:
            cost = cost + (i+1)*j
    return cost

def cost1(state, discs):
    cost = discs*discs
    for i in range(0,3):
        for j in range(len(state.poles[i])):
            if i % 2 == 0:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("A ", i+1, state.poles[i][j], j+1)
                        cost = cost - (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("B ", i+1, state.poles[i][j], j+1)
                        cost = cost + (i+1)*state.poles[i][j]*(j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("C ", i+1, state.poles[i][j], j+1)
                        cost = cost - (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("D ", i+1, state.poles[i][j], j+1)
                        cost = cost + (i+1)*state.poles[i][j]*(j+1)
            else:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("E ", i+1, state.poles[i][j], j+1)
                        cost = cost - (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("F ", i+1, state.poles[i][j], j+1)
                        cost = cost + (i+1)*state.poles[i][j]*(j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("G ", i+1, state.poles[i][j], j+1)
                        cost = cost - (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("H ", i+1, state.poles[i][j], j+1)
                        cost = cost + (i+1)*state.poles[i][j]*(j+1)
            # print(state.cost)
    d = discs
    # print(state.poles)
    for j in range(len(state.poles[0])):
        if d == state.poles[0][j]:
            # print("j: ", state.poles[0][j])
            cost = cost + state.poles[0][j]*(j+1)
            d = d - 1
    return cost

def cost2(state, discs):
    cost = discs*discs
    for i in range(0,3):
        for j in range(len(state.poles[i])):
            if i % 2 == 0:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("A ", i+1, state.poles[i][j], j+1)
                        cost = cost + (j+1)
                    else:
                        # print("B ", i+1, state.poles[i][j], j+1)
                        cost = cost - (j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("C ", i+1, state.poles[i][j], j+1)
                        cost = cost + (j+1)
                    else:
                        # print("D ", i+1, state.poles[i][j], j+1)
                        cost = cost - (j+1)
            else:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("E ", i+1, state.poles[i][j], j+1)
                        cost = cost + (j+1)
                    else:
                        # print("F ", i+1, state.poles[i][j], j+1)
                        cost = cost - (j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("G ", i+1, state.poles[i][j], j+1)
                        cost = cost + (j+1)
                    else:
                        # print("H ", i+1, state.poles[i][j], j+1)
                        cost = cost - (j+1)
            # print(cost)
    d = discs
    # print(state.poles)
    for j in range(len(state.poles[0])):
        if d == state.poles[0][j]:
            # print("j: ", state.poles[0][j], j)
            cost = cost - (j+1)
            # print(state.cost)
            d = d - 1
    return cost

def PropImp(m,CLOSED):
    # print("prpp")
    neighbours = movegen(state_set[m])
    for s in neighbours:
        new_g = state_set[m].g + cost(state_set[m]) - cost(state_set[n])
        if new_g < state_set[s].g:
            state_set[s].g = new_g
            if s in CLOSED:
                PropImp(s,CLOSED)

discs = int(input())

for i in range(0,3):
    state_set = []

    ls = list(range(1,discs+1))
    ls.reverse()

    start = state()
    start.parent = 0
    start.index = 0
    start.poles = [ls,[],[]]

    state_set.append(start)

    goal = state()
    goal.index = 1
    goal.poles = [[],[],ls]

    state_set.append(goal)

    ref = 0
    if i == 0:
        ref = cost(goal)
        print("Normal Funciton ")
        print(ref - cost(start),ref - cost(goal))
        start.h = ref - cost(start)
        goal.h = ref - cost(goal)
    if i == 1:
        ref = cost1(goal, discs)
        print("Over estimate")
        start.h = -1* (ref - cost1(start, discs))
        goal.h = -1* (ref - cost1(goal, discs))
        print(start.h, goal.h)
    if i == 2:
        ref = cost2(goal, discs)
        print("Under estimate")
        print(ref - cost2(start, discs),ref - cost2(goal, discs))
        start.h = ref - cost2(start, discs)
        goal.h = ref - cost2(goal, discs)

    OPEN = []
    CLOSED = []

    path = []

    start.f = start.h
    OPEN.append(start.index)

    while(len(OPEN) != 0):
        OPEN.sort(key = lambda x: state_set[x].f)
        n = OPEN[0]
        nem = state_set[n]
        del OPEN[0]
        CLOSED.append(n)
        if n == goal.index:
            print("goal reached")
            path = reconstruct_path(n)
            break
        neighbours = movegen(nem)
        for m in neighbours:
            mem = state_set[m]
            knm = 1
            # if i == 1:
            knm = cost(mem) - cost(nem)
            if m in OPEN:
                # print("mem in OPEN")
                if(nem.g + knm < mem.g):
                    mem.parent = n
                    mem.g = nem.g + knm
                    mem.f = mem.g + mem.h
            if m in CLOSED:
                # print("mem in CLOSED")
                if(nem.g + knm < mem.g):
                    mem.parent = n
                    mem.g = nem.g + knm
                    mem.f = mem.g + mem.h
                    PropImp(m,CLOSED)
            if m not in OPEN and m not in CLOSED:
                # print("mem is NEW")
                OPEN.append(m)
                if i == 0:
                    mem.h = ref - cost(mem)
                if i == 1 and mem.index != goal.index:
                    mem.h = (ref - cost1(mem, discs)) + 2*(start.h)
                if i == 2:
                    mem.h = ref - cost2(mem, discs)
                mem.parent = n
                mem.g = nem.g + knm
                mem.f = mem.g + mem.h

    # for item in state_set:
    #     print(item.index, item.h, item.g)
    print("path length = ",len(path))
    print("path     -> ",path)

    ls = list(map(lambda x: state_set[x].h,path))
    print("h-values -> ",ls)

    ls = list(map(lambda x: state_set[x].g,path))
    print("g-values -> ",ls)

    ls = list(map(lambda x: state_set[x].f,path))
    print("f-values -> ",ls)

    print("---------------------------------")
