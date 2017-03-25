from Position import Position
from Direction import Direction


class MazeHeuristic(object):
    def __init__(self, maze_dim):
        self.maze_dim = maze_dim

    def get_value(self, state):
        raise NotImplemented("You must override get_value in a subclass.")

    def display_heuristic(self):
        heuristic = []
        for i in range(self.maze_dim):
            row = []
            for j in range(self.maze_dim):
                pos = Position(i, j)
                head = Direction(0)
                state = (pos, head)
                h = self.get_value(state)
                row.append(h)
            heuristic.append(row)

        for i in reversed(heuristic):
            print i
