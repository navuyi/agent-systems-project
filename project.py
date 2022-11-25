
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

OBSTACLE_SHAPE_ELLIPSE = 0

DEBUG_MODE = True

cell_size = 0.1
block_size_coefficient = 2.5
room_height = 10.0
room_width = 20.0
rows = int(room_width / cell_size)
cols = int(room_height / cell_size)
window_width = 1300
window_height = (window_width * cols) / rows


class ShapeEllipse(object):
    def __init__(self, a, b, rectangle_range):
        self.a = a
        self.b = b
        self.rectangle_range = list(rectangle_range)
        self.body_cells = None

    def calculate_cells(self, pos_x, pos_y, angle_degrees):
        a_pow_2 = math.pow(self.a, 2)
        b_pow_2 = math.pow(self.b, 2)
        angle_radians = math.radians(angle_degrees)
        sine_angle = math.sin(angle_radians)
        cosine_angle = math.cos(angle_radians)

        body_cells = []
        for dy in self.rectangle_range:
            for dx in self.rectangle_range:
                num_x_pow_2 = math.pow((dx) * cosine_angle + (dy) * sine_angle, 2)
                num_y_pow_2 = math.pow((dx) * sine_angle - (dy) * cosine_angle, 2)
                result = num_x_pow_2 / a_pow_2 + num_y_pow_2 / b_pow_2
                if result <= 1:
                    body_cells.append((dx + pos_x, dy + pos_y))

        self.body_cells = body_cells

    def get_body_cells(self):
        return self.body_cells


class ExitCell(object):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class Obstacle(object):
    def __init__(self, pos_x, pos_y, shape):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shape = shape


class Human(object):
    def __init__(self, name, cell_pos_x, cell_pos_y, first_known_exit_cell):
        self.name = name
        self.shape = ShapeEllipse(a=2.5, b=1.5, rectangle_range=range(-4, 5)) # [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        self.pos_x = cell_pos_x
        self.pos_y = cell_pos_y

        self.cell_center_pos_x = self.pos_x + (cell_size / 2)
        self.cell_center_pos_y = self.pos_y + (cell_size / 2)

        self.look_angle_alpha = 0.0

        self.calculate_moving_direction(first_known_exit_cell.pos_x, first_known_exit_cell.pos_y)

    def get_body_cells(self):
        return self.body_cells

    def calculate_body_cells(self):
        self.shape.calculate_cells(pos_x=self.pos_x, pos_y=self.pos_y, angle_degrees=self.look_angle_alpha)
        self.body_cells = self.shape.get_body_cells()

    def calculate_moving_direction(self, exit_x, exit_y):
        delta_x = self.pos_x - exit_x
        delta_y = self.pos_y - exit_y
        tangent_radians = math.atan2(delta_y, delta_x)
        self.look_angle_alpha = math.degrees(tangent_radians)
    
    def move(self):
        if self.look_angle_alpha < 0:
            self.pos_y += 1
        else:
            self.pos_y -= 1
        if self.look_angle_alpha < -90 or self.look_angle_alpha > 90:
            self.pos_x += 1
        else:
            self.pos_x -= 1
        
        self.cell_center_pos_x = self.pos_x + (cell_size / 2)
        self.cell_center_pos_y = self.pos_y + (cell_size / 2)


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
    for human in humans:
        human.move()
        human.calculate_moving_direction(exit_cell.pos_x, exit_cell.pos_y)

    rows, cols = grid.shape
    new_grid = init_grid(rows, cols, humans, exit_cell)

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

    exit_cell = ExitCell(100, 50)
    humans = [
        Human('first', 30, 20, exit_cell),
        Human('second', 30, 75, exit_cell),
        Human('third', 150, 20, exit_cell),
        Human('fourth', 150, 75, exit_cell)
    ]
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
