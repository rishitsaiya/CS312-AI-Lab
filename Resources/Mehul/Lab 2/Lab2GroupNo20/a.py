# Heuristic value 1: number of numbers which can fit into a given space
#
#

import sys
import copy

def generate_constraints(n, i, j):
    # print(n)
    if (n[i][j] != 0):
        return [0, 1, 2, 3, 4]
    l = []
    for i1 in range(4):
        l.append(n[i1][j])
        l.append(n[i][i1])
    if i <= 1 and j <= 1:
        l.append(n[0][0])
        l.append(n[0][1])
        l.append(n[1][0])
        l.append(n[1][1])
    elif i >= 2 and j <= 1:
        l.append(n[2][0])
        l.append(n[2][1])
        l.append(n[3][0])
        l.append(n[3][1])
    elif i <= 1 and j >= 2:
        l.append(n[0][2])
        l.append(n[0][3])
        l.append(n[1][2])
        l.append(n[1][3])
    elif i >= 2 and j >= 2:
        l.append(n[2][2])
        l.append(n[2][3])
        l.append(n[3][2])
        l.append(n[3][3])
    # print (l)
    l = list(dict.fromkeys(l)) 
    l1 = [0, 1, 2, 3, 4]
    for i in l:
        l1.remove(i)
    return l1

def generate_full(a):
    k = []
    for i in range(4):
        l = []
        for j in range(4):
            # print (i, j)
            l.append((generate_constraints(a, i, j)))
        k.append(l)
    return k

def hill_climb_search(a, k):
    for i in range(4):
        for j in range(4):
            if len(k[i][j]) == 1:
                a[i][j] = k[i][j][0]
                return a
    for i in range(4):
        for j in range(4):
            if len(k[i][j]) == 2:
                a[i][j] = k[i][j][0]
                return a
    

def Possible(k):
    for i in range(4):
        for j in range(4):
            if len(k[i][j]) < 5:
                return True 
    return False

def print_sudoku(a):
    for i in a:
        for j in i:
            print (j, end = " ")
        print ()

def k_counter(k):
	c = 0
	n = 0
	for i in k:
		for j in i:
			if len(j) != 5:
				c += len(j)
				n += 1
	return c

# def heuristic_fewer(k):
#     rv = 0
#     for i in k:
#         for j in i:
#             if len(j) != 5:
#                 rv += len(j)
#     return rv

def heuristic_fewer(k):
    rv = 0
    for i in k:
        for j in i:
            if len(j) == 1:
                rv += 1
    return rv

def construct_possibilities(a, k):
    rl = []
    for i in range(4):
        for j in range(4):
            if a[i][j] != 0:
                continue
            for l in k[i][j]:
                b = copy.deepcopy(a)
                b[i][j] = l
                rl.append(b)
    return rl

def main_hill_climb_1():
    a = []
    f = open(sys.argv[1], "r+")
    for i in f:
        l = []
        for j in i:
            if j == "\n":
                break;
            l.append(int(j))
        #print (i, end = "")
        a.append(l)
    k = generate_full(a)
    print_sudoku(a)
    print ()
    print ()
    #print (a)
    print (k_counter(k))

    while Possible(k):
        a = hill_climb_search(a, k)
        k = generate_full(a)
        #print (a)
        print (k_counter(k))

    print_sudoku(a)    

def main_BFS():
    a = []
    priority_q = []
    f = open(sys.argv[1], "r+")
    for i in f:
        l = []
        for j in i:
            if j == "\n":
                break
            l.append(int(j))
        #print (i, end = "")
        a.append(l)
    print_sudoku(a)
    print ()
    print ()
    k = generate_full(a)
    count = 0
    while Possible(k):
        print (count)
        count += 1
        next = construct_possibilities(a, k)
        for i in next:
            k1 = generate_full(i)
            h_f = heuristic_fewer(k1)
            priority_q.append((h_f, i))
        priority_q.sort(key=lambda x:x[0])
        # for i,j in priority_q:
        #     print_sudoku(j)
        #     print ("Heuristic: ", i)
        #     print ()
        #     print ()
        a = priority_q.pop(0)[1]
        k = generate_full(a)

    print_sudoku(a)

def main_hill_climb_2():
    a = []
    f = open(sys.argv[1], "r+")
    for i in f:
        l = []
        for j in i:
            if j == "\n":
                break
            l.append(int(j))
        #print (i, end = "")
        a.append(l)
    # print_sudoku(a)
    # print ()
    # print ()
    k = generate_full(a)
    count = 0
    while Possible(k):
        priority_q = []
        print_sudoku(a)
        print (count)
        count += 1
        next = construct_possibilities(a, k)
        # print (len(next))
        for i in next:
            k1 = generate_full(i)
            h_f = heuristic_fewer(k1)
            priority_q.append((h_f, i))
        priority_q.sort(key=lambda x:x[0], reverse=True)
        # for i,j in priority_q:
        #     print_sudoku(j)
        #     print ("Heuristic: ", i)
        #     print ()
        #     print ()
        try:
            a = priority_q.pop(0)[1]
            k = generate_full(a)
        except IndexError:
            # print_sudoku(a)
            print ("Hill Climb Failed.")
            return

    print_sudoku(a)
    print ("Hill climb works!\n\n")

def main_beam_search(n):
    a = []
    f = open(sys.argv[1], "r+")
    for i in f:
        l = []
        for j in i:
            if j == "\n":
                break;
            l.append(int(j))
        a.append(l)
    k = generate_full(a)
    count = 1
    beams = []
    next = construct_possibilities(a, k)
    for i in next:
        k1 = generate_full(i)
        h_f = heuristic_fewer(k1)
        beams.append((h_f, i))
    beams.sort(key=lambda x:x[0], reverse=True)
    beams = beams[:n]
    while True:
        priority_q = []
        print_sudoku(beams[0][1])
        print (count)
        count += 1
        for i in beams:
            k = generate_full(i[1])
            next = construct_possibilities(i[1], k)
        # print (len(next))
            for j in next:
                k1 = generate_full(j)
                h_f = heuristic_fewer(k1)
                priority_q.append((h_f, j))
        # for i,j in priority_q:
        #     print_sudoku(j)
        #     print ("Heuristic: ", i)
        #     print ()
        #     print ()
        priority_q.sort(key=lambda x:x[0], reverse=True)
        beams = priority_q[:n]
        if beams == []:
            print ("Beam Failed.")
            return
        try:
            for i in beams:
                # print_sudoku(i[1])
                kn = generate_full(i[1])
                if not Possible(kn):
                    break;
            # a = priority_q.pop(0)[1]
            # k = generate_full(a)
        except IndexError:
            # print_sudoku(a)
            print ("Beam Failed.")
            return

    print_sudoku(a)


    
# main_BFS()
main_hill_climb_2()
main_beam_search(1)