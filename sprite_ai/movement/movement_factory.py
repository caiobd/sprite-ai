from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.idle_movement import IdleMovement
from sprite_ai.movement.walking_movement import WalkingMovement


class MovementFactory:
    def __init__(self, world_size: tuple[int, int]) -> None:
        self.world_size = world_size
        self.movements = {
            "walking": WalkingMovement,
            "idle": IdleMovement,
        }

    def build(self, movement_name, current_position: Coordinate):
        movement_type = self.movements[movement_name]
        return movement_type(self.world_size, current_position)
