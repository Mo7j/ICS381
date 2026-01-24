class NxNGridProblem:
    def __init__(self, initial_state, goal_state, N):
        self.initial_state = initial_state
        self.goal_state = goal_state   
        self.N = N
        
    def actions(self, state):
        row, col = state
        
        available_actions = ['up', 'down', 'left', 'right']
        
        if row == (self.N - 1):
            available_actions.remove('down')
        elif row == 0:
            available_actions.remove('up')
        
        if col == (self.N - 1):
            available_actions.remove('right')
        elif col == 0:
            available_actions.remove('left')
            
        return available_actions
        
    def result(self, state, action):
        row, col = state
        
        # just safe-gaurd against illegal moves.
        # agent stays in place.
        if action == 'down' and row == (self.N - 1):
            new_state = (row, col)
            return new_state
        elif action == 'up' and row == 0:
            new_state = (row, col)
            return new_state
        elif action == 'right' and col == (self.N - 1):
            new_state = (row, col)
            return new_state
        elif action == 'left' and col == 0:
            new_state = (row, col)
            return new_state
        
        # TODO: finish remainder implementation for movement
        if action == 'up':
            new_state = (row-1, col)
        elif action == 'down':
            new_state = (row+1, col)
        elif action == 'left':
            new_state = (row, col-1)
        elif action == 'right':
            new_state = (row, col+1)
            
        return new_state    
        
    def is_goal(self, state):
        row, col = state
        goal_row, goal_col = self.goal_state
        
        # TODO: finish remainder implementation for goal boolean condition
        goal_condition = (row == goal_row) and (col == goal_col)
        
        return goal_condition
        
    def action_cost(self, state1, action, state2):
        return 1