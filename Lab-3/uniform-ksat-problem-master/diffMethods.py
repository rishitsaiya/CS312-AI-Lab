# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from string import ascii_lowercase
import random
from itertools import combinations
import numpy as np

# %%
print("Enter the number of clauses ")
m = int(input())
print("Enter the number of variables in a clause ")
k = int(input())
print("Enter number of variables ")
n = int(input())

# %%
def createProblem(m, k, n):
    #lower Case +ve
    positive_var = (list(ascii_lowercase))[:n]
    negative_var = [c.upper() for c in positive_var]
    variables = positive_var + negative_var
    threshold = 10
    problems = []
    allCombs = list(combinations(variables, k))
    i = 0

    while i<threshold:
        c = random.sample(allCombs, m)
        if c not in problems:
            i += 1
            problems.append(list(c))
    return variables, problems

# %%
variables, problems = createProblem(m, k, n)

# %%
def assignment(variables, n):
    forPositive = list(np.random.choice(2,n))
    forNegative = [abs(1-i) for i in forPositive]
    assign = forPositive + forNegative
    var_assign = dict(zip(variables, assign))
    return var_assign

# %%
assign = assignment(variables, n)
print(assign)
print(problems[0])

# %%
def solve(problem, assign):
    count = 0
    for sub in problem:
        l = [assign[val] for val in sub]
        count += any(l)
    return count

# %%
def hillClimbing(problem, assign, parentNum, received, step):
    
    bestAssign = assign.copy()      
    assignValues = list(assign.values())
    assignKeys = list(assign.keys())
    
    maxNum = parentNum
    maxAssign = assign.copy()
    editAssign = assign.copy()
    
    for i in range(len(assignValues)):
        step += 1
        editAssign[assignKeys[i]] = abs(assignValues[i]-1)
        c = solve(problem, editAssign)
        if maxNum<c:
            received = step
            maxNum = c
            maxAssign = editAssign.copy()
            
    if maxNum==parentNum:
        s = str(received) + "/" + str(step-len(assignValues))
        return bestAssign, maxNum, s
    else:
        parentNum = maxNum
        bestassign = maxAssign.copy()
        return hillClimbing(problem, bestassign, parentNum, received, step)

# %%
def beamSearch(problem, assign,  b, stepSize):
    
    bestAssign = assign.copy()      
    assignValues = list(assign.values())
    assignKeys = list(assign.keys())
    steps = []
    possibleAssigns = []
    possibleScores = []
    
    editAssign = assign.copy()
    
    initail = solve(problem, assign)
    if initial == len(problem):
        p = str(stepSize) + "/" + str(stepSize)
        return assign, p
    
    for i in range(len(assignValues)):
        stepSize += 1
        editAssign[assignKeys[i]] = abs(assignValues[i]-1)
        c = solve(problem, editAssign)
        possibleAssigns.append(editAssign.copy())
        possibleScores.append(c)
        steps.append(stepSize)
    
    selected = list(np.argsort(possibleScores))[-b:]
    
    if len(problem) in possibleScores:
        index = [i for i in range(len(possibleScores)) if possibleScores[i]==len(problem)]
        p = str(steps[index[0]]) + "/" + str(steps[-1])
        return possibleAssigns[ index[0] ], p
    else:
        selectedAssigns = [possibleAssigns[i] for i in selected]
        for a in selectedAssigns:
            return beamSearch(problem, a, b, stepSize)

# %%
def variableNeighbor(problem, assign, b, step):
    bestAssign = assign.copy()      
    assignValues = list(assign.values())
    assignKeys = list(assign.keys())
    steps = []
    possibleAssigns = []
    possibleScores = []
    
    editAssign = assign.copy()
    
    initail = solve(problem, assign)
    if initial == len(problem):
        p = str(step) + "/" + str(step)
        return assign, p, b
    
    for i in range(len(assignValues)):
        step += 1
        editAssign[assignKeys[i]] = abs(assignValues[i]-1)
        c = solve(problem, editAssign)
        possibleAssigns.append(editAssign.copy())
        possibleScores.append(c)
        steps.append(step)
    
    selected = list(np.argsort(possibleScores))[-b:]
    
    if len(problem) in possibleScores:
        index = [i for i in range(len(possibleScores)) if possibleScores[i]==len(problem)]
        p = str(steps[index[0]]) + "/" + str(steps[-1])
        return possibleAssigns[index[0]], p, b
    
    else:
        selectedAssigns = [possibleAssigns[i] for i in selected]
        for a in selectedAssigns:
            return variableNeighbor(problem, a, b+1, step)

# %%
hAssigns = []
assigns = []
h_n = []
initials = []
hill_penetration = []
beam_penetration = []
var_penetration = []
v_n = []
b_var = []
b_n = []
bAssigns = []
vAssigns = []
i = 0

for problem in problems:
    i += 1
    l =[]
    assign = assignment(variables, n)
    initial = solve(problem, assign)
    bestAssign, score, hp = hillClimbing(problem, assign, initial, 1, 1)
    hAssigns.append(bestAssign)
    assigns.append(assign)
    h_n.append(score)
    initials.append(initial)
    hill_penetration.append(hp)
    
    h, b3p = beamSearch(problem, assign, 3, 1)
    bAssigns.append(h)
    beam_penetration.append(b3p)
    
    h4, b4p = beamSearch(problem, assign, 4, 1)
    
    v, p, bb = variableNeighbor(problem, assign, 1, 1)
    var_penetration.append(p)
    b_var.append(bb)
    vAssigns.append(v)
    
    print('Problem ',i,': ',problem)
    print('HillClimbing: ',bestAssign,', Penetrance:', hp)
    print('Beam search (3): ',h,', Penetrance:', b3p)
    print('Beam search (4): ', h4,', Penetrance:',b4p)
    print('Variable Neighbourhood: ',v,', Penetrance:',p)
    print()

# %%

