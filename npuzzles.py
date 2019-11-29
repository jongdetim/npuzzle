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

import heapq

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
		self.neighbours = 0 #	function to generate and return neighbour states

def	manhattan_distance(state, puzzle):
	h = 0
	for y, _ in enumerate(state):
		for x, _ in enumerate(state[y]):
			y2, x2 = puzzle.goal[state[y][x]]
			h += abs(x - x2) + abs(y - y2)
	return h


#	testing

size = 3
puzzle = Puzzle(size)
puzzle.get_goal()

start_state = State([[2, 1, 3], [4, 5, 6], [7, 8, 0]], puzzle)
another_state = State([[1, 2, 3], [4, 5, 6], [7, 8, 0]], puzzle)

print (start_state.h)


#	turns 2d list into tuples to use as a dictionary key

def get_tuple(matrix):
	return tuple(tuple(line) for line in matrix)


#	implementation of a* algorithm:

def a_star_search(puzzle, start):
	openset = []
	closedset = {}
	heapq.heappush(openset, (start.g + start.h, start))
	closedset[get_tuple(start.matrix)] = start.g

	while len(openset) > 0:
		current = heapq.heappop(openset)

		if current.h == 0:
			return current

		for move in current.neighbours:
			move.g = current.g + G
			key = get_tuple(move.matrix)
			if key not in closedset or move.g < closedset[key]:
				closedset[key] = move.g
				heapq.heappush(openset, (move.g + move.h, move))
				move.parent = current

	return None
