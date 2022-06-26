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

    def calculate_makespan(self):
        temp = 0
        for robot in self.solution.keys():
            for sol in self.solution[str(robot)].items():
                if(sol[0] > temp):
                    temp = sol[0]
        return(temp)

    def calculate_cost(self, instance):
        sum = 0
        for goal in instance.goals:
            for robot in self.solution.keys():
                if(str(goal["robot_id"]) == str(robot)):
                    for node in self.solution[str(robot)].items():
                        if(node[1]== goal["node_id"]):
                            sum += int(node[0])
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
            if(str(symbol).startswith("min_conflict")):
                conflict_id = str(symbol.arguments[0])
                robot1_id = str(symbol.arguments[1])
                robot2_id = str(symbol.arguments[2])
                node_id = str(symbol.arguments[3])
                step = int(str(symbol.arguments[4]))
                
                self.min_conflict = {"type" : conflict_id, "robots" : [robot1_id, robot2_id], "node" : node_id, "step" : step}


    def update_solution(self, horizon, instance, agent, binfo, performance_start_time, start_time, file):
        ctl = clingo.Control(["--opt-mode=opt", f"-c horizon={horizon}"])
        ctl.load("Encodings/plans.lp")
        instance.load_in_clingo(ctl, True, agent)
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
                ctl.add("base", [], f":- robot_at({cons[0]}, {cons[1]}, {cons[2]}).")

    def show(self):
        print("ID:", self.id)
        print("Parent ID:", self.parent)
        print("Constraints:", self.constraint)
        print("Minimum Conflict:", self.min_conflict)
        print("Plans:", self.solution)
        print("Sum of Costs:", self.cost)