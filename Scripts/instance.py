
class ClingoInstance():
    def __init__(self):
        self.nodes = []
        self.robots = []
        self.goals = []

    def show(self):
        print("Nodes:", self.nodes)
        print("Robot starting positions:", self.robots)
        print("Goal positions:", self.goals)

    def on_model_load_input(self, m):
        for symbol in m.symbols(shown=True):
            if(str(symbol).startswith("node")):
                self.nodes.append({
                    "id": str(symbol.arguments[0]),
                    "X": str(symbol.arguments[1]),
                    "Y": str(symbol.arguments[2])
                })
            elif(str(symbol).startswith("robot_at")):
                self.robots.append({
                    "id": str(symbol.arguments[0]),
                    "node_id": str(symbol.arguments[1])
                })
            elif(str(symbol).startswith("goal")):
                self.goals.append({
                    'node_id': str(symbol.arguments[0]),
                    'robot_id': int(str(symbol.arguments[1]))
                })

    def load_in_clingo(self, ctl, flag, agent):
        for node in self.nodes:
            ctl.add("base", [],  f"node({node['id']}, {node['X']}, {node['Y']}).")
        for robot in self.robots:
            if(flag == True):
                if(robot["id"] == agent):
                    ctl.add("base", [], f"robot_at({robot['id']}, {robot['node_id']}).")
            else:
                ctl.add("base", [], f"robot_at({robot['id']}, {robot['node_id']}).")

        for goal in self.goals:
            if(flag == True):
                if(int(goal['robot_id']) == int(agent)):
                    ctl.add("base", [], f"goal({goal['node_id']}, {goal['robot_id']}).")
            else:
                ctl.add("base", [], f"goal({goal['node_id']}, {goal['robot_id']}).")

        ctl.add("base", [], f"robot(ID) :- robot_at(ID, _).")