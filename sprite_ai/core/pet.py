from sprite_ai.core.pet_behaviour import PetBehaviour
from sprite_ai.core.world import World
from sprite_ai.gui.sprite_gui import SpriteGui
from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.movement_factory import MovementFactory


class Pet:
    def __init__(
        self, sprite_gui: SpriteGui, pet_behaviour: PetBehaviour, world: World
    ) -> None:
        self.sprite_gui = sprite_gui
        self.pet_behaviour = pet_behaviour
        self.world = world
        width, height = world.world_size
        self.current_position = Coordinate(width // 2, height)
        self.movement_factory = MovementFactory(world.world_size)
        self.sprite_gui.on_position_updated = self.on_position_update

        self.world.event_manager.subscribe(
            'ui.pet.animation', self.on_animation_event
        )
        self.world.event_manager.subscribe('ui.pet.movement', self.on_movement_event)
        self.world.event_manager.subscribe('state', self.set_state)
        self.world.event_manager.subscribe('world_clock', self.on_clocktick)
        self.animation = None
        self._update_state()

    def _update_state(self):
        state = self.pet_behaviour.get_state()
        animation_name = state.animation
        movement_name = state.movement
        self.world.event_manager.publish('ui.pet.animation', animation_name)
        self.world.event_manager.publish('ui.pet.movement', movement_name)

    def next_state(self):
        self.pet_behaviour.next_state()
        self._update_state()

    def set_state(self, state_name: str):
        self.pet_behaviour.set_state(state_name)
        self._update_state()

    def get_state(self):
        return self.pet_behaviour.get_state()

    def on_position_update(self, position_update: dict[str, Coordinate]):
        old_position = position_update['old_position']
        new_position = position_update['new_position']
        self.current_position = new_position

    def on_animation_event(self, animation: str):
        self.animation = animation
        self.sprite_gui.set_animation(animation)

    def on_movement_event(self, movement_name: str):
        movement = self.movement_factory.build(
            movement_name, self.current_position
        )

        if self.animation is not None:
            self.sprite_gui.set_animation(self.animation)

        self.sprite_gui.set_movement(movement)

    def on_clocktick(self, tick: int) -> str:
        if tick % 5 == 0:
            self.next_state()

    def run(self):
        self.sprite_gui.run()

    def shutdown(self):
        self.sprite_gui.shutdown()
