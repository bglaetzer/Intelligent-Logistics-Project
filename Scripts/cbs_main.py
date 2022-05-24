import clingo, argparse

from numpy import full

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree

#Yields initial single agent plans
def initial_solve(horizon, trans_instance, node):
    ctl = clingo.Control([])
    ctl.add("base", [], f"#const horizon={horizon}.")
    ctl.load("Encodings/plans.lp")
    trans_instance.load_in_clingo(ctl)
    ctl.ground([("base", [])])

    ctl.solve(on_model = lambda m: on_model_solution(node, m)) #TODO: If instance is unsatisfied (could not understand python API on this)

#Saves plans in a dict and first conflict in a list
def on_model_solution(node, m):
    for symbol in m.symbols(shown=True):
        if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
            robot_id = str(symbol.arguments[0])
            node_id = str(symbol.arguments[1])
            step = int(str(symbol.arguments[2]))

            if robot_id in node.solution.keys():
                node.solution[robot_id][node_id] = [step]
            else:
                node.solution[robot_id] = {step : node_id}
        
        if(str(symbol).startswith("conflict") and len(symbol.arguments) > 4):
            conflict_id = str(symbol.arguments[0])
            robot1_id = str(symbol.arguments[1])
            robot2_id = str(symbol.arguments[2])
            node_id = str(symbol.arguments[3])
            step = int(str(symbol.arguments[4]))

            if(len(node.min_conflict) == 0 or step < node.min_conflict[4]):#TODO: check if more than 2 agents collide
                node.min_conflict = [conflict_id, robot1_id, robot2_id, node_id, step]


def run(args):

    #Benchmarking timer probably starts here

    trans_instance = ClingoInstance()
    tree = ConstraintTree()
    horizon = args.horizon
    instance = args.instance

    # Load instance and transform input
    ctl = clingo.Control()
    ctl.load(instance)
    ctl.load("encodings/input.lp")
    ctl.ground([("base", [])])
    ctl.solve(on_model= lambda m: trans_instance.on_model_load_input(m))

    #Initialize root node
    root_node = ConstraintNode()
    root_node.parent = 0
    root_node.id = 1
    initial_solve(horizon, trans_instance, root_node)
    root_node.calculate_cost(trans_instance)
    tree.nodes.append(root_node)

    tree.get_next()
    
    # TODO: Start the loop


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--instance", help="Instance that should be solved. Asprilo Input format is required", required=True)
parser.add_argument("-o", "--horizon", help="The upper bound for the solution, as in maximum number of steps for a single agent.", type=int, required=True)

args = parser.parse_args()

run(args)