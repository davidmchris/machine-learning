from MazeMap import MazeMap
from Planner import Planner
from PriorityQueue import PriorityQueue
from Position import Position
from Direction import Direction

class AStarPlanner(Planner):
    def __init__(self, maze_map):
        """
        Initializer for this class
        :type maze_map: MazeMap
        :param maze_map: The maze map stores and updates information about the maze.
        """
        self.maze_map = maze_map
        self.maze_dim = maze_map.dim
        self.policy = []  # list of tuples of moves

    def next_move(self, location, heading):
        if len(self.policy) == 0:
            return "Reset", "Reset"
        return self.policy.pop()

    def get_possible_moves(self, state):
        location = state[0]
        heading = state[1]
        possible_moves = []
        for rot in [90, 0, -90]:
            for mov in range(-3, 4):
                if self.maze_map.check_valid_move(location, heading, rot, mov):
                    possible_moves.append((rot, mov))
        return possible_moves

    def get_move_result(self, state, move):
        location = state[0]
        heading = state[1]
        new_heading = heading.rotate(move[0])
        new_location = location
        direction_of_movement = new_heading if move[1] > 0 else new_heading.flip()
        for i in range(abs(move[1])):
            new_location = new_location.add(direction_of_movement)
        return new_location, new_heading

    def go_back(self, end_state, move):
        """
        Gets the original location and heading given a final location and heading and the move it took to get there.
        :param end_state: The end state from the movement
        :param move: The movement that got you to the end state
        :return: The start state
        """
        end_location = end_state[0]
        end_heading = end_state[1]
        rotation = move[0]
        movement = move[1]
        start_heading = end_heading.rotate(rotation * -1)
        start_location = end_location
        direction_of_movement = end_heading if movement < 0 else end_heading.flip()
        for i in range(abs(movement)):
            start_location = start_location.add(direction_of_movement)
        return start_location, start_heading

    def get_heuristic_value(self, state):
        location = state[0]
        if self.maze_map.at_goal(location):
            return 0

        x_dist_to_goal = min(abs(self.maze_dim / 2 - location.x), abs(location.x - self.maze_dim / 2 + 1))
        y_dist_to_goal = min(abs(self.maze_dim / 2 - location.y), abs(location.y - self.maze_dim / 2 + 1))

        x_timesteps_to_goal = 0 if x_dist_to_goal == 0 else (x_dist_to_goal-1)/3+1
        y_timesteps_to_goal = 0 if y_dist_to_goal == 0 else (y_dist_to_goal-1)/3+1
        return x_timesteps_to_goal + y_timesteps_to_goal

    def get_cost(self, move):
        """
        :param move: The move to get the cost of (could penalize left turns for example).
        :type move: (int, int)
        """
        return 1

    def replan(self, location, heading):
        """
        :type location: Position
        :param location: The current location of the robot
        :type heading: Direction
        :param heading: The current direction the robot is pointing
        """
        open_nodes = PriorityQueue()
        closed_nodes = {}

        initial_state = (location, heading)
        g = 0
        h = self.get_heuristic_value(initial_state)
        f = g + h
        initial_node = (initial_state, g, None)
        open_nodes.insert(f, initial_node)
        current_state = initial_state
        current_node = initial_node
        while len(open_nodes) > 0 and not self.maze_map.at_goal(current_state[0]):
            while current_node[0] in closed_nodes:
                current_node = open_nodes.pop_min()
            current_state = current_node[0]
            moves = self.get_possible_moves(current_state)
            for move in moves:
                new_state = self.get_move_result(current_state, move)
                g = current_node[1] + self.get_cost(move)
                h = self.get_heuristic_value(new_state)
                f = g + h
                new_node = (new_state, g, move)
                if not new_state in closed_nodes:
                    open_nodes.insert(f, new_node)
            closed_nodes[current_node[0]] = (current_node[1], current_node[2])

        # Get the policy
        self.policy = []
        print "-------"
        while current_state != initial_state:
            print current_state[0].x, current_state[0].y, current_state[1].nesw
            move = closed_nodes[current_state][1]
            self.policy.append(move)
            current_state = self.go_back(current_state, move)

    def display_heuristic(self):
        heuristic = []
        for i in range(self.maze_dim):
            row = []
            for j in range(self.maze_dim):
                pos = Position(i, j)
                head = Direction(0)
                state = (pos, head)
                h = self.get_heuristic_value(state)
                row.append(h)
            heuristic.append(row)

        for i in heuristic:
            print i
