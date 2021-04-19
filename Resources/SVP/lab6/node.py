import enum
import numpy as np
from heuristics import h1, h2


class T(enum.Enum):
    AND = 0
    OR = 1
    SOLVED = 2
    TERMINAL = 3


class Node():
    
    def __init__(self, indices, dims, node_type=T.OR, parent=None):
        self.type = node_type
        self.cost = float("Inf")
        self.parent = parent
        self.children = []
        self.indices = indices
        self.marked_child = None
        self.cost = self.getCost(dims)


    def getCost(self, dims):
         # If terminal node with single matrix, return 0
        if len(self.indices) == 1:
            self.type = T.TERMINAL
            return 0

        # If terminal node with two matrices, return cost of product
        if len(self.indices) == 2:
            self.type = T.TERMINAL
            return dims[self.indices[0]] * dims[self.indices[1]] * dims[self.indices[1]+1]

        # If non terminal node, get cost using heuristic
        else:
            return h2(self, dims)


    def addChild(self, child):
        self.children.append(child)