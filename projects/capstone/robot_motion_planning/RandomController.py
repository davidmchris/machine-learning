from RobotController import RobotController
from RandomPlanner import RandomPlanner
from AStarPlanner import AStarPlanner
from GoalHeuristic import GoalHeuristic

class RandomController(RobotController):
    """
    This controller chooses random moves always. If it reaches the goal, it immediately resets since there is nothing
    to gain by exploring more of the maze.
    """
    def __init__(self, maze_dim):
        """
        :type maze_dim: int
        """
        super(RandomController, self).__init__(maze_dim)
        self.planner = RandomPlanner(self.maze_map)
        print "Using RandomController"


    def next_move(self, sensors):
        """
        :param sensors: The distances in number of cells from the left, front, and right walls
        :type sensors: (int, int, int)
        """
        self.update(sensors)
        if self.maze_map.at_goal(self.location):
            self.planner = AStarPlanner(self.maze_map, GoalHeuristic(self.maze_map.dim))
            return self.reset()
        else:
            rotation, movement = self.planner.next_move(self.location, self.heading)
            self.move(rotation, movement)
            return rotation, movement
