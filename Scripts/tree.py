
from node import ConstraintNode


class ConstraintTree():
    def __init__(self):
        self.nodes = []
        self.next = ConstraintNode()

    def get_next(self):
        cur = ConstraintNode()
        cur.id = -1
        for node in self.nodes:
            if(cur.id == -1 or node.cost < cur.cost):
                cur = node
        self.next = cur

    def show(self, level):
        if(level > 0):
            print("Nodes:")
            for node in self.nodes:
                node.show()
            print("Next node to expand:")
            self.next.show()
        else:
            print(len(self.nodes))