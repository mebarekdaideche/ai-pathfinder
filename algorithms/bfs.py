import time
from collections import deque
from core.node import Node


def bfs(problem):
    t0 = time.time()
    root = Node(problem.get_initial_state())

    if problem.is_goal(root.state):
        return _res(root, 0, t0)

    queue = deque([root])
    seen = {root.state}
    count = 0

    while queue:
        node = queue.popleft()
        count += 1

        for state, action, cost in problem.get_successors(node.state):
            if state in seen:
                continue
            child = Node(state, node, action, node.cost + cost)
            if problem.is_goal(child.state):
                return _res(child, count, t0)
            seen.add(state)
            queue.append(child)

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
