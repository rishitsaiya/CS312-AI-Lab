import numpy as np
import random

POSSIBLE_ACTIONS = ['↑', '↓', '←', '→']

gamma = 0.9

def value_iteration(env, start, stop, discount_factor=gamma, threshold=0.001):

    def calculate_v(V, state, actions):
        """ V[s] = max[a]{ sum[s',r] { p(s',r|s,a)[r + gamma*V[s']] } }
        """
        new_V = {'↑': 0, '↓': 0, '←': 0, '→': 0}

        for action in actions:
            # get all possible transitions list
            possible_transitions = env.transition(action, state)
            for prob, next_state, reward in possible_transitions:
                new_V[action] += prob * \
                    (reward + discount_factor * V[next_state])

        # key with max value
        best_a = max(new_V, key=new_V.get)
        # max value in the dict
        best_V = new_V[best_a]

        return best_V, best_a

    all_states = set(env.rewards.keys())
    # Initialize V to 0
    V = {}
    for state in all_states:
        V[state] = 0

    episode = 0
    stats = []

    # run until convergence
    while True:

        stats.append({})
        delta = 0

        for state in all_states:
            best_V, _ = calculate_v(V, state, env.actions[state])
            delta = max(delta, np.abs(best_V - V[state]))
            V[state] = best_V

        # collect stats for visuaization
        policy_list, v_list = [], []
        # iterate on sorted states as policy and v are a list with
        # index representing the states
        for state in sorted(all_states):
            best_v, best_a = calculate_v(V, state, env.actions[state])
            policy_list.append(best_a)
            v_list.append(best_v)

        # stats for this iteration
        stats[episode] = {'policy': policy_list, 'score': v_list}

        episode += 1

        # check if converged
        if delta < threshold:
            break

    
    print("episodes ", episode)
    # get optimal policy
    policy = {}
    for state in all_states:
        _, best_a = calculate_v(V, state, env.actions[state])
        policy[state] = best_a


    steps = []
    state = start
    while state != stop:
        # get 1D index from state tuple
        state_idx = state[0] * env.height + state[1]
        action = stats[episode - 1]['policy'][state_idx]
        # make a transition with choose=True
        new_state, reward = env.transition(action, state, choose=True)
        steps.append([action, list(state), reward])
        state = new_state
    # append the goal state for visualization
    steps.append(['G', list(stop), 0])

    return policy, V, stats, episode, steps

def _epsilon_greedy(action, epsilon):
    p = random.random()
    if p < (1 - epsilon):
        return action
    else:
        return np.random.choice(POSSIBLE_ACTIONS, 1)[0]

def policy_iteration(env, num_episodes, epsilon, alpha, start, stop, discount_factor=gamma):
    all_states = set(env.rewards.keys())

    # initialize Q[s][a]
    Q = {}
    for state in all_states:
        Q[state] = {}
        for action in POSSIBLE_ACTIONS:
            Q[state][action] = 0

    stats = []
    # repeat for number of episodes
    for episode in range(num_episodes):
        state = start
        stats.append({})
        # until end state is reached
        while state != stop:
            # take best action for current state and use epsilon greedy
            action = max(Q[state], key=Q[state].get)
            action = _epsilon_greedy(action, epsilon)

            # using above action, find next state and best action for that
            # state
            new_state, reward = env.transition(action, state, choose=True)
            best_next_action = max(Q[new_state], key=Q[new_state].get)

            # calculate td target and update Q[s][a]
            td_target = reward + discount_factor * \
                Q[new_state][best_next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])

            state = new_state

        # collect stats
        policy_list, q_list = [], []
        # iterate on sorted states as policy and v are a list with
        # index representing the states
        for state in sorted(all_states):
            best_a = max(Q[state], key=Q[state].get)
            best_q = Q[state][best_a]
            if state != stop:
                policy_list.append(best_a)
            else:
                policy_list.append('G')
            q_list.append(best_q)
        # print(q_list)

        # add steps according to current policy to visualize agent's actions
        stats[episode] = {
            'policy': policy_list,
            'score': q_list}

    # optimal policy and V
    policy, V, = {}, {}
    for state in all_states:
        best_a = max(Q[state], key=Q[state].get)
        best_q = Q[state][best_a]
        policy[state] = best_a if state != stop else 'G'
        V[state] = best_q

    steps = []
    state = start
    while state != stop:
        # get 1D index from state tuple
        state_idx = state[0] * env.height + state[1]
        action = stats[episode - 1]['policy'][state_idx]
        # make a transition with choose=True
        new_state, reward = env.transition(action, state, choose=True)
        steps.append([action, list(state), reward])
        state = new_state
    # append the goal state for visualization
    steps.append(['G', list(stop), 0])

    return policy, V, stats, steps