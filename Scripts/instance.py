
class ClingoInstance():
    def __init__(self):
        self.nodes = []
        self.robots = []
        self.goals = []

    def on_model_load_input(self, m):
        for symbol in m.symbols(shown=True):
            if(str(symbol).startswith("node")):
                self.nodes.append({
                    "id": str(symbol.arguments[0])
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