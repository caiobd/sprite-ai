from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RigidBody:
    x: int
    y: int
    width: int
    height: int

    def check_collision(self, other: RigidBody) -> bool:
        is_collision_in_x = (
            other.x + other.width >= self.x >= other.x
            or other.x + other.width >= self.x + self.width >= other.x
        )
        is_collision_in_y = (
            other.y + other.height >= self.y >= other.y
            or other.y + other.height >= self.y + self.height >= other.y
        )
        is_collision = is_collision_in_x and is_collision_in_y
        return is_collision
