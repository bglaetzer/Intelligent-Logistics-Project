import os, subprocess, clingo

class ConstraintNode():
    def __init__(self):
        self.id = 0
        self.parent = 0
        self.constraints = {}
        self.solution = {}
        self.cost = 0

    def solve(self, horizon, instance):
        ctl = clingo.Control([])
        ctl.add("base", [], f"#const horizon={horizon}.")
        ctl.load("Encodings/plans.lp")
        instance.load_in_clingo(ctl)
        ctl.ground([("base", [])])
        
        # TODO:Integrate constraints from current node into solving and replan 2 agents

    def calculate_cost(self):
        pass #TODO: Calculate Sum of Costs for a node solution here (might be helpful to use some ASP)

    def identify_conflict(self):
        pass #TODO: get the first conflict or identify that there a no conflicts 