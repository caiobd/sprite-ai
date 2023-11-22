import random

from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.linear_movement import LinearMovement


class WalkingMovement(LinearMovement):
    def __init__(self, world_size: tuple[int, int], current_position: Coordinate):
        world_width, world_height = world_size
        start_coordinate = current_position
        if start_coordinate is None:
            start_coordinate = Coordinate(
                random.choice(range(world_width)), world_height
            )
        target_x = random.choice(range(world_width))
        target_y = world_height
        target_coordinate = Coordinate(target_x, target_y)
        super().__init__(start_coordinate, target_coordinate, 40)
