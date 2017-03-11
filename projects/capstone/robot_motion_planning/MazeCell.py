from Position import Position
from Direction import Direction


class MazeCell(object):
    def __init__(self, position):
        self.position = position
        self.walls = {}
        for i in range(4):
            self.walls[Direction(i)] = None
