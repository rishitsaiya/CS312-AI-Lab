import copy
import queue
class state:
    cost = 0
    childs = []
    poles = [[],[],[]]
    visited = False
    explored = False
    parent = 0

def d_s(state):
    i = 0
    for pole in state.poles:
        print(i," -> ",pole)
        i = i + 1
    print()

def deepcopy(a):
    node = state()
    node.childs = copy.deepcopy(a.childs)
    node.poles = copy.deepcopy(a.poles)
    return node

def cost(state):
    for i in range(0,3):
        for j in state.poles[i]:
            state.cost = state.cost + (i+1)*j

def cost1(state, discs):
    for i in range(0,3):
        for j in range(len(state.poles[i])):
            if i % 2 == 0:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("A ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost + (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("B ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost - (i+1)*state.poles[i][j]*(j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("C ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost + (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("D ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost - (i+1)*state.poles[i][j]*(j+1)
            else:
                if discs % 2 == 0:
                    if (j == 0 and state.poles[i][j] % 2 != 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("E ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost + (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("F ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost - (i+1)*state.poles[i][j]*(j+1)
                else:
                    if (j == 0 and state.poles[i][j] % 2 == 0) or (j != 0 and (state.poles[i][j-1] - state.poles[i][j]) % 2 != 0):
                        # print("G ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost + (i+1)*state.poles[i][j]*(j+1)
                    else:
                        # print("H ", i+1, state.poles[i][j], j+1)
                        state.cost = state.cost - (i+1)*state.poles[i][j]*(j+1)
            # print(state.cost)
    d = discs
    # print(state.poles)
    for j in range(len(state.poles[0])):
        if d == state.poles[0][j]:
            # print("j: ", state.poles[0][j])
            state.cost = state.cost - state.poles[0][j]*(j+1)
            d = d - 1

def reconstruct_path(path, adj_list, goal):
    print("Path Reconstruction")
    re_path = []
    # print(len(path))
    while len(path) > 0:
        x = path.pop()
        # print(x, goal)
        if x == goal:
            # print(x)
            goal = adj_list[x].parent
            # print(goal)
            re_path.append(x)
    re_path.reverse()
    # print()
    # print("Total States: ", len(re_path))
    print()
    for x in re_path:
        # print("node: ", x)
        # print("cost: ", adj_list[x].cost)
        # print("parent: ", adj_list[x].parent)
        d_s(adj_list[x])
    print("Total States: ", len(re_path))
            
def hill_climbing_v(n, k, adj_list, path):
    path.pop()
    pq = []
    y = []
    # path = []
    pq.append(n)
    y.append(adj_list[n].cost)
    adj_list[n].visited = True
    goal = adj_list[n].cost + 1
    g = 0
    while len(pq) > 0:
        node = pq.pop()
        c = y.pop()
        # print()
        # print()
        # print()
        # print()
        check = 0
        # print("check ", c, goal)
        if c >= goal:
            for x in adj_list[adj_list[node].parent].childs:
                if adj_list[x].parent == adj_list[node].parent:
                    adj_list[x].visited = False
                    # print("node: ", x)
            break
        else:
            check = 1
            goal = adj_list[node].cost
            # print("path -> ", path)
            # print(len(path))
            path.append(node)
            # print("path -> ", path)
            # print(len(path))
            g = node
            # print("g: ", g)
            # print("node: ", node)
            # print("cost ",adj_list[node].cost)
            # print(adj_list[node].childs)
            # d_s(adj_list[node])
            # print("c: ", c)
            pq.clear()
            y.clear()
            for x in range(len(adj_list[node].childs)):
                # print("child: ", adj_list[node].childs[x])
                if adj_list[adj_list[node].childs[x]].visited == False and adj_list[adj_list[node].childs[x]].explored == False:
                    if k != 1:
                        # print("Variable Changing")
                        xx = []
                        for yy in range(len(adj_list[adj_list[node].childs[x]].childs)):
                            # print(adj_list[adj_list[node].childs[x]].childs[yy])
                            # print(adj_list[adj_list[adj_list[node].childs[x]].childs[yy]].cost)
                            # print()
                            # print(adj_list[adj_list[node].childs[x]].cost)
                            c = adj_list[adj_list[node].childs[x]].cost - adj_list[adj_list[adj_list[node].childs[x]].childs[yy]].cost
                            xx.append(c)
                            # print(xx)
                        pq.append(adj_list[node].childs[x])
                        # print(pq)
                        adj_list[adj_list[node].childs[x]].visited = True
                        adj_list[adj_list[node].childs[x]].parent = node
                        xx.sort(reverse=True)
                        y.append(xx.pop())
                        # print(y)
                    else:
                        pq.append(adj_list[node].childs[x])
                        adj_list[adj_list[node].childs[x]].visited = True
                        adj_list[adj_list[node].childs[x]].parent = node
                        y.append(adj_list[adj_list[node].childs[x]].cost)
            k = 1
        if check == 1:
            adj_list[node].explored = True
        # print("pq -> ", pq)
        # print("y -> ", y)
        z = [x for _, x in sorted(zip(y,pq), reverse=True)]
        # print("z -> ", z)
        pq = z
        y.sort(reverse=True)
        # print("pq -> ", pq)
        # print("y -> ", y)
    # print("path -> ", path)
    # print(len(path))
    # print()
    # reconstruct_path(path, adj_list, g)
    return g, path

def variable_neighbourhood_descent(adj_list, goal):
    path = [0]
    g = 0
    i = 1
    while(g != goal):
        # print("Neighbour: ", i)
        g, path = hill_climbing_v(g, i, adj_list, path)
        i = i + 1
    reconstruct_path(path, adj_list, g)

    # print(goal)

adj_list = []

node = state()

discs = int(input())
ls = []
for i in range(0,discs):
    ls.append(discs - i)
node.poles = [ls,[],[]]
cost1(node, discs)

goal = state()
ls = []
for i in range(0,discs):
    ls.append(discs - i)
goal.poles = [[],[],ls]
cost1(goal, discs)

ref = goal.cost
goal.cost = 0
node.cost = ref - node.cost

gg = 0

adj_list.append(node)

size = 0
while(size != len(adj_list)):
    size = len(adj_list)
    for l in range(0,size):
        ref_state = adj_list[l]
        # Pole i -> j
        for i in range(0,3):
            for j in range(0,3):
                if(i != j):
                    if(len(ref_state.poles[i]) != 0):
                        if(len(ref_state.poles[j]) == 0) or (ref_state.poles[j][-1] > ref_state.poles[i][-1]):
                            temp = deepcopy(ref_state)
                            temp.poles[j].append(temp.poles[i][-1])
                            temp.poles[i].pop()
                            cost1(temp, discs)
                            temp.cost = ref - temp.cost
                            ind = -1
                            r = 0
                            for x in adj_list:
                                if(x.poles == goal.poles):
                                    gg = r
                                if(x.poles == temp.poles):
                                    ind = r
                                    break
                                r = r + 1
                            if(ind < 0):
                                ind = len(adj_list)
                                adj_list.append(temp)
                            ref_state.childs.append(ind)
        lok = set(ref_state.childs)
        ref_state.childs = list(lok)

print("VND")

variable_neighbourhood_descent(adj_list, gg)