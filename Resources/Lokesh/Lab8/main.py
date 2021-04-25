import environment as env
import policies as policy

MyGrid = env.grid()

#   Value Iteration
print("Value Iteration")

poli, V, stats, iterations, steps = policy.value_iteration(MyGrid, (1, 0), (3, 3))

env.print_grid(MyGrid, poli)
env.print_grid(MyGrid, V)
print()
for each in steps:
    print(each)

print("-----------------------------------------------------")
print()

#   Policy Iteration
print("Policy Iteration")

episodes = 30
epsilon = 0.05
alpha = 0.5
poli, V, stats, steps = policy.policy_iteration(MyGrid, episodes, epsilon, alpha, (1, 0), (3, 3))

print("episodes", episodes)
env.print_grid(MyGrid, poli)
env.print_grid(MyGrid, V)
print()
for each in steps:
    print(each)

print("-----------------------------------------------------")
print()
