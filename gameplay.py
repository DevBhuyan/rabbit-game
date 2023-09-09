#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 19:22:20 2023

@author: dev
"""

import numpy as np
from random import randint
import os
import sys
import time

class Board:
    def __init__(self, a=10, n_car=5, n_hol=5):
        self.grid = np.full((a, a), "-", dtype=str)
        pos = divmod(randint(0, a * a - 1), a)
        for i in range(n_car):
            while self.grid[pos] != "-":
                pos = divmod(randint(0, a * a - 1), a)
            self.grid[pos] = "c"
        for i in range(n_hol):
            while self.grid[pos] != "-":
                pos = divmod(randint(0, a * a - 1), a)
            self.grid[pos] = "o"


class Rabbit():
    def __init__(self):
        global board
        
        a = len(board.grid)
        pos = divmod(randint(0, a * a - 1), a)
        while board.grid[pos] != "-":
            pos = divmod(randint(0, a * a - 1), a)
        self.pos = pos
        self.state = 0  # 0 if empty, 1 if holding carrot

    def is_valid_move(self, new_pos):
        global board
        
        a = len(board.grid)
        if 0 <= new_pos[0] < a and 0 <= new_pos[1] < a and (board.grid[new_pos[0], new_pos[1]] not in ["c", "o"]):
                return True
        return False
    
    def moves(self):
        return {
            "a": (0, -1),
            "d": (0, 1),
            "w": (-1, 0),
            "s": (1, 0),
            "wa": (-1, -1),
            "wd": (-1, 1),
            "sa": (1, -1),
            "sd": (1, 1),
            "aw": (-1, -1),
            "dw": (-1, 1),
            "as": (1, -1),
            "ds": (1, 1),
        }
    
    def move(self, direction):
        # TODO: Diagonals
        global board
        
        moves = self.moves()

        new_pos = (self.pos[0] + moves[direction][0], self.pos[1] + moves[direction][1])

        if self.is_valid_move(new_pos):
            board.grid[self.pos] = "-"
            self.pos = new_pos
        
    def pick_n_drop_carrot(self):
        # FIXME: Test this
        global board
        
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                try:
                    if board.grid[self.pos[0] + i, self.pos[1] + j] == "c" and self.state == 0 and (i or j):
                        self.state = 1
                        board.grid[self.pos[0] + i][self.pos[1] + j] = "-"
                        return 0
                    if board.grid[self.pos[0] + i, self.pos[1] + j] == "o" and self.state == 1 and (i or j):
                        self.state = 0
                        board.grid[self.pos[0] + i][self.pos[1] + j] = "O"
                        return 1   # Game Over trigger
                except:
                    pass

    def jump_over_hole(self):
        global board
        
        if not self.state:
            for i in [-1, 1]:
                if board.grid[self.pos[0]][self.pos[1] + i] == "o":
                    new_pos = (self.pos[0], self.pos[1] + 2*i)
                if board.grid[self.pos[0] + i][self.pos[1]] == "o":
                    new_pos = (self.pos[0] + 2*i, self.pos[1])
                    
                if self.is_valid_move(new_pos, board.grid):
                    board.grid[self.pos] = "-"
                    self.pos = new_pos
                    
def find_carrots_and_holes():
    global board
    
    carrots = []
    holes = []
    grid = board.grid

    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == "c":
                carrots.append((row_idx, col_idx))
            elif cell == "o":
                holes.append((row_idx, col_idx))

    return carrots, holes

def find_closest(items):
    global board
    global rabbit
    
    closest_item = None
    min_distance = float('inf')
    pos = rabbit.pos

    for item in items:
        distance = np.abs(pos[0] - item[0]) + np.abs(pos[1] - item[1])

        if distance < min_distance:
            min_distance = distance
            closest_item = item

    return closest_item, min_distance

def move_rabbit_to_destination(source, destination):
    global board
    global rabbit
    
    rabbit_pos = source
    while rabbit_pos != destination:
        if board.grid[rabbit_pos] == "o":
            rabbit.jump_over_hole()
        else:
            direction = ""

            if rabbit_pos[0] < destination[0]:
                direction += "s"
            elif rabbit_pos[0] > destination[0]:
                direction += "w"

            if rabbit_pos[1] < destination[1]:
                direction += "d"
            elif rabbit_pos[1] > destination[1]:
                direction += "a"

            rabbit.move(direction)
        
        board.grid[rabbit.pos] = "R" if rabbit.state else "r"
        display_grid()

        rabbit_pos = rabbit.pos
        print('rabbit_pos: ', rabbit_pos)
        # time.sleep(0.4)
    
    return rabbit_pos    

def solution():
    global board
    global rabbit
    
    pos = rabbit.pos
    carrots, holes = find_carrots_and_holes()
    closest_carrot_pos, _ = find_closest(carrots)
    pos = move_rabbit_to_destination(pos, closest_carrot_pos)
    closest_hole_pos, _ = find_closest(holes)
    pos = move_rabbit_to_destination(pos, closest_hole_pos)
    return
    
    
def display_grid():
    global board
    
    grid = board.grid
    os.system('clear')
    
    for row in grid:
        sys.stdout.write(" ".join(row) + "\n")
    sys.stdout.flush()
    
def play_as_human():
    global board
    global rabbit
    
    while(True):
        ip = input()
        if ip in rabbit.moves():
            rabbit.move(ip)
        if ip == 'p':
            res = rabbit.pick_n_drop_carrot()
            if res:
                board.grid[rabbit.pos] = "R" if rabbit.state else "r"
                display_grid(board)
                print('You won!')
                break
        
        board.grid[rabbit.pos] = "R" if rabbit.state else "r"
        display_grid(board)
        
    return

           
def start():
    global board
    global rabbit
    
    a = max(int(input('Enter grid size (min 10): ')), 10)
    
    n_car = max(int(input('Enter number of carrots: ')), 1)
    n_hol = max(int(input('Enter number of holes: ')), 1)
    
    board = Board(a, n_car, n_hol)
    rabbit = Rabbit()
    
    board.grid[rabbit.pos] = "R" if rabbit.state else "r"
    display_grid()
    
    # play_as_human()
    solution()
    
    return


if __name__ == "__main__":
    start()
    


