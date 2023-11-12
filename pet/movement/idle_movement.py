from pet.movement.coordinate import Coordinate
from pet.movement.linear_movement import LinearMovement


class IdleMovement(LinearMovement):
    def __init__(self, world_size: tuple[int, int], current_position: Coordinate):
        super().__init__(current_position, current_position, 2)
