import heapq
from collections import deque
import pandas as pd
import numpy as np

import time




initial_matrix = [[('a', 1), ('a', 7), ('a', 2), ('b', 5), ('o', 4), ('a', 3), ('a', 10), ('a', 9), ('o', 5), ('b', 6)], [('a', 8), ('a', 5), ('b', 8), ('o', 2), ('b', 4), ('o', 6), ('a', 4), ('o', 3), ('o', 9), ('a', 6)], [('o', 1), ('b', 7), ('o', 8), ('b', 1), ('o', 10), ('b', 2), ('b', 3), ('b', 9), ('b', 10), ('o', 7)]]



fruits = ['a', 'b', 'o']

# Recursive function to generate 6 fruit combinations
def generate_fruit_order(combination, index, fruit_order):
    if index == 3:
        fruit_order.append(''.join(combination))
        return

    for fruit in fruits:
        if fruit not in combination:
            combination.append(fruit)
            generate_fruit_order(combination, index + 1, fruit_order)
            combination.pop()

combination = []
fruit_order = []
generate_fruit_order(combination, 0, fruit_order)
    


# this method estimates the right position in a vertical direction 
def estimate_position(initial_matrix):
    values = []
    
    for f in fruits:
        value = [element[1] for row in initial_matrix for element in row if element[0] == f]
        values.append(value)
    positions = {}
    for col in range(10):
        for row in range(3):
            fruit = initial_matrix[row][col][0]
            fruit_type = fruits.index(fruit)
            num = sum(1 for x in values[fruit_type] if x <= initial_matrix[row][col][1]) - 1
            positions.update({initial_matrix[row][col] : num})
    

    return positions







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
    def __init__(self, matrix,fruit_order_i, parent=None, move=None, path=(), g=0):
        self.matrix = matrix
        self.parent = parent
        self.path = path
        self.move = move
        self.g = g
        self.h = self.heuristic(fruit_order_i)
        self.f = self.g + self.h
        

    def __lt__(self, other):
        return self.f < other.f
    
    # this method shows the board
    def show_board(self, i):
        print(fruit_order[i])
        for i in range(10):
            print(i, end = " ")
            for j in range(len(self.matrix)):
                print(self.matrix[j][i][0] + str(self.matrix[j][i][1]) , end = " ")
            print('\n')


    # this method finds the distance till the correct position for all cells in board, and returns it as a heuristic value
    def heuristic(self, fruit_order_i):
        misplaced_fruits = 0
        for col in range(10):
            for row in range(3):
                fruit = self.matrix[row][col][0]
                value = self.matrix[row][col][1]
                s1 = right_positions[self.matrix[row][col]]
                misplaced_fruits += abs(col - s1)
                fruit_order_v1 = fruit_order[fruit_order_i].index(fruit)
                
                act_o_v1 = row                 
                
                if fruit_order_v1 != act_o_v1:
                    misplaced_fruits += (abs(fruit_order_v1 - act_o_v1))
                    
        return misplaced_fruits
    
    # this method checks if the board reached the target value
    def is_goal(self, fruit_order_i):
        return self.heuristic(fruit_order_i) == 0
    
    # this method swaps 2 cells and creates new board 
    def swap(self, x1, y1, x2, y2, fruit_order_i):
        new_matrix = [row.copy() for row in self.matrix]
        new_matrix[x1][y1], new_matrix[x2][y2] = new_matrix[x2][y2], new_matrix[x1][y1]
        return State(new_matrix, fruit_order_i, parent=self, move=((x1, y1), (x2, y2)), path =self.path + (((x1, y1), (x2, y2)), ), g=self.g + 1)
    
    # this method generates next moves
    def get_neighbors(self, fruit_order_i):
        neighbors = []
        for sp in pm:
            new = self.swap(sp[0][0], sp[0][1], sp[1][0], sp[1][1], fruit_order_i)
            if new.h <= self.h:
                neighbors.append(new)
        return neighbors

start_time = time.time()
right_positions = estimate_position(initial_matrix)
sorted_versions = []

# generates 6 versions of sorted array for each combination
# because of good heuristic 1 iteration takes 1-2 seconds, so calculation of 6 combinations takes 6-15 seconds 
for fruit_order_i in range(6):
    
    initial_state = State(initial_matrix, fruit_order_i)
    if fruit_order_i == 0:
        print("Initial state")
        initial_state.show_board(fruit_order_i)
    open_list = [(initial_state.f, initial_state.h, initial_state)]

    closed_list = set()
    closed_pathes = set()
    counter = 0
    while open_list:
        counter+=1
        # all next steps are saved in open_list. New move is taken from it
        current_state = heapq.heappop(open_list)[2]
        
        # if counter % 10 == 0:
        #     print(current_state.move,current_state.g, current_state.h, counter,'\n')
            
        #     current_state.show_board(fruit_order_i)            
        #     print('\n')
 
        
    
        if current_state.is_goal(fruit_order_i):
            print('SORTED', end = " ")
            print(f'It took {len(current_state.path)} swaps for {fruit_order[fruit_order_i]} combination')
            break
    
        # generates possible moves
        neighbors =  current_state.get_neighbors(fruit_order_i)
    
        # here it chooses next move from possible moves
        for neighbor in neighbors:
            # here it checks if the new board is in closed_list, if so it checks other moves
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
    current_state.show_board(fruit_order_i)
    sorted_versions.append(current_state)

    
print("iterations:", counter)
print("--- %s seconds ---" % (time.time() - start_time))

min_swaps = 100000000
best_state = ''
best_fruit_order = 0
best_fruit_orders = []
c = 0

# it picks the one with minimum swaps among all 6 sorted versions of initial array. 
print("BEST STATES:")
for state in sorted_versions:
    # print(len(state.path))
    if len(state.path) <= min_swaps:
        best_state = state
        best_fruit_order = c
        min_swaps = len(state.path) 
    c+=1
    
    

print('number_of_swaps=', len(best_state.path))
best_state.show_board(best_fruit_order)
    
print()


