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
            
def beam_search(width, adj_list):
    pq = []
    y = []
    path = []
    pq.append(0)
    y.append(adj_list[0].cost)
    adj_list[0].visited = True
    goal = adj_list[0].cost + 1
    g = 0
    while len(pq) > 0:
        pq1 = []
        y1 = []
        w = 0
        n = 0
        check = 0
        if len(pq) < width:
            w = len(pq)
        else:
            w = width
        for i in range(w):
            node = pq.pop()
            c = y.pop()
            # print()
            # print()
            # print()
            # print()
            # print("check ", adj_list[node].cost, goal)
            if adj_list[node].cost >= goal:
                break
            else:
                if check == 0:
                    n = node
                    check = 1
                path.append(node)
                g = node
                # print("g: ", g)
                # print("node: ", node)
                # print("cost ",adj_list[node].cost)
                # print(adj_list[node].childs)
                # d_s(adj_list[node])
                # print("c: ", c)
                # pq1.clear()
                # y1.clear()
                for x in range(len(adj_list[node].childs)):
                    # print(adj_list[node].childs[x])
                    if adj_list[adj_list[node].childs[x]].visited == False and adj_list[adj_list[node].childs[x]].explored == False:
                        pq1.append(adj_list[node].childs[x])
                        adj_list[adj_list[node].childs[x]].visited = True
                        adj_list[adj_list[node].childs[x]].parent = node
                        y1.append(adj_list[adj_list[node].childs[x]].cost)
            adj_list[node].explored = True
            # print("pq1 -> ", pq1)
            # print("y1 -> ", y1)
            z = [x for _, x in sorted(zip(y1,pq1), reverse=True)]
            # print("z -> ", z)
            pq1 = z
            y1.sort(reverse=True)
            # print("pq1 -> ", pq1)
            # print("y1 -> ", y1)
        goal = adj_list[n].cost
        pq = pq1
        y = y1
        # print("pq -> ", pq)
        # print("y -> ", y)
    # print("path -> ", path)
    # print(len(path))
    # print()
    reconstruct_path(path, adj_list, g)

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

# for x in adj_list:
#     print("cost ",x.cost)
#     print(x.childs)
#     d_s(x)

print("BEAM SEARCH")
beam_search(3, adj_list)