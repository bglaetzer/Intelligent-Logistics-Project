
from node import ConstraintNode


class ConstraintTree():
    def __init__(self):
        self.nodes = []


    def add_node(self, rootNodeID, nodeID, paths, constraints, cost):
        node = ConstraintNode(rootNodeID, nodeID, constraints, paths, cost)
        self.nodes.append(node)

    def get_best(self):
        pass #TODO: Get next node to expand (node with lowest cost)