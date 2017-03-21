from MazeMap import MazeMap
import random
from Planner import Planner


class RandomPlanner(Planner):
    def __init__(self, maze_map):
        """
        Initializer for this class
        :param maze_map: The maze map stores and updates information about the maze.
        """
        self.maze_map = maze_map

    def next_move(self, location, heading):
        if self.maze_map.at_goal(location):
            self.reached_goal = True
            self.run = 2
            return "Reset", "Reset"
        possible_moves = self.get_possible_moves((location, heading))
        return random.choice(possible_moves)


