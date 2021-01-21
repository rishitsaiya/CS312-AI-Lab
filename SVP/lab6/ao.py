import sys
import numpy as np
from node import Node
from node import T

class AOSearch():

    def __init__(self, dims):
        self.dims = dims
        self.root = Node(indices=np.arange(len(dims)-1), dims=dims)
        self.Q = [] # Q of or nodes


    def run(self):
        se = 0
        self.Q.append(self.root)
        while(self.root.type != T.SOLVED):
            se = se + 1
            # Get best leaf node to explore
            
            node = self.Q[0]
            self.Q.remove(node)

            # Make successors
            if len(node.children) <= 0:
                self.makeChildren(node)

            # Revise costs
            self.reviseCosts(node)  
        print(self.root.cost)
        print(f'Num explored: {se}')
    

    def makeChildren(self, node):
        '''
         Assuming node is OR Node, add all possible AND node solutions, with their children OR Nodes
        '''
        indices = node.indices
        N = len(indices)
        if N <= 2:
            return
        # print("Child of: ", *indices)
        for i in indices[:-1]:
            
            # Add new AND node as child to node
            new_node = Node(indices=indices, dims=self.dims, node_type=T.AND, parent=node)
            node.addChild(new_node)

            # Create left OR Node
            left_node = Node(indices=np.arange(indices[0], i+1), dims=self.dims, node_type=T.OR, parent=new_node)
            new_node.addChild(left_node)

            # Create right OR Node
            right_node = Node(indices=np.arange(i+1, indices[N-1] + 1), dims=self.dims, node_type=T.OR, parent=new_node)
            new_node.addChild(right_node)
            # print("L => ", left_node.indices, "R => ", right_node.indices)

    def reviseCosts(self, current):
        # if node is terminal, mark solved
        if current.type == T.TERMINAL:
            current.type = T.SOLVED
            self.reviseCosts(current.parent.parent)
            return
        
        min_cost = float("Inf")
        prev_marked = current.marked_child

        if current.type == T.OR:
            # Explore AND node children of current
            for node in current.children:
                if node.type == T.AND:
                    
                    # Get left and right children of AND node
                    left = node.children[0]
                    right = node.children[1]

                    # Get cost of multiply two childs
                    mult_cost = self.dims[left.indices[0]] * self.dims[right.indices[0]] * self.dims[right.indices[-1] + 1]
                    
                    # Update cost of AND node
                    node.cost = left.cost + right.cost + mult_cost

                    # Update current's marked_child
                    if node.cost < min_cost:
                        min_cost = node.cost
                        current.marked_child = node
            
            # Update OR node's cost with min_cost
            current.cost = min_cost

            # Remove prev_marked from list 
            if prev_marked in self.Q:
                self.Q.remove(prev_marked)

            # Add child of marked AND node with higher cost to Q
            if current.marked_child is not None:
                left = current.marked_child.children[0]
                right = current.marked_child.children[1]
                if (left.cost >= right.cost or right.type == T.SOLVED) and left.type != T.SOLVED:
                    self.Q.append(left)
                if (right.cost >= left.cost or left.type == T.SOLVED) and right.type != T.SOLVED:
                    self.Q.append(right)
                
                # Check if current is solved
                if left.type == T.SOLVED and right.type == T.SOLVED:
                    current.marked_child.type = T.SOLVED
                    current.type = T.SOLVED
            
            if current.parent != None and current.parent.parent.marked_child == current.parent:
                self.reviseCosts(current.parent.parent)

    def printBrackets(self):
        current = self.root
        while current != None:
            and_child = current.marked_child
            

if __name__ == '__main__':

    with open(sys.argv[1], "r") as file:
        input_dims = list(map(int, next(file).rstrip().split()))
    print(input_dims)
    AO = AOSearch(input_dims)
    AO.run()