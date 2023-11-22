import numpy as np
from loguru import logger
from pydantic import BaseModel


class PetState(BaseModel):
    name: str
    animation: str
    movement: str
    state_transitions: dict

    def next(self) -> str:
        try:
            possible_states = tuple(self.state_transitions.keys())
            probabilities = tuple(self.state_transitions.values())
        except ValueError as e:
            logger.error(e, f"{self.state_transitions = }")

        next_state = np.random.choice(possible_states, p=probabilities)
        return next_state
