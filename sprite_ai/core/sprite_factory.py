from importlib import resources
from typing import Callable
import imagesize

from sprite_ai.core.sprite import Sprite
from sprite_ai.profile.sprite_profile_config import SpriteProfileConfig
from sprite_ai.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from sprite_ai.defaults.default_states import POSSIBLE_STATES
from sprite_ai.defaults.default_profiles import PROFILES


class SpriteFactory:
    def build(
        self,
        profile_config: SpriteProfileConfig,
        screen_size: tuple[int, int],
        on_clicked: Callable,
        icon_location: str = '',
    ) -> Sprite:
        sprite_profile = PROFILES[profile_config.name]
        sprite_sheet_file_name = f'{sprite_profile.name}.png'
        sprite_sheet_location = str(
            resources.path(
                'sprite_ai.resources.sprites', sprite_sheet_file_name
            )
        )
        width, height = imagesize.get(sprite_sheet_location)
        sprite_sheet_metadata = SpriteSheetMetadata(
            sprite_sheet_location,
            width,
            height,
            sprite_profile.sprite_sheet_columns,
            sprite_profile.sprite_sheet_rows,
        )
        sprite = Sprite(
            screen_size,
            sprite_sheet_metadata,
            sprite_profile.animations,
            POSSIBLE_STATES,
            'appearing',
            on_clicked,
            icon_location,
        )

        return sprite
