#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 17:09:05 2021

@author: Jeremiah Smith
Date   : 03/11/2021
Lab    : Dijkstras algorithm

- left click to place a start point, end point, and walls 
- Right click to erase any points
- Press the space bar to begin the algorthim 
pulled
"""


import pygame

from queue import PriorityQueue



Size = 505
num = 25
WIDTH = 20
HEIGHT = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 255, 255)
MARGIN = 5



pygame.display.set_caption("Dijkstras")
screen = pygame.display.set_mode((Size, Size))

class Node:
    
    def __init__(self, row, col):
        self.color = WHITE
        self.row = row
        self.col = col
        self.neighbors = []
        self.distance = float("inf")
        self.parent = None
        
        
    def get_pos(self):
        return self.row, self.col
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [(MARGIN + WIDTH) * self.col + MARGIN,
                              (MARGIN + HEIGHT) * self.row + MARGIN,
                              WIDTH,
                              HEIGHT])
    def checking(self):
        self.color = GREEN
    
    def make_start(self):
        self.color = BLUE
        
    def make_end(self):
        self.color = ORANGE
        
    def make_barrier(self):
        self.color = BLACK
        
    def clear(self):
        self.color = WHITE
        
    def is_barrier(self):
        return self.color == BLACK
        
    def visited(self):
        self.color = RED
        
    def path(self):
        self.color = PURPLE
    
    def __lt__(self, other):
        return self.distance < other.distance
    
    def is_visited(self):
        return self.color == RED
    
    def is_checking(self):
        return self.color == GREEN
        
        
    def update_neighbors(self, grid):
        self.neighbors = []
    
        
        if self.row < 19 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < 19 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
            



def dijkstras_algorithm(grid, start, end):
    q = PriorityQueue()
    q.put(start)
    start.distance = 0;
    found = False
    
    while not q.empty():
         if found:
             break
         
         cur = q.get()
         cur.visited()
         dis = cur.distance + 1
         draw_grid(grid)
         
        
             
         for neigh in cur.neighbors:
             
             if neigh.row == end.row and neigh.col == end.col:
                 neigh.parent = cur
                 found = True
                 break
             
             if neigh.is_visited() == False:
                if neigh.is_checking() == False:
                    neigh.parent = cur
                    neigh.distance = dis
                    neigh.checking()
                    q.put(neigh)
                    
                    
                elif neigh.distance  > dis:
                    q.get(neigh)
                    neigh.parent = cur
                    neigh.distance = dis
                    q.put(neigh)
                    
    if found: 
        find_path(grid, start, end)
                 
    



def get_clicked_pos(pos, num):
    
    x, y = pos
    
    x = x // num
    y = y // num
    return y, x


def find_path(grid, start, end):
    
    cur = end.parent
    
    while cur.parent != None:
        cur.path()
        cur = cur.parent
        draw_grid(grid)   
    start.make_start()



def grid():
    grid = []
    for i in range(20):
        grid.append([])
        for j in range(20):
            node = Node(i, j)
            grid[i].append(node)
    return grid


        
def draw_grid(grid):     
    screen.fill(BLACK)      
    for row in grid:
        for node in row:
            node.draw(screen)
            
    pygame.display.update()



grid = grid()
draw_grid(grid)

run = True

start = None
end = None


while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, num)
            node = grid[row][col]
            if not start:
                start = node
                node.make_start()
            elif not end and node != start:
                end = node
                node.make_end()
                
            elif node != start and node != end:
                node.make_barrier()
            
        elif pygame.mouse.get_pressed()[2]:
            if node == start:
                start = None
            if node == end:
                end  = None
                
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, num)
            node = grid[row][col]
            node.clear()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)
                        
                dijkstras_algorithm(grid, start, end)
                
            
        draw_grid(grid)
        
pygame.quit()
            
            
       
       
    






     
