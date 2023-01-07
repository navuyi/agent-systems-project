
from structures import (
    GRID_FREE, is_grid_block_free, block_size_coefficient, window_height, window_width,
    Mid, Child, Senior, Obstacle, ExitCell, rows, cols, ShapeEllipse
)
import numpy as np
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


class GridBlockTakenException(Exception):
    pass


def init_grid(rows, cols, humans, obstacles, exit_cell):
    grid = np.zeros(shape=(rows, cols), dtype=[('x', 'int'), ('y', 'int'), ('z', 'int')])
    grid.fill(GRID_FREE)

    # add obstacles to grid, no collisions here
    for ob in obstacles:
        ob.calculate_cells()
        for c in ob.get_cells():
            grid[c[0], c[1]] = ob.get_color()

    # add exit cell to grid
    if not is_grid_block_free(grid, exit_cell.pos_x, exit_cell.pos_y):
        raise GridBlockTakenException("Exit Cell could no be initialized at pos_x {} pos_y {} are already taken!".format(
            exit_cell.pos_x, exit_cell.pos_y
        ))

    grid[exit_cell.pos_x, exit_cell.pos_y] = exit_cell.color

    # add humans to grid
    for human in humans:
        human.calculate_body_cells(grid, exit_cell)
        for body_cell_pos in human.get_body_cells():
            #if not is_grid_block_free(grid, body_cell_pos[0], body_cell_pos[1]):
            #    raise GridBlockTakenException("Human {} could no be initialized at pos_x {} pos_y {} are already taken!".format(
            #        human.get_name(), body_cell_pos[0], body_cell_pos[1]
            #    ))

            grid[body_cell_pos[0], body_cell_pos[1]] = human.get_color()

    return grid


def update_grid(grid, humans, obstacles, exit_cell):
    for human in humans:
        human.move()

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
        Child('first', 30, 35),
        Senior('second', 30, 85),
        Mid('third', 163, 20),
        Child('fourth', 150, 75),
        Senior('fifth', 125, 50),
        Mid('sixth', 115, 20),
        Child('seventh', 180, 20),
        Mid('eight', 180, 80),
        Mid('ninth', 165, 45),
        Senior('tenth', 65, 15),
        Mid('eleventh', 65, 65),
        Mid('twelve', 20, 10),
        Child('asdf', 20, 30),
        Senior('zxcv', 20, 55),
        Child('qwer', 20, 75),
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
