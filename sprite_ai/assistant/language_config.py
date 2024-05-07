from __future__ import annotations
from typing_extensions import Annotated

from pydantic import AfterValidator, BaseModel, ValidationError

from sprite_ai.utils.supported_languages import is_supported_variant_code
from sprite_ai.utils.locations import user_voices_location

def supported_variant_validator(variant_code: str) -> str:
    if not is_supported_variant_code(user_voices_location, variant_code):
        raise ValidationError(f'Unsupported variant code: {variant_code}')
    return variant_code

VariantCode = Annotated[str, AfterValidator(supported_variant_validator)]

class LanguageConfig(BaseModel):
    variant: VariantCode
    speaker: int = 0

    @property
    def dialect_code(self) -> str:
        code = self.variant.split('-')[0]
        return code
    
    @property
    def language_code(self) -> str:
        code = self.variant.split('_')[0]
        return code
