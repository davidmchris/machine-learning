from MazeMap import MazeMap
from AStarPlanner import AStarPlanner
from Visualizer import Visualizer
from Position import Position
from Direction import Direction
from maze import Maze
import sys

if __name__ == '__main__':
    file_path = str(sys.argv[1])
    maze_map = MazeMap(file_path=file_path)
    maze = Maze(file_path)
    planner = AStarPlanner(maze_map)
    vis = Visualizer(maze_map.dim)
    start_pos = Position(0,0)
    start_head = Direction(0)
    planner.replan(start_pos, start_head)
    vis.draw_maze(maze)
    vis.draw_policy(reversed(planner.policy), start_pos, start_head)
    vis.show_window()
