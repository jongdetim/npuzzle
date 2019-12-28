# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    npuzzles.py                                        :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2019/11/25 13:33:51 by tide-jon       #+#    #+#                 #
#    Updated: 2019/12/28 22:31:55 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from numpy import matrix as printmatrix

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
						if self.state[y2][x2] \
						and not (self.state[y2][x2] in puzzle.goal_array[(puzzle.goal[item])[0]][puzzle.goal[item][1]:]) \
						and not any(self.state[y2][x2] in row for row in puzzle.goal_array[(puzzle.goal[item])[0]+1:][:]):
							inversions += 1
						x2 += 1
					y2 += 1
					x2 = 0
				print (item, inversions)
		if (puzzle.size % 2 == 1 and (inversions % 2 is (abs(puzzle.size // 2 - zero_col) + abs(puzzle.size // 2 - zero_row)) % 2 or \
			(puzzle.size % 2 == 0 and inversions % 2 is not abs(zero_col - (puzzle.goal[0])[1]) % 2))):
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
			if state[y][x] is not 0:
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

	print ("can't be solved")
	return None

def	print_solution(solution, start):
	global MOVES
	if solution is not start:
		MOVES += 1
		print_solution(solution.parent, start)
	print (printmatrix(solution.state))
	print ()


#	testing

puzzle = Puzzle(5)
puzzle.get_goal()
# start = State([[2, 1, 3], [4, 5, 6], [7, 0, 8]], puzzle)
# start = State([[1, 2, 3, 4], [12, 14, 5, 0], [11, 13, 15, 6], [10, 9, 8, 7]], puzzle)
start = State([[1,2,3,18,5],[16,17,22,4,6],[15,24,19,21,7],[14,11,0,20,8],[13,23,12,10,9]], puzzle)

#	we first check if the starting state is solveable

if not start.can_be_solved():
	print ("can't be solved")
	quit()

#	execute the algorithm

solution = a_star_search(puzzle, start)


#	output

# while solution is not start:
# 	print (printmatrix(solution.state))
# 	MOVES += 1
# 	solution = solution.parent
print_solution(solution, start)
# print (np.matrix(solution.state))
print ("total moves:\t\t%10i\ntime complexity:\t%10i\nspace complexity:\t%10i" %(MOVES, TIME, SPACE))
