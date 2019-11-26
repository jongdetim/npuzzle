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

	def __init__(self, size, state):
		self.size = size
		self.state = state

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

# 	OpenSet
# 	ClosedSet


def	manhattan_distance(puzzle):
	h = 0
	for y, _ in enumerate(puzzle.state):
		for x, _ in enumerate(puzzle.state[y]):
			y2, x2 = puzzle.goal[puzzle.state[y][x]]
			h += abs(x - x2) + abs(y - y2)
	return h

size = 3

state = [[2, 1, 3], [4, 5, 6], [7, 8, 0]]
puzzle = Puzzle(size, state)
puzzle.get_goal()

print (manhattan_distance(puzzle))

# heap tests
heap = []
heapq.heappush(heap, (manhattan_distance(puzzle), puzzle.state))
heapq.heappush(heap, (12, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]))

print (heapq.heappop(heap))
print (heapq.heappop(heap))