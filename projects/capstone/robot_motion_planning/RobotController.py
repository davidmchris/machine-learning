from Position import Position
from Direction import Direction
from MazeMap import MazeMap
from Visualizer import Visualizer
from maze import Maze
from Planner import Planner
import os


class RobotController(object):
    """
    This is the base class for all robot controllers. You must override next_move and initialize self.planner in
    a sub-class.
    """
    def __init__(self, maze_dim, dump_mazes=False):
        self.location = Position(0, 0)
        self.heading = Direction(0)
        self.maze_map = MazeMap(maze_dim)
        self.timestep = 0
        self.run_number = 0
        self.found_goal = False
        self.dump_mazes = dump_mazes
        self.planner = Planner(self.maze_map)  # planner needs to be set by sub-class

    def next_move(self, sensors):
        """
        This is the main method to implement for a controller. Make sure that the move the controller returns is a valid
        move (it doesn't try to go through walls). If it does, the location and heading class members will be incorrect.
        :param sensors: The distance in squares to the next wall for the left, middle and right sensors.
        :return: The sub-class should return the next move as a (int, int). The first is the rotation
        (could be -90, 0 or 90), the second is the number of squares to move (from -3 to 3).
        """
        raise NotImplemented("Implement by overriding in sub-class.")

    def update(self, sensors):
        """
        Convenience function for updating the maze, re-planning (if the maze was updated), and dumping the maze for
        debugging.
        :param sensors:
        :return: True if maze was updated
        """
        self.timestep += 1
        maze_updated = self.maze_map.update(self.location, self.heading, sensors)
        if maze_updated:
            self.planner.replan(self.location, self.heading)
        if self.dump_mazes:
            self.maze_map.dump_to_file(os.path.join(os.curdir, "known_maze.txt"))
        return maze_updated

    def move(self, rotation, movement):
        """
        Update the current location and heading for the class. This should be called in the sub-class after choosing
        a move.
        :type rotation: int
        :type movement: int
        :param rotation: The rotation to perform
        :param movement: The number of squares to move
        :return: None
        """
        self.heading = self.heading.rotate(rotation)
        direction_of_movement = self.heading if movement > 0 else self.heading.flip()
        for i in range(abs(movement)):
            self.location = self.location.add(direction_of_movement)
        if self.maze_map.at_goal(self.location):
            self.found_goal = True

    def reset(self):
        """
        Move the robot back to 0,0 and facing north. Also changes the run_number to 1. Call this when you are ready to
        start the second run.
        :return: Returns the reset string for convenience.
        """
        self.location = Position(0, 0)
        self.heading = Direction(0)
        self.run_number = 1
        print "Number of moves in first run: {}".format(self.timestep)
        print "Exploration efficiency: {}".format(self.get_exploration_efficiency())
        self.planner.replan(self.location, self.heading)
        return "Reset", "Reset"

    def show_current_policy_and_map(self):
        """
        For visualization of the maze and policy when using the A* planner.
        :return: None
        """
        vis = Visualizer(self.maze_map.dim)
        vis.draw_maze(Maze('known_maze.txt'))
        vis.draw_policy(reversed(self.planner.policy), self.location, self.heading)
        vis.show_window()

    def get_exploration_efficiency(self):
        return self.maze_map.get_num_known_walls() / float(self.timestep)
