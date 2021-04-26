import argparse

manhattan, linear = False, False

parser = argparse.ArgumentParser()

parser.add_argument("--verbose", "-v", help="show key steps in output", action='store_true')
parser.add_argument("--manhattan", "-m", help="use the manhattan distance heuristic", action='store_true')
parser.add_argument("--linear", "-l", help="use the linear conflict heuristic", action='store_true')
args = parser.parse_args()

if args.verbose:
	print('verbose mode')

manhattan = args.manhattan
linear_conflict = args.linear
# dumb = args.dumb

# if no heuristic argument is provided, use both manhattan and linear conflict
if True not in (manhattan, linear_conflict):
	manhattan, linear_conflict = True, True