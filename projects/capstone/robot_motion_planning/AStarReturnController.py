from RobotController import RobotController
from AStarPlanner import AStarPlanner
from GoalHeuristic import GoalHeuristic
from BackToStartHeuristic import BackToStartHeuristic
from Position import Position


class AStarReturnController(RobotController):
    """
    This controller goes back and forth between the start and goal until it reaches the goal without having to replan.
    """

    def __init__(self, maze_dim):
        """
        :type maze_dim: int
        """
        super(AStarReturnController, self).__init__(maze_dim)
        self.goal_heuristic = GoalHeuristic(maze_dim)
        self.back_heuristic = BackToStartHeuristic(maze_dim)
        self.planner = AStarPlanner(self.maze_map, self.goal_heuristic)
        self.planner.replan(self.location, self.heading)
        self.replanned = False
        print "Using AStarReturnController"

    def next_move(self, sensors):
        """
        :param sensors: The distances in number of cells from the left, front, and right walls
        :type sensors: (int, int, int)
        """
        maze_updated = self.update(sensors)
        if self.planner.heuristic == self.goal_heuristic:
            if self.maze_map.at_goal(self.location):
                if not self.replanned:
                    return self.reset()
                else:
                    self.planner.heuristic = self.back_heuristic
                    self.planner.replan(self.location, self.heading)
                    self.found_goal = True
            elif maze_updated:
                self.replanned = True
                self.planner.replan(self.location, self.heading)
        else:
            if self.location == Position(0, 0) and self.run_number != 1:
                self.planner.heuristic = self.goal_heuristic
                self.planner.replan(self.location, self.heading)
                self.replanned = False

        rotation, movement = self.planner.next_move(self.location, self.heading)
        self.move(rotation, movement)
        return rotation, movement
