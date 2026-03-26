class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = (parent.depth + 1) if parent else 0

    def path(self):
        node, out = self, []
        while node:
            out.append(node.state)
            node = node.parent
        return out[::-1]

    def actions_path(self):
        node, out = self, []
        while node.parent:
            out.append(node.action)
            node = node.parent
        return out[::-1]

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f"Node({self.state}, cost={self.cost})"
