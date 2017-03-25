from RobotController import RobotController
from AStarPlanner import AStarPlanner
from GoalHeuristic import GoalHeuristic
from BackToStartHeuristic import BackToStartHeuristic
from Position import Position

class AStarReturnController(RobotController):
    """
    This controller chooses random moves always. If it reaches the goal, it immediately resets since there is nothing
    to gain by exploring more of the maze.
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

    def next_move(self, sensors):
        """
        :param sensors: The distances in number of cells from the left, front, and right walls
        :type sensors: (int, int, int)
        """
        self.update(sensors)
        if self.maze_map.at_goal(self.location) and self.planner.heuristic != self.back_heuristic:
            self.planner.heuristic = self.back_heuristic
            self.planner.replan(self.location, self.heading)
            self.found_goal = True

        if self.found_goal and self.location == Position(0,0) and self.run_number != 1:
            self.planner.heuristic = self.goal_heuristic
            return self.reset()
        else:
            rotation, movement = self.planner.next_move(self.location, self.heading)
            self.move(rotation, movement)
            return rotation, movement
