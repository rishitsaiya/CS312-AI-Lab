# uniform-ksat-problem

# Introduction
k-SAT or the Boolean Satisfiability problem is the problem of determining if a Boolean 
formula is satisfiable or unsatisfiable.

## Generate k-Sat problem
**k** : Clause length<br />
**m** : The number of clauses in the formula<br />
**n** : Number of variables

## Solving
Program to solve uniform 3-sat problem.
### Description
**Heuristic function** : Number of clauses which are true<br />
**Hill Climbing** : Initially variables are assigned values of 0 or 1 randomly. For each k-sat problem we calculate the heuristic function, if it is less than the maximum i.e. the number of clauses then we change the variable values one bit at the time. Then we again calculate the heuristic function and check again. 
We continue in this manner until the current value of the funtion is equal to its parent’s value.<br />
**Beam Search** : We have used the same heuristic function. This algorithm explores a graph by 
expanding the most promising node in a limited set.
