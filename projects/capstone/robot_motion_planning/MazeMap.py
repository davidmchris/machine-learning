from MazeCell import MazeCell
from Position import Position
from Direction import Direction
from Wall import Wall
import numpy as np

n = Direction(0)
e = Direction(1)
s = Direction(2)
w = Direction(3)


class MazeMap(object):
    def __init__(self, maze_dim = None, file_path = None):
        if file_path is not None:
            with open(file_path, 'rb') as f_in:
                # First line should be an integer with the maze dimensions
                self.dim = int(f_in.next())
        else:
            self.dim = maze_dim
        self.cells = {}
        for x in range(self.dim):
            for y in range(self.dim):
                pos = Position(x, y)
                cell = MazeCell(pos)
                self.cells[pos] = cell
                # West wall
                if pos.x == 0:
                    cell.walls[w] = Wall(True)
                else:
                    cell.walls[w] = self.cells[pos.add(w)].walls[e]
                # East wall
                if pos.x == self.dim-1 or (pos.x == 0 and pos.y == 0):
                    cell.walls[e] = Wall(True)
                else:
                    cell.walls[e] = Wall(None)
                # South wall
                if pos.y == 0:
                    cell.walls[s] = Wall(True)
                else:
                    cell.walls[s] = self.cells[pos.add(s)].walls[n]
                # North wall
                if pos.y == self.dim-1:
                    cell.walls[n] = Wall(True)
                else:
                    cell.walls[n] = Wall(None)
        if file_path is not None:
            self.read_from_file(file_path)

    def update(self, position, heading, sensors):
        """
        Update the cells data based on what the sensors can see.
        :param position: The indices of the grid where the robot is currently positioned
        :param heading: The orientation of the robot (0=n, 1=e, 2=s, or 3=w)
        :param sensors: Number of squares in the l, fwd, and r directions before a wall
        """
        updated = False
        sensor_directions = [heading.rotate(-90), heading, heading.rotate(90)]
        for i in range(0, 3):
            temp_pos = position
            sensor_direction = sensor_directions[i]
            spaces_to_wall = sensors[i]
            for j in range(0, spaces_to_wall + 1):
                walls = self.cells[temp_pos].walls
                if j == spaces_to_wall:
                    if walls[sensor_direction].is_wall is None:
                        updated = True
                    walls[sensor_direction].is_wall = True
                else:
                    walls[sensor_direction].is_wall = False
                temp_pos = temp_pos.add(sensor_direction)
        return updated

    def get_wall_value(self, position, direction):
        return self.cells[position].walls[direction].is_wall

    def check_valid_move(self, location, heading, rotation, movement):
        if movement == 0:
            return False  # Don't allow the robot to just sit there
        new_heading = heading.rotate(rotation)
        movement_direction = new_heading if movement > 0 else new_heading.flip()
        i = 0
        temp_location = location
        while abs(movement) - i > 0:
            hit_wall = self.get_wall_value(temp_location, movement_direction)
            if hit_wall is not None and hit_wall:
                return False
            i += 1
            temp_location = temp_location.add(movement_direction)
        return True

    def at_goal(self, location):
        goal = [self.dim / 2, self.dim / 2 - 1]
        return location.x in goal and location.y in goal

    def dump_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self.dim))
            f.write("\n")
            for i in range(self.dim):
                for j in range(self.dim):
                    pos = Position(i, j)
                    cell_val = 0
                    cell_val |= (1 if self.get_wall_value(pos, n) is None else not self.get_wall_value(pos, n))
                    cell_val |= (1 if self.get_wall_value(pos, e) is None else not self.get_wall_value(pos, e)) << 1
                    cell_val |= (1 if self.get_wall_value(pos, s) is None else not self.get_wall_value(pos, s)) << 2
                    cell_val |= (1 if self.get_wall_value(pos, w) is None else not self.get_wall_value(pos, w)) << 3
                    f.write(str(cell_val))
                    if j < self.dim - 1:
                        f.write(",")
                f.write("\n")

    def read_from_file(self, file_path):
        """
        This is a modified copy of the __init__ function in Udacity's maze.py
        :param file_path: The path to the file
        :return: Doesn't return anything
        """
        with open(file_path, 'rb') as f_in:

            # First line should be an integer with the maze dimensions
            self.dim = int(f_in.next())

            # Subsequent lines describe the permissability of walls
            walls = []
            for line in f_in:
                walls.append(map(int,line.split(',')))
            wall_vals = np.array(walls)

        # # Perform validation on maze
        # # Maze dimensions
        # if self.dim % 2:
        #     raise Exception('Maze dimensions must be even in length!')
        # if wall_vals.shape != (self.dim, self.dim):
        #     raise Exception('Maze shape does not match dimension attribute!')
        #
        # # Wall permeability
        # wall_errors = []
        # # vertical walls
        # for x in range(self.dim-1):
        #     for y in range(self.dim):
        #         if (wall_vals[x,y] & 2 != 0) != (wall_vals[x+1,y] & 8 != 0):
        #             wall_errors.append([(x,y), 'v'])
        # # horizontal walls
        # for y in range(self.dim-1):
        #     for x in range(self.dim):
        #         if (wall_vals[x,y] & 1 != 0) != (wall_vals[x,y+1] & 4 != 0):
        #             wall_errors.append([(x,y), 'h'])
        #
        # if wall_errors:
        #     for cell, wall_type in wall_errors:
        #         if wall_type == 'v':
        #             cell2 = (cell[0]+1, cell[1])
        #             print 'Inconsistent vertical wall betweeen {} and {}'.format(cell, cell2)
        #         else:
        #             cell2 = (cell[0], cell[1]+1)
        #             print 'Inconsistent horizontal wall betweeen {} and {}'.format(cell, cell2)
        #     raise Exception('Consistency errors found in wall specifications!')

        for x in range(self.dim):
            for y in range(self.dim):
                pos = Position(x, y)
                self.cells[pos].walls[n].is_wall = (wall_vals[x,y] & 1) == 0
                self.cells[pos].walls[e].is_wall = (wall_vals[x,y] & 2) == 0
                self.cells[pos].walls[s].is_wall = (wall_vals[x,y] & 4) == 0
                self.cells[pos].walls[w].is_wall = (wall_vals[x,y] & 8) == 0


