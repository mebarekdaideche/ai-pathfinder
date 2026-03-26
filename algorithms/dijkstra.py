import time
import heapq
from core.node import Node


def dijkstra(problem):
    t0 = time.time()
    root = Node(problem.get_initial_state(), cost=0)

    heap = [(0, 0, root)]
    seen = {}
    count = 0
    i = 0

    while heap:
        cost, _, node = heapq.heappop(heap)

        if node.state in seen:
            continue
        seen[node.state] = cost
        count += 1

        if problem.is_goal(node.state):
            return _res(node, count, t0)

        for state, action, c in problem.get_successors(node.state):
            if state not in seen:
                i += 1
                child = Node(state, node, action, cost + c)
                heapq.heappush(heap, (cost + c, i, child))

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
