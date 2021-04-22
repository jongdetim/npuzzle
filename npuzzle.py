# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzles.py                                        :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon       #+#    #+#                 #
#    Updated: 2019/12/28 23:03:41 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from numpy import matrix as printmatrix
from random import choice

from scipy.spatial import distance
import timeit

import heapq
import copy

#	move cost G
G = 1

#	performance tracking
TIME = 0
SPACE = 0
MOVES = 0

class	Puzzle:

	def __init__(self, size):
		self.size = size

	@staticmethod
	def rotate(rows, cols, x):
		return ([list(range(x, x + cols))] + \
		[list(reversed(x)) for x in zip(*Puzzle.rotate(cols, rows - 1, x + cols))]
		if 0 < cols \
		else [[0]])

	def get_goal(self):
		self.goal_array = Puzzle.rotate(self.size, self.size, 1)
		self.goal = [None] * (self.size**2)
		for y, _ in enumerate(self.goal_array):
			for x, _ in enumerate(self.goal_array[y]):
				self.goal[self.goal_array[y][x]] = (y, x)

	def shuffle(self, state, amount):
		for _ in range(amount):
			state = State(choice(state.get_neighbours()), self)
		return state

class	State():

	def __init__(self, matrix, puzzle):
		self.state = matrix
		self.parent = 0
		self.h = manhattan_distance(matrix, puzzle)
		self.g = 0

	def find_zero(self):
		y = 0
		while y < len(self.state):
			x = 0
			while x < len(self.state[y]):
				if self.state[y][x] == 0:
					return y, x
				x += 1
			y += 1
	
	def can_be_solved(self):
		inversions = 0
		for y, _ in enumerate(self.state):
			for x, item in enumerate(self.state[y]):
				if item == 0:
					zero_row = y
					zero_col = x
				x2, y2 = x + 1, y
				while y2 < puzzle.size:
					while x2 < puzzle.size:
						if not (self.state[y2][x2] in puzzle.goal_array[(puzzle.goal[item])[0]][puzzle.goal[item][1]:]) \
						and not any(self.state[y2][x2] in row for row in puzzle.goal_array[(puzzle.goal[item])[0]+1:][:]):
							inversions += 1
						x2 += 1
					y2 += 1
					x2 = 0
		if inversions % 2 + puzzle.size % 2 is not (abs(puzzle.size // 2 - zero_col) + abs(puzzle.size // 2 - zero_row)) % 2:
			return True
		return False
		

 #	function to generate and return neighbour states
 #	<replace array structures for NumPy arrays for better memory and time usage>

	def get_neighbours(self):
		y, x = self.find_zero()
		if self.parent:
			yp, xp = self.parent.find_zero()
		neighbour_coords = get_nb_coords(puzzle.size, y, x)
		neighbours = []

		for i in range(len(neighbour_coords)):
			y2, x2 = neighbour_coords[i]
			if self.parent and (y2, x2) == (yp, xp):
				continue
			neighbours.append(copy.deepcopy(self.state))
			neighbours[-1][y][x], neighbours[-1][y2][x2] = \
			self.state[y2][x2], self.state[y][x]

		return neighbours



# lambda calculus. --> Does it make sense to use this over a normal function?

get_nb_coords =	lambda size, y, x: \
	[(y2, x2) for y2, x2 in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
	if ((0 <= y2 < size) and
	(0 <= x2 < size))]	

#	turns 2d list into tuples to use as a dictionary key

def get_tuple(matrix):
	return tuple(tuple(line) for line in matrix)

#	our heuristic function

# def	manhattan_distance(state, puzzle):
# 	h = 0
# 	for y in range(len(state)):
# 		for x in range(len(state[y])):
# 			if state[y][x]:
# 				y2, x2 = puzzle.goal[state[y][x]]
# 				h += distance.cityblock([y2, x2],[y, x])
# 	return h


def	manhattan_distance(state, puzzle):
	h = 0
	for y in range(len(state)):
		for x in range(len(state[y])):
			if state[y][x]:
				y2, x2 = puzzle.goal[state[y][x]]
				h += abs(x - x2) + abs(y - y2)
	return h

#	implementation of a* algorithm:

def a_star_search(puzzle, start):
	openset = []
	seenset = {}
	heapq.heappush(openset, (start.g + start.h, id(start), start))
	seenset[get_tuple(start.state)] = start.g
	global TIME
	global SPACE

	while len(openset) > 0:
		current = heapq.heappop(openset)[2]
		TIME += 1

		if current.h == 0:
			return current

		for matrix in current.get_neighbours():
			move = State(matrix, puzzle)
			move.g = current.g + G
			key = get_tuple(move.state)
			if key not in seenset or move.g < seenset[key]:
				if key not in seenset:
					SPACE += 1
				seenset[key] = move.g
				heapq.heappush(openset, (move.g + move.h, key, move))
				move.parent = current

	print("can't be solved")
	return None

def	print_solution(solution, start):
	global MOVES
	if solution is not start:
		MOVES += 1
		print_solution(solution.parent, start)
	print(printmatrix(solution.state))
	print()

#___________________________________________________________________________________________________
#	testing


# start = State([[1, 3, 6], [0, 2, 8], [4, 5, 7]], puzzle)
# start = State([[1, 2, 3, 4], [12, 0, 14, 5], [11, 13, 6, 7], [10, 15, 9, 8]], puzzle)


#___________________________________________________________________________________________________
#	we read user input to determine the size and amount of shuffles

# puzzle_size = input("please enter the n size of an n x n puzzle:\n")
# if not puzzle_size.isdigit():
# 	print("wrong input. please enter a number")
# 	quit()
puzzle = Puzzle(5)
puzzle.get_goal()
# start = State(puzzle.goal_array, puzzle)

# shuffles_amount = input("how many times should the puzzle be shuffled?\n")
# if not shuffles_amount.isdigit():
# 	print("wrong input. please enter a number")
# 	quit()
# start = puzzle.shuffle(start, int(shuffles_amount))

start = State([[1,2,3,18,5],[16,22,4,6,7],[24,17,19,21,9],[15,14,11,8,10],[13,23,20,0,12]], puzzle)

#___________________________________________________________________________________________________
#	we first check if the starting state is solveable

if not start.can_be_solved():
	print("can't be solved")
	quit()

#___________________________________________________________________________________________________
#	execute the algorithm

solution = a_star_search(puzzle, start)

#___________________________________________________________________________________________________
#	output

print_solution(solution, start)

print("total moves:\t\t%10i\ntime complexity:\t%10i\nspace complexity:\t%10i" %(MOVES, TIME, SPACE))
