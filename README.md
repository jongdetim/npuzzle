# npuzzle
A python-implemented n-puzzle solver that uses the A* algorithm.

A solved puzzle here is different from the classical solved state, see: https://en.wikipedia.org/wiki/15_puzzle<br/>
The puzzle is solved when a snail (or spiral) state is reached, with the empty tile at the end of the snail.<br/>
These are some examples of the snail solution:

![npuzzle.PNG](https://github.com/jongdetim/npuzzle/blob/master/npuzzle.PNG)

Currently the search uses the Manhattan Distance heuristic to estimate the distance to the goal, and a uniform cost of 1 per additional move.

At the end of the search, the program prints the following:<br/>
1. The ordered sequence of states that make up the solution, according to the search
2. Total number of states ever selected in the "opened" set (complexity in time)
3. Maximum number of states ever represented in memory at the same time during the search (complexity in size)
4. Number of moves required to transition from the initial state to the final state, according to the search<br/>
! The puzzle may be unsolvable, in which case it prints such and exits.


**Possible improvements:**

- Take user input to determine the puzzle starting position
- Implement a scrambler to create random starting positions
- Replace array structures for NumPy arrays for better memory and time usage
- Implement alternative (admissible) heuristics, such as inverse distance, euclidian distance, walking distance
- Use iterative deepening with the A* algorithm to reduce space complexity considerably
