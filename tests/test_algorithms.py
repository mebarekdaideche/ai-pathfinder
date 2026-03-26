import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.solver import Solver
from problems.loup_chevre import LoupChevreSalade
from problems.die_hard import DieHard
from problems.taquin import Taquin
from problems.hanoi import Hanoi

solver = Solver()
ALGOS = ['BFS', 'DFS', 'Dijkstra', 'A*']


@pytest.mark.parametrize("algo", ALGOS)
def test_loup_chevre(algo):
    res = solver.solve(LoupChevreSalade(), algo)
    assert res['found']
    assert LoupChevreSalade().is_goal(res['path'][-1])

def test_loup_chevre_bfs_7steps():
    res = solver.solve(LoupChevreSalade(), 'BFS')
    assert len(res['path']) - 1 == 7


@pytest.mark.parametrize("algo", ALGOS)
def test_die_hard(algo):
    pb = DieHard()
    res = solver.solve(pb, algo)
    assert res['found']
    assert pb.is_goal(res['path'][-1])


def test_taquin_astar():
    assert solver.solve(Taquin(), 'A*')['found']

def test_astar_beats_bfs_on_taquin():
    pb = Taquin()
    assert solver.solve(pb, 'A*')['explored'] <= solver.solve(pb, 'BFS')['explored']


@pytest.mark.parametrize("algo", ALGOS)
def test_hanoi(algo):
    assert solver.solve(Hanoi(3), algo)['found']

def test_hanoi_optimal():
    for algo in ['BFS', 'A*', 'Dijkstra']:
        res = solver.solve(Hanoi(3), algo)
        assert len(res['path']) - 1 == 7


def test_bad_algo():
    with pytest.raises(ValueError):
        solver.solve(DieHard(), 'YOLO')

def test_compare_all():
    res = solver.compare_all(DieHard())
    assert set(res) == {'BFS', 'DFS', 'Dijkstra', 'A*'}
    assert all(r['found'] for r in res.values())
