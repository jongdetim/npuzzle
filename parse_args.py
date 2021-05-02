import argparse

def	parse_args():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
description="* npuzzle solver using a-star pathfinding *\n\nif no heuristic flags are chosen, defaults to both manhattan distance and linear conflict heuristics")

	parser.add_argument("filepath", nargs='?', help="path to input file. if none is specified, user is prompted for puzzle generation input")
	parser.add_argument("--greedy", "-g", help="find a path as fast as possible, not guaranteed to be shortest solution", action='store_true')
	parser.add_argument("--uniform", "-u", help="find the shortest path with no heuristic, only the cost", action='store_true')
	parser.add_argument("--verbose", "-v", help="show key steps in output", action='store_true')
	parser.add_argument("--misplaced", "-m", help="use the misplaced tiles heuristic (Hamming distance)", action='store_true')
	parser.add_argument("--manhattan", "-t", help="use the manhattan distance heuristic (Taxicab geometry)", action='store_true')
	parser.add_argument("--linear", "-l", help="use the linear conflict heuristic", action='store_true')
	
	args = parser.parse_args()

	# if no heuristic argument is provided, use both manhattan and linear conflict
	if True not in (args.misplaced, args.manhattan, args.linear):
		args.manhattan, args.linear = True, True
	
	return args
