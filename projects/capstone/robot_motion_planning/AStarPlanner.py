from MazeMap import MazeMap
from Planner import Planner
from PriorityQueue import PriorityQueue
from Position import Position
from Direction import Direction
from MazeHeuristic import MazeHeuristic


class AStarPlanner(Planner):
    def __init__(self, maze_map, heuristic):
        """
        Initializer for this class
        :type maze_map: MazeMap
        :param maze_map: The maze map stores and updates information about the maze.
        :type heuristic: MazeHeuristic
        """
        super(AStarPlanner, self).__init__(maze_map)
        self.maze_dim = maze_map.dim
        self.policy = []  # list of tuples of moves
        self.heuristic = heuristic

    def next_move(self, location, heading):
        super(AStarPlanner, self).next_move(location, heading)
        if len(self.policy) == 0:
            return None
        return self.policy.pop()

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
        open_nodes = PriorityQueue(lifo=False)
        closed_nodes = set()
        came_from = {}  # The key is the end state, the value is a tuple of g, move, and start state

        initial_state = (location, heading)
        g = 0
        h = self.heuristic.get_value(initial_state)
        f = g + h
        open_nodes.insert(f, initial_state)
        came_from[initial_state] = (g, None, None)
        current_state = initial_state
        while len(open_nodes) > 0:
            while current_state in closed_nodes:
                current_state = open_nodes.pop_min()

            closed_nodes.add(current_state)

            if self.heuristic.get_value(current_state) == 0:
                pol = self.create_policy(current_state, initial_state, came_from)
                return self.policy

            moves = self.get_possible_moves(current_state)
            for move in moves:
                new_state = self.get_move_result(current_state, move)
                if new_state in closed_nodes:
                    continue
                g = came_from[current_state][0] + self.get_cost(move)
                h = self.heuristic.get_value(new_state)
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
