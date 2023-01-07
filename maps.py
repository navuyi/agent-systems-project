
from logic import ExitCell, Child, Mid, Senior, Obstacle, ShapeEllipse

# cell_size = 0.1
# block_size_coefficient = 2.5
# room_height = 10.0
# room_width = 20.0

# ASSUMING THOSE PARAMETERS FOR MAPS

CLASS_214_MAP = {
    "exit_cell": ExitCell(150, 50),
    "humans": [
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
    ],
    'obstacles': [
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
}
