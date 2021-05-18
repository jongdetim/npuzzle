# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    heuristics.py                                      :+:    :+:             #
#                                                      +:+                     #
#    By: tide-jon <tide-jon@student.codam.nl>         +#+                      #
#                                                    +#+                       #
#    Created: 2021/05/18 17:40:11 by tide-jon      #+#    #+#                  #
#    Updated: 2021/05/18 17:40:17 by tide-jon      ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import numpy as np

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

def	line_conflict(linenum, line, puzzle, goal_func):
	conflicts = 0
	conflict_graph = {}
	# print(line)
	for i, tile in enumerate(line):
		if tile == 0:
			continue
		y, x = goal_func(puzzle.goal, tile)
		if linenum != y:
			continue
		
		for j in range(i + 1, puzzle.size):
			other_tile = line[j]
			if other_tile == 0:
				continue
			y2, x2 = goal_func(puzzle.goal, other_tile)
			# if conflict; add to conflict graph
			if y2 == y and x2 <= x:
				tile_degree, tile_nbrs = conflict_graph.get(tile) or (0, set())
				tile_nbrs.add(other_tile)
				conflict_graph[tile] = (tile_degree + 1, tile_nbrs)
				other_tile_degree, other_tile_nbrs = conflict_graph.get(other_tile) or (0, set())
				other_tile_nbrs.add(tile)
				conflict_graph[other_tile] = (other_tile_degree + 1, other_tile_nbrs)

	# clear out graph from max conflict to lower until it's empty
	while sum([other_tile[0] for other_tile in conflict_graph.values()]) > 0:
		popped = max(conflict_graph.keys(), key=lambda k: conflict_graph[k][0])
		for neighbour in conflict_graph[popped][1]:
			degree, nbtiles = conflict_graph[neighbour]
			nbtiles.remove(popped)
			conflict_graph[neighbour] = (degree - 1, nbtiles)
			conflicts += 1
		conflict_graph.pop(popped)

	return conflicts

def	row_goal(goal, tile):
	return goal[tile]

def	col_goal(goal, tile):
	return goal[tile][::-1]

def	linear_conflict(state, puzzle):
	h = 0
	# rows
	for y, row in enumerate(state.matrix):
		h += 2 * line_conflict(y, row, puzzle, row_goal)

	# columns
	for x, column in enumerate(np.transpose(state.matrix)):
		h += 2 * line_conflict(x, column, puzzle, col_goal)

	return h

def	linear_conflict_single(state, puzzle):
	h = state.parent.h_linear
	y, x = state.zero_tile
	y2, x2 = state.parent.zero_tile
	tile = state.matrix[y2][x2]
	y_goal, x_goal = puzzle.goal[tile]
	if y == y2:
		# horizontal move
		if x2 == x_goal or x == x_goal:
			line = state.matrix[:,x_goal]
			h += 2 * line_conflict(x_goal, line, puzzle, col_goal)
			line = state.parent.matrix[:,x_goal]
			h -= 2 * line_conflict(x_goal, line, puzzle, col_goal)
	elif x == x2:
		# vertical move
		if y2 == y_goal or y == y_goal:
			line = state.matrix[y_goal]
			h += 2 * line_conflict(y_goal, line, puzzle, row_goal)
			line = state.parent.matrix[y_goal]
			h -= 2 * line_conflict(y_goal, line, puzzle, row_goal)
	return h


def get_heuristics(state, puzzle, args):
	if not args.uniform:
		if args.misplaced:
			state.h_misplaced = misplaced_tiles(state.matrix, puzzle.goal)
		if args.manhattan:
			state.h_manhattan = manhattan_distance(state.matrix, puzzle.goal)
		if args.linear:
			state.h_linear = linear_conflict(state, puzzle)

	state.h_total = state.h_misplaced + state.h_manhattan + state.h_linear

def	get_optimized_heuristics(state, puzzle, args):
	if not args.uniform:
		if args.misplaced:
			state.h_misplaced = misplaced_tile_single(state, puzzle.goal)
		if args.manhattan:
			state.h_manhattan = manhattan_dist_single(state, puzzle.goal)
		if args.linear:
			state.h_linear = linear_conflict_single(state, puzzle)

	state.h_total = state.h_misplaced + state.h_manhattan + state.h_linear
