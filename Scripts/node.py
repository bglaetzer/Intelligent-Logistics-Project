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
        self.load_in_clingo(ctl, instance)
        ctl.ground([("base", [])])
        
        # TODO:Integrate constraints from current node into solving
        ctl.solve(on_model = lambda m: self.on_model_solution(m))

    def on_model_solution(self, m):
        for symbol in m.symbols(shown=True):
            if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
                robot_id = str(symbol.arguments[0])
                node_id = str(symbol.arguments[1])
                step = int(str(symbol.arguments[2]))

                self.solution.append([robot_id][step][node_id])
                # TODO: Calculate and  Update Cost here

    def load_in_clingo(ctl, instance):
        for node in instance.nodes:
            ctl.add("base", [],  f"node({node['id']}).")\

        for robot in instance.robots:
            ctl.add("base", [], f"robot_at({robot['id']}, {robot['node_id']}).")

        for goal in instance.goals:
            ctl.add("base", [], f"goal({goal['node_id']}, {goal['robot_id']}).")