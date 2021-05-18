# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    classes.py                                         :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2021/05/18 17:40:10 by tide-jon      #+#    #+#                  #
#    Updated: 2021/05/18 17:40:18 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from random import choice
import numpy as np

class	Puzzle:

	def __init__(self, size):
		self.size = size
		self.goal_array = np.array(Puzzle.rotate(self.size, self.size, 1), dtype=np.uint16)
		self.goal = [None] * (self.size**2)

	@staticmethod
	def rotate(rows, cols, x):
		if rows == 1 and cols == 1:
			return [[0]]
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
			neighbour, zero_loc = choice(state.get_neighbours(self))
			state = State(neighbour)
			state.zero_tile = zero_loc
		return state

class	State():

	def __init__(self, matrix):
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
	
	def can_be_solved(self, puzzle):
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

	def get_neighbours(self, puzzle):
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

get_nb_coords =	lambda size, y, x: \
	[(y2, x2) for y2, x2 in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
	if ((0 <= y2 < size) and
	(0 <= x2 < size))]
