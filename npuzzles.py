# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzles.py                                        :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon       #+#    #+#                 #
#    Updated: 2019/11/29 19:22:49 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import numpy as np

import heapq
import copy

#	move cost G
G = 1

class	Puzzle():

	def __init__(self, size):
		self.size = size

	def get_goal(self):
		def rotate(rows, cols, x):
			return ([list(range(x, x + cols))] + \
			[list(reversed(x)) for x in zip(*rotate(cols, rows - 1, x + cols))]
			if 0 < cols \
			else [[0]])
		goal_array = rotate(self.size, self.size, 1)
		self.goal = {}
		for y, _ in enumerate(goal_array):
			for x, _ in enumerate(goal_array[y]):
				self.goal[goal_array[y][x]] = (y, x)


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
			y2, x2 = puzzle.goal[state[y][x]]
			h += abs(x - x2) + abs(y - y2)
	return h

#	implementation of a* algorithm:

def a_star_search(puzzle, start):
	openset = []
	closedset = {}
	heapq.heappush(openset, (start.g + start.h, id(start), start))
	closedset[get_tuple(start.state)] = start.g

	while len(openset) > 0:
		current = heapq.heappop(openset)[2]

		if current.h == 0:
			return current
		
		if current is not start and current.parent.h == 2: # this only works with the manhattan distance heuristic
			print ("can't be solved")
			return None

		for matrix in current.get_neighbours():
			move = State(matrix, puzzle)
			move.g = current.g + G
			key = get_tuple(move.state)
			if key not in closedset or move.g < closedset[key]:
				closedset[key] = move.g
				heapq.heappush(openset, (move.g + move.h, id(move), move))
				move.parent = current

		# print (np.matrix(current.state))

	print ("can't be solved")
	return None


#	testing

size = 4
puzzle = Puzzle(size)
puzzle.get_goal()

start_state = State([[2, 1, 3], [4, 5, 6], [7, 0, 8]], puzzle)
another_state = State([[0, 2, 1, 4], [12, 13, 3, 5], [11, 15, 14, 8], [10, 9, 7, 6]], puzzle)

test = a_star_search(puzzle, another_state)
if not test == None:
	print (np.matrix(test.state))
