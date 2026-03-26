from abc import ABC, abstractmethod


class Problem(ABC):

    @abstractmethod
    def get_initial_state(self): pass

    @abstractmethod
    def get_goal_state(self): pass

    @abstractmethod
    def get_successors(self, state): pass

    @abstractmethod
    def is_goal(self, state): pass

    def heuristic(self, state):
        return 0
