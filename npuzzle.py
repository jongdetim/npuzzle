#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzle.py                                         :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon      #+#    #+#                  #
#    Updated: 2021/04/30 19:50:07 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from random import choice
import heapq
from parse_args import *

class	Puzzle:

	def __init__(self, size):
		self.size = size
		self.goal_array = Puzzle.rotate(self.size, self.size, 1)
		self.goal = [None] * (self.size**2)

	@staticmethod
	def rotate(rows, cols, x):
		return ([list(range(x, x + cols))] + \
		[list(reversed(x)) for x in zip(*Puzzle.rotate(cols, rows - 1, x + cols))]
		if 0 < cols \
		else [[0]])

	def get_goal(self):
		for y, _ in enumerate(self.goal_array):
			for x, _ in enumerate(self.goal_array[y]):
				self.goal[self.goal_array[y][x]] = (y, x)

	def shuffle(self, state, amount):
		for _ in range(amount):
			neighbour, zero_loc = choice(state.get_neighbours())
			state = State(neighbour, self)
			state.zero_tile = zero_loc
		return state

class	State():

	def __init__(self, matrix, puzzle):
		self.matrix = matrix
		self.parent = 0
		self.h_total = 0
		self.h_misplaced = 0
		self.h_manhattan = 0
		self.h_linear = 0
		self.g = 0
		self.zero_tile = 0

	def find_zero(self):
		y = 0
		while y < len(self.matrix):
			x = 0
			while x < len(self.matrix[y]):
				if self.matrix[y][x] == 0:
					return y, x
				x += 1
			y += 1
	
	def can_be_solved(self):
		inversions = 0
		for y, _ in enumerate(self.matrix):
			for x, item in enumerate(self.matrix[y]):
				if item == 0:
					zero_row = y
					zero_col = x
				x2, y2 = x + 1, y
				while y2 < puzzle.size:
					while x2 < puzzle.size:
						if not (self.matrix[y2][x2] in puzzle.goal_array[(puzzle.goal[item])[0]][puzzle.goal[item][1]:]) \
						and not any(self.matrix[y2][x2] in row for row in puzzle.goal_array[(puzzle.goal[item])[0]+1:][:]):
							inversions += 1
						x2 += 1
					y2 += 1
					x2 = 0
		if (inversions + puzzle.size) % 2 is not (abs(puzzle.size // 2 - zero_col) + abs(puzzle.size // 2 - zero_row)) % 2:
			return True
		return False
		

 #	function to generate and return neighbour states

	def get_neighbours(self):
		y, x = self.zero_tile
		if self.parent:
			yp, xp = self.parent.zero_tile
		neighbour_coords = get_nb_coords(puzzle.size, y, x)
		neighbours = []
		zero_locs = []

		for i, _ in enumerate(neighbour_coords):
			y2, x2 = neighbour_coords[i]
			if self.parent and (y2, x2) == (yp, xp):
				continue
			neighbours.append(np.copy(self.matrix))
			
			neighbours[-1][y][x], neighbours[-1][y2][x2] = \
			self.matrix[y2][x2], self.matrix[y][x]

			zero_locs.append((y2, x2))

		return tuple(zip(neighbours, zero_locs))



# lambda calculus. --> Does it make sense to use this over a normal function?

get_nb_coords =	lambda size, y, x: \
	[(y2, x2) for y2, x2 in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
	if ((0 <= y2 < size) and
	(0 <= x2 < size))]	

#	turns 2d list into tuples to use as a dictionary key

# def get_tuple(matrix):
# 	return tuple(tuple(line) for line in matrix)

#	our heuristic functions

# def	manhattan_distance(state, puzzle):
# 	h = 0
# 	for y in range(len(state)):
# 		for x in range(len(state[y])):
# 			if state[y][x]:
# 				y2, x2 = puzzle.goal[state[y][x]]
# 				h += distance.cityblock([y2, x2],[y, x])
# 	return h

def	misplaced_tiles(matrix, goal):
	h = 0
	for y, _ in enumerate(matrix):
		for x, _ in enumerate(matrix[y]):
			num = matrix[y][x]
			if num and (y, x) != goal[num]:
				h += 1
	return h

def	misplaced_tile_single(state, goal):
	h = state.parent.h_misplaced

	# add the NEW h of last moved tile
	y, x = state.parent.zero_tile
	tile = state.matrix[y][x]
	y2, x2 = goal[tile]
	h += (y, x) != (y2, x2)

	# remove the PREVIOUS h of last moved tile
	y, x = state.zero_tile
	h -= (y, x) != (y2, x2)

	return h

def	manhattan_distance(matrix, goal):
	h = 0
	for y, _ in enumerate(matrix):
		for x, _ in enumerate(matrix[y]):
			if matrix[y][x]:
				y2, x2 = goal[matrix[y][x]]
				h += abs(x - x2) + abs(y - y2)
	return h

def manhattan_dist_single(state, goal):
	h = state.parent.h_manhattan

	# add the NEW h of last moved tile
	y, x = state.parent.zero_tile
	tile = state.matrix[y][x]
	y2, x2 = goal[tile]
	h += abs(x - x2) + abs(y - y2)

	# remove the PREVIOUS h of last moved tile
	y, x = state.zero_tile
	h -= abs(x - x2) + abs(y - y2)

	return h

def get_heuristics(state, goal):
	if not args.uniform:
		if args.misplaced:
			state.h_misplaced = misplaced_tiles(state.matrix, puzzle.goal)
		if args.manhattan:
			state.h_manhattan = manhattan_distance(state.matrix, puzzle.goal)
		if args.linear:
			pass

	state.h_total = state.h_misplaced + state.h_manhattan + state.h_linear

def	get_optimized_heuristics(state, goal):
	if not args.uniform:
		if args.misplaced:
			state.h_misplaced = misplaced_tile_single(state, goal)
		if args.manhattan:
			state.h_manhattan = manhattan_dist_single(state, puzzle.goal)
		if args.linear:
			pass

	state.h_total = state.h_misplaced + state.h_manhattan + state.h_linear


#	implementation of a* algorithm:

def a_star_search(puzzle, start):
	openset = []
	seenset = {}
	tiebreaker = 0
	heapq.heappush(openset, (start.g + start.h_total, start.h_total, tiebreaker, start))
	seenset[start.matrix.tobytes()] = start.g
	global TIME
	global SPACE
	

	while len(openset) > 0:
		current = heapq.heappop(openset)[3]
		if args.verbose and TIME > 1:
			print('current node heuristic value: ', current.h_total, ' next node: ', openset[0][3].h_total)
		TIME += 1

		if current.h_total == 0:
			if not args.uniform:
				return current
			elif array_equal(current.matrix, puzzle.goal_array):
				return current

		for matrix, zero_loc in current.get_neighbours():
			move = State(matrix, puzzle)
			move.zero_tile = zero_loc
			move.parent = current
			get_optimized_heuristics(move, puzzle.goal)
			move.g = current.g + G
			key = (move.matrix.tobytes())
			seen = key in seenset
			if not seen or move.g < seenset[key]:
				if not seen:
					SPACE += 1
				seenset[key] = move.g
				heapq.heappush(openset, (move.g + move.h_total, move.h_total, tiebreaker, move))
				tiebreaker += 1
				
	print("can't be solved")
	exit()

def	print_solution(solution, start):
	global MOVES
	if solution is not start:
		MOVES += 1
		print_solution(solution.parent, start)
	print(solution.matrix, '\n')

#___________________________________________________________________________________________________
#	testing


# start = State([[1, 3, 6], [0, 2, 8], [4, 5, 7]], puzzle)
# start = State([[1, 2, 3, 4], [12, 0, 14, 5], [11, 13, 6, 7], [10, 15, 9, 8]], puzzle)


#___________________________________________________________________________________________________
#	we read user input to determine the size and amount of shuffles

# puzzle_size = input("please enter the n size of an n x n puzzle:\n")
# while not puzzle_size.isdigit() or not 1 <= int(puzzle_size) <= 100:
# 	print("wrong input. please enter a number")
# 	puzzle_size = input("please enter the n size of an n x n puzzle:\n")
# puzzle_size = 5
# shuffles_amount = 125
# puzzle = Puzzle(int(puzzle_size))
# puzzle.get_goal()
# start = State(puzzle.goal_array, puzzle)

# shuffles_amount = input("how many times should the puzzle be shuffled?\n")
# if not shuffles_amount.isdigit():
# 	print("wrong input. please enter a number")
# 	quit()

# start.zero_tile = start.find_zero()

# start = puzzle.shuffle(start, int(shuffles_amount))

# start.parent = 0
# start.h = manhattan_distance(start.matrix, puzzle.goal)

if __name__ == '__main__':

	TIME = 0
	SPACE = 0
	MOVES = 0

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
		if not shuffles_amount.isdigit() or int(shuffles_amount) < 1:
			print("wrong input. please enter a number above 0")
			quit()

	puzzle = Puzzle(int(puzzle_size))
	puzzle.get_goal()
	if args.filepath:
		start = State(start, puzzle)
	else:
		start = State(puzzle.goal_array, puzzle)
	start.zero_tile = start.find_zero()
	start = puzzle.shuffle(start, int(shuffles_amount))
	start.parent = 0

	# puzzle = Puzzle(int(5))
	# puzzle.get_goal()
	# start = State(arr([[1,2,3,18,5],[16,22,4,6,7],[24,17,19,21,9],[15,14,11,8,10],[13,23,0,20,12]]), puzzle)
	# hell 5-puzzle
	# start = State(arr([[9,10,11,12,13],[8,21,22,23,14],[7,20,0,24,15],[6,19,18,17,16],[5,4,3,2,1]]), puzzle)

	
	#___________________________________________________________________________________________________
	#	we first check if the starting state is solvable

	if args.filepath and not start.can_be_solved():
		print("can't be solved")
		quit()

	#___________________________________________________________________________________________________
	#	execute the algorithm

	get_heuristics(start, puzzle)

	solution = a_star_search(puzzle, start)
  
	#___________________________________________________________________________________________________
	#	output

	print_solution(solution, start)

	print("total moves:\t\t%10i\ntime complexity:\t%10i\nspace complexity:\t%10i" %(MOVES, TIME, SPACE))
