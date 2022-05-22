import clingo, argparse

from numpy import full

from node import ConstraintNode
from instance import ClingoInstance
from tree import ConstraintTree

def run(args):

    #Benchmarking timer probably starts here

    trans_instance = ClingoInstance()
    tree = ConstraintTree()
    horizon = args.horizon

    # Load instance and transform input
    ctl = clingo.Control()
    ctl.load(args.instance)
    ctl.load("encodings/input.lp")
    ctl.ground([("base", [])])
    ctl.solve(on_model= lambda m: trans_instance.on_model_load_input(m))

    root_node = ConstraintNode(1,0,{},{},0)
    root_node.solve(horizon, trans_instance)
    tree.add_node(root_node)

    # TODO: Start the loop


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--instance", help="Instance that should be solved. Asprilo Input format is required", required=True)
parser.add_argument("-o", "--horizon", help="The upper bound for the solution, as in maximum number of steps for a single agent.", type=int)

args = parser.parse_args()