import clingo, argparse, sys, subprocess, time

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree
from benchmarkInfo import BenchmarkInfo

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
    root_node.update_solution(horizon, trans_instance, False, 0, binfo, performance_start_time, start_time, args.benchmark)
    root_node.calculate_cost(trans_instance)
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
            print("Instance solved. SoC: ", tree.next.cost)

            if(args.asprilo_output):
                transform_to_asprilo_output(trans_instance, tree.next)
                if(args.visualize):
                    #clin_out = subprocess.Popen(['clingo', instance, args.asprilo_output, '-n', '0', '--outf=2'], stdout=subprocess.PIPE)
                    #output = subprocess.run(["python", args.visualize, "--viz-encoding=Encodings/viz.lp", "--out=animate", "--engine=neato", "--dir=Out/clingraph", "--select-model=0", "--type=digraph", "--view", "--sort=asc-int"], stdin=clin_out.stdout)
                    subprocess.run(["viz", "-t", instance, "-p", args.asprilo_output], capture_output=True)
            break
        else:
            expansions += 1
            #print("EX:", expansions)
            cnt = 0
            for robot in tree.next.min_conflict.get("robots"):
                child_node = ConstraintNode()
                child_node.parent = tree.next.id
                child_node.id = tree.next.id*2 + cnt

                #Vertex conflict as new constraint
                if tree.next.min_conflict.get("type") == 0:
                    child_node.constraint.append(["vertex", robot, tree.next.min_conflict.get("node"), tree.next.min_conflict.get("step")])
                #Edge conflict as new constraint
                else:
                    if cnt == 0:
                        child_node.constraint.append(["edge", robot, tree.next.min_conflict.get("node_1"), tree.next.min_conflict.get("node_2"), tree.next.min_conflict.get("step")])
                    else:
                        child_node.constraint.append(["edge",robot, tree.next.min_conflict.get("node_2"), tree.next.min_conflict.get("node_1"), tree.next.min_conflict.get("step")])
                
                #Append constraints of parent node
                for cons in tree.next.constraint:
                    child_node.constraint.append(cons)
                
                #Append plans of parent node for non-constrained agents
                for plan in tree.next.solution.items():
                    if(plan[0]!=robot):
                        child_node.solution[plan[0]] = plan[1]

                #Update plan of the newly constrained agent
                child_node.update_solution(horizon, trans_instance, True, robot, binfo, performance_start_time, start_time, args.benchmark)

                #Calculate new SoC for the node
                child_node.calculate_cost(trans_instance)
                cnt += 1

                #Add child node to the open list
                tree.nodes.append(child_node)

            #Remove parent node from the open list
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