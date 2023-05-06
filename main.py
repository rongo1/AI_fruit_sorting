import heapq
from collections import deque
import pandas as pd
import numpy as np

import time



data_frame = pd.read_csv('a4.csv', sep = ';', header=None)

initial_matrix = [[('b', 4), ('o', 4), ('a', 1), ('a', 5), ('o', 2), ('b', 6), ('b', 8), ('o', 3), ('o', 6), ('o', 9)], [('a', 9), ('b', 7), ('o', 10), ('a', 3), ('b', 5), ('a', 4), ('a', 2), ('o', 5), ('o', 8), ('o', 1)], [('a', 10), ('o', 7), ('a', 7), ('a', 8), ('b', 2), ('b', 10), ('b', 9), ('b', 3), ('a', 6), ('b', 1)]]

# this method counts fruits and decided in which column which fruit should be. 
# It estimates the right column of fruit
def count_fruits(m):
    a = []
    fruits = ['b', 'a', 'o']
    for row in m:
        counts = {'b': 0, 'a': 0, 'o': 0}
        for letter, _ in row:
            counts[letter] += 1
        a.append(counts)
    # print("a", a)
    keys = []
    for d in a:
        if max(d, key=d.get) not in keys:
            keys.append(max(d, key=d.get))
        else:
            for f in fruits:
                if f not in keys:
                    keys.append(f)
                    break
            
    return keys
fruit_order = count_fruits(initial_matrix)

# this method estimates the right position in a vertical direction 
def estimate_position(initial_matrix):
    values = []
    
    for f in fruit_order:
        value = [element[1] for row in initial_matrix for element in row if element[0] == f]
        values.append(value)
    positions = {}
    for col in range(10):
        for row in range(3):
            fruit = initial_matrix[row][col][0]
            fruit_type = fruit_order.index(fruit)
            num = sum(1 for x in values[fruit_type] if x <= initial_matrix[row][col][1]) - 1
            positions.update({initial_matrix[row][col] : num})
    

    return positions
right_positions = estimate_position(initial_matrix)






# this method geneartes all the possible values 
def genrate_possible_moves(m):
    rows = range(0, len(m[0]))
    cols = range(0, len(m))
    possible_moves = []
    for i in cols:
        for j in range(len(rows) - 1):
            possible_swaps = ((i, j), (i, j + 1))
            possible_moves.append(possible_swaps)
    for j in rows:
        for i in range(len(cols) - 1):
            possible_swaps = ((i, j), (i + 1, j))
            possible_moves.append(possible_swaps)
    return possible_moves

pm = genrate_possible_moves(initial_matrix)

class State:
    def __init__(self, matrix, parent=None, move=None, path=(), g=0):
        self.matrix = matrix
        self.parent = parent
        self.path = path
        self.move = move
        self.g = g
        self.h = self.heuristic()
        self.f = self.g + self.h
        

    def __lt__(self, other):
        return self.f < other.f
    
    # this method shows the board
    def show_board(self):
        print(fruit_order)
        for i in range(10):
            print(i, end = " ")
            for j in range(len(self.matrix)):
                print(self.matrix[j][i][0] + str(self.matrix[j][i][1]) , end = " ")
            print('\n')


    # this method finds the distance till the correct position for the all cells in board, and returns heuristic value
    def heuristic(self):
        misplaced_fruits = 0
        for col in range(10):
            for row in range(3):
                fruit = self.matrix[row][col][0]
                value = self.matrix[row][col][1]
                s1 = right_positions[self.matrix[row][col]]
                misplaced_fruits += abs(col - s1)
                fruit_order_v1 = fruit_order.index(fruit)
                act_o_v1 = row                 
                if fruit_order_v1 != act_o_v1:
                    misplaced_fruits += (abs(fruit_order_v1 - act_o_v1))
        return misplaced_fruits
    
    # this method checks if the board reached the target value
    def is_goal(self):
        return self.heuristic() == 0
    
    # this method swaps 2 cells 
    def swap(self, x1, y1, x2, y2):
        new_matrix = [row.copy() for row in self.matrix]
        new_matrix[x1][y1], new_matrix[x2][y2] = new_matrix[x2][y2], new_matrix[x1][y1]
        return State(new_matrix, parent=self, move=((x1, y1), (x2, y2)), path =self.path + (((x1, y1), (x2, y2)), ), g=self.g + 1)
    
    # this nethod generates next moves
    def get_neighbors(self):
        neighbors = []
        for sp in pm:
            new = self.swap(sp[0][0], sp[0][1], sp[1][0], sp[1][1])
            if new.h <= self.h:
                neighbors.append(new)
        return neighbors

start_time = time.time()
initial_state = State(initial_matrix)

initial_state.show_board()
open_list = [(initial_state.f, initial_state.h, initial_state)]

closed_list = set()
closed_pathes = set()
counter = 0


while open_list:
    # all next steps are saved in open_list. New move is taken from it
    current_state = heapq.heappop(open_list)[2]

    counter+=1

    if current_state.is_goal():
        print('SORTED')
        break

    # generates possible moves
    neighbors =  current_state.get_neighbors()

    # here it checks if the new board is in closed_list
    for neighbor in neighbors:
        matrix_tuple = tuple(map(tuple, neighbor.matrix))
        if matrix_tuple in closed_list:
            continue
        
        in_open_list = False
        for s in open_list:
            if neighbor.matrix == s[2].matrix and neighbor.g >= s[2].g:
                in_open_list = True
                break
        
        # it adds new board to open_list and current one to closed_list
        if not in_open_list:
            heapq.heappush(open_list, (neighbor.h, neighbor.f, neighbor))
            closed_list.add(tuple(map(tuple, current_state.matrix)))

    

current_state.show_board()
print("iterations:", counter)
print("moves:", len(current_state.path))
print("--- %s seconds ---" % (time.time() - start_time))


