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
        
        goal_condition = (row == goal_row) and (col == goal_col)
        
        return goal_condition
        
    def action_cost(self, state1, action, state2):
        return 1
        
    """
        Compute euclidean distance from node.state to goal.
    """
    def h(self, node):
        if self.is_goal(node.state):
            return 0
            
        arow, acol = node.state
        grow, gcol = self.goal_state
        edist = abs(arow - grow) + abs(acol - gcol)

        return edist