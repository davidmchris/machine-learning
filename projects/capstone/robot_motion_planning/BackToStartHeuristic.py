from MazeHeuristic import MazeHeuristic


class BackToStartHeuristic(MazeHeuristic):
    def __init__(self, maze_dim):
        super(BackToStartHeuristic, self).__init__(maze_dim)

    def get_value(self, state):
        location = state[0]
        x_timesteps_to_goal = (location.x + 2) / 3
        y_timesteps_to_goal = (location.y + 2) / 3
        return x_timesteps_to_goal + y_timesteps_to_goal
