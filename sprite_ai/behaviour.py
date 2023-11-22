import random as rd
from dataclasses import asdict, dataclass
from typing import Callable


@dataclass
class Transition:
    event: str
    new_state: str
    chance: float = 1.0

@dataclass
class State:
    name: str
    animation: str
    transitions: dict[str,list[Transition]]

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class Behaviour:
    start_state: str
    states: dict[str,State]
    current_state: State
    on_state_updated: Callable

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
    
    def set_state(self, state: str):
        try:
            self.current_state = self.states[state]
        except KeyError:
            raise ValueError(f'Tried to set invalid state: "{state}"')
    
    def update_state(self, event: str):
        state_transitions = self.current_state.transitions
        transitions = state_transitions.get(event, [])
        new_state = None
        for transition in transitions:
            if transition.chance < rd.random():
                new_state = self.states[transition.new_state]
                self.current_state = new_state
                break
        
