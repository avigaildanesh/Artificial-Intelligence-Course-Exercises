import search
import utils

ids = ["No numbers - I'm special!"]

""" Rules """
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4
COLORS = [RED, BLUE, YELLOW, GREEN]


class ZumaProblem(search.Problem):
    """This class implements a pacman problem"""

    def _init_(self, initial):
        """ Magic numbers for balls:
        1 - red, 2 - blue, 3 - yellow, 4 - green."""

        self.line = initial[0]
        self.ammo = initial[1]

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem._init_(self, initial)

    def successor(self, state):
        line, ammo = state
        successors = []

        if not ammo and line:
            return successors

        seen_states = set()
        ball = ammo[0]
        remaining_ammo = ammo[1:]
        new_state = (line, remaining_ammo)
        # if new_state not in seen_states:
        if line or remaining_ammo :
            action = ("skip", ball)
            successors.append((action, new_state))

        for j in range(len(line) + 1):
            new_line = self.remove_sequences(line, j, ball)
            new_state = (new_line, tuple(remaining_ammo))
            if new_state in seen_states:
                continue

            # if new_line or remaining_ammo:
            seen_states.add(new_state)
            action = (ball, j)
            successors.append((action, new_state))
        
        return successors

    def remove_sequences(self, line, j, ball):
        """
        Remove sequences of 3 or more consecutive balls of the same color.
        - line: A tuple representing the current line.
        Returns a new tuple with sequences removed.
        """
        line = list(line)
        line.insert(j, ball)

        while True:
            i = 0
            found_sequence = False
            while i < len(line):
                count = 1
                while i + count < len(line) and line[i] == line[i + count]:
                    count += 1
                if count >= 3:
                    line = line[:i] + line[i + count:]
                    found_sequence = True
                    break
                i = count + i
            if not found_sequence:
                break
        return tuple(line)



    def goal_test(self, state):
        """ Given a state, checks if this is the goal state (row is empty). """
        return len(state[0]) == 0

    def h(self, node):
        line = node.state[0]
        ammo = node.state[1]
        isolated_balls = 0
        for j in range(len(line)):
            if (j==0 or line[j] != line[j - 1]) and (j==len(line)-1 or line[j] != line[j + 1]):
                isolated_balls += 1

        return isolated_balls
    


def create_zuma_problem(game):
    # print("<<create_zuma_problem")
    # """ Create a zuma problem, based on the description.
    # game - pair of lists as described in pdf file"""
    return ZumaProblem(game)

# game = ()

# create_zuma_problem(game)