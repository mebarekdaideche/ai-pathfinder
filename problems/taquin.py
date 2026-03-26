from core.problem import Problem

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
TARGET_POS = {v: i for i, v in enumerate(GOAL)}

MOVES = {'haut': -3, 'bas': 3, 'gauche': -1, 'droite': 1}


class Taquin(Problem):

    def __init__(self, initial=None):
        self._init = tuple(initial) if initial else (1, 2, 3, 4, 0, 6, 7, 5, 8)

    def get_initial_state(self):
        return self._init

    def get_goal_state(self):
        return GOAL

    def is_goal(self, state):
        return state == GOAL

    def get_successors(self, state):
        res = []
        blank = state.index(0)
        row, col = divmod(blank, 3)

        neighbors = {}
        if row > 0: neighbors['haut']   = blank - 3
        if row < 2: neighbors['bas']    = blank + 3
        if col > 0: neighbors['gauche'] = blank - 1
        if col < 2: neighbors['droite'] = blank + 1

        for move, target in neighbors.items():
            lst = list(state)
            lst[blank], lst[target] = lst[target], lst[blank]
            res.append((tuple(lst), move, 1))

        return res

    def heuristic(self, state):
        # manhattan distance — marche bien avec A*
        dist = 0
        for i, tile in enumerate(state):
            if tile == 0:
                continue
            r1, c1 = divmod(i, 3)
            r2, c2 = divmod(TARGET_POS[tile], 3)
            dist += abs(r1 - r2) + abs(c1 - c2)
        return dist

    def describe_state(self, state):
        rows = []
        for i in range(0, 9, 3):
            rows.append(' | '.join(str(state[i+j]) if state[i+j] else ' ' for j in range(3)))
        return '\n---\n'.join(rows)
