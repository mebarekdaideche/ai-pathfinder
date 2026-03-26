from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

ALGORITHMES = {
    'BFS': bfs,
    'DFS': dfs,
    'Dijkstra': dijkstra,
    'A*': astar,
}


class Solver:

    def solve(self, problem, algorithm='A*'):
        if algorithm not in ALGORITHMES:
            raise ValueError(f"algo inconnu: '{algorithm}'. dispo: {list(ALGORITHMES)}")
        return ALGORITHMES[algorithm](problem)

    def compare_all(self, problem):
        return {algo: self.solve(problem, algo) for algo in ALGORITHMES}
