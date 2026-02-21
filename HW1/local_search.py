import copy
import numpy as np


def objective_f(state, S, T):
    B = S[[idx for idx in range(len(S)) if state[idx] == 1]]
    return abs(T - B.sum())


def get_neighbor(state):
    n_state = copy.deepcopy(state)
    on_indices = [idx for idx in range(len(state)) if state[idx] == 1]
    off_indices = [idx for idx in range(len(state)) if state[idx] == 0]

    if len(on_indices) > 0 and len(off_indices) > 0:
        u = np.random.uniform()
        if u < 0.5:
            idx = np.random.choice(on_indices)
            n_state[idx] = 0
        else:
            idx = np.random.choice(off_indices)
            n_state[idx] = 1
    elif sum(state) == len(state):
        idx = np.random.choice(on_indices)
        n_state[idx] = 0
    elif sum(state) == 0:
        idx = np.random.choice(off_indices)
        n_state[idx] = 1

    return n_state


def simulated_annealing(initial_state, S, T, initial_temp=1000):
    temp = initial_temp
    current = copy.deepcopy(initial_state)
    iters = 0

    while temp >= 0:
        temp = temp * 0.9999

        if temp < 1e-14:
            return current, iters

        if objective_f(current, S, T) == 0:
            return current, iters

        nxt = get_neighbor(current)
        deltaE = objective_f(current, S, T) - objective_f(nxt, S, T)

        if deltaE > 0:
            current = nxt
        else:
            u = np.random.uniform()
            if u <= np.exp(deltaE / temp):
                current = nxt

        iters += 1

    return current, iters
