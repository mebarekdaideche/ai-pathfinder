from core.problem import Problem

# (loup, chevre, salade, bateau) — 0=gauche 1=droite
INVALID = {
    (0, 0, 1, 1),
    (1, 1, 0, 0),
    (1, 0, 0, 1),
    (0, 1, 1, 0),
}


class LoupChevreSalade(Problem):

    def get_initial_state(self):
        return (0, 0, 0, 0)

    def get_goal_state(self):
        return (1, 1, 1, 1)

    def is_goal(self, state):
        return state == (1, 1, 1, 1)

    def get_successors(self, state):
        loup, chevre, salade, bateau = state
        dest = 1 - bateau
        res = []

        # passagers dispo de ce côté
        passagers = []
        if loup == bateau:    passagers.append(('loup', 0))
        if chevre == bateau:  passagers.append(('chevre', 1))
        if salade == bateau:  passagers.append(('salade', 2))

        # traversée seul
        s = list(state)
        s[3] = dest
        self._add(tuple(s), 'seul', res)

        for nom, idx in passagers:
            s = list(state)
            s[3] = dest
            s[idx] = dest
            self._add(tuple(s), f'avec {nom}', res)

        return res

    def _add(self, state, action, lst):
        if state not in INVALID:
            lst.append((state, action, 1))

    def heuristic(self, state):
        return sum(1 for v in state[:3] if v == 0)

    def describe_state(self, state):
        labels = ['Loup', 'Chevre', 'Salade', 'Bateau']
        g = [labels[i] for i, v in enumerate(state) if v == 0]
        d = [labels[i] for i, v in enumerate(state) if v == 1]
        return f"Gauche: {g}  |  Droite: {d}"
