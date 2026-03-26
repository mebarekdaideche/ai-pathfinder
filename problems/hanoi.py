from core.problem import Problem

LABELS = ['A', 'B', 'C']


class Hanoi(Problem):

    def __init__(self, n=3):
        self.n = n
        self._init = (tuple(range(n, 0, -1)), (), ())
        self._goal = ((), (), tuple(range(n, 0, -1)))

    def get_initial_state(self):
        return self._init

    def get_goal_state(self):
        return self._goal

    def is_goal(self, state):
        return state == self._goal

    def get_successors(self, state):
        res = []
        for src in range(3):
            if not state[src]:
                continue
            disk = state[src][-1]
            for dst in range(3):
                if src == dst:
                    continue
                if state[dst] and state[dst][-1] < disk:
                    continue
                pegs = [list(p) for p in state]
                pegs[src].pop()
                pegs[dst].append(disk)
                new_state = tuple(tuple(p) for p in pegs)
                res.append((new_state, f'disk{disk}: {LABELS[src]}->{LABELS[dst]}', 1))
        return res

    def heuristic(self, state):
        # combien de disques pas encore en place sur C
        in_place = 0
        for i, d in enumerate(state[2]):
            if i < len(self._goal[2]) and d == self._goal[2][i]:
                in_place += 1
            else:
                break
        return self.n - in_place

    def describe_state(self, state):
        return '\n'.join(f"{LABELS[i]}: {list(state[i])}" for i in range(3))
