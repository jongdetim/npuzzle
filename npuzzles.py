# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzles.py                                        :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon       #+#    #+#                 #
#    Updated: 2019/11/26 19:44:45 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import heapq

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

def	manhattan_distance(state, puzzle):
	h = 0
	for y, _ in enumerate(state):
		for x, _ in enumerate(state[y]):
			y2, x2 = puzzle.goal[state[y][x]]
			h += abs(x - x2) + abs(y - y2)
	return h


size = 3
puzzle = Puzzle(size)
puzzle.get_goal()

start_state = State([[2, 1, 3], [4, 5, 6], [7, 8, 0]], puzzle)
another_state = State([[1, 2, 3], [4, 5, 6], [7, 8, 0]], puzzle)

print (start_state.h)

# heap tests
openset = []
heapq.heappush(openset, (start_state.h, start_state))
heapq.heappush(openset, (another_state.h, another_state))

print (heapq.heappop(openset))
print (heapq.heappop(openset))

closedset = {}

#	check to see if a state has been seen before. if not; adds state to closedset and openset

# thing = tuple(tuple(item) for item in start_state)
if not closedset.get(start_state):
	closedset[start_state] = 1
	heapq.heappush(openset, start_state.h)
