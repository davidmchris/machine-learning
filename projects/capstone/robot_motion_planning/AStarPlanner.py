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
        super(AStarPlanner, self).__init__(maze_map)
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

    # def get_heuristic_value(self, state):
    #     location = state[0]
    #     if self.maze_map.at_goal(location):
    #         return 0
    #     x_dist_to_goal = min(abs(self.maze_dim / 2 - location.x), abs(location.x - self.maze_dim / 2 + 1))
    #     y_dist_to_goal = min(abs(self.maze_dim / 2 - location.y), abs(location.y - self.maze_dim / 2 + 1))
    #     x_timesteps_to_goal = 0 if x_dist_to_goal == 0 else (x_dist_to_goal - 1) + 1
    #     y_timesteps_to_goal = 0 if y_dist_to_goal == 0 else (y_dist_to_goal - 1) + 1
    #     return x_timesteps_to_goal + y_timesteps_to_goal
    def get_heuristic_value(self, state):
        location = state[0]
        if self.maze_map.at_goal(location):
            return 0
        x_dist_to_goal = min(abs(self.maze_dim / 2 - location.x), abs(location.x - self.maze_dim / 2 + 1))
        y_dist_to_goal = min(abs(self.maze_dim / 2 - location.y), abs(location.y - self.maze_dim / 2 + 1))
        x_timesteps_to_goal = 0 if x_dist_to_goal == 0 else (x_dist_to_goal - 1) / 3 + 1
        y_timesteps_to_goal = 0 if y_dist_to_goal == 0 else (y_dist_to_goal - 1) / 3 + 1
        return x_timesteps_to_goal + y_timesteps_to_goal
    # def get_heuristic_value(self, state):
    #     return 0

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
        print "========================"
        print "        Replan          "
        print "========================"
        open_nodes = PriorityQueue()
        closed_nodes = set()
        came_from = {}  # The key is the end state, the value is a tuple of g, move, and start state

        initial_state = (location, heading)
        g = 0
        h = self.get_heuristic_value(initial_state)
        f = g + h
        open_nodes.insert(f, initial_state)
        came_from[initial_state] = (g, None, None)
        current_state = initial_state
        while len(open_nodes) > 0:
            while current_state in closed_nodes:
                current_state = open_nodes.pop_min()

            closed_nodes.add(current_state)

            if self.maze_map.at_goal(current_state[0]):
                pol = self.create_policy(current_state, initial_state, came_from)
                return self.policy

            moves = self.get_possible_moves(current_state)
            for move in moves:
                new_state = self.get_move_result(current_state, move)
                if new_state in closed_nodes:
                    continue
                g = came_from[current_state][0] + self.get_cost(move)
                h = self.get_heuristic_value(new_state)
                f = g + h
                if new_state not in open_nodes:
                    open_nodes.insert(f, new_state)
                elif new_state in came_from and f >= open_nodes.get_priority(new_state):
                    continue
                came_from[new_state] = (g, move, current_state)
                open_nodes.update_priority(new_state,f)

        return "No path to goal!"

    def state_str(self,state):
        return "({}, {}) {}".format(state[0].x, state[0].y, state[1].letter())


    def create_policy(self, goal_state, initial_state, came_from):
        # Get the policy
        self.policy = []
        current_state = goal_state
        while current_state != initial_state:
            move = came_from[current_state][1]
            self.policy.append(move)
            current_state = came_from[current_state][2]
        return self.policy

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
