
from logic import ExitCell, Child, Mid, Senior, Obstacle, ShapeEllipse, ShapeRectangle, PanicCell

# ASSUMING THOSE PARAMETERS FOR MAPS
# cell_size = 0.1
# block_size_coefficient = 2.5
# room_height = 10.0
# room_width = 20.0

CLASS_214_MAP = {
    'panic_cell': PanicCell(25, 75, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
    "exit_cell": ExitCell(150, 50, 0, ShapeEllipse(a=1, b=1, rectangle_range=range(-3, 3))),
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
        Child('thirteen', 20, 30),
        Senior('fourteen', 20, 55),
        Child('fifteen', 20, 75),
    ],
    'obstacles': [
        Obstacle(60, 45, 0, ShapeRectangle(a=3, b=6)),
        Obstacle(145, 68, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(105, 75, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(125, 25, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(125, 75, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(150, 30, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(165, 65, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(65, 30, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(75, 20, 0, ShapeEllipse(a=3, b=3, rectangle_range=range(-5, 6))),
        Obstacle(10, 10, 0, ShapeRectangle(a=3, b=5))
    ]
}
