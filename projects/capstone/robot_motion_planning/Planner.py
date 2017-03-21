
class Planner(object):
    def __init__(self, maze_map):
        self.maze_map = maze_map
        self.reached_goal = False
        self.run = 1

    def next_move(self, location, heading):
        pass

    def replan(self, location, heading):
        pass

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
