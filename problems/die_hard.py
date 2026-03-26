from core.problem import Problem


class DieHard(Problem):
    CAP = (5, 3)
    TARGET = 4

    def get_initial_state(self):
        return (0, 0)

    def get_goal_state(self):
        return (4, None)

    def is_goal(self, state):
        return self.TARGET in state

    def get_successors(self, state):
        a, b = state
        ca, cb = self.CAP
        res = []

        if a < ca: res.append(((ca, b), 'remplir 5L', 1))
        if b < cb: res.append(((a, cb), 'remplir 3L', 1))
        if a > 0:  res.append(((0, b),  'vider 5L', 1))
        if b > 0:  res.append(((a, 0),  'vider 3L', 1))

        if a > 0 and b < cb:
            t = min(a, cb - b)
            res.append(((a - t, b + t), '5L -> 3L', 1))

        if b > 0 and a < ca:
            t = min(b, ca - a)
            res.append(((a + t, b - t), '3L -> 5L', 1))

        return res

    def heuristic(self, state):
        return min(abs(v - self.TARGET) for v in state)

    def describe_state(self, state):
        return f"5L: {state[0]}  |  3L: {state[1]}"
