# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzle.py                                         :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon       #+#    #+#                 #
#    Updated: 2020/01/13 16:21:37 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from numpy import matrix as printmatrix
from random import choice

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

	def get_goal(self):
		def rotate(rows, cols, x):
			return ([list(range(x, x + cols))] + \
			[list(reversed(x)) for x in zip(*rotate(cols, rows - 1, x + cols))]
			if 0 < cols \
			else [[0]])
		self.goal_array = rotate(self.size, self.size, 1)
		self.goal = {}
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
		if (inversions + puzzle.size) % 2 is not (abs(puzzle.size // 2 - zero_col) + abs(puzzle.size // 2 - zero_row)) % 2:
			return True
		return False
		

 #	function to generate and return neighbour states
 #	<replace array structures for NumPy arrays for better memory and time usage>

	def get_neighbours(self):
		y, x = self.find_zero()
		neighbour_coords = get_nb_coords(puzzle.size, y, x)
							
		neighbours = [copy.deepcopy(self.state) for _ in neighbour_coords]
		for i in range(len(neighbour_coords)):
			y2, x2 = neighbour_coords[i]
			neighbours[i][y][x], neighbours[i][y2][x2] = \
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

def	manhattan_distance(state, puzzle):
	h = 0
	for y, _ in enumerate(state):
		for x, _ in enumerate(state[y]):
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
				heapq.heappush(openset, (move.g + move.h, id(move), move))
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
#	we read user input to determine the size and amount of shuffles

game_type = input("choose '1' to randomly shuffle the puzzle, or choose '2' to set the puzzle state manually\n")
while not game_type == '1' and not game_type == '2':
	game_type = input("wrong input. please enter either 1 or 2:\n")
puzzle_size = input("please enter the n size of an n x n puzzle:\n")
while not puzzle_size.isdigit():
	puzzle_size = input("wrong input. please enter a number:\n")
puzzle = Puzzle(int(puzzle_size))
puzzle.get_goal()
if game_type == '1':
	start = State(puzzle.goal_array, puzzle)
	shuffles_amount = input("how many times should the puzzle be shuffled?\n")
	while not shuffles_amount.isdigit():
		shuffles_amount = input("wrong input. please enter a number\n")
	start = puzzle.shuffle(start, int(shuffles_amount))
else:
	print("please input your puzzle state, piece by piece from top left to bottomright:")
	arr = [[] for i in range(int(puzzle_size))]
	row = 0
	for i in range(int(puzzle_size) ** 2):
		piece = input()
		while not piece.isdigit():
			piece = puzzle_size = input("wrong input. please enter a number:\n")
		arr[row].append(int(piece))
		if (i + 1) % int(puzzle_size) == 0:
			row += 1
	start = State(arr, puzzle)

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
