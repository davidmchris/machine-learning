"""
Developer: David Christensen
The draw_maze function is shamelessly copied from Udacity's showmaze.py. The other stuff is my own.
"""
import turtle
from Tkinter import *
from maze import Maze


class Visualizer(object):
    def __init__(self, maze_dim):
        """
        :type maze: Maze
        :param maze: The maze to draw
        """
        tk = Toplevel()
        screen = Canvas(tk, width=500, height=500)
        screen.pack()

        self.window = turtle.TurtleScreen(screen)

        self.wally = turtle.RawTurtle(screen)
        # self.wally = turtle.Turtle()
        self.wally.speed(0)
        self.wally.hideturtle()
        self.wally.penup()
        # maze centered on (0,0), squares are 20 units in length.
        self.sq_size = 20
        self.origin = maze_dim * self.sq_size / -2

    def draw_maze(self, maze):
        # iterate through squares one by one to decide where to draw walls
        for x in range(maze.dim):
            for y in range(maze.dim):
                if not maze.is_permissible([x, y], 'up'):
                    self.wally.goto(self.origin + self.sq_size * x, self.origin + self.sq_size * (y + 1))
                    self.wally.setheading(0)
                    self.wally.pendown()
                    self.wally.forward(self.sq_size)
                    self.wally.penup()

                if not maze.is_permissible([x, y], 'right'):
                    a = self.origin + self.sq_size * (x + 1), self.origin + self.sq_size * y
                    self.wally.goto(a)
                    self.wally.setheading(90)
                    self.wally.pendown()
                    self.wally.forward(self.sq_size)
                    self.wally.penup()

                # only check bottom wall if on lowest row
                if y == 0 and not maze.is_permissible([x, y], 'down'):
                    self.wally.goto(self.origin + self.sq_size * x, self.origin)
                    self.wally.setheading(0)
                    self.wally.pendown()
                    self.wally.forward(self.sq_size)
                    self.wally.penup()

                # only check left wall if on leftmost column
                if x == 0 and not maze.is_permissible([x, y], 'left'):
                    self.wally.goto(self.origin, self.origin + self.sq_size * y)
                    self.wally.setheading(90)
                    self.wally.pendown()
                    self.wally.forward(self.sq_size)
                    self.wally.penup()

    def draw_policy(self, policy, start_location, start_heading):
        self.wally.goto(start_location.x * self.sq_size + self.origin + self.sq_size / 2,
                        start_location.y * self.sq_size + self.origin + self.sq_size / 2)
        self.wally.setheading(90-start_heading.angle())
        self.wally.color('red')
        self.wally.pendown()
        for move in policy:
            self.draw_move(move)
        self.wally.penup()
        # Show the turtle back at the beginning
        self.wally.goto(start_location.x * self.sq_size + self.origin + self.sq_size / 2,
                        start_location.y * self.sq_size + self.origin + self.sq_size / 2)
        self.wally.setheading(90 - start_heading.angle())
        self.wally.showturtle()

    def draw_move(self, move):
        self.wally.right(move[0])
        self.wally.forward(move[1] * self.sq_size)

    def show_window(self):
        turtle.mainloop()
        # self.window.exitonclick()
        pass
