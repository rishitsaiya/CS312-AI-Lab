# %%
import random
from string import ascii_lowercase, ascii_uppercase
from itertools import combinations


# %%
def createProblem(m, k, n):

    variables = (list(ascii_lowercase))[:n] + (list(ascii_uppercase))[:n]
    variables.sort()

    allCombs = list(combinations(variables, k))
    allCombs.sort()

    for comb in allCombs:
        for lits in comb:
            if (lits.upper() in comb) and (lits.lower() in comb):
                allCombs.remove(comb)
                break

    problems = []
    threshold = 1
    i = 0

    while i < threshold:

        c = random.sample(allCombs, m)
        c.sort()

        if c not in problems:
            i += 1
            problems.append(list(c))

    problems.sort()
    return problems


# %%
problems = createProblem(5, 3, 4)

f = open("clauses.txt", "w")

for expression in problems:
    for clause in expression:
        f.write(str(clause) + "\n")

f.close()