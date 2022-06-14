import clingo, argparse

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree

#Yields initial single agent plans
def initial_solve(horizon, trans_instance, node):
    ctl = clingo.Control([])
    ctl.add("base", [], f"#const horizon={horizon}.")
    ctl.load("Encodings/plans.lp")
    trans_instance.load_in_clingo(ctl, False, 0)
    ctl.ground([("base", [])])

    ctl.solve(on_model = lambda m: on_initial_model(node, m)) #TODO: If instance is unsatisfied (could not understand python API on this)

#Saves plans in a dict and first conflict in a list
def on_initial_model(node, m):
    for symbol in m.symbols(shown=True):
        if(str(symbol).startswith("robot_at") and len(symbol.arguments) > 2):
            robot_id = str(symbol.arguments[0])
            node_id = str(symbol.arguments[1])
            step = int(str(symbol.arguments[2]))

            if robot_id in node.solution.keys():
                node.solution[robot_id][step] = node_id
            else:
                node.solution[robot_id] = {step : node_id}

        if(str(symbol).startswith("sum_of_costs")):
            node.cost = int(str(symbol.arguments[0]))

def transform_to_asprilo_output(trans_instance, node):
    ctl = clingo.Control([])
    ctl.load("Encodings/output.lp")
    trans_instance.load_in_clingo(ctl, False, 0)
    node.load_paths_in_clingo(ctl)
    ctl.ground([("base", [])])

    ctl.solve(on_model = lambda m: write_to_file( m))

def write_to_file(m):
    file = open(args.asprilo_output,"w")

    for atom in m.symbols(shown=True):
        file.write(f"{atom}.\n")

    file.close()

def run(args):

    #Benchmarking timer probably starts here

    trans_instance = ClingoInstance()
    tree = ConstraintTree()
    horizon = args.horizon
    instance = args.instance

    # Load instance and transform input
    ctl = clingo.Control()
    ctl.load(instance)
    ctl.load("Encodings/input.lp")
    ctl.ground([("base", [])])
    ctl.solve(on_model= lambda m: trans_instance.on_model_load_input(m))

    #Initialize root node
    root_node = ConstraintNode()
    root_node.parent = 0
    root_node.id = 1
    initial_solve(horizon, trans_instance, root_node)
    tree.nodes.append(root_node)

    #Main CBS loop
    while len(tree.nodes) > 0:
        tree.get_next()
        tree.next.validate_solution()
        if(len(tree.next.min_conflict) == 0):
            print("Instance solved.")
            if(args.asprilo_output):
                transform_to_asprilo_output(trans_instance, tree.next)
            break
        else:
            cnt = 0
            for robot in tree.next.min_conflict.get("robots"):
                child_node = ConstraintNode()
                child_node.parent = tree.next.id
                child_node.id = tree.next.id*2 + cnt
                child_node.constraint.append([robot, tree.next.min_conflict.get("node"), tree.next.min_conflict.get("step")])
                for cons in tree.next.constraint:
                    child_node.constraint.append(cons)
                for plan in tree.next.solution.items():
                    if(plan[0]!=robot):
                        child_node.solution[plan[0]] = plan[1]
                child_node.update_solution(horizon, trans_instance, robot)
                child_node.calculate_cost(trans_instance)
                cnt += 1
                tree.nodes.append(child_node)
            tree.nodes.remove(tree.next)
    else:
        print("Instance unsolvable.")




parser = argparse.ArgumentParser()

parser.add_argument("-i", "--instance", help="Instance that should be solved. Asprilo Input format is required", required=True)
parser.add_argument("-o", "--horizon", help="The upper bound for the solution, as in maximum number of steps for a single agent.", type=int, required=True)
parser.add_argument("-v", "--visualize", help="Visualizes the graph with clingraph", action='store_true')
parser.add_argument("-a", "--asprilo_output", help="Generates an asprilo output file for the solution and saves it at the specified location", default="")

args = parser.parse_args()

if args.visualize and not args.asprilo_output: parser.error("Clingraph needs asprilo output instance, please specify by using --asprilo_output OUTPUT_FILE")

run(args)