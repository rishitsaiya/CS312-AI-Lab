import networkx as nx 
import sys

def makeG(mg, costs):
    for i in mg.nodes:
        mg.node[i]['solved']=False
        mg.node[i]['cost'] = costs[i]

    for i in mg.edges:
        mg[i[0]][i[1]]['marked']=False
        mg[i[0]][i[1]]['andby']=None
        

def cost(mg,node):
    return nx.get_node_attributes(mg,'cost')[node]


def solved(mg,node):
    return nx.get_node_attributes(mg,'solved')[node]


def andby(mg,edge1,edge2):
    return nx.get_edge_attributes(mg,'andby')[edge1,edge2]


def marked(mg,edge1,edge2):
    return nx.get_edge_attributes(mg,'marked')[edge1,edge2]


def findleaf(g, goalNodes):
    for i in g.nodes:
        if not g.__getitem__(i):
            if i not in goalNodes:
                return i

    return None

def addToG(g, n, nodeList, goalNodes, mainGraph):
    for i in nodeList:
        if not g.has_edge(n,i):
            g.add_edge(n,i,marked=False,andby=andby(mainGraph,n,i))
            g.node[i]['cost'] = cost(mainGraph,i)
            g.node[i]['solved'] = False
            if i in goalNodes : 
                g.node[i]['solved'] = True

def findMin(q, m, g):
    ls = []
    MinNode = min(q, key=q.get)
    ls.append(MinNode)
    if andby(g, m, MinNode):
        ls.append(andby(g, m, MinNode))
    return ls

def AO_Star(filename, mode):
    """
    Mode 1 -> Underestimation
    Mode 2 => Overestimation
    """
    file = open(filename, "r")

    l = [i[:-1] for i in file.readlines()]
    costs = {}

    numNodes = int(l.pop(0))

    startNode = "n" + l.pop(0)

    goalNodes = ["n" + i for i in l.pop(0).split(" ")]

    for i in range(numNodes):
        k = l.pop(0).split()
        costs.update({"n" + k[0]: int(k[1])})

    numEdges = int(l.pop(0))
    edges = []
    for i in range(numEdges):
        k = ["n" + i for i in l.pop(0).split(" ")]
        edges.append((k[0], k[1]))

    if mode == 1:
        edgecost = max(costs.values()) # Underestimation
    elif mode == 2:
        edgecost = min(costs.values()) # Overestimation

    mainGraph = nx.DiGraph()

    mainGraph.add_edges_from(edges)

    makeG(mainGraph, costs)

    for i in l:
        k = ["n" + j for j in i.split(" ")]
        mainGraph.edges[k[0], k[1]]["andby"] = k[2]
        mainGraph.edges[k[0], k[2]]["andby"] = k[1]

    g = mainGraph.subgraph(startNode).copy()

    if startNode in goalNodes :
        g.node[startNode]['solved'] = True

    while (solved(g,startNode) != True):
        gprime = g.subgraph(startNode).copy()
        for i in g.edges:
            if marked(g, i[0], i[1]):
                gprime.add_edge(i[0],i[1])

        n = findleaf(gprime, goalNodes)

        nodeList = list(mainGraph.neighbors(n))
        
        addToG(g, n, nodeList, goalNodes, mainGraph)
        s = [n]

        while (len(s) != 0):
            # Restricting Self Loops while choosing next node 'm'
            for i in s:
                if i not in list(g.neighbors(i)):
                    m = s.pop(s.index(i))
                    break

            # Finding which direction to go in from the node 'm'
            q = {}
            for i in list(g.neighbors(m)):
                if andby(g, m, i):
                    q[i] = 2 * edgecost + costs[i] + costs[andby(g, m, i)]
                else:
                    q[i] = 1 * edgecost + costs[i]

            markList = findMin(q, m, g)

            # Marking the selected edge.
            for i in markList:
                g.edges[m, i]['marked'] = True
                # Un-marking other previously marked edges
                for j in list(g.neighbors(m)):
                    if andby(g, m, j) != i and i != j:
                        g.edges[m, j]['marked'] = False
                        for a in list(g.neighbors(j)):
                            g.edges[j,a]['marked'] = False

            # Checking if this particular node has been solved
            checkNeighbors = True
            for i in g.neighbors(m):
                if marked(g,m,i):
                    if solved(g,i) == False:
                        checkNeighbors = False  
            if checkNeighbors:        
                g.node[m]['solved'] = True
            
            # updating the cost of the node m, and adding it's marked predecessors the list s
            if costs[m] != q[markList[0]]:
                costs[m] = q[markList[0]]
                for i in list(g.predecessors(m)):
                    if marked(g,i,m):
                        s.append(i)

            # if m is solved, add marked predecessors of m in s to be re-evaluated.
            if solved(g, m):
                for i in list(g.predecessors(m)):
                    if marked(g,i,m):
                        s.append(i)

    markedge = nx.get_edge_attributes(g, 'marked')

    if mode == 1:
        print("The answer graph contains below edges for underestimating heuristic:")
    if mode == 2:
        print("The answer graph contains below edges for overestimating heuristic:")
    for i in markedge:
        if markedge[i]:
            print(i)

def main(filename):
    """
    Run AO* with both underestimating heuristic and then overestimating heuristic
    """
    AO_Star(filename, 1)
    AO_Star(filename, 2)

main(sys.argv[1])
