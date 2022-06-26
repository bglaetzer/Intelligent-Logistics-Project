import clingo, argparse, sys, subprocess, time

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree
from benchmarkInfo import BenchmarkInfo

#Yields initial single agent plans
def initial_solve(horizon, trans_instance, node, binfo, performance_start_time, start_time):
    ctl = clingo.Control(["--opt-mode=opt", f"-c horizon={horizon}"])
    ctl.load("Encodings/plans.lp")
    trans_instance.load_in_clingo(ctl, False, 0)
    ctl.ground([("base", [])])

    ctl.solve(on_finish = lambda sat: on_unsat(sat, binfo, performance_start_time, start_time), on_model = lambda m: on_initial_model(node, m))

def on_unsat(sat, binfo, performance_start_time, start_time):
    if (sat.unsatisfiable == True):
        binfo.solving_successfull = -1
        if(args.benchmark):
            binfo.end_benchmark(performance_start_time, start_time, args.benchmark)
        sys.exit("Instance unsolvable. Maybe try a greater horizon.")

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

    binfo = BenchmarkInfo()
    binfo.instance = args.instance
    binfo.horizon = args.horizon
    expansions = 0
    binfo.node_expansions = expansions
    performance_start_time = time.perf_counter_ns()
    start_time = time.process_time_ns()

    trans_instance = ClingoInstance()
    tree = ConstraintTree()
    horizon = args.horizon
    instance = args.instance

    start_input_translation_time = time.process_time_ns()
    # Load instance and transform input
    ctl = clingo.Control()
    ctl.load(instance)
    ctl.load("Encodings/input.lp")
    ctl.ground([("base", [])])
    ctl.solve(on_model= lambda m: trans_instance.on_model_load_input(m))

    if(args.benchmark):
        end_input_translation_time = time.process_time_ns()
        binfo.input_translation = end_input_translation_time - start_input_translation_time

    #Initialize root node
    root_node = ConstraintNode()
    root_node.parent = 0
    root_node.id = 1
    initial_solve(horizon, trans_instance, root_node, binfo, performance_start_time, start_time)
    tree.nodes.append(root_node)

    #Main CBS loop
    while len(tree.nodes) > 0:
        binfo.node_expansions = expansions
        tree.get_next()
        tree.next.validate_solution()
        if(len(tree.next.min_conflict) == 0):
            if(args.benchmark):
                binfo.solving_successfull = 1
                binfo.end_benchmark(performance_start_time, start_time, args.benchmark)
            print("Instance solved.")

            if(args.asprilo_output):
                transform_to_asprilo_output(trans_instance, tree.next)
                if(args.visualize):
                    #clin_out = subprocess.Popen(['clingo', instance, args.asprilo_output, '-n', '0', '--outf=2'], stdout=subprocess.PIPE)
                    #output = subprocess.run(["python", args.visualize, "--viz-encoding=Encodings/viz.lp", "--out=animate", "--engine=neato", "--dir=Out/clingraph", "--select-model=0", "--type=digraph", "--view", "--sort=asc-int"], stdin=clin_out.stdout)
                    subprocess.run(["viz", "-t", instance, "-p", args.asprilo_output], capture_output=True)
            break
        else:
            expansions += 1
            print(expansions)
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
                child_node.update_solution(horizon, trans_instance, robot, binfo, performance_start_time, start_time, args.benchmark)
                child_node.calculate_cost(trans_instance)
                cnt += 1
                tree.nodes.append(child_node)
            tree.nodes.remove(tree.next)
    else:
        if(args.benchmark):
            binfo.solving_successfull = 0
            binfo.end_benchmark(performance_start_time, start_time, args.benchmark)
            print("Instance unsolvable. Complete searchspace exhausted.")




parser = argparse.ArgumentParser()

parser.add_argument("-i", "--instance", help="Instance that should be solved. Asprilo Input format is required", required=True)
parser.add_argument("-o", "--horizon", help="The upper bound for the solution, as in maximum number of steps for a single agent.", type=int, required=True)
parser.add_argument("-v", "--visualize", help="Visualizes the solution with asprilo viz. Clingraph visualization currently disabled.", action='store_true')
parser.add_argument("-a", "--asprilo_output", help="Generates an asprilo output file for the solution and saves it at the specified location", default="")
parser.add_argument("-b", "--benchmark", help="Activate Benchmarking and output it to the specified file", default="")


args = parser.parse_args()

if args.visualize and not args.asprilo_output: parser.error("Visualization needs asprilo output instance, please specify by using --asprilo_output OUTPUT_FILE")

run(args)