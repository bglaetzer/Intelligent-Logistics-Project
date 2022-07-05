from ast import arguments
import clingo
import sys

class ConstraintNode():
    def __init__(self):
        self.id = 0
        self.parent = 0
        self.constraint = []
        self.min_conflict = {}
        self.solution = {}
        self.cost = 0

    def calculate_cost(self, instance):
        sum = 0
        # Every move that is not a wait action on the goal has cost 1 (same as in CBS Paper)
        for goal in instance.goals:
            for robot in self.solution.keys():
                if(str(goal["robot_id"]) == str(robot)):
                    for node in self.solution[str(robot)].items():
                        if(node[1] != goal["node_id"]):
                            sum += 1
        self.cost = sum

    def validate_solution(self):
        ctl = clingo.Control([])
        ctl.load("Encodings/validate.lp")
        self.load_paths_in_clingo(ctl)

        ctl.ground([("base", [])])
        ctl.solve(on_model = lambda m: self.on_validation(m))

    def load_paths_in_clingo(self, ctl):
        for robot in self.solution.keys():
            for robots in self.solution[robot].items():
                ctl.add("base", [], f"robot_at({robot}, {robots[1]}, {robots[0]}).")

    def on_validation(self, m):
        for symbol in m.symbols(shown=True):
            #TODO: Change this arbitrary tiebraking to something more performant
            if(str(symbol).startswith("min_conflict") and int(str(symbol.arguments[0])) == 0):
                conflict_id = int(str(symbol.arguments[0]))
                robot1_id = str(symbol.arguments[1])
                robot2_id = str(symbol.arguments[2])
                node_id = str(symbol.arguments[3])
                step = int(str(symbol.arguments[4]))
                
                self.min_conflict = {"type" : conflict_id, "robots" : [robot1_id, robot2_id], "node" : node_id, "step" : step}
            
            if(str(symbol).startswith("min_conflict") and int(str(symbol.arguments[0])) == 1 and len(symbol.arguments) > 5):
                conflict_id = int(str(symbol.arguments[0]))
                robot1_id = str(symbol.arguments[1])
                robot2_id = str(symbol.arguments[2])
                node_1_id = int(str(symbol.arguments[3]))
                node_2_id = int(str(symbol.arguments[4]))
                step = int(str(symbol.arguments[5]))
                
                self.min_conflict = {"type" : conflict_id, "robots" : [robot1_id, robot2_id], "node_1" : node_1_id, "node_2" : node_2_id, "step" : step}



    def update_solution(self, horizon, instance, flag, agent, binfo, performance_start_time, start_time, file):
        ctl = clingo.Control(["-n 1", "--opt-mode=optN", f"-c horizon={horizon}"])
        ctl.load("Encodings/plans.lp")
        instance.load_in_clingo(ctl, flag, agent)
        self.load_constraints_in_clingo(ctl)

        ctl.ground([("base", [])])
        
        ctl.solve(on_finish = lambda sat: self.on_unsat(sat, binfo, performance_start_time, start_time, file), on_model = lambda m: self.on_model_solution(m))

    def on_unsat(self, sat, binfo, performance_start_time, start_time, file):
        if (sat.unsatisfiable == True):
            binfo.solving_successfull = -1
            if(file):
                binfo.end_benchmark(performance_start_time, start_time, file)
            sys.exit("Instance unsolvable. Maybe try a greater horizon.")

    def on_model_solution(self, m):
        if (m.optimality_proven):
            for symbol in m.symbols(shown=True):
                if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
                    robot_id = str(symbol.arguments[0])
                    node_id = str(symbol.arguments[1])
                    step = int(str(symbol.arguments[2]))

                    if robot_id in self.solution.keys():
                        self.solution[robot_id][step] = node_id
                    else:
                        self.solution[robot_id] = {step : node_id}

    def load_constraints_in_clingo(self, ctl):
        for cons in self.constraint:
            if(len(cons) > 0):
                if(cons[0] == "vertex"):
                    ctl.add("base", [], f":- robot_at({cons[1]}, {cons[2]}, {cons[3]}).")
                    ctl.add("base", [], f" constraint({cons[1]}, {cons[2]}, {cons[3]}).")
                if(cons[0] == "edge"):
                    ctl.add("base", [], f":- robot_at({cons[1]}, {cons[2]}, {cons[4]}), robot_at({cons[1]}, {cons[3]}, {cons[4]+1}).")

    def show(self):
        print("ID:", self.id)
        print("Parent ID:", self.parent)
        print("Constraints:", self.constraint)
        print("Minimum Conflict:", self.min_conflict)
        print("Plans:", self.solution)
        print("Sum of Costs:", self.cost)