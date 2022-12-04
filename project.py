
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
GRID_FREE = (255, 255, 255) # white color
STEP_SIZE = 2

cell_size = 0.1
block_size_coefficient = 2.5
room_height = 10.0
room_width = 20.0
rows = int(room_width / cell_size)
cols = int(room_height / cell_size)
window_width = 1300
window_height = (window_width * cols) / rows


def is_grid_block_free(grid, pos_x, pos_y):
    grid_block = grid[pos_x, pos_y]
    if  grid_block[0] == GRID_FREE[0] and\
        grid_block[1] == GRID_FREE[1] and\
        grid_block[2] == GRID_FREE[2]:
        return True
    
    return False


def is_grid_free_for_body_cells(grid, body_cells):
    for pos in body_cells:
        if not is_grid_block_free(grid, pos[0], pos[1]):
            return False
    return True


class GridBlockTakenException(Exception):
    pass


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
        self.color = (255, 0, 0)


class Obstacle(object):
    def __init__(self, pos_x, pos_y, angle_degrees, shape):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle_degrees
        self.shape = shape
        self.color = (0, 255, 0)
        self.body_cells = None

    def calculate_cells(self):
        self.shape.calculate_cells(pos_x=self.pos_x, pos_y=self.pos_y, angle_degrees=self.angle)
        self.body_cells = self.shape.get_body_cells()
    
    def get_cells(self):
        return self.body_cells
    
    def get_color(self):
        return self.color


class Human(object):
    def __init__(self, name, cell_pos_x, cell_pos_y, first_known_exit_cell):
        self.name = name
        self.shape = ShapeEllipse(a=2.5, b=1.5, rectangle_range=range(-4, 5)) # [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        self.pos_x = cell_pos_x
        self.pos_y = cell_pos_y
        self.color = tuple(np.random.randint(256, size=3))

        self.__calculate_cell_center()

        self.look_angle_alpha = 0.0
        self.reverse_steps_x = []
        self.reverse_steps_y = []

        self.__calculate_moving_direction(first_known_exit_cell.pos_x, first_known_exit_cell.pos_y)

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color
    
    def get_body_cells(self):
        return self.body_cells

    def calculate_body_cells(self, grid):
        while True:
            tries += 1
            self.shape.calculate_cells(pos_x=self.pos_x, pos_y=self.pos_y, angle_degrees=self.look_angle_alpha)
            tmp_body_cells = self.shape.get_body_cells()
            if is_grid_free_for_body_cells(grid, tmp_body_cells):
                self.body_cells = tmp_body_cells
                break

            if self.__are_reverse_steps_available():
                self.__take_reverse_step()
            self.__change_moving_direction_as_grid_was_taken()

    def __are_reverse_steps_available(self):
        if not self.reverse_steps_x or not self.reverse_steps_y:
            return False
        
        return True

    def __take_reverse_step(self):
        self.pos_x += self.reverse_steps_x[-1]
        self.pos_y += self.reverse_steps_y[-1]

        self.__calculate_cell_center()

        self.reverse_steps_x.pop()
        self.reverse_steps_y.pop()

    def __change_moving_direction_as_grid_was_taken(self):
        if self.look_angle_alpha < 0:
            self.look_angle_alpha -= 90
        else:
            self.look_angle_alpha += 90

    def __calculate_cell_center(self):
        self.cell_center_pos_x = self.pos_x + (cell_size / 2)
        self.cell_center_pos_y = self.pos_y + (cell_size / 2)

    def __calculate_moving_direction(self, exit_x, exit_y):
        delta_x = self.pos_x - exit_x
        delta_y = self.pos_y - exit_y
        tangent_radians = math.atan2(delta_y, delta_x)
        self.look_angle_alpha = math.degrees(tangent_radians)
    
    def move(self, exit_x, exit_y):
        if self.look_angle_alpha < 0:
            self.pos_y += STEP_SIZE
            self.reverse_steps_y.append(-STEP_SIZE)
        else:
            self.pos_y -= STEP_SIZE
            self.reverse_steps_y.append(+STEP_SIZE)

        if self.look_angle_alpha < -90 or self.look_angle_alpha > 90:
            self.pos_x += STEP_SIZE
            self.reverse_steps_x.append(-STEP_SIZE)
        else:
            self.pos_x -= STEP_SIZE
            self.reverse_steps_x.append(+STEP_SIZE)
        
        self.__calculate_cell_center()
        self.__calculate_moving_direction(exit_x, exit_y)


def init_grid(rows, cols, humans, obstacles, exit_cell):
    grid = np.zeros(shape=(rows, cols), dtype=[('x', 'int'), ('y', 'int'), ('z', 'int')])
    grid.fill(GRID_FREE)

    # add obstacles to grid, no collisions here
    for ob in obstacles:
        ob.calculate_cells()
        obstacle_cells = ob.get_cells()
        for c in obstacle_cells:
            grid[c[0], c[1]] = ob.get_color()

    # add exit cell to grid
    if not is_grid_block_free(grid, exit_cell.pos_x, exit_cell.pos_y):
        raise GridBlockTakenException("Exit Cell could no be initialized at pos_x {} pos_y are already taken!".format(
            exit_cell.pos_x, exit_cell.pos_y
        ))

    grid[exit_cell.pos_x, exit_cell.pos_y] = exit_cell.color

    # add humans to grid
    for human in humans:
        human.calculate_body_cells(grid)
        human_cells = human.get_body_cells()
        human_color = human.get_color()
        for body_cell_pos in human_cells:
            if not is_grid_block_free(grid, body_cell_pos[0], body_cell_pos[1]):
                raise GridBlockTakenException("Human {} could no be initialized at pos_x {} pos_y are already taken!".format(
                    human.get_name(), body_cell_pos[0], body_cell_pos[1]
                ))

            grid[body_cell_pos[0], body_cell_pos[1]] = human_color

    return grid


def update_grid(grid, humans, obstacles, exit_cell):
    for human in humans:
        human.move(exit_cell.pos_x, exit_cell.pos_y)

    rows, cols = grid.shape
    new_grid = init_grid(rows, cols, humans, obstacles, exit_cell)

    return new_grid


def draw_grid(screen, grid, w_width, w_height):
    rows, cols = grid.shape
    blockSize = ((min(w_width, w_height) - max(rows, cols)) / max(rows, cols)) * block_size_coefficient

    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            pos_x = (blockSize + 1) * x
            pos_y = (blockSize + 1) * y
            rect = pygame.Rect(pos_x, pos_y, blockSize, blockSize)
            pygame.draw.rect(screen, grid[x, y], rect, 0)

    pygame.display.flip()


if __name__ == "__main__":
    print("Window Size: {} x {}".format(window_width, window_height))
    print("Cells: {} x {}".format(rows, cols))
    pygame.init()
    screen = pygame.display.set_mode([window_width, window_height])
    screen.fill((128, 128, 128))
    clock = pygame.time.Clock()

    exit_cell = ExitCell(150, 50)
    humans = [
        Human('first', 30, 35, exit_cell),
        Human('second', 30, 85, exit_cell),
        Human('third', 150, 20, exit_cell),
        Human('fourth', 150, 75, exit_cell),
        Human('fifth', 125, 50, exit_cell),
        Human('sixth', 115, 20, exit_cell),
        Human('seventh', 180, 20, exit_cell),
        Human('eight', 180, 80, exit_cell),
        Human('ninth', 165, 45, exit_cell),
        Human('tenth', 65, 15, exit_cell),
        Human('eleventh', 65, 65, exit_cell)
    ]
    obstacles = [
        Obstacle(60, 45, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(145, 68, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(105, 75, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(125, 25, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(125, 75, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(150, 30, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(165, 65, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(65, 30, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(75, 20, 25, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6)))
    ]
    grid = init_grid(rows, cols, humans, obstacles, exit_cell)

    draw_grid(screen, grid, window_width, window_height)

    running = True

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
        
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    grid = update_grid(grid, humans, obstacles, exit_cell)
                    draw_grid(screen, grid, window_width, window_height)

    pygame.quit()
