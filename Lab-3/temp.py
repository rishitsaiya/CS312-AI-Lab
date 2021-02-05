import numpy as np
from string import ascii_lowercase, ascii_uppercase


f = open("clauses.txt", "r")

Expression = list()

for j in range(5):
    clause = (
        f.readline().strip("\n)").strip("(").replace(",", "").replace("'", "").split()
    )
    Expression.append(clause)

# print(Expression)
n = 4

variables = (list(ascii_lowercase))[:n] + (list(ascii_uppercase))[:n]


def assignment(variables, n):
    forLowercase = list(np.random.choice(2, n))
    forUppercase = [abs(1 - i) for i in forLowercase]
    assign = forLowercase + forUppercase
    var_assign = dict(zip(variables, assign))
    return var_assign


print(Expression)

intialState = assignment(variables, n)

def solve(Expression, assign):
    count = 0
    for sub in Expression:
        l = [assign[val] for val in sub]
        count += any(l)
    return count

initialValue = solve(Expression, intialState)

print(initialValue)

print("Initial state : ", intialState,"\nHeuristic Value : ",initialValue, sep="")







# %%

statesExplored = []

def beamSearch(Expression, intermediateState, beam, stepSize):

    statesExplored.append(intermediateState)
    # print(statesExplored)

    if initialValue == len(Expression):
        p = str(stepSize)
        return intermediateState, p

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    steps = []
    possibleintermediateStates = []
    possibleScores = []

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

    selected = list(np.argsort(possibleScores))[-beam:]
    # print(selected)

    if len(Expression) in possibleScores:
        index = [
            i
            for i in range(len(possibleScores))
            if possibleScores[i] == len(Expression)
        ]
        p = str(steps[-1])
        # p = str(steps[index[0]]) + "/" + str(steps[-1])
        return possibleintermediateStates[index[0]], p
    else:
        selectedintermediateStates = [possibleintermediateStates[i] for i in selected]
        for a in selectedintermediateStates:
            if(not a in statesExplored):
                return beamSearch(Expression, a, beam, stepSize)

# %%
ttarray = [6,7,5,8]
# ttarray = [2,3,1,4]
# ttarray = [0,0,0,0]
time = 0


def Tabu(Expression, intermediateState, tt,stepSize):

    print(ttarray)
    # print(time+1)
    global time
    time+=1
    
    if (not intermediateState in statesExplored):
        statesExplored.append(intermediateState)

    if initialValue == len(Expression):
        p = str(stepSize)
        return intermediateState, p

    intermediateStateValues = list(intermediateState.values())
    intermediateStateKeys = list(intermediateState.keys())

    steps = []
    possibleintermediateStates = []
    possibleScores = []

    for i in range(int(len(intermediateStateValues) / 2)):

        if(ttarray[i]>0):
            ttarray[i]-=1
            # possibleScores.append(-1)
            continue
        else:
            ttarray[i]=-1

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


    if(len(possibleintermediateStates)==0):
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
            if(ttarray[j]==-1):
                if(temp==0):
                    ttarray[j]=tt
                else:
                    ttarray[j]=0
                temp-=1
        return possibleintermediateStates[index[0]], p
    else:
        selectedintermediateStates = [possibleintermediateStates[i] for i in selected]
        # print("Hell O")
        for a in selectedintermediateStates:
            temp = selected[0]
            # print(temp)
            # print(ttarray)
            for j in range(len(ttarray)):
                if(ttarray[j]==-1):
                    if(temp==0):
                        ttarray[j]=tt
                    else:
                        ttarray[j]=0
                    temp-=1
            # ttarray[selected[0]] = tt
            # print(ttarray)
            if(not a in statesExplored):
                return Tabu(Expression, a, tt, stepSize)

# %%

# statesExplored.clear()
# finalState, b3p = beamSearch(Expression, intialState, 3, 1)
# if(not finalState in statesExplored):
#     statesExplored.append(finalState)
# print("States Explored : "+b3p)
# for e in statesExplored:
#     print(e)

# print(finalState)

# print("\n-------------------------\n")
# statesExplored.clear()
# finalState, b4p = beamSearch(Expression, intialState, 4, 1)
# if(not finalState in statesExplored):
#     statesExplored.append(finalState)
# print("States Explored : "+b4p)
# for e in statesExplored:
#     print(e)

print("\n-------------------------\n")
statesExplored.clear()
tt = 4 
finalState, tabu = Tabu(Expression, intialState, tt, 1)
if(not finalState in statesExplored):
    statesExplored.append(finalState)
print("States Explored : "+tabu)
for e in statesExplored:
    print(e)

print(ttarray)
print(time)
# print(finalState)
