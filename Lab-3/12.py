import numpy as np
from string import ascii_lowercase, ascii_uppercase

# reading clauses from clauses.txt

f = open("clauses.txt", "r")

Expression = list()

# clearing each of the clause input
for j in range(5):
    clause = (
        f.readline().strip("\n)").strip("(").replace(",", "").replace("'", "").split()
    )
    Expression.append(clause)

n = 4

variables = (list(ascii_lowercase))[:n] + (list(ascii_uppercase))[:n]

# randomly creating intial state
def assignment(variables, n):
    forLowercase = list(np.random.choice(2, n))
    forUppercase = [abs(1 - i) for i in forLowercase]
    assign = forLowercase + forUppercase
    var_assign = dict(zip(variables, assign))
    return var_assign


print(Expression)

# creating random initial state
intialState = assignment(variables, n)

# calculate hueristic value expression (for each true clause HV increases by +1)
def solve(Expression, assign):
    count = 0
    for sub in Expression:
        l = [assign[val] for val in sub]
        count += any(l)
    return count

# setting initial values
initialValue = solve(Expression, intialState)

print("Initial state : ", intialState, "\nHeuristic Value : ", initialValue, sep="")


# %%
# defining Beam search :

# storing all intermediate states
statesExplored = []

def beamSearch(Expression, intermediateState, beam, stepSize):

    statesExplored.append(intermediateState)

    if initialValue == len(Expression):
        p = str(stepSize)
        return intermediateState, p

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    steps = []
    possibleintermediateStates = []
    possibleScores = []

    #  considering all possible intermediate states form any particular state
    for i in range(int(len(intermediateStateValues) / 2)):

        editintermediateState = intermediateState.copy()
        editintermediateState[intermediateStateKeys[i]] = abs(
            intermediateStateValues[i] - 1
        )
        editintermediateState[intermediateStateKeys[i + 4]] = abs(
            intermediateStateValues[i + 4] - 1
        )
        possibleintermediateStates.append(editintermediateState)

        c = solve(Expression, editintermediateState)
        possibleScores.append(c)

        stepSize += 1
        steps.append(stepSize)

    # for i in range(len(possibleintermediateStates)):
    #     print(possibleScores[i])
    #     print(possibleintermediateStates[i])

    # sorting the intermediate states
    selected = list(np.argsort(possibleScores))[-beam:]
    # print(selected)

    # if we get goal state ==> exit
    if len(Expression) in possibleScores:
        index = [
            i
            for i in range(len(possibleScores))
            if possibleScores[i] == len(Expression)
        ]
        p = str(steps[-1])
        # p = str(steps[index[0]]) + "/" + str(steps[-1])
        return possibleintermediateStates[index[0]], p
    # else consider next best-state among best beam-length elements
    else:
        selectedintermediateStates = [possibleintermediateStates[i] for i in selected]
        for a in selectedintermediateStates:
            if not a in statesExplored:
                return beamSearch(Expression, a, beam, stepSize)


# %%
# tabu tenure array 
# ttarray = [6,7,5,8]
# ttarray = [2,3,1,4]
ttarray = [0, 0, 0, 0]
time = 0

# tabu search algo
def Tabu(Expression, intermediateState, tt, stepSize):

    # print(ttarray)
    # print(time+1)
    global time
    time += 1
    
    # time limit can be added HERE

    if not intermediateState in statesExplored:
        statesExplored.append(intermediateState)

    if initialValue == len(Expression):
        p = str(stepSize)
        return intermediateState, p

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    steps = []
    possibleintermediateStates = []
    possibleScores = []

    # adding intermediate states depending on tabu tenure values
    for i in range(int(len(intermediateStateValues) / 2)):

        if ttarray[i] > 0:
            ttarray[i] -= 1
            # possibleScores.append(-1)
            continue
        else:
            ttarray[i] = -1

        editintermediateState = intermediateState.copy()
        editintermediateState[intermediateStateKeys[i]] = abs(
            intermediateStateValues[i] - 1
        )
        editintermediateState[intermediateStateKeys[i + 4]] = abs(
            intermediateStateValues[i + 4] - 1
        )
        possibleintermediateStates.append(editintermediateState)

        c = solve(Expression, editintermediateState)
        possibleScores.append(c)

        stepSize += 1
        steps.append(stepSize)

    if len(possibleintermediateStates) == 0:
        return Tabu(Expression, intermediateState, tt, stepSize)

    # for i in range(len(possibleintermediateStates)):
    #     print(possibleScores[i])
    #     print(possibleintermediateStates[i])

    selected = list(np.argsort(possibleScores))[-1:]
    # print("Selected : ",selected[0],sep='')

    if len(Expression) in possibleScores:
        index = [
            i
            for i in range(len(possibleScores))
            if possibleScores[i] == len(Expression)
        ]
        p = str(steps[-1])
        # print("index : ",index,sep='')
        temp = selected[0]
        for j in range(len(ttarray)):
            if ttarray[j] == -1:
                if temp == 0:
                    ttarray[j] = tt
                else:
                    ttarray[j] = 0
                temp -= 1
        return possibleintermediateStates[index[0]], p
    else:
        selectedintermediateStates = [possibleintermediateStates[i] for i in selected]
        for a in selectedintermediateStates:
            temp = selected[0]
            for j in range(len(ttarray)):
                if ttarray[j] == -1:
                    if temp == 0:
                        ttarray[j] = tt
                    else:
                        ttarray[j] = 0
                    temp -= 1
            if not a in statesExplored:
                return Tabu(Expression, a, tt, stepSize)


# %%

# hill climbing for variableNeighbor
def hillClimbing(Expression, intermediateState, parentNum, received, step):

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    maxNum = parentNum
    maxAssign = intermediateState.copy()

    for i in range(int(len(intermediateStateValues) / 2)):

        editintermediateState = intermediateState.copy()
        bestAssign = intermediateState.copy()

        editintermediateState[intermediateStateKeys[i]] = abs(
            intermediateStateValues[i] - 1
        )
        editintermediateState[intermediateStateKeys[i + 4]] = abs(
            intermediateStateValues[i + 4] - 1
        )

        step += 1
        c = solve(Expression, editintermediateState)
        if maxNum < c:
            received = step
            maxNum = c
            maxAssign = editintermediateState.copy()

    if maxNum == parentNum:
        s = str(received)
        return bestAssign, maxNum, s
    else:
        parentNum = maxNum
        bestassign = maxAssign.copy()
        return hillClimbing(Expression, bestassign, parentNum, received, step)


# %%

# defining variableNeighbor:

def variableNeighbor(Expression, intermediateState, b, step):

    statesExplored.append(intermediateState)

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    steps = []
    possibleintermediateStates = []
    possibleScores = []

    initialValue = solve(Expression, intermediateState)

    if initialValue == len(Expression):
        p = str(step)
        return intermediateState, p, b

    for i in range(int(len(intermediateStateValues) / 2)):

        editintermediateState = intermediateState.copy()
        editintermediateState[intermediateStateKeys[i]] = abs(
            intermediateStateValues[i] - 1
        )
        editintermediateState[intermediateStateKeys[i + 4]] = abs(
            intermediateStateValues[i + 4] - 1
        )

        c = solve(Expression, editintermediateState)
        step += 1
        possibleintermediateStates.append(editintermediateState.copy())
        possibleScores.append(c)
        steps.append(step)

    # for i in range(len(possibleintermediateStates)):
    #     print(possibleScores[i])
    #     print(possibleintermediateStates[i])

    selected = list(np.argsort(possibleScores))[-b:]
    # print(selected)

    if len(Expression) in possibleScores:
        index = [
            i
            for i in range(len(possibleScores))
            if possibleScores[i] == len(Expression)
        ]
        p = str(steps[-1])
        return possibleintermediateStates[index[0]], p, b

    else:
        selectedAssigns = [possibleintermediateStates[i] for i in selected]
        for a in selectedAssigns:
            bestAssign, maxNum, s = hillClimbing(Expression, a, initialValue, 1, 1)
            step += int(s)
            if maxNum == len(Expression):
                statesExplored.append(a)
                return variableNeighbor(Expression, bestAssign, b, step)

        variableNeighbor(Expression, intermediateState, b + 1, step)


# %%

# print("\n------------Beam Search (beam length-1)-------------\n")
# statesExplored.clear()
# finalState, b1p = beamSearch(Expression, intialState, 1, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + b1p)
# for e in statesExplored:
#     print(e)

print("\n------------Beam Search (beam length-2)-------------\n")
statesExplored.clear()
finalState, b2p = beamSearch(Expression, intialState, 2, 1)
if not finalState in statesExplored:
    statesExplored.append(finalState)
print("States Explored : " + b2p)
for e in statesExplored:
    print(e)

# print("\n------------Beam Search (beam length-3)-------------\n")
# statesExplored.clear()
# finalState, b3p = beamSearch(Expression, intialState, 3, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + b3p)
# for e in statesExplored:
#     print(e)


# print("\n------------Beam Search (beam length-4)-------------\n")
# statesExplored.clear()
# finalState, b4p = beamSearch(Expression, intialState, 4, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + b4p)
# for e in statesExplored:
#     print(e)

# print("\n-------------Tabu search (tabu tenure-1)------------\n")
# statesExplored.clear()
# tt = 1
# finalState, tabu = Tabu(Expression, intialState, tt, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + tabu)
# for e in statesExplored:
#     print(e)

print("\n-------------Tabu search (tabu tenure-2)------------\n")
statesExplored.clear()
tt = 2
finalState, tabu = Tabu(Expression, intialState, tt, 1)
if not finalState in statesExplored:
    statesExplored.append(finalState)
print("States Explored : " + tabu)
for e in statesExplored:
    print(e)

# print("\n-------------Tabu search (tabu tenure-3)------------\n")
# statesExplored.clear()
# tt = 3
# finalState, tabu = Tabu(Expression, intialState, tt, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + tabu)
# for e in statesExplored:
#     print(e)

# print("\n-------------Tabu search (tabu tenure-4)------------\n")
# statesExplored.clear()
# tt = 4
# finalState, tabu = Tabu(Expression, intialState, tt, 1)
# if not finalState in statesExplored:
#     statesExplored.append(finalState)
# print("States Explored : " + tabu)
# for e in statesExplored:
#     print(e)

# print(ttarray)
# print(time)
# print(finalState)

print("\n-----------Variable neighborhood descent--------------\n")
statesExplored.clear()
finalState, p, bb = variableNeighbor(Expression, intialState, 1, 1)
if not finalState in statesExplored:
    statesExplored.append(finalState)
print("States explored : ", p, sep="")

for e in statesExplored:
    print(e)
