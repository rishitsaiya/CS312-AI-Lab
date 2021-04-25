import numpy as np


class GridWorld:
    """
    Gird environment with following stochastic property:

    | Agent Action | Possible Actions  |  Probability  |
    | :----------: | :---------------: | :-----------: |
    |      UP      |  UP, RIGHT, LEFT  | 0.8, 0.1, 0.1 |
    |     DOWN     | DOWN, RIGHT, LEFT | 0.8, 0.1, 0.1 |
    |     LEFT     |  LEFT, UP, DOWN   | 0.8, 0.1, 0.1 |
    |    RIGHT     |  RIGHT, UP, DOWN  | 0.8, 0.1, 0.1 |
    """

    POSSIBLE_ACTIONS = ['↑', '↓', '←', '→']

    def __init__(self, size, rewards, actions):

        self.height, self.width = size

        self.rewards = rewards
        self.actions = actions

        self.num_states = np.prod(size)
        self.num_actions = len(GridWorld.POSSIBLE_ACTIONS)

    def _limit_coordinates(self, state):
        i, j = state
        if i < 0:
            i = 0
        elif i > self.height - 1:
            i = self.height - 1
        if j < 0:
            j = 0
        elif j > self.width - 1:
            j = self.width - 1
        return (i, j)

    def _new_state_reward(self, action, state):
        i, j = state
        if action == '↑':
            i, j = i - 1, j
        elif action == '↓':
            i, j = i + 1, j
        elif action == '→':
            i, j = i, j + 1
        elif action == '←':
            i, j = i, j - 1

        # make sure the new state is not out of grid
        new_state = self._limit_coordinates((i, j))

        return new_state, self.rewards.get(new_state)

    def transition(self, action, state, choose=False):
        def stochastic_transition(possible_actions, prob):
            if not choose:
                # create and return a list of all possible actions
                result = []
                for i, a in enumerate(possible_actions):
                    coord, reward = self._new_state_reward(a, state)
                    result.append((prob[i], coord, reward))
                return result
            else:
                # choose a random action with given probabilities
                a = np.random.choice(possible_actions, 1, p=prob)
                coord, reward = self._new_state_reward(a, state)
                return coord, reward

        """ uncomment for purely stochastic  """
        # if action == '↑':
        #     return stochastic_transition(['↑', '→', '←'], [0.8, 0.1, 0.1])
        # elif action == '↓':
        #     return stochastic_transition(['↓', '→', '←'], [0.8, 0.1, 0.1])
        # elif action == '→':
        #     return stochastic_transition(['→', '↑', '↓'], [0.8, 0.1, 0.1])
        # elif action == '←':
        #     return stochastic_transition(['←', '↑', '↓'], [0.8, 0.1, 0.1])
            

        ''' uncomment for purely deterministic '''
        if action == '↑':
            return stochastic_transition(['↑'], [1])
        elif action == '↓':
            return stochastic_transition(['↓'], [1])
        elif action == '→':
            return stochastic_transition(['→'], [1])
        elif action == '←':
            return stochastic_transition(['←'], [1])


def grid():
    rewards = {
        (0, 0): -1, (0, 1): -1, (0, 2): -1, (0, 3): -1,
        (1, 0): -1, (1, 1): -1, (1, 2): -1, (1, 3): -1,  # start state is 1x0
        (2, 0): -1, (2, 1): -70, (2, 2): -1, (2, 3): -1,  # bad state is 2x1
        (3, 0): -1, (3, 1): -1, (3, 2): -1, (3, 3): 100  # goal state is 3x3
    }

    actions = {
        (0, 0): ['→', '↓'], (0, 1): ['→', '←', '↓'],
        (0, 2): ['→', '←', '↓'], (0, 3): ['←', '↓'],
        (1, 0): ['→', '↑', '↓'], (1, 1): ['→', '←', '↑', '↓'],
        (1, 2): ['→', '←', '↑', '↓'], (1, 3): ['←', '↑', '↓'],
        (2, 0): ['→', '↑', '↓'], (2, 1): ['→', '←', '↑', '↓'],
        (2, 2): ['→', '←', '↑', '↓'], (2, 3): ['←', '↑', '↓'],
        (3, 0): ['→', '↑'], (3, 1): ['→', '←', '↑'],
        (3, 2): ['→', '←', '↑'], (3, 3): []
    }

    return GridWorld(size=(4, 4), rewards=rewards, actions=actions)


def print_grid(env, content_dict):
    grid = np.arange(env.num_states, dtype=object).reshape(
        env.height, env.width)
    for coord, content in content_dict.items():
        if type(content) is float:
            content = round(content, 2)
        grid[coord[0], coord[1]] = content
    print(grid)

