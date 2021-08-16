import numpy as np
import pygame as pg
import os

##Classes

class square() :
    def __init__(self, C, parent, grid) :
        self.C = C
        self.parent = parent
        try :
            self.F = getF(self, grid)
        except :
            self.F = np.inf

##Functions

def loadGrid(directory) :
    File = open(directory)
    Text = File.read()
    File.close()
    lines = Text.split('\n')
    grid = np.array([line.split(' ') for line in lines], dtype='str')
    return grid

def getPath(sq) :
    Path = [sq]
    G = 0
    while Path[-1].parent is not None :
        Path.append(Path[-1].parent)
    return Path

def getGfromPath(path) :
    G = 0
    for i in range(len(path)-1) :
        G += getCost(path[i], path[i+1])
    return G

def getCost(sq, Tsq) :
    ##'distance' from Tsq (Target square) :
    Cost = 0
    x, y = sq.C
    xT, yT = Tsq.C
    while (x, y) != (xT, yT) :
        if x == xT :
            Cost += 10
            if y > yT :
                y -= 1
            else :
                y += 1
        elif y == yT :
            Cost += 10
            if x > xT :
                x -= 1
            else :
                x += 1
        else :
            Cost += 14
            if x > xT :
                x -= 1
            else :
                x += 1
            if y > yT :
                y -= 1
            else :
                y += 1
    return Cost

def getF(sq, grid) :
    w, h = grid.shape
    for x in range(w) :
        for y in range(h) :
            if grid[y, x] == 'B' :
                B = square((x, y), None, grid)
    return getGfromPath(getPath(sq)) + getCost(sq, B)

def minF(openSq) :
    minF = np.inf
    minSq = None
    for sq in openSq :
        if sq.F <= minF :
            minF = sq.F
            minSq = sq
    return minSq

def addNeighbours(sq, grid, openSq, closedSq) :
    w, h = grid.shape
    x, y = sq.C
    nbC = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1,y-1)]
    traversable = True
    for i in range(len(nbC)) :
        nbx, nby = nbC[i]
        if nbx < 0 or nbx >= w or nby < 0 or nby >= h :
            traversable = False
        if traversable and grid[nby, nbx] == 'X' :
            traversable = False
        for k in range(len(closedSq)) :
            if closedSq[k].C == (nbx, nby) :
                traversable = False
        for k in range(len(openSq)) :
            if openSq[k].C == (nbx, nby) :
                traversable = False
                newSq = square((nbx, nby), sq, grid)
                if openSq[k].F > newSq.F :
                    openSq[k] = newSq
        if traversable :
            openSq.append(square((nbx, nby), sq, grid))
        traversable = True
    return openSq

def pathFind(data) :
    [Window, grid, ẟ, openSq, closedSq, A, B] = data
    search = True
    openSq = addNeighbours(A, grid, openSq, closedSq)
    draw(data, 'walls', False)
    while search :
        if len(openSq) == 0 :
            print('no path found')
            return None
        curSq = minF(openSq)
        openSq.remove(curSq)
        closedSq.append(curSq)
        if curSq.C == B.C :
            search = False
        openSq = addNeighbours(curSq, grid, openSq, closedSq)
        draw(data, 'walls', False)
    path = getPath(curSq)
    for i in range(len(path)) :
        x, y = path[i].C
        if grid[y, x] == '.' :
            grid[y, x] = 'O'
    draw(data, 'walls', True)
    return grid

##Drawing functions

pg.init()

current = pg.image.load(os.path.join("Sprites", "Current.png"))
button1 = pg.image.load(os.path.join("Sprites", "Button1.png"))
buttonA = pg.image.load(os.path.join("Sprites", "ButtonA.png"))
buttonB = pg.image.load(os.path.join("Sprites", "ButtonB.png"))
Pf = pg.image.load(os.path.join("Sprites", "Pathfind.png"))

all_fonts = pg.font.get_fonts()
if "comicsansms" in all_fonts :
    font = pg.font.SysFont("comicsansms", 18)
else :
    font = pg.font.Font(None, 40)

def draw(data, action, Final) :
    [Window, grid, ẟ, openSq, closedSq] = data[:5]
    w, h = grid.shape
    Surface = pg.display.get_surface()
    Window.fill((192, 192, 192))

    for i in range(h) :
        for j in range(w) :
            Rect = pg.Rect(j*ẟ, i*ẟ, ẟ, ẟ)
            if grid[i, j] == 'X' :
                pg.draw.rect(Surface, (0, 0, 0), Rect)
            elif grid[i, j] == '.' :
                pg.draw.rect(Surface, (255, 255, 255), Rect)
            elif grid[i, j] == 'A' :
                pg.draw.rect(Surface, (0, 0, 255), Rect)
                text = font.render("A", True, (0, 0, 0))
                tw, th = text.get_width(), text.get_height()
                Window.blit(text, (j*ẟ + (ẟ-tw)//2, i*ẟ + (ẟ-th)//2))
            elif grid[i, j] == 'B' :
                pg.draw.rect(Surface, (0, 0, 255), Rect)
                text = font.render("B", True, (0, 0, 0))
                tw, th = text.get_width(), text.get_height()
                Window.blit(text, (j*ẟ + (ẟ-tw)//2, i*ẟ + (ẟ-th)//2))
            elif grid[i, j] == 'O' :
                pg.draw.rect(Surface, (0, 0, 255), Rect)
    
    if not Final :
        for sq in closedSq :
            x, y = sq.C
            Rect = pg.Rect(x*ẟ, y*ẟ, ẟ, ẟ)
            pg.draw.rect(Surface, (255, 0, 0), Rect)
        for sq in openSq :
            x, y = sq.C
            Rect = pg.Rect(x*ẟ, y*ẟ, ẟ, ẟ)
            pg.draw.rect(Surface, (0, 255, 0), Rect)
            text = font.render(str(sq.F), True, (0, 0, 0))
            tw, th = text.get_width(), text.get_height()
            Window.blit(text, (x*ẟ + (ẟ-tw)//2, y*ẟ + (ẟ-th)//2))
    
    #drawing buttons :
    Window.blit(current, (20, h*ẟ))
    if action == 'walls' :
        Window.blit(button1, (75, h*ẟ))
    elif action == 'A' :
        Window.blit(buttonA, (75, h*ẟ))
    elif action == 'B' :
        Window.blit(buttonB, (75, h*ẟ))
    Window.blit(Pf, (w*ẟ-73, h*ẟ))

    pg.display.flip()
    return None

##Interaction functions

def toggle(act) :
    if act == 'walls' :
        return 'A'
    elif act == 'A' :
        return 'B'
    return 'walls'

def saveGrid(grid) :
    text = ''
    for line in grid :
        for sq in line :
            text += sq+' '
        text = text[:-1]
        text += '\n'
    text = text[:-1]
    File = open('map.txt', 'r+')
    File.write(text)
    File.close()
