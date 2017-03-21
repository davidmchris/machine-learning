from Planner import Planner
from MazeMap import MazeMap


class VisitCountPlanner(Planner):
    def __init__(self, maze_map):
        """
        :type maze_map: MazeMap
        """
        super(VisitCountPlanner, self).__init__(maze_map)
        self.maze_map = maze_map
        self.visits = [[0 for j in range(maze_map.dim)] for i in range(maze_map.dim)]

    def next_move(self, location, heading):
        self.visits[location.x][location.y] += 1
        print "({}, {}) visit_count = {}".format(location.x, location.y, self.visits[location.x][location.y])
        current_state = (location, heading)
        moves = self.get_possible_moves(current_state)
        lowest_visits = 1000
        best_move = None
        for move in moves:
            new_location, new_heading = self.get_move_result(current_state, move)
            visit_count = self.visits[new_location.x][new_location.y]
            if visit_count < lowest_visits:
                lowest_visits = visit_count
                best_move = move
        return best_move

    def print_visits(self):
        for i in self.visits:
            print i
