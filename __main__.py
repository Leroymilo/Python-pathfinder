import numpy as np
import pygame as pg
from pygame.locals import *

from __modules__ import *


##Global variables

grid = loadGrid('map.txt')
openSq = []
closedSq = []

w, h = grid.shape
for x in range(w) :
    for y in range(h) :
        if grid[y, x] == 'A' :
            A = square((x, y), None, grid)
        elif grid[y, x] == 'B' :
            B = square((x, y), None, grid)

closedSq.append(A)

##Pygame functions

pg.init()
pg.key.set_repeat(500, 100)
ẟ = 32
Window = pg.display.set_mode((w*ẟ, h*ẟ + 15))
Continue = True
prevC = None
action = 'walls'
data = [Window, grid, ẟ, openSq, closedSq, A, B]
draw(data, action, True)

while Continue :
    for event in pg.event.get() :

        if event.type == QUIT :
            Continue = False

        else :
            if pg.mouse.get_pressed()[0] :
                try :
                    x, y = event.pos
                except :
                    x, y = -1, -1

                if y >= h*ẟ and 75 <= x <= 90 :
                    action = toggle(action)
                
                if y >= h*ẟ and w*ẟ-73 <= x <= w*ẟ-20 :
                    saveGrid(grid)
                    newGrid = pathFind(data)
                    if newGrid is not None :
                        grid = newGrid
                    Done = False
                    while not Done :
                        for event in pg.event.get() :
                            if event.type == QUIT :
                                Continue = False
                                Done = True
                            elif event.type == MOUSEBUTTONDOWN :
                                if event.button == 1 :
                                    x, y = event.pos
                                    if y >= h*ẟ and w*ẟ-73 <= x <= w*ẟ-20 :
                                        Done = True
                    grid = loadGrid('map.txt')
                    openSq = []
                    closedSq = [A]
                
                else :
                    for i in range(h) :
                        for j in range(w) :
                            if i*ẟ <= y < (i+1)*ẟ and j*ẟ <= x < (j+1)*ẟ and (j, i) != prevC :
                                prevC = j, i
                                if action == 'walls' :
                                    if grid[i, j] == 'X' :
                                        grid[i, j] = '.'
                                    elif grid[i, j] == '.' :
                                        grid[i, j] = 'X'
                                
                                elif action == 'A' :
                                    if grid[i, j] == '.' :
                                        xA, yA = A.C
                                        grid[yA, xA] = '.'
                                        grid[i ,j] = 'A'
                                        A.C = (j, i)
                                
                                elif action == 'B' :
                                    if grid[i, j] == '.' :
                                        xB, yB = B.C
                                        grid[yB, xB] = '.'
                                        grid[i ,j] = 'B'
                                        B.C = (j, i)
            
            else : prevC = None
    
    data = [Window, grid, ẟ, openSq, closedSq, A, B]
    draw(data, action, True)
        
pg.quit