import clingo

class ConstraintNode():
    def __init__(self):
        self.id = 0
        self.parent = 0
        self.constraint = []
        self.min_conflict = {}
        self.solution = {}
        self.cost = 0

    def update_solution(self, horizon, instance):
        ctl = clingo.Control([])
        ctl.add("base", [], f"#const horizon={horizon}.")
        ctl.load("Encodings/plans.lp")
        instance.load_in_clingo(ctl)
        self.load_constraints_in_clingo(ctl)

        ctl.ground([("base", [])])
        
        ctl.solve(on_model = lambda m: self.on_model_solution(m))
        # TODO: Only replan conflicting agents

    def on_model_solution(self, m):
        for symbol in m.symbols(shown=True):
            if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
                robot_id = str(symbol.arguments[0])
                node_id = str(symbol.arguments[1])
                step = int(str(symbol.arguments[2]))

                if robot_id in self.solution.keys():
                    self.solution[robot_id][node_id] = [step]
                else:
                    self.solution[robot_id] = {step : node_id}
        
        if(str(symbol).startswith("conflict") and len(symbol.arguments) > 4):
            conflict_id = str(symbol.arguments[0])
            robot1_id = str(symbol.arguments[1])
            robot2_id = str(symbol.arguments[2])
            node_id = str(symbol.arguments[3])
            step = int(str(symbol.arguments[4]))

            if(len(self.min_conflict) == 0 or step < self.min_conflict[4]):#TODO: check if more than 2 agents collide
                self.min_conflict = {"type" : conflict_id, "robots" : [robot1_id, robot2_id], "node" : node_id, "step" : step}

    def load_constraints_in_clingo(self, ctl):
        for cons in self.constraint:
            if(len(cons) > 0):
                ctl.add("base", [], f":- robot_at({cons[0]}, {cons[1]}, {cons[2]}).")

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