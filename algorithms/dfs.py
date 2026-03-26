import time
from core.node import Node

# limite à 500 sinon ça tourne en rond sur certains problèmes
MAX_DEPTH = 500


def dfs(problem):
    t0 = time.time()
    stack = [Node(problem.get_initial_state())]
    seen = set()
    count = 0

    while stack:
        node = stack.pop()

        if node.state in seen:
            continue
        seen.add(node.state)
        count += 1

        if problem.is_goal(node.state):
            return _res(node, count, t0)

        if node.depth >= MAX_DEPTH:
            continue

        for state, action, cost in reversed(problem.get_successors(node.state)):
            if state not in seen:
                stack.append(Node(state, node, action, node.cost + cost))

    return _res(None, count, t0)


def _res(node, count, t0):
    ok = node is not None
    return {
        'found': ok,
        'path': node.path() if ok else [],
        'actions': node.actions_path() if ok else [],
        'explored': count,
        'time': time.time() - t0,
    }
