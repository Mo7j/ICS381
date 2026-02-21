class GridHunterProblem:
    def __init__(self, initial_agent_info, N, monster_coords):
        self.initial_agent_info = initial_agent_info
        self.N = N
        self.monster_coords = list(monster_coords)
        self.num_monsters = len(self.monster_coords)
        self.initial_state = tuple(initial_agent_info) + (0,) + tuple(False for _ in range(self.num_monsters))

    def __str__(self):
        return f"GridHunterProblem(N={self.N}, M={self.num_monsters})"

    def move_monsters(self, timestep):
        new_coords = []
        phase = timestep % 4
        for row, col in self.monster_coords:
            if phase == 1:
                new_col = max(0, col - 1)
                new_coords.append((row, new_col))
            elif phase == 3:
                new_col = min(self.N - 1, col + 1)
                new_coords.append((row, new_col))
            else:
                new_coords.append((row, col))
        return new_coords

    def actions(self, state):
        row, col, orient, health, _, *dead_status = state
        if health <= 0:
            return []

        legal = ["move-forward", "turn-left", "turn-right", "shoot-arrow", "stay"]

        next_row, next_col = row, col
        if orient == "north":
            next_row -= 1
        elif orient == "south":
            next_row += 1
        elif orient == "east":
            next_col += 1
        elif orient == "west":
            next_col -= 1

        if not (0 <= next_row < self.N and 0 <= next_col < self.N):
            legal.remove("move-forward")

        return legal

    def _turn_left(self, orient):
        return {
            "north": "west",
            "west": "south",
            "south": "east",
            "east": "north",
        }[orient]

    def _turn_right(self, orient):
        return {
            "north": "east",
            "east": "south",
            "south": "west",
            "west": "north",
        }[orient]

    def _is_in_arrow_path(self, agent_row, agent_col, orient, monster_row, monster_col):
        if orient == "north":
            return monster_col == agent_col and monster_row < agent_row
        if orient == "south":
            return monster_col == agent_col and monster_row > agent_row
        if orient == "east":
            return monster_row == agent_row and monster_col > agent_col
        if orient == "west":
            return monster_row == agent_row and monster_col < agent_col
        return False

    def result(self, state, action):
        row, col, orient, health, mstep, *dead_status = state
        dead_status = list(dead_status)

        mstep = (mstep + 1) % 4
        monster_locs = self.move_monsters(mstep)

        if action == "shoot-arrow":
            for i, (mrow, mcol) in enumerate(monster_locs):
                if self._is_in_arrow_path(row, col, orient, mrow, mcol):
                    dead_status[i] = True

        if action == "move-forward":
            if orient == "north":
                row -= 1
            elif orient == "south":
                row += 1
            elif orient == "east":
                col += 1
            elif orient == "west":
                col -= 1

        if action == "turn-left":
            orient = self._turn_left(orient)
        elif action == "turn-right":
            orient = self._turn_right(orient)

        touching_alive_monster = False
        for i, (mrow, mcol) in enumerate(monster_locs):
            if not dead_status[i] and mrow == row and mcol == col:
                touching_alive_monster = True
                break
        if touching_alive_monster:
            health -= 1

        return (row, col, orient, health, mstep, *dead_status)

    def action_cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        health = state[3]
        dead_status = state[5:]
        return health > 0 and all(dead_status)

    def h(self, node):
        state = node.state
        if self.is_goal(state):
            return 0

        row, _, _, _, mstep, *dead_status = state
        monster_locs = self.move_monsters(mstep)

        distances = []
        for i, (mrow, _) in enumerate(monster_locs):
            if not dead_status[i]:
                distances.append(abs(row - mrow))

        if len(distances) == 0:
            return 0
        return min(distances)
