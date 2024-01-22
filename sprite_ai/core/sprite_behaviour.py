from sprite_ai.core.sprite_state import SpriteState


class SpriteBehaviour:
    def __init__(
        self, possible_states: dict[str, SpriteState], first_state: str
    ) -> None:
        self.possible_states = possible_states
        self.current_state = possible_states[first_state]

    def next_state(self):
        next_state_name = self.current_state.next()
        self.set_state(next_state_name)

    def set_state(self, state_name):
        state = self.possible_states[state_name]
        self.current_state = state

    def get_state(self) -> SpriteState:
        return self.current_state
