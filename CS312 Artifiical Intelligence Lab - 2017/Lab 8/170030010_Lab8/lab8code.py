import numpy as np
import sys
import random

class environment:
	def __init__(self, numStates, numActions, gamma, grid, cost_per_dig, probSuccess, convert):
		self.nS = numStates
		self.nA = numActions
		self.gamma = gamma
		self.grid = grid
		self.cost = cost_per_dig
		self.prob = probSuccess
		self.topblock = [(0, 1, 2), (3, 1, 2), (0, 4, 2), (0, 1, 5), (-1, 1, 2), (3, 4, 2), (3, 1, 5), (0, 4, 5), (0, -1, 2), (0, 1, -1), (-1, 1, 5), (-1, 4, 2), (3, 4, 5), (3, -1, 2), (3, 1, -1), (0, 4, -1), (0, -1, 5), (-1, 4, 5), (-1, 1, -1), (-1, -1, 2), (0, -1, -1), (3, 4, -1), (3, -1, 5), (3, -1, -1), (-1, 4, -1), (-1, -1, 5), (-1, -1, -1)]
		self.nextstate = [(0, 1, 2, 3), (1, 4, 5, 6), (2, 1, 8, 7), (3, 6, 7, 9), (4, 4, 10, 11), (5, 11, 13, 12), (6, 10, 12, 14), (7, 12, 16, 15), (8, 13, 8, 16), (9, 14, 15, 9), (10, 10, 17, 18), (11, 11, 19, 17), (12, 17, 22, 21), (13, 19, 13, 22), (14, 18, 21, 14), (15, 21, 20, 15), (16, 22, 16, 20), (17, 17, 25, 24), (18, 18, 24, 18), (19, 19, 19, 25), (20, 23, 20, 20), (21, 24, 23, 21), (22, 25, 22, 23), (23, 26, 23, 23), (24, 24, 26, 24), (25, 25, 25, 26), (26, 26, 26, 26)]
		self.current = 0
		self.convert = convert
		self.maxMoves = 8
	def expectedNextStates(self, currentState):
		l = self.nextstate[currentState]
		d = {}
		for i in l:
			v = d.get(i, 0)
			d.update({i : v + 0.25})
		return d
	def expectedReward(self, currentState, nextAction):
		l = self.nextstate[currentState]
		tbs = self.topblock[currentState]
		nextState = l[nextAction]
		if nextState == currentState:
			return 0
		else:
			gain = self.grid[tbs[nextAction - 1]] * self.convert # Since 1, 2, 3 are block removing actions
			return gain - self.cost
	def valueIteration(self):
		values = np.zeros(self.nS)
		maxIterations = 100000
		epsilon = 1e-20
		for i in range(maxIterations):
			prev_values = np.copy(values)
			for s in range(self.nS):
				q_sa = []
				for a in range(self.nA):
					ExRew = self.expectedReward(s, a)
					ExNSt = self.expectedNextStates(s)
					su = 0
					for n in ExNSt.keys():
						su += values[n] * ExNSt.get(n) * self.prob
					q_sa.append(ExRew + self.gamma * su)
				values[s] = max(q_sa)
			if (np.sum(np.fabs(prev_values - values)) <= epsilon):
				break
		return (values)
	def computePolicyValues(self, policy):
		values = np.zeros(self.nS)
		epsilon = 1e-10
		while True:
			prev_values = np.copy(values)
			for s in range(self.nS):
				policy_a = policy[s]
				ExRew = self.expectedReward(s, int(policy_a))
				ExNSt = self.expectedNextStates(s)
				v = 0
				for n in ExNSt.keys():
					v += ExNSt.get(n) * (ExRew + self.gamma * prev_values[n])
				values[s] = v
			if (np.sum((np.fabs(prev_values - values))) <= epsilon):
				break
		return values
	def policyIteration(self):
		policy = np.random.choice(self.nA, size = self.nS)
		maxIterations = 10000
		for i in range(maxIterations):
			oldPolicyValues = self.computePolicyValues(policy)
			newPolicy = self.extractPolicy(oldPolicyValues)
			if (np.all(policy == newPolicy)):
				break
			policy = newPolicy
		return policy
	def extractPolicy(self, values):
		policy = np.zeros(self.nS)
		for s in range(self.nS):
			q_sa = np.zeros(self.nA)
			for a in range(self.nA):
				ExRew = self.expectedReward(s, a)
				ExNSt = self.expectedNextStates(s)
				for n in ExNSt.keys():
					q_sa[a] += ExNSt.get(n) * (ExRew + self.gamma * values[n])
			policy[s] = np.argmax(q_sa)
		return policy
	# def finalPolicyMaker(self, policy):
	# 	print ("PolicyMaker: ", end = "")
	# 	l = []
	# 	uniqueElements, countsElements = np.unique(policy, return_counts = True)
	# 	print (countsElements)
	# 	return policy
	def reset(self):
		self.current = 0
	def runEpisode(self, policy):
		self.reset()
		totalReward = 0
		for p in policy:
			i = int(p)
			tbs = self.topblock[i]
			ran = random.random()
			if ran > 0.2:
				totalReward += self.expectedReward(self.current, i)
			self.current = self.nextstate[self.current][i]
		return totalReward
	def evaluatePolicy(self, policy, n = 100):
		scores = []
		scores = [self.runEpisode(policy) for _ in range(n)]
		return np.mean(scores)

def main(filename):
	gamma = 0.0
	numStates = 27
	numActions = 4 # 1 means picking from the left-most stack, 2 from the center, 3 from the right and 0 means not digging at all
	file = open(filename, "r")
	lines = file.readlines()
	if len(lines) != 5:
		print ("Incorrect Arguments provided! Check the input again.")
	lines = [i[:-1] for i in lines]
	gridcost = [int(i) for i in lines[0].split() + lines[1].split()]
	probability = float(lines[2])
	cost = int(lines[3])
	convert = int(lines[4])

	# VALUE ITERATION
	env = environment(numStates, numActions, gamma, gridcost, cost, probability, convert)
	opt_value = env.valueIteration()
	opt_policy = env.extractPolicy(opt_value)
	policy_score = env.evaluatePolicy(opt_policy)
	print ("Policy Score for value iteration: ", end = "")
	print(policy_score)

	# POLICY ITERATION
	env2 = environment(numStates, numActions, gamma, gridcost, cost, probability, convert)
	opt_policy = env2.policyIteration()
	policy_score = env2.evaluatePolicy(opt_policy)
	print ("Policy Score for policy iteration: ", end = "")
	print (policy_score)




main(sys.argv[1])