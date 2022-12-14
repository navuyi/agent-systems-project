
from logic import (
    GRID_FREE, is_grid_block_free, block_size_coefficient, window_height, window_width, rows, cols,
    Mid, Child, Senior, Obstacle, ExitCell, ShapeEllipse,
    human_is_at_the_exit_cell, get_children_count, get_mids_count, get_senior_count
)
from maps import CLASS_214_MAP
import numpy as np
import pygame
from pygame.locals import (
    K_RIGHT,
    KEYDOWN,
    QUIT,
)


# Configuration -> select map
MAP = CLASS_214_MAP

# Stats for grid
TIME_TO_LEAVE_ALL_HUMANS = 0


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

    # when human is close to exit cell we want to remove it from scene
    index_to_remove_human = []    

    # add humans to grid
    for i in range(len(humans)):
        humans[i].calculate_body_cells(grid, exit_cell)

        # check if any grid is so close to exit cell
        if human_is_at_the_exit_cell(humans[i], exit_cell):
            index_to_remove_human.append(i)

        # write color of the human to the grid
        for body_cell_pos in humans[i].get_body_cells():
            grid[body_cell_pos[0], body_cell_pos[1]] = humans[i].get_color()

    for i in index_to_remove_human:
        humans.pop(i)

    global TIME_TO_LEAVE_ALL_HUMANS
    if not humans:
        print("All humans has leaved the room in {} time_to_leave".format(TIME_TO_LEAVE_ALL_HUMANS))
    else:
        TIME_TO_LEAVE_ALL_HUMANS += 1

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

    humans = MAP['humans']
    obstacles = MAP['obstacles']
    exit_cell = MAP['exit_cell']

    print("Map consists of {} obstacles, {} humans, where there are {} children, {} mids and {} seniors".format(
        len(obstacles), len(humans), get_children_count(humans), get_mids_count(humans), get_senior_count(humans)
    ))

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
