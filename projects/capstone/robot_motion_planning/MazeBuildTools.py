from Position import Position
from Direction import Direction
from MazeMap import MazeMap

n = Direction(0)
e = Direction(1)
s = Direction(2)
w = Direction(3)


class MazeBuildTools(object):
    def __init__(self):
        self.m = MazeMap(16, "test_maze_05.txt")

    def set_wall(self, x, y, d, is_wall=True):
        self.m.cells[Position(x, y)].walls[d].is_wall = is_wall

    def mass_wall(self, x1, y1, x2, y2, d, is_wall=True):
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.set_wall(i, j, d, is_wall)

    def stair(self, x1, y1, x2):
        x = x1
        y = y1
        while x < x2:
            self.set_wall(x, y, e)
            self.set_wall(x, y, s)
            self.set_wall(x, y, n, is_wall=False)
            self.set_wall(x, y, w, is_wall=False)
            x += 1
            y += 1

    def clear_vertical_path(self, x, y1, y2):
        for i in range(y1, y2 + 1):
            self.set_wall(x, i, n, is_wall=False)

    def goal(self):
        self.set_wall(7, 7, s)
        self.set_wall(7, 7, w)
        self.set_wall(7, 7, n, is_wall=False)
        self.set_wall(7, 7, e, is_wall=False)
        self.set_wall(7, 8, w)
        self.set_wall(7, 8, n)
        self.set_wall(8, 8, n)
        self.set_wall(8, 8, e)
        self.set_wall(8, 8, w, is_wall=False)
        self.set_wall(8, 8, s, is_wall=False)
        self.set_wall(8, 7, s)
        self.set_wall(8, 7, e)

    def vertical_ladder(self, x, y, height):
        self.mass_wall(x, y, x, y + height, w)
        self.mass_wall(x + 1, y, x + 1, y + height, e)
        self.mass_wall(x, y, x, y + height, e, is_wall=False)
        for i in range(height):
            if i % 2 == 0:
                self.set_wall(x, y + i, s)
                self.set_wall(x + 1, y + i, s, is_wall=False)
            else:
                self.set_wall(x, y + i, s, is_wall=False)
                self.set_wall(x + 1, y + i, s)
