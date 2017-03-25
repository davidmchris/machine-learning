import random
from Planner import Planner
from MazeMap import MazeMap
from Position import Position
from Direction import Direction


class RandomPlanner(Planner):
    def __init__(self, maze_map):
        """
        Initializer for this class
        :type maze_map: MazeMap
        :param maze_map: The maze map stores and updates information about the maze.
        """
        super(RandomPlanner, self).__init__(maze_map)

    def next_move(self, location, heading):
        """
        Chooses a random move every time.
        :type location: Position
        :type heading: Direction
        :param location:
        :param heading:
        :return:
        """
        possible_moves = self.get_possible_moves((location, heading))
        return random.choice(possible_moves)


