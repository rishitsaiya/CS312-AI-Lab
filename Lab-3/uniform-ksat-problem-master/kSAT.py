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
            
    problems_new = []
    for c in problems:
        temp = []
        for sub in c:
            temp.append(list(sub))
        problems_new.append(temp)
    return problems

# %%
problems = createProblem(m, k, n)

# %%
for i in range(len(problems)):
    print(problems[i])

# %%

