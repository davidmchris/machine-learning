from MazeHeuristic import MazeHeuristic


class GoalHeuristic(MazeHeuristic):
    def __init__(self, maze_dim):
        super(GoalHeuristic, self).__init__(maze_dim)

    def get_value(self, state):
        location = state[0]
        x_dist_to_goal = min(abs(self.maze_dim / 2 - location.x), abs(location.x - self.maze_dim / 2 + 1))
        y_dist_to_goal = min(abs(self.maze_dim / 2 - location.y), abs(location.y - self.maze_dim / 2 + 1))
        x_timesteps_to_goal = 0 if x_dist_to_goal == 0 else (x_dist_to_goal - 1) / 3 + 1
        y_timesteps_to_goal = 0 if y_dist_to_goal == 0 else (y_dist_to_goal - 1) / 3 + 1
        return x_timesteps_to_goal + y_timesteps_to_goal

