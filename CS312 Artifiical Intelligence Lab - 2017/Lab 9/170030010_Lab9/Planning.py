import sys

class Arm:
	def __init__(self):
		self._holding = None
		self._empty = True
	def isEmpty(self):
		return self._empty
	def setEmpty(self, val):
		self._empty = val
	def getHolding(self):
		return self._holding
	def setHolding(self, val):
		self._holding = val
	def pick(self, blk):
		self.setHolding(blk)
		self.setEmpty(False)
		blk.setOnTable(False)
	def putdown(self, blk):
		self.setHolding(None)
		self.setEmpty(True)
		blk.setOnTable(True)
		blk.setOn(None)
	def __str__(self):
		if self._empty:
			return "Arm is Empty"
		else:
			return "Arm is holding " + str(self.getHolding().getName())

class block:
	def __init__(self, name):
		self._name = name
		self._clear = True
		self._onTable = True
		self._on = None
		self._top = None
	def getName(self):
		return self._name
	def isClear(self):
		return self._clear
	def setClear(self, val):
		self._clear = val
	def isOnTable(self):
		return self._onTable
	def setOnTable(self, val):
		self._onTable = val
	def isOn(self):
		return self._on
	def setOn(self, val):
		self._on = val	
	def getTop(self):
		return self._top
	def setTop(self, blk):
		self._top = blk
	def stack(self, other, arm): # stack self on other
		other.setClear(False)
		other.setTop(self)
		self.setOnTable(False)
		self.setOn(other)
		arm.setHolding(None)
		arm.setEmpty(True)
	def unstack(self, other, arm): # removes self from other
		arm.setHolding(self)
		arm.setEmpty(False)
		other.setClear(True)
		self.setOn(None)
		other.setTop(None)
	def __str__(self):
		if self.isOnTable():
			return "Block " + self._name + "\n" + "Placed on Table\nClear: " + str(self.isClear())
		elif self.isOn() != None:
			return "Block " + self._name + "\n" + "Placed on " + str(self.isOn().getName())+ "\nClear: " + str(self.isClear())
		else:
			return "Block " + self._name + "\n" + "Held by Arm\nClear: " + str(self.isClear())

def findBlock(blocklist, word):
	return blocklist[ord(word) - 97]

def generate_starting_state(filename):
	f = open(filename, "r")
	lines = f.readlines()
	# print (lines)
	lines = [i[:-1] for i in lines]
	# print (lines)
	blocks = int(lines[0])
	blocklist = []
	arm = Arm()
	for i in range(97, 97 + blocks):
		newBlock = block(chr(i))
		blocklist.append(newBlock)
	# on b a => b is on a
	# b.stack(a) => b is being placed on a
	current_state = [i[1:-1] for i in lines[1].split("^")]
	for i in current_state:
		precond = i.split()
		if len(precond) == 3:
			block1 = findBlock(blocklist, precond[1])
			block2 = findBlock(blocklist, precond[2])
			block1.stack(block2, arm)
		if len(precond) == 2:
			if precond[0] == "ontable":
				pass
			if precond[0] == "hold":
				block1 = findBlock(blocklist, precond[1])
				arm.setHolding(block1)
				arm.setEmpty(False)
				block1.setClear(False)
				block1.setOnTable(False)
			if precond[0] == "clear":
				pass
		if len(precond) == 1:
			arm.setHolding(None)
			arm.setEmpty(True)
	goalState = lines[2]
	return blocklist, arm, goalState

def checkCondition(condition, blocks, arm):
	condition = condition[1:-1]
	cond = condition.split()
	if len(cond) == 3:
		block1 = findBlock(blocks, cond[1])
		block2 = findBlock(blocks, cond[2])
		if block1.isOn() != None:
			if (block1.isOn().getName() == block2.getName()):
				return True
		return False
	elif len(cond) == 2:
		if cond[0] == "ontable":
			block1 = findBlock(blocks, cond[1])	
			if block1.isOnTable():
				return True	
			else:
				return False
		if cond[0] == "hold":
			block1 = findBlock(blocks, cond[1])			
			if not arm.isEmpty():
				if arm.getHolding().getName() == block1.getName():
					return True
			return False
		if cond[0] == "clear":
			block1 = findBlock(blocks, cond[1])			
			return block1.isClear()
	elif len(cond) == 1:
		return arm.isEmpty()


def main(filename):
	blocks, arm, goalState = generate_starting_state(filename)
	actions = []
	stack = []
	stack.append(goalState)

	while len(stack) != 0:
		nxt = stack.pop(-1)
		# A condition
		if nxt[0] == "(": 
			if "^" in nxt:
				# Conditions for multiple conditions.
				All = True
				conds = nxt.split("^")
				for i in conds:
					All = All and checkCondition(i, blocks, arm)
				if All:
					pass
				else:
					stack.append(nxt)
					for i in range(len(conds) - 1, -1, -1):
						stack.append(conds[i])
				continue
			# Check if the condition is true:
			if (checkCondition(nxt, blocks, arm)):
				continue
			nxt = nxt[1:-1]
			cond = nxt.split()
			# Condition: On 
			if len(cond) == 3:
				block1 = findBlock(blocks, cond[1])
				block2 = findBlock(blocks, cond[2])
				stack.append("stack " + block1.getName() + " " + block2.getName())
			if len(cond) == 2:
				# Condition: ontable
				if cond[0] == "ontable":
					stack.append("putdown " + cond[1])
					pass
				# Condition: hold
				if cond[0] == "hold":
					block1 = findBlock(blocks, cond[1])
					# If the block is on the table
					if block1.isOnTable():
						stack.append("pick " + cond[1])
					# If the block is on another block
					else:
						stack.append("unstack " + cond[1] + " " + block1.isOn().getName())
				# Condition: clear
				if cond[0] == "clear":
					block1 = findBlock(blocks, cond[1])
					block2 = block1.getTop()
					stack.append("unstack " + block2.getName() + " " + cond[1])
			# Condition: AE
			if len(cond) == 1:
				if arm.isEmpty():
					continue
				else:
					stack.append("putdown " + arm.getHolding().getName())
		# An action			
		else: 
			cond = nxt.split()
			# Condition: Stack
			if cond[0] == "stack":
				block1 = findBlock(blocks, cond[1])
				block2 = findBlock(blocks, cond[2])
				precondition1 = "(clear " + block1.getName() + ")" # b
				precondition2 = "(clear " + block2.getName() + ")" # a
				precondition3 = "(AE)"
				if checkCondition(precondition1, blocks, arm) and checkCondition(precondition2, blocks, arm) and checkCondition(precondition3, blocks, arm):
					block1.stack(block2, arm) # block 1 is being stacked on block 2; on b a => b is on top of a 
					actions.append(nxt)
					continue
				else:
					stack.append(nxt)
					stack.append(precondition1 + "^" + precondition2)
					stack.append(precondition3)
					stack.append(precondition1)
					stack.append(precondition2)
			# Condition: Unstack
			if cond[0] == "unstack":
				block1 = findBlock(blocks, cond[1])
				block2 = findBlock(blocks, cond[2])
				precondition1 = "(AE)"
				precondition2 = "(on " + block1.getName() + " " + block2.getName() + ")"
				precondition3 = "(clear " + block1.getName() + ")"				
				if checkCondition(precondition1, blocks, arm) and checkCondition(precondition2, blocks, arm) and checkCondition(precondition3, blocks, arm) :
					block1.unstack(block2, arm)
					actions.append(nxt)
					continue
				else:
					stack.append(nxt)
					stack.append(precondition1 + "^" + precondition2 + "^" + precondition3)
					stack.append(precondition1)
					stack.append(precondition3)
					stack.append(precondition2)
			# Condition: Pick
			if cond[0] == "pick":
				block1 = findBlock(blocks, cond[1])
				precondition1 = "(AE)"
				precondition2 = "(ontable " + block1.getName() + ")"
				precondition3 = "(clear " + block1.getName() + ")"
				if checkCondition(precondition1, blocks, arm) and checkCondition(precondition2, blocks, arm) and checkCondition(precondition3, blocks, arm) :
					arm.pick(block1)
					actions.append(nxt)
					continue
				else:
					stack.append(nxt)
					stack.append(precondition1 + "^" + precondition2 + "^" + precondition3)
					stack.append(precondition1)
					stack.append(precondition3)
					stack.append(precondition2)
			# Condition: Putdown
			if cond[0] == "putdown":
				block1 = findBlock(blocks, cond[1])
				precondition1 = "(hold " + block1.getName() + ")"
				if checkCondition(precondition1, blocks, arm):
					arm.putdown(block1)
					actions.append(nxt)
					continue
				else:
					stack.append(nxt)
					stack.append(precondition1)

	# Printing into output file:
	outfile = open("output.txt", "w+")
	for i in actions:
		outfile.write("(" + str(i) + ")\n")

main(sys.argv[1])