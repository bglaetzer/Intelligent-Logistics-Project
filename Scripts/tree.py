
from node import ConstraintNode


class ConstraintTree():
    def __init__(self):
        self.nodes = []
        self.next = ConstraintNode()

    def get_next(self):
        for node in self.nodes:
            cur = 0
            if(cur == 0 or node.cost < cur):
                self.next = node

    def show(self):
        print("Nodes:")
        for node in self.nodes:
            node.show()
        print("Next node to expand:")
        self.next.show()