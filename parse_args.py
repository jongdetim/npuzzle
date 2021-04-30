import argparse

def	parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument("--greedy", "-g", help="find a path as fast as possible, not guaranteed to be shortest solution", action='store_true')
	parser.add_argument("--verbose", "-v", help="show key steps in output", action='store_true')
	parser.add_argument("--misplaced", "-m", help="use the misplaced tiles heuristic (Hamming distance)", action='store_true')
	parser.add_argument("--manhattan", "-t", help="use the manhattan distance heuristic (Taxicab geometry)", action='store_true')
	parser.add_argument("--linear", "-l", help="use the linear conflict heuristic", action='store_true')
	args = parser.parse_args()

	greedy = args.greedy
	verbose = args.verbose
	misplaced = args.misplaced
	manhattan = args.manhattan
	linear_conflict = args.linear

	# if no heuristic argument is provided, use both manhattan and linear conflict
	if True not in (misplaced, manhattan, linear_conflict):
		manhattan, linear_conflict = True, True
	
	return greedy, verbose, misplaced, manhattan, linear_conflict
