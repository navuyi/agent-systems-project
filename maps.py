
from logic import ExitCell, Child, Mid, Senior, Obstacle, ShapeEllipse, ShapeRectangle, PanicCell

# ASSUMING THOSE PARAMETERS FOR MAPS
# cell_size = 0.1
# block_size_coefficient = 2.5
# room_height = 10.0
# room_width = 20.0

EMPTY_MAP_WITH_SPECIFIC_EXIT_CELL_1 = {
    'panic_cell': PanicCell(50, 50, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    "exit_cell": ExitCell(175, 54, 0, ShapeEllipse(a=1, b=1, rectangle_range=range(-3, 3))),
    "humans": [
        # first series
        Child('first', 110, 35),
        Senior('second', 110, 50),
        Mid('third', 110, 65),
        Child('first_1', 95, 25),
        Senior('second_1', 95, 50),
        Mid('third_1', 95, 75),
        Child('first_2', 80, 35),
        Senior('second_2', 80, 50),
        Mid('third_2', 80, 65),
        # second series
        Child('first_3', 5, 35),
        Senior('second_3', 5, 50),
        Mid('third_3', 5, 65),
        Child('first_4', 15, 25),
        Senior('second_4', 15, 50),
        Mid('third_4', 15, 75),
        Child('first_5', 25, 35),
        Senior('second_5', 25, 50),
        Mid('third_5', 25, 65),
        # third series
        Child('first_6', 45, 35),
        Senior('second_6', 45, 50),
        Mid('third_6', 45, 65),
        Child('first_7', 55, 25),
        Senior('second_7', 55, 50),
        Mid('third_7', 55, 75),
        Child('first_8', 65, 35),
        Senior('second_8', 65, 50),
        Mid('third_8', 65, 65)
    ],
    'obstacles': [
        Obstacle(150, 35, 0, ShapeRectangle(a=37, b=10)), # upper wall
        Obstacle(150, 65, 0, ShapeRectangle(a=37, b=10)), # down wall
        Obstacle(177, 40, 0, ShapeRectangle(a=10, b=30)), # after exit
        Obstacle(150, 0, 0, ShapeRectangle(a=15, b=45)), # up blocking
        Obstacle(150, 65, 0, ShapeRectangle(a=15, b=34)), # down blocking
    ]
}

EMPTY_MAP_WITH_SPECIFIC_EXIT_CELL_2 = EMPTY_MAP_WITH_SPECIFIC_EXIT_CELL_1.copy()
EMPTY_MAP_WITH_SPECIFIC_EXIT_CELL_2['obstacles'] = [
    Obstacle(170, 26, 0, ShapeEllipse(a=30, b=10, rectangle_range=range(-19, 20), angle_degrees=45)), # upper wall
    Obstacle(170, 75, 0, ShapeEllipse(a=30, b=10, rectangle_range=range(-19, 20), angle_degrees=-45)), # down wall
    Obstacle(177, 40, 0, ShapeRectangle(a=10, b=30)), # after exit
    Obstacle(155, 0, 0, ShapeRectangle(a=15, b=15)), # up blocking
    Obstacle(155, 84, 0, ShapeRectangle(a=15, b=15)), # down blocking
]

RANDOM_MAP = EMPTY_MAP_WITH_SPECIFIC_EXIT_CELL_1.copy()
RANDOM_MAP['obstacles'].extend([
    Obstacle(135, 55, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(105, 55, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(125, 45, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(125, 65, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(150, 55, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(115, 65, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(105, 34, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    Obstacle(75, 40, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6)))
])
