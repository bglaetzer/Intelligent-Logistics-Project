import clingo, argparse

from numpy import full

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree

#Yields initial single agent plans
def initial_solve(horizon, trans_instance, solution):
    ctl = clingo.Control([])
    ctl.add("base", [], f"#const horizon={horizon}.")
    ctl.load("Encodings/plans.lp")
    trans_instance.load_in_clingo(ctl)
    ctl.ground([("base", [])])
    
    ctl.solve(on_model = lambda m: on_model_solution(solution, m)) #TODO: If instance is unsatisfied (could not understand python API on this)

#Saves plans in a dict
def on_model_solution(solution, m):
    for symbol in m.symbols(shown=True):
        if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
            robot_id = str(symbol.arguments[0])
            node_id = str(symbol.arguments[1])
            step = int(str(symbol.arguments[2]))

            if robot_id in solution.keys():
                solution[robot_id][node_id] = [step]
            else:
                solution[robot_id] = {step : node_id}

def run(args):

    #Benchmarking timer probably starts here

    trans_instance = ClingoInstance()
    tree = ConstraintTree()
    horizon = args.horizon
    instance = args.instance

    # Load instance and transform input
    ctl = clingo.Control()
    ctl.load(args.instance)
    ctl.load("encodings/input.lp")
    ctl.ground([("base", [])])
    ctl.solve(on_model= lambda m: trans_instance.on_model_load_input(m))

    #Initialize root node
    root_node = ConstraintNode()
    root_node.parent = 0
    root_node.id = 1
    initial_solve(horizon, trans_instance, root_node.solution)
    print(root_node.solution)
    tree.nodes.append(root_node)

    # TODO: Start the loop


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--instance", help="Instance that should be solved. Asprilo Input format is required", required=True)
parser.add_argument("-o", "--horizon", help="The upper bound for the solution, as in maximum number of steps for a single agent.", type=int, required=True)

args = parser.parse_args()

run(args)