import sys
import random
import copy
from scipy.special import expit
import time
import math
from operator import attrgetter

class Town:
	def __init__(self, x, y, distance_list):
		self.x = x
		self.y = y
		self.dist = distance_list
	def get_distance_to_town(self, town_number):
		return self.dist[town_number]
	def get_co_ordinates(self):
		return (self.x, self.y)
	def get_all_distances(self):
		return self.dist

class solution:
	def __init__(self, order, towns):
		self.ordered = order
		self.towns = towns
		self.cost = self.calculate_cost_of_state()
	def calculate_cost_of_state(self):
		cost = 0
		for i in range(len(self.ordered) - 1):
			cost += self.towns[self.ordered[i]].get_distance_to_town(self.ordered[i + 1])
		return cost
	def get_ordering(self):
		return self.ordered
	def generate_neighbours(self):
		neighbours = []
		for i in range(len(self.ordered) - 1):
			new_list = copy.deepcopy(self.ordered)
			new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
			new_solution = solution(new_list, self.towns)
			neighbours.append(new_solution)
		return neighbours
	def generate_random_neighbour(self):
		a = random.randrange(len(self.ordered))
		b = random.randrange(len(self.ordered))
		new_list = copy.deepcopy(self.ordered)
		new_list[a], new_list[b] = new_list[b], new_list[a]
		new_solution = solution(new_list, self.towns)
		return new_solution
	def __eq__(self, other):
		if self.ordered == other.ordered:
			return True
		return False
	def __str__(self):
		s = str(self.calculate_cost_of_state()) + "\n"
		for i in self.ordered:
			s += str(i)
			s += " "
		return s

class simulated_annealing:
	def __init__(self, number_of_towns, towns, cooling_rate, initial_temperature, closing_temperature, closing_iterations):
		self.current_solution = solution(self.generate_random_starting_solution(number_of_towns), towns)
		self.cooling_rate = cooling_rate
		self.current_temperature = initial_temperature
		self.current_iteration = 1
		self.closing_temperature = closing_temperature
		self.closing_iterations = closing_iterations
		self.best_solution = self.current_solution
	def get_next_solution(self):
		current_cost = self.current_solution.calculate_cost_of_state()
		while (True):
			i = self.current_solution.generate_random_neighbour()
			neighbouring_cost = (current_cost - i.calculate_cost_of_state()) / self.current_temperature
			probability = expit(neighbouring_cost)
			random_number = random.random()
			if probability > random_number:
				if self.best_solution.calculate_cost_of_state() > i.calculate_cost_of_state():
					self.best_solution = i
				return i
		return self.current_solution
	def generate_random_starting_solution(self, number_of_towns):
		l = [i for i in range(number_of_towns)]
		random.shuffle(l)
		return (l)
	def run_sim(self):
		while ((self.current_iteration < self.closing_iterations) and (self.current_temperature > self.closing_temperature)):
			self.current_solution = self.get_next_solution()
			self.current_iteration += 1
			self.current_temperature *= self.cooling_rate
		return (self.best_solution)
	def get_current_solution(self):
		return self.current_solution

class genetic_algorithm:
	def __init__(self, number_of_towns, towns, initial_solution_size, crossover_algorirhm, mutation_prob, terminating_iterations):
		initial_solutions = []
		for i in range(initial_solution_size):
			initial_solutions.append(solution(self.generate_random_starting_solution(number_of_towns), towns))
		self.current_solutions = initial_solutions
		self.towns = towns
		self.number_of_towns = number_of_towns
		self.crossover_algorirhm = crossover_algorirhm
		self.mutation_prob = mutation_prob
		self.terminating_iterations = terminating_iterations
	def mutate(self, solution_order):
		k = random.random()
		if (k < self.mutation_prob):
			a = random.randrange(self.number_of_towns)
			b = random.randrange(self.number_of_towns)
			solution_order[a], solution_order[b] = solution_order[b], solution_order[a]
			new_solution = solution(solution_order, self.towns)
			return new_solution
		else:
			sn = solution(solution_order, self.towns)
			return sn
	def create_new_offsprings(self):
		a = random.randrange(len(self.current_solutions))
		b = random.randrange(len(self.current_solutions))
		parent1 = self.current_solutions[a].get_ordering()
		parent2 = self.current_solutions[b].get_ordering()
		offspring1, offspring2 = self.crossover_algorirhm(parent1, parent2)
		offspring1 = self.mutate(offspring1)
		offspring2 = self.mutate(offspring2)
		return offspring1, offspring2
	def run_model(self):
		for i in range(self.terminating_iterations):
			new_1, new_2 = self.create_new_offsprings()
			self.current_solutions.append(new_1)
			self.current_solutions.append(new_2)
			self.current_solutions.sort(key = attrgetter("cost"))
			self.current_solutions = self.current_solutions[:-2]
		return self.current_solutions[0]
	def generate_random_starting_solution(self, number_of_towns):
		l = [i for i in range(number_of_towns)]
		random.shuffle(l)
		return (l)

class ant_colony_optimisation:
	def __init__(self, number_of_towns, towns, ants, alpha, beta, rho, q, pheromone, terminating_iterations):
		self.number_of_towns = number_of_towns
		self.towns = towns
		self.ants = ants
		self.alpha = alpha
		self.beta = beta
		self.rho = rho
		self.q = q
		self.pheromone = pheromone
		self.iterations = terminating_iterations
	def update_pheromone(self, pheromone_to_be, current_path):
		s = solution(current_path, self.towns)
		Lk = s.calculate_cost_of_state()
		pheromone_to_add = self.q / Lk
		for i in range(len(current_path) - 1):
			pheromone_to_be[current_path[i]][current_path[i + 1]] *= self.rho
			pheromone_to_be[current_path[i]][current_path[i + 1]] += pheromone_to_add
			pheromone_to_be[current_path[i + 1]][current_path[i]] *= self.rho
			pheromone_to_be[current_path[i + 1]][current_path[i]] += pheromone_to_add
		return pheromone_to_be
	def decide_next_move(self, current_path):
		valid_moves = [i for i in range(self.number_of_towns) if i not in current_path]
		current_location = current_path[-1]
		valid_pheromone = [math.pow(self.pheromone[current_location][valid_moves[i]], self.alpha) for i in range(len(valid_moves))]
		valid_distances = [math.pow((1 / self.towns[current_location].get_distance_to_town(i)), self.beta) for i in valid_moves]
		valid_product = [valid_pheromone[i] * valid_distances[i] for i in range(len(valid_moves))]
		valid_prob = [valid_product[i] / sum(valid_product) for i in range(len(valid_moves))]			
		a = random.random()
		i = 0
		s = valid_prob[0]
		while True:
			if (s > a):
				return valid_moves[i] 
			i += 1
			s += valid_prob[i]
	def run_ants(self):
		min = -1
		best_solution = solution([i for i in range(self.number_of_towns)], self.towns)
		for i in range(self.iterations):
			pheromone_to_be = copy.deepcopy(self.pheromone)
			for i in range(self.ants):
				current_path = [0]
				while (len(current_path) != self.number_of_towns):
					current_path.append(self.decide_next_move(current_path))
				if min == -1:
					min = solution(current_path, self.towns).calculate_cost_of_state()
					best_solution = solution(current_path, self.towns)
				elif min > solution(current_path, self.towns).calculate_cost_of_state():
					min = solution(current_path, self.towns).calculate_cost_of_state()
					best_solution = solution(current_path, self.towns)
				pheromone_to_be = self.update_pheromone(pheromone_to_be, current_path)
			self.pheromone = pheromone_to_be
		return best_solution

def CX2_modified(p1, p2):
	circular_list = []
	circular_list.append(p2[0])
	while len(circular_list) != len(p1):
		if p2[p1.index(circular_list[-1])] not in circular_list:
			circular_list.append(p2[p1.index(circular_list[-1])])
		else:
			for i in p2:
				if i not in circular_list:
					circular_list.append(i)
					break
	offspring1 = []
	offspring2 = []
	index = 0
	number_of_elements = len(circular_list)
	for i in range(number_of_elements):
		offspring2.append(circular_list[index])
		index += 2
		index = index % number_of_elements
		offspring1.append(circular_list[index])
		index += 1
		index = index % number_of_elements
	return (offspring1, offspring2)

def Order_Crossover(p1, p2):
	a = random.randrange(len(p1))
	b = random.randrange(len(p1))
	while (a >= b):
		a = random.randrange(len(p1))
		b = random.randrange(len(p1))
	offspring1 = [-1 for i in range(len(p1))]
	offspring2 = [-1 for i in range(len(p2))]
	offspring1[a:b] = p1[a:b]
	offspring2[a:b] = p2[a:b]
	parent1_copy = copy.deepcopy(p1)
	parent2_copy = copy.deepcopy(p2)
	for i in p1[a:b]:
		parent2_copy.remove(i)
	for i in p2[a:b]:
		parent1_copy.remove(i)	
	for i in range(len(offspring2)):
		if offspring2[i] == -1:
			offspring2[i] = parent1_copy.pop(0)
		if offspring1[i] == -1:
			offspring1[i] = parent2_copy.pop(0)
	return (offspring1, offspring2)

def read_file(file):
	f = open(file, "r+");
	l = []
	for i in f:
		l.append(i)
	dst = str(l.pop(0)[:-1])
	n = int(l.pop(0)[:-1])
	number_of_towns = n
	towns = []
	for i in range(n):
		dl = [float(i) for i in str(l.pop(n)[:-1]).split(" ")]
		k = l.pop(0)
		x = float(str(k[:-1]).split(" ")[0])
		y = float(str(k[:-1]).split(" ")[1])
		t = Town(x, y, dl)
		towns.append(t)
		n = n - 1
	return number_of_towns, towns

def main():
	random.seed(time.time())
	number_of_towns, towns = read_file(sys.argv[1])
	print ("Staritng Simulated Annealing: ")
	annealing1 = simulated_annealing(number_of_towns, towns, 0.9995, 100, 1, 100000)
	final_cost_annealing = annealing1.run_sim()
	print ("Results for Simulated Annealing: ", end = "")
	print (final_cost_annealing)
	print ("Starting Genetic Algorithm: ")
	genetic1 = genetic_algorithm(number_of_towns, towns, 100, Order_Crossover, 0.15, 10000)
	final_cost_genetic = (genetic1.run_model())
	print ("Results for Genetic Algorithm: ", end = "")
	print (final_cost_genetic)
	print ("Starting Ant Colony Optimisation: ")
	initial_pheromone = [[1 / (number_of_towns * number_of_towns) for j in range(number_of_towns)] for i in range(number_of_towns)]
	ants1 = ant_colony_optimisation(number_of_towns, towns, 10, 1.0, 10.0, 0.5, 10, initial_pheromone, 100)
	final_cost_aco = (ants1.run_ants())
	print ("Results for Ant Colony Optimisation: ", end = "")
	print (final_cost_aco)

main()
