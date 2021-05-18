#!/usr/bin/env python3
 
# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    main.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2021/05/18 17:30:36 by tide-jon      #+#    #+#                  #
#    Updated: 2021/05/18 17:30:41 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import sys, heapq, numpy as np
from parse_args import parse_args, parse_file
from heuristics import get_heuristics, get_optimized_heuristics
from classes import Puzzle, State

#	implementation of a* algorithm:
def a_star_search(puzzle, start, args):
	openset = []
	seenset = {}
	tiebreaker = 0
	heapq.heappush(openset, (start.g + start.h_total, start.h_total, tiebreaker, start))
	seenset[start.matrix.tobytes()] = start.g
	time, space = 0, 0
	
	while len(openset) > 0:
		current = heapq.heappop(openset)[3]
		if args.verbose:
			print("current node heuristic value: ", current.h_total)
		time += 1

		if current.h_total == 0:
			if not args.uniform and args.manhattan:
				return current, time, space
			elif np.array_equal(current.matrix, puzzle.goal_array):
				return current, time, space

		for matrix, zero_loc in current.get_neighbours(puzzle):
			move = State(matrix)
			move.zero_tile = zero_loc
			move.parent = current
			get_optimized_heuristics(move, puzzle, args)
			move.g = current.g + G
			key = (move.matrix.tobytes())
			seen = key in seenset
			if not seen or move.g < seenset[key]:
				if not seen:
					space += 1
				seenset[key] = move.g
				heapq.heappush(openset, (move.g + move.h_total, move.h_total, tiebreaker, move))
				tiebreaker += 1
				
	print("can't be solved")
	exit()

def	print_path(solution, start, moves):
	if solution is not start:
		moves += 1
		moves = print_path(solution.parent, start, moves)
	print(solution.matrix, '\n')
	return moves

def	print_solution(solution, start, time, space):
	np.set_printoptions(linewidth=1000, threshold=10000, )
	moves = print_path(solution, start, 0)
	print("total moves:\t\t%10i\ntime complexity:\t%10i\nspace complexity:\t%10i" %(moves, time, space))
	exit()

if __name__ == "__main__":
	args = parse_args()
	G = not args.greedy
	shuffles_amount = 0

	if args.filepath:
		puzzle_size, start = parse_file(args.filepath)
	else:
		#	we read user input to determine the size and amount of shuffles
		puzzle_size = input("please enter the n size of an n x n puzzle:\n")
		while not puzzle_size.isdigit() or not 1 <= int(puzzle_size) <= 100:
			print("wrong input. please enter a number between 1 and 100")
			puzzle_size = input("please enter the n size of an n x n puzzle:\n")
		
		shuffles_amount = input("how many times should the puzzle be shuffled?\n")
		while not shuffles_amount.isdigit() or int(shuffles_amount) < 1:
			print("wrong input. please enter a number above 0")
			shuffles_amount = input("how many times should the puzzle be shuffled?\n")

	puzzle = Puzzle(int(puzzle_size))

	if puzzle.size == 1:
		start = goal = State(puzzle.goal_array)
		print_solution(start, goal, 1, 0)
	
	puzzle.get_goal()
	if args.filepath:
		start = State(start)
	else:
		start = State(puzzle.goal_array)
	start.zero_tile = start.find_zero()
	start = puzzle.shuffle(start, int(shuffles_amount))
	start.parent = 0
	get_heuristics(start, puzzle, args)

	#	we first check if the starting state is solvable
	if args.filepath and not start.can_be_solved(puzzle):
			print("can't be solved")
			sys.exit()

	#	execute the algorithm
	solution, time, space = a_star_search(puzzle, start, args)

	#	output
	print_solution(solution, start, time, space)
