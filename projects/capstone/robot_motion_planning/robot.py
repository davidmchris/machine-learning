from maze import Maze
from Visualizer import Visualizer
from RandomPlanner import RandomPlanner
from AStarPlanner import  AStarPlanner
from MazeMap import MazeMap
from Direction import Direction
from Position import Position
import os

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = Position(0, 0)
        self.heading = Direction(0)
        self.maze_map = MazeMap(maze_dim)
        self.planner = AStarPlanner(self.maze_map)
        #self.planner = RandomPlanner(self.maze_map)
        self.planner.replan(self.location, self.heading)
        self.planner.display_heuristic()
        self.count = 0

    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returning the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        maze_updated = self.maze_map.update(self.location, self.heading, sensors)  # update state
        self.maze_map.dump_to_file(os.path.join(os.curdir, "known_maze.txt"))
        if maze_updated:
            self.planner.replan(self.location, self.heading)
            self.show_current_policy_and_map()
            self.count += 1
        rotation, movement = self.planner.next_move(self.location, self.heading)  # choose next action
        # Assumption: The planner will not choose a value that will run into a wall
        if rotation == "Reset" and movement == "Reset":
            self.reset()
        else:
            self.move(rotation, movement)

        return rotation, movement

    def move(self, rotation, movement):
        self.heading = self.heading.rotate(rotation)
        direction_of_movement = self.heading if movement > 0 else self.heading.flip()
        for i in range(abs(movement)):
            self.location = self.location.add(direction_of_movement)

    def reset(self):
        self.location = Position(0, 0)
        self.heading = Direction(0)
        self.planner.replan(self.location, self.heading)
        self.show_current_policy_and_map()

    def show_current_policy_and_map(self):
        vis = Visualizer(self.maze_map.dim)
        vis.draw_maze(Maze('known_maze.txt'))
        vis.draw_policy(reversed(self.planner.policy), self.location, self.heading)
        vis.show_window()
