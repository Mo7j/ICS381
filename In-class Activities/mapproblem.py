class MapProblem:
    def __init__(self, initial_agent_loc, goal_list, map_graph):
        self.initial_state = initial_agent_loc
        self.goal_list = goal_list
        self.map_graph = map_graph

        # setup neighbors dictionary to simplify implementation later
        # see example map_graph below
        self.neighbors = {}
        for v1, v2 in self.map_graph:
            self.neighbors[v1] = []
            self.neighbors[v2] = []
        for v1, v2 in self.map_graph:
            self.neighbors[v1].append(v2)
            self.neighbors[v2].append(v1)
    
    """
        return list locations (names) that can be reached from state.
        use self.neighbors.
    """
    def actions(self, state):
        return self.neighbors[state]

    """
        in our implementation, action is a named location 
        so for result(), action will be the named location we want to go to
        return the next state as action if it is neighbor of state
    """
    def result(self, state, action):
        return action

    """
        action cost is determined by map_graph values
        return self.map_graph[state1, state2] or self.map_graph[state2, state1] whichever is applicable
    """
    def action_cost(self, state1, action, state2):
        if (state1, state2) in self.map_graph:
            return self.map_graph[(state1, state2)]
        elif (state2, state1) in self.map_graph:
            return self.map_graph[(state2, state1)]
        else:
            return 0

    """
        goal is if state is in the list of goals
    """
    def is_goal(self, state):
        return state in self.goal_list