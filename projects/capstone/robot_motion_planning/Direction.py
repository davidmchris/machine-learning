class Direction(object):
    def __init__(self, nesw):
        self.nesw = nesw % 4

    def __hash__(self):
        return hash(self.nesw)

    def __eq__(self, other):
        return self.nesw == other.nesw

    def __ne__(self, other):
        return not (self == other)

    def rotate(self, angle):
        if angle == 90:
            return Direction(self.nesw+1)
        elif angle == -90:
            return Direction(self.nesw-1)
        else:
            return Direction(self.nesw)

    def flip(self):
        return Direction(self.nesw + 2)

    def x(self):
        if self.nesw == 1:
            return 1
        elif self.nesw == 3:
            return -1
        return 0

    def y(self):
        if self.nesw == 0:
            return 1
        elif self.nesw == 2:
            return -1
        return 0

    def angle(self):
        return 90*self.nesw