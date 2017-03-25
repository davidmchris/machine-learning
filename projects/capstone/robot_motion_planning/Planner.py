from MazeMap import MazeMap
from Position import Position
from Direction import Direction


class Planner(object):
    """
    This is the base class for all planners. It provides some common methods for convenience and defines next_move
    which must be overridden in a sub-class.
    """
    def __init__(self, maze_map):
        """
        :param maze_map: The known map of the maze
        :type maze_map: MazeMap
        """
        self.maze_map = maze_map
        self.reached_goal = False
        self.run = 1
        self.visits = [[0 for j in range(maze_map.dim)] for i in range(maze_map.dim)]


    def next_move(self, location, heading):
        """
        This must be overridden in sub-classes
        :type location: Position
        :type heading: Direction
        :param location: current location of the robot
        :param heading: current heading of the robot
        :return:
        """
        self.visits[location.x][location.y] += 1

    def percent_coverage(self):
        been_there_done_that = 0
        for i in range(len(self.visits)):
            for j in range(len(self.visits[i])):
                if self.visits[i][j] > 0:
                    been_there_done_that += 1
        pct = float(been_there_done_that) / float(self.maze_map.dim * self.maze_map.dim)
        return pct

    def replan(self, location, heading):
        """
        :type location: Position
        :type heading: Direction
        :param location: The current location of the robot
        :param heading: The current heading of the robot
        :return:
        """
        pass

    def get_possible_moves(self, state):
        """
        :type state: (Position, Direction)
        :param state: The current location and heading of the robot
        :return:
        """
        location = state[0]
        heading = state[1]
        possible_moves = []
        for rot in [90, 0, -90]:
            for mov in range(-3, 4):
                if self.maze_map.check_valid_move(location, heading, rot, mov):
                    possible_moves.append((rot, mov))
        return possible_moves

    def get_move_result(self, state, move):
        """
        :type state: (Position, Direction)
        :type move: (int, int)
        :param state: The current location and heading of the robot
        :param move: The desired turn and advance information
        :return: Returns the new state after performing the given move from the given state
        """
        location = state[0]
        heading = state[1]
        new_heading = heading.rotate(move[0])
        new_location = location
        direction_of_movement = new_heading if move[1] > 0 else new_heading.flip()
        for i in range(abs(move[1])):
            new_location = new_location.add(direction_of_movement)
        return new_location, new_heading
