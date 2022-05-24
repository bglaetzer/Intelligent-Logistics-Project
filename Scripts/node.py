import os, subprocess, clingo

class ConstraintNode():
    def __init__(self):
        self.id = 0
        self.parent = 0
        self.constraint = {}
        self.min_conflict = []
        self.solution = {}
        self.cost = 0

    def solve(self, horizon, instance):
        ctl = clingo.Control([])
        ctl.add("base", [], f"#const horizon={horizon}.")
        ctl.load("Encodings/plans.lp")
        instance.load_in_clingo(ctl)
        ctl.ground([("base", [])])
        
        # TODO:Integrate constraints from current node into solving and replan conflicting agents

    def calculate_cost(self, instance):
        sum = 0
        for goal in instance.goals:
            for robot in self.solution.items():
                for node in robot[1].items():
                    if(node[0]==goal["node_id"]):
                        sum += int(node[1][0])
        self.cost = sum

    def show(self):
        print("ID:", self.id)
        print("Parent ID:", self.parent)
        print("Constraints:", self.constraint)
        print("Minimum Conflict:", self.min_conflict)
        print("Plans:", self.solution)
        print("Sum of Costs:", self.cost)