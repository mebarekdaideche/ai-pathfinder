import time
import heapq
from core.node import Node


def astar(problem):
    t0 = time.time()
    init = problem.get_initial_state()
    root = Node(init, cost=0)

    heap = [(problem.heuristic(init), 0, root)]
    seen = {}
    count = 0
    i = 0

    while heap:
        _, _, node = heapq.heappop(heap)

        if node.state in seen:
            continue
        seen[node.state] = node.cost
        count += 1

        if problem.is_goal(node.state):
            return _res(node, count, t0)

        for state, action, c in problem.get_successors(node.state):
            if state in seen:
                continue
            g = node.cost + c
            f = g + problem.heuristic(state)
            i += 1
            child = Node(state, node, action, g)
            heapq.heappush(heap, (f, i, child))

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
