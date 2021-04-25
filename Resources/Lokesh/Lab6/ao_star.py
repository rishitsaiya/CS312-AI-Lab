ls = input()
data = list(map(int, ls.split()))

N = len(data)

heutype = int(input())

class NODE:
    contains = []
    cost = float('inf')
    sibling = None
    type = None
    parent = None
    children = []
    marked = None

def h_under(node):
    if len(node.contains) == 1:
        node.type = "terminal"
        return 0
    if len(node.contains) == 2:
        node.type = 'terminal'
        ref = node.contains[0]
        return data[ref] * data[ref + 1] * data[ref + 2]
    return data[node.contains[0]] * data[node.contains[-1] + 1]

def h_over(node):
    if len(node.contains) == 1:
        node.type = "terminal"
        return 0
    if len(node.contains) == 2:
        node.type = 'terminal'
        ref = node.contains[0]
        return data[ref] * data[ref + 1] * data[ref + 2]
    cost = N * N * data[node.contains[0]]
    for i in node.contains:
        cost = cost * data[i + 1]
    return cost

def gen_child(node):
    for i in range(1, len(node.contains)):
        baby_A = NODE()
        baby_B = NODE()

        baby_A.sibling = baby_B
        baby_B.sibling = baby_A

        baby_A.contains = node.contains[0:i]
        baby_B.contains = node.contains[i:]

        baby_A.parent = node
        baby_B.parent = node

        if heutype == 0:
            baby_A.cost = h_over(baby_A)
            baby_B.cost = h_over(baby_B)
        else:
            baby_A.cost = h_under(baby_A)
            baby_B.cost = h_under(baby_B)

        node.children.extend([baby_A, baby_B])

        baby_A.children = []
        baby_B.children = []
        

root = NODE()
root.contains = list(range(0, N - 1))
if heutype == 0:
    root.cost = h_over(root)
else:
    root.cost = h_under(root)

List = [root]

def revise(node):
    if node.type == 'terminal':
        node.type = 'solved'
        revise(node.parent)
        return
    
    mini = float('inf')
    old_marked = node.marked
    
    for i in range(0, len(node.children), 2):
        left = node.children[i]
        right = node.children[i].sibling
        
        cost = data[left.contains[0]] * data[right.contains[0]] * data[right.contains[-1] + 1]

        cost = cost + left.cost + right.cost

        if mini > cost:
            mini = cost
            node.marked = left
            
    node.cost = mini        

    if old_marked in List:
        List.remove(old_marked)

    if node.marked is not None:
        left = node.marked
        right = left.sibling
        if (left.cost >= right.cost or right.type == 'solved') and left.type != 'solved':
            List.append(left)
        if (right.cost >= left.cost or left.type == 'solved') and right.type != 'solved':
            List.append(right)
            
        if left.type == 'solved' and right.type == 'solved':
            node.type = 'solved'
            if node.parent is not None:
                revise(node.parent)
                
states = 0
while root.type != 'solved':
    states += 1
    pick = List[0]
    List.remove(pick)

    if len(pick.children) == 0:
        gen_child(pick)

    revise(pick)

if heutype == 0:
    print('overi ', root.cost, "\t", states) 
else:
    print('under ', root.cost, "\t", states) 
