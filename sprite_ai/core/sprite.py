from sprite_ai.core.sprite_behaviour import SpriteBehaviour
from sprite_ai.core.world import World
from sprite_ai.gui.sprite_gui import SpriteGui
from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.movement_factory import MovementFactory


class Sprite:
    def __init__(
        self, sprite_gui: SpriteGui, sprite_behaviour: SpriteBehaviour, world: World
    ) -> None:
        self.sprite_gui = sprite_gui
        self.sprite_behaviour = sprite_behaviour
        self.world = world
        width, height = world.world_size
        self.current_position = Coordinate(width // 2, height)
        self.movement_factory = MovementFactory(world.world_size)
        self.sprite_gui.on_position_updated = self.on_position_update

        self.world.event_manager.subscribe(
            'ui.sprite.animation', self.on_animation_event
        )
        self.world.event_manager.subscribe('ui.sprite.movement', self.on_movement_event)
        self.world.event_manager.subscribe('ui.sprite.state', self.set_state)
        self.world.event_manager.subscribe('world.clock', self.on_clocktick)
        self.animation = None
        self._update_state()

    def _update_state(self):
        state = self.sprite_behaviour.get_state()
        animation_name = state.animation
        movement_name = state.movement
        self.world.event_manager.publish('ui.sprite.animation', animation_name)
        self.world.event_manager.publish('ui.sprite.movement', movement_name)

    def next_state(self):
        self.sprite_behaviour.next_state()
        self._update_state()

    def set_state(self, state_name: str):
        self.sprite_behaviour.set_state(state_name)
        self._update_state()

    def get_state(self):
        return self.sprite_behaviour.get_state()

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
