from __future__ import annotations

from pet.core.pet_state import PetState

POSSIBLE_STATES = {
    'appearing': PetState(
        name='idle',
        animation='appearing', 
        movement='idle',
        state_transitions={
            'walking': 1, 
        }
    ),
    'idle': PetState(
        name='idle',
        animation='idle', 
        movement='idle',
        state_transitions={
            'idle': 1/7, 
            'walking': 2/7, 
            'jumping_idle': 2/7, 
            'jumping_walking': 2/7
        }
    ),
    'walking': PetState(
        name='walking',
        animation='walking', 
        movement='walking',
        state_transitions={
            'idle': 2/7, 
            'walking': 1/7, 
            'jumping_idle': 2/7, 
            'jumping_walking': 2/7
        }
    ),
    'jumping_idle': PetState(
        name='jumping_idle',
        animation='walking', 
        movement='walking',
        state_transitions={
            'idle': 2/7, 
            'walking': 1/7, 
            'jumping_idle': 2/7, 
            'jumping_walking': 2/7
        }
    ),
    'jumping_walking': PetState(
        name='jumping_walking',
        animation='jumping', 
        movement='walking',
        state_transitions={
            'idle': 2/7, 
            'walking': 2/7, 
            'jumping_idle': 2/7, 
            'jumping_walking': 1/7
        }
    ),
    'thinking': PetState(
        name='thinking',
        animation='thinking', 
        movement='idle',
        state_transitions={
            'thinking': 1, 
        }
    ),
}
