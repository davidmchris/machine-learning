from RobotController import RobotController
from VisitCountPlanner import VisitCountPlanner
from AStarPlanner import AStarPlanner
from GoalHeuristic import GoalHeuristic


class VisitCountController(RobotController):
    """
    This controller chooses random moves always. If it reaches the goal, it immediately resets since there is nothing
    to gain by exploring more of the maze.
    """
    def __init__(self, maze_dim):
        """
        :type maze_dim: int
        """
        super(VisitCountController, self).__init__(maze_dim)
        self.planner = VisitCountPlanner(self.maze_map)
        print "Using VisitCountController"

    def next_move(self, sensors):
        """
        :param sensors: The distances in number of cells from the left, front, and right walls
        :type sensors: (int, int, int)
        """
        self.update(sensors)
        if self.planner.percent_coverage() > .99 and self.found_goal:
            self.planner = AStarPlanner(self.maze_map, GoalHeuristic(self.maze_map.dim))
            return self.reset()
        else:
            rotation, movement = self.planner.next_move(self.location, self.heading)
            self.move(rotation, movement)
            return rotation, movement
