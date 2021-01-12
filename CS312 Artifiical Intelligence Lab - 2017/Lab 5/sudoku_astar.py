#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#| code for solving 4 x 4 sudoku puzzles using different search algorithms and heuristic functions |
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Some important notes:
# move gen has two different objectives to implement: find next empty cell to be filled in the matrix and decide what value is supposed to be filled in this next empty cell
# to implement both of these, heuristics are used
# there are two different kinds of heuristics used, one which fetches the next cell according to some value; and the other which sorts the neighbours according to some value
# mode in the driver code defines the first type of heuristic to be chosen based either on the maximun constrained empty cell or empty cell in the order of matrix traversal; and the second type of heuristic is the default one for sorting neighbours of the current state using the constraint number of the neighbour matrix 
import sys
import heapq # heapq module for implementing priority queue
import queue # queue module for implementing queue
import copy # copy module for copying nested lists
import random
# function to process output file
def process_output(matrix, as_matrix, flag5, as_states_explored):
	f = open("stats.txt", "a+")
	print("Puzzle\t\tSolution\n", file=f)
	for i in range(0,4):
		for j in range(0,4):
			print(matrix[i][j], end=" ", file=f)
		print("\t", end=" ", file=f)
		for j in range(0,4):
			print(as_matrix[i][j], end=" ", file=f)
		print("\n", file=f)
	print("A* States Explored:\t",as_states_explored, end=" ", file=f)
	if flag5:
		print("\t\t\tSolution found!", file=f)
	else:
		print("\t\t\tSolution not found!", file=f)
	f.close()
	g = open("table.txt", "a+")
	print(as_states_explored, end=" ", file=g)
	g.close()
# function to process input sudoku puzzle from text file into matrix
def process_input(input_file):
	matrix = []
	f = open(input_file, "r+")
	for rows in f:
		l = []
		for cols in rows:
			if cols == "\n":
				break
			l.append(int(cols))
		matrix.append(l)
	return matrix

# function to check if goal state is reached (goal test)
def is_matrix_solved(matrix):
	final_state = True
	for i in range(0,4):
		for j in range(0,4):
			if matrix[i][j] == 0:
				final_state = False
				break
	if final_state:
		return True

# function to get the next most constrained empty cell in the matrix
def get_most_constrained_cell(matrix):
	max_constraints = 0
	x, y = 0, 0
	for i in range(0,4): # for every cell in the matrix which is empty, calculate the constraint number and find the cell with maximum constrained number
		for j in range(0,4):
			constraints = 0
			if matrix[i][j]==0:
				for a in range(0,4):
					if a!=i:
						if matrix[a][j]!=0:
							constraints+=1
							break
				for b in range(0,4):
					if b!=j:
						if matrix[i][b]!=0:
							constraints+=1
							break
				if constraints>max_constraints:
					max_constraints = constraints
					x, y = i, j
	return x, y

# function to calculate the constaint number of the given configuration of matrix (state)
def get_constraint_number_of_matrix(new_matrix, val, x, y):
	new_matrix[x][y] = val
	constraints = 0
	for i in range(0,4):
		for j in range(0,4):
			if new_matrix[i][j]==0:
				for a in range(0,4):
					if a!=i:
						if new_matrix[a][j]!=0:
							constraints+=1
							break
				for b in range(0,4):
					if b!=j:
						if new_matrix[i][b]!=0:
							constraints+=1
							break
	return constraints

# function to get the next empty cell in the matrix in the order of traversal
def get_next_empty_cell(matrix):
	for i in range(0,4):
		for j in range(0,4):
			if matrix[i][j] == 0:
				return i, j

# function to get the quadrant of a given cell in the matrix
def get_quadrant(x, y):
	x+=1
	y+=1
	if((x == 1 or x == 2) and (y == 1 or y == 2)):
		return 0
	elif((x == 1 or x == 2) and (y == 3 or y == 4)):
		return 1
	elif((x == 3 or x == 4) and (y == 1 or y == 2)):
		return 2
	else:
		return 3

# function to check if a given configuration of matrix (state) is valid
def is_valid_configuration(matrix, x, y, val):
	is_valid = True
	for i in range(0,4): # check if the value entered in current cell (x,y) is unique in its column
		if matrix[i][y] == val and i!=x:
			is_valid = False
			return is_valid
	for j in range(0,4): # check if the value entered in current cell (x,y) is unique in its row
		if matrix[x][j] == val and j!=y:
			is_valid = False
			return is_valid
	quadrant = get_quadrant(x, y) # check the quadrant of the value entered in current cell (x,y) and check if all the values in this quadrant are unique
	if quadrant == 0:
		a, b = quadrant, quadrant
	elif quadrant == 1:
		a, b = quadrant-1, quadrant+1
	elif quadrant == 2:
		a, b = quadrant, quadrant-2
	else:
		a, b = quadrant-1, quadrant-1
	for i in range(a,a+2):
		for j in range(b,b+2):
			if i!=x and j!=y:
				if matrix[i][j] == val:
					is_valid = False
					break;
	return is_valid

# function to implement best-first search
def best_first_search(matrix, mode):
	bfs_q = []
	heapq.heappush(bfs_q,(0, matrix)) # priority queue to contain matrix states
	bfs_states_explored = 0
	while (len(bfs_q)!=0):  # while queue is not empty
		bfs_states_explored+=1
		current_matrix = heapq.heappop(bfs_q) # pop the head from the priority queue
		current_matrix = current_matrix[1]
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			return current_matrix, bfs_states_explored
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		####################
		# print(x, y)
		# for i in range(0,4):
		# 	print(current_matrix[i])
		####################
		for i in range(1,5): # check neighbours
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # if valid, push to priority queue based on heuristic value
				heapq.heappush(bfs_q,(-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix))
				# print(get_constraint_number_of_matrix(temp_matrix, i, x, y))
		# print("\n")

# function to implement hill-climbing search
def hill_climbing_search(matrix, mode):
	hcs_q = queue.Queue(maxsize=0) # queue to contain matrix states
	hcs_q.put(matrix) # initialize the queue with initial state
	hcs_states_explored = 0
	while (not(hcs_q.empty())): # while queue is not empty
		hcs_states_explored+=1
		current_matrix = hcs_q.get() # pop the head of the queue
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			return current_matrix, 1, hcs_states_explored
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		####################
		# print(x, y)
		# for i in range(0,4):
		# 	print(current_matrix[i])
		####################
		next_cell = [] # list to store neighbours
		for i in range(1,5):
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # if valid, add to neighbours list
				next_cell.append((-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix))
		sorted(next_cell, key=lambda tup: tup[0]) # sort the neoighbours according to heuristic value
		if len(next_cell) == 0: # if local optimum (no further valid neighbours) is reached, return current state and mention that goal state is not reached
			return current_matrix, 0, hcs_states_explored
		hcs_q.put(next_cell[0][1]) # add the neighbour with best heuristic value to the queue
		# print("\n")

# function to implement variable neighbourhood descent search
def variable_neighbourhood_descent_search(matrix, mode):
	vnds_q = queue.Queue(maxsize=0)  # queue to contain matrix states
	vnds_q.put(matrix) # initialize the queue with initial state
	neighbour_density = 1 # initialize neighbour density to 1
	vnds_states_explored = 0
	while (not(vnds_q.empty())): # while queue is not empty
		vnds_states_explored+=1
		current_matrix = vnds_q.get() # pop the head of the queue
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			return current_matrix, 1, vnds_states_explored
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		####################
		# print(x, y)
		# for i in range(0,4):
		# 	print(current_matrix[i])
		####################
		next_cell = [] # list to store neighbours
		for i in range(1,5):
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # if valid, add to neighbours list
				next_cell.append((-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix))
		sorted(next_cell, key=lambda tup: tup[0]) # sort the neighbours according to heuristic value
		if len(next_cell) == 0: # if local optimum (no further valid neighbours) is reached, restart from initial state and increase neighbour density
			neighbour_density+=1
			vnds_q.put(matrix)
		else: # add those many neighbours to the queue as is the neighbour density
			for i in range(0, len(next_cell)):
				if i>neighbour_density:
					break
				vnds_q.put(next_cell[i][1])

# function to implement beam search
def beam_search(matrix, beam_density, mode):
	bs_q = []
	heapq.heappush(bs_q,(0, matrix)) # priority queue to contain matrix states
	bs_states_explored = 0
	while (len(bs_q)!=0): # while queue is not empty
		bs_states_explored+=1
		current_matrix = heapq.heappop(bs_q) # pop the head from the priority queue
		current_matrix = current_matrix[1]
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			return current_matrix, 1, bs_states_explored
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		####################
		# print(x, y)
		# for i in range(0,4):
		# 	print(current_matrix[i])
		####################
		beam_counter = 0
		for i in range(1,5): # check neighbours
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # if valid, push to priority queue based on heuristic value
				heapq.heappush(bs_q,(-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix))
				beam_counter+=1
				if beam_counter == beam_density: # push only those many neighbours as is the size of beam width
					break
	return current_matrix, 0, bs_states_explored

# function to check if a given state is tabu
def is_tabu(matrix, x, y, i, tabu_list, tenure):
	in_tabu_list = False
	matrix[x][y] = i
	for i in range(0, tabu_list.qsize()):
		if tabu_list.queue[i]==matrix:
			in_tabu_list = True
			break
	return in_tabu_list	

# function to implement tabu search
def tabu_search(matrix, tenure, mode):
	ts_q = queue.Queue(maxsize=0) # queue to contain matrix state
	ts_q.put(matrix) # initialize queue with initial matrix state
	# aspiration_criterion = 1 
	ts_states_explored = 0 # counter for number of states explored
	tabu_list = queue.Queue(maxsize=0) # tabu list of size tenure
	while (not(ts_q.empty())): # run until queue is not empty
		ts_states_explored+=1
		current_matrix = ts_q.get() # pop the head of the queue
		# tabu_list.put(current_matrix)
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			return current_matrix, ts_states_explored, 1
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		####################
		# print(x, y)
		# for i in range(0,4):
		# 	print(current_matrix[i])
		####################
		next_cell = [] # list to store neighbour states of current state
		for i in range(1,5): # check neighbours
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i) and (not is_tabu(temp_matrix, x, y, i, tabu_list, tenure)): # check if neighbour state is valid and is not in tabu list
				next_cell.append((-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix)) # append to neighbours list
		sorted(next_cell, key=lambda tup: tup[0]) # sort neighbours according to heuristic value
		if len(next_cell) == 0: # if local optimum (no further valid neighbours) is reached, restart from initial state
			# ts_q.put(tabu_list.get())
			ts_q.put(matrix)
		else: # add neighbours to queue, add them to tabu list and if tabu list is full, pop the oldest entry (head) from the list
			for i in range(0, len(next_cell)):
				# print(len(next_cell), tenure)
				if tabu_list.qsize() == tenure:# if i>aspiration_criterion:# or ts_q.qsize() == tenure:
						tabu_list.get()
						# break
				ts_q.put(next_cell[i][1])
	
				tabu_list.put(next_cell[i][1])

class Node: 
      
    # Constructor to create a new node 
    def __init__(self, data, g, h, f, x, y): 
        self.data = data
        self.g = g
        self.h = h
        self.f = f
        self.parent = None
        self.x = x
        self.y = y

def get_empty_cell_count(temp_matrix):
	count = 0
	for i in range(0,4):
		for j in range(0,4):
			if temp_matrix[i][j]==0:
				count+=1
	return count

def find_matrix_sum(temp_matrix):
	summ = 0
	for i in range(0,4):
		for j in range(0,4):
				summ+=temp_matrix[i][j]
	return summ

def compute_h(temp_matrix, x, y, i, hmode): #takes current node
	if hmode == 0:
		h = get_constraint_number_of_matrix(temp_matrix, i, x, y) # overestimating heurisitc
	elif hmode == 1:
		h = random.random()# underestimating heuristic
	elif hmode == 2:
		h = get_empty_cell_count(temp_matrix) # optimal heuristic f =12
	else:
		h = random.random()*get_empty_cell_count(temp_matrix)
	# h = find_matrix_sum(temp_matrix)/random.random() # heuristic 3
	# h = (40-find_matrix_sum(temp_matrix))/12 # heurisitc 4
	# h = 0 # heuristic 5 (branch and bound)
	return  h

def compute_g(node): #takes parent node
	return node.g+1
	# return 0

def compute_f(node): #takes current node
	return node.g+node.h

def propagate_movement(node, open_list, closed):
	current_matrix = node.data
	x = node.x
	y = node.y
	for i in range(1,5): # check neighbours
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # check if neighbour state is valid
				is_in_open = False
				is_in_closed = False
				for i in range(0, len(open_list)):
					if temp_matrix == open_list[i].data:
						is_in_open = True
						prev_occurence = open_list[i]
						break
				for i in range(0, len(closed)):
					if temp_matrix == closed[i].data:
						is_in_closed = True
						prev_occurence = closed[i]
						break
				if node.g+1<prev_occurence.g:
					prev_occurence.parent=node
					prev_occurence.g=node.g+1
					if is_in_closed==True and is_in_open==False:
						propagate_movement(prev_occurence, open_list, closed)

def astar_search(matrix, mode, hmode):
	open_list = [] # open list
	root = Node(matrix, 0, 0, 0, 0 ,0)
	heapq.heappush(open_list,(0, root.data, root)) # priority queue to contain matrix states
	as_states_explored=0
	#fstart = hstart
	closed = [] # closed list
	while (len(open_list)!=0): # open list is not empty 
		as_states_explored+=1
		current_node = heapq.heappop(open_list) # pop the head from the priority queue
		current_node = current_node[2]
		closed.append(current_node)
		current_matrix = current_node.data
		# print(current_node.g)
		if is_matrix_solved(current_matrix.copy()): # check for goal state
			print(current_node.g)
			return current_matrix, as_states_explored, 1
		if mode == 0: # apply heurisitc acccording to mode
			x, y = get_next_empty_cell(current_matrix.copy())
		elif mode == 1:
			x, y = get_most_constrained_cell(current_matrix.copy())
		current_node.x = x
		current_node.y = y
		next_cell = [] # list to store neighbour states of current state
		for i in range(1,5): # check neighbours
			temp_matrix = copy.deepcopy(current_matrix)
			if is_valid_configuration(temp_matrix, x, y, i): # check if neighbour state is valid
				temp_matrix[x][y]=i
				# next_cell.append((-get_constraint_number_of_matrix(temp_matrix, i, x, y), temp_matrix)) # append to neighbours list
				is_in_open = False
				is_in_closed = False

				for k in range(0, len(open_list)):
					if temp_matrix == open_list[k][2].data:
						is_in_open = True
						prev_occurence = open_list[k][2]
						break
				for k in range(0, len(closed)):
					if temp_matrix == closed[k].data:
						is_in_closed = True
						prev_occurence = closed[k]
						break
				if is_in_open==False and is_in_closed==False:
					node = Node(temp_matrix, 0, 0, 0, 0, 0)
					node.g = compute_g(current_node)
					node.h = compute_h(temp_matrix, x, y, i, hmode)
					node.f = compute_f(node)
					node.parent = current_node
					# print(node.g, node.h, node.f)
					heapq.heappush(open_list,(-node.f, node.data, node))
					
				elif is_in_open==True and is_in_closed==False:
					if compute_g(current_node)<prev_occurence.g:
						node.g = compute_g(current_node)
						node.h = compute_h(temp_matrix, x, y, i, hmode)
						node.f = compute_f(node)
						node.parent = current_node
						# print("in open")
	
				elif is_in_open==False and is_in_closed==True:
					if compute_g(current_node)<prev_occurence.g:
						node.g = compute_g(current_node)
						node.h = compute_h(temp_matrix, x, y, i, hmode)
						node.f = compute_f(node)
						node.parent = current_node
						# print("in closed")
						propagate_movement(node, open_list, closed)

	print("open length",len(open_list))
	return current_matrix, as_states_explored, 0

def main():
	# declarations
	matrix = process_input(sys.argv[1]) # problem sudoku matrix (initial state)
	bfs_matrix = copy.deepcopy(matrix)	# instance of initial state for applying best-first search
	hcs_matrix = copy.deepcopy(matrix) # instance of initial state for applying hill-climbing search
	vnds_matrix = copy.deepcopy(matrix) # instance of initial state for applying variable neighbourhood descent search
	bs_matrix = copy.deepcopy(matrix) # instance of initial state for applying beam search
	ts_matrix = copy.deepcopy(matrix) # instance of initial state for applying tabu search
	as_matrix = copy.deepcopy(matrix) # instance of initial state for applying A* search
	# heuristic functions:	
	# mode = 0 => get next empty cell in order of matrix traversal
	# mode = 1 => get next mosht constrained cell
	bfs_mode = 0 # heuristic mode for best-first search
	hcs_mode = 0 # heuristic mode for hill-climbing search
	vnds_mode = 0 # heuristic mode for variable neighbourhood descent search
	bs_mode = 0 # heuristic mode for beam search
	beam_density = 4 # beam width for beam search
	ts_mode = 0 # heuristic mode for tabu search
	as_mode = 1 # meta heuristic mode for A* search
	hmode = 2 # 0 => overestimating heuristic, 1=> underestimating heuristic, 2=> optimal heuristic
	# driver code
	# bfs_matrix, bfs_states_explored = best_first_search(bfs_matrix, bfs_mode) # apply best-first search and print result
	# print("Puzzle solved after exploring", bfs_states_explored,"states using Best First Search ;)")
	# for i in range(0,4):
	# 	print(bfs_matrix[i])
	# print("*************")
	
	# ######################################################################################################################################
	# hcs_matrix, flag1, hcs_states_explored = hill_climbing_search(hcs_matrix, hcs_mode) # apply hill-climbing search and print result
	# if not flag1:
	# 	print("Goal state not reached after exploring", hcs_states_explored,"states using Hill Climbing Search. Puzzle un-solved :(")
	# else:
	# 	print("Puzzle solved after exploring", hcs_states_explored, "states using Hill Climbing Search!")
	# 	for i in range(0,4):
	# 		print(hcs_matrix[i])
	# print("*************")
	# ######################################################################################################################################
	
	# vnds_matrix, flag2, vnds_states_explored = variable_neighbourhood_descent_search(vnds_matrix, vnds_mode) # apply variable neighbourhood descent search and print result
	# if not flag2:
	# 	print("Goal state not reached after exploring", vnds_states_explored, "states using Variable Neighbourhood Descent Search. Puzzle un-solved :(")
	# else:
	# 	print("Puzzle solved after exploring", vnds_states_explored, "states using Variable Neighbourhood Descent Search ;)")
	# 	for i in range(0,4):
	# 		print(vnds_matrix[i])
	# print("*************")
	# ######################################################################################################################################
	
	# bs_matrix, flag3, bs_states_explored = beam_search(bs_matrix, beam_density, bs_mode) # apply beam search and print result
	# if not flag3:
	# 	print("Goal state not reached after exploring", bs_states_explored, "states using Beam Search with width", beam_density, ". Puzzle un-solved :(")
	# else:
	# 	print("Puzzle solved after exploring", bs_states_explored, "states using Beam Search with width", beam_density, " ;)")
	# 	for i in range(0,4):
	# 		print(bs_matrix[i])
	# print("*************")
	# ######################################################################################################################################
	
	# ts_matrix, ts_states_explored, flag4 = tabu_search(ts_matrix, 10, ts_mode) # apply tabu search and print result
	# if not flag4:
	# 	print("Goal state not reached after exploring", ts_states_explored, "states using Tabu Search. Puzzle un-solved :(")
	# else:
	# 	print("Puzzle solved after exploring", ts_states_explored, "states using Tabu Search ;)")
	# 	for i in range(0,4):
	# 		print(ts_matrix[i])
	# print("*************")
	######################################################################################################################################
	as_matrix, as_states_explored, flag5 = astar_search(as_matrix, as_mode, hmode) # apply a star search and print result
	if not flag5:
		print("Goal state not reached after exploring", as_states_explored, "states using A* Search. Puzzle un-solved :(")
	else:
		print("Puzzle solved after exploring", as_states_explored, "states using A* Search ;)")
		for i in range(0,4):
			print(as_matrix[i])
	print("*************")
	process_output(matrix, as_matrix, flag5, as_states_explored)
main()