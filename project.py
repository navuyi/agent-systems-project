
from time import sleep
import numpy as np
import itertools
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Grid size
rows = 40
cols = 40


def initGrid(rows,cols):
    grid = np.random.randint(2, size=(rows, cols))
    return grid


def calculateAliveNeighbours(y, x, grid):
    rows, cols = grid.shape
    count = 0 

    # Go through Moore's neighbourhood
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            count += grid[(y + dy) % rows][(x + dx) % cols] 

    # We don't want to count the center
    aliveNeigh = count - grid[y, x]
    return aliveNeigh


def update(grid, rule_for_alive=None, rule_for_dead=None):
    if not rule_for_alive:
        rule_for_alive = [2, 3]
    if not rule_for_dead:
        rule_for_dead = [3]

    rows, cols = grid.shape
    newGrid = grid.copy()

    for y in range(rows):
        for x in range(cols):
            aliveNeigh = calculateAliveNeighbours(y, x, grid)

            if grid[y][x] == 1:
                if aliveNeigh in rule_for_alive:
                    newGrid[y][x] = 1
                else:
                    newGrid[y][x] = 0    
            elif grid[y][x] == 0:
                if aliveNeigh in rule_for_dead:
                    newGrid[y][x] = 1
                else:
                    newGrid[y][x] = 0
                            
    return newGrid


def drawGrid(screen,grid,w_width, w_height):
    alive_colour = (0,0,0)
    dead_colour = (255,255,255)
    rows, cols = grid.shape
    blockSize = (min(w_width, w_height)-max(rows, cols))/max(rows, cols)
    # For the sake of simplicity, we're skipping first and last rows & columns
    for x in range(1, rows-1):
        for y in range(1, cols-1):
            pos_x = (blockSize+1)*x
            pos_y = (blockSize+1)*y
            rect = pygame.Rect(pos_x, pos_y, blockSize, blockSize)
            if grid[x][y] == 1:
                pygame.draw.rect(screen, alive_colour, rect, 0)
            else:
                pygame.draw.rect(screen, dead_colour, rect, 0)    
    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    w_width = 800
    w_height = 800
    # Set up the drawing window, adjust the size
    screen = pygame.display.set_mode([w_width, w_height])
    grid = initGrid(rows,cols)
    clock = pygame.time.Clock()

    # Set background
    screen.fill((128, 128, 128))

    drawGrid(screen, grid, w_width, w_height)

    running = True

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
        
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    grid = update(grid)
                    drawGrid(screen, grid, w_width, w_height)

    pygame.quit()
