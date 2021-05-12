import argparse
import sys
import numpy as np

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

def	parse_file(filepath):
	try:
		with open(filepath, 'r') as input_file:

				start = []
				puzzle_size = None
				lines = input_file.readlines()
				for n, line in enumerate(lines):
					values = []
					tokens = line.split()
					for token in tokens:
						if token[0] == '#':
							break
						if not token.isdigit():
							handle_error(SyntaxError)
						if puzzle_size == None:
							puzzle_size = int(token)
							if 0 > puzzle_size > 100:
								handle_error(ValueError)
						else:
							values.append(int(token))
					if values:
						start.append(values)
	except Exception as e:
		handle_error(e, filepath)
	
	start = np.array(start)

	# check if the matrix is the right shape
	if np.shape(start) != (puzzle_size, puzzle_size):
		handle_error(SyntaxError)

	# check if the tiles numbers are correct
	if not np.in1d(list(range(puzzle_size ** 2)), start).all():
		handle_error(SyntaxError)

	return puzzle_size, start

def	handle_error(error, filepath=None):
	if error == SyntaxError:
		print('input file is not correctly formatted')
	elif error == ValueError:
		print('puzzle size must be between 1 and 100')
	else:
		print(error, type(error))
	exit()