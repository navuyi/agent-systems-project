
import numpy as np
import pygame
import math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

DEBUG_MODE = True

cell_size = 0.09
block_size_coefficient = 2.5
room_height = 10.0
room_width = 20.0
rows = int(room_width / cell_size)
cols = int(room_height / cell_size)
window_width = 1300
window_height = (window_width * cols) / rows


class ExitCell(object):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class Human(object):
    def __init__(self, cell_pos_x, cell_pos_y, first_known_exit_cell):
        self.pos_x = cell_pos_x
        self.pos_y = cell_pos_y

        self.cell_center_pos_x = self.pos_x + (cell_size / 2)
        self.cell_center_pos_y = self.pos_y + (cell_size / 2)

        self.known_exit_cell_pos_x = first_known_exit_cell.pos_x
        self.known_exit_cell_pos_y = first_known_exit_cell.pos_y

        self.look_angle_alpha = 0.0

    def get_body_cells(self):
        return self.body_cells

    def calculate_body_cells(self):
        a = 2.5
        a_pow_2 = math.pow(a, 2)
        b = 1.5
        b_pow_2 = math.pow(b, 2)

        body_cells = []
        for dy in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
            for dx in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
                dcell_x = dx + self.pos_x
                dcell_y = dy + self.pos_y
                num_x_pow_2 = math.pow(dx, 2)
                num_y_pow_2 = math.pow(dy, 2)
                result = num_x_pow_2 / a_pow_2 + num_y_pow_2 / b_pow_2
                if result <= 1:
                    body_cells.append((dcell_x, dcell_y))

        self.body_cells = body_cells


def init_grid(rows, cols, humans, exit_cell):
    grid = np.zeros(shape=(rows, cols))

    for human in humans:
        human.calculate_body_cells()
        body_cells = human.get_body_cells()
        for bd in body_cells:
            grid[bd[0], bd[1]] = 1

    grid[exit_cell.pos_x, exit_cell.pos_y] = 1

    return grid


def update_grid(grid, humans, exit_cell):
    new_grid = grid.copy()



    return new_grid


def draw_grid(screen, grid, w_width, w_height):
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    rows, cols = grid.shape
    blockSize = ((min(w_width, w_height) - max(rows, cols)) / max(rows, cols)) * block_size_coefficient

    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            pos_x = (blockSize + 1) * x
            pos_y = (blockSize + 1) * y
            rect = pygame.Rect(pos_x, pos_y, blockSize, blockSize)
            if grid[x, y] == 0:
                pygame.draw.rect(screen, white_color, rect, 0)
            else:
                pygame.draw.rect(screen, black_color, rect, 0)  

    pygame.display.flip()


if __name__ == "__main__":
    print("Window Size: {} x {}".format(window_width, window_height))
    print("Cells: {} x {}".format(rows, cols))
    pygame.init()
    screen = pygame.display.set_mode([window_width, window_height])
    screen.fill((128, 128, 128))
    clock = pygame.time.Clock()

    exit_cell = ExitCell(175, 50)
    humans = [Human(20, 20, exit_cell), Human(30, 30, exit_cell)]
    grid = init_grid(rows, cols, humans, exit_cell)

    draw_grid(screen, grid, window_width, window_height)

    running = True

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
        
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    grid = update_grid(grid, humans, exit_cell)
                    draw_grid(screen, grid, window_width, window_height)

    pygame.quit()
