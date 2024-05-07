from pathlib import Path
from typing import Any
from faster_whisper.tokenizer import _LANGUAGE_CODES
from piper.download import get_voices
from pydantic import BaseModel


class PiperLanguageInfo(BaseModel):
    code: str
    family: str
    region: str
    name_native: str
    name_english: str
    country_english: str

class PiperVoiceInfo(BaseModel):
    key: str
    name: str
    language: PiperLanguageInfo
    quality: str
    num_speakers: int
    files: dict[str, dict[str, Any]]
    aliases: list[str]

class SupportedVariantInfo(BaseModel):
    code: str
    n_speakers: int

class SupportedDialectInfo(BaseModel):
    name: str
    code: str
    variants: dict[str, SupportedVariantInfo] = {}

class SupportedLanguageInfo(BaseModel):
    name: str
    code: str
    dialects: dict[str, SupportedDialectInfo] = {}



def get_tts_voices(download_dir: str|Path) -> dict[str, PiperVoiceInfo]:
    tts_voices_info = get_voices(download_dir)
    tts_voices_info = {
        voice_id: PiperVoiceInfo.model_validate(voice_info)
        for voice_id, voice_info in tts_voices_info.items()
    }
    return tts_voices_info

def get_tts_languages(download_dir: str|Path) -> set[str]:
    tts_voices = get_tts_voices(download_dir)
    tts_languages = {
        voice_info.language.family
        for voice_info 
        in tts_voices.values()
    }   
    return tts_languages

def get_stt_languages() -> set[str]:
    stt_languages = set(_LANGUAGE_CODES)
    return stt_languages

def get_supported_languages_codes(download_dir: str|Path) -> set[str]:
    download_dir = str(Path(download_dir).absolute())
    stt_languages = get_stt_languages()
    tts_languages = get_tts_languages(download_dir)
    supported_languages_codes = stt_languages.intersection(tts_languages)
    return supported_languages_codes

def get_supported_languages(download_dir: str|Path) -> dict[str,SupportedLanguageInfo]:
    supported_languages_codes = get_supported_languages_codes(download_dir)
    tts_voices = get_tts_voices(download_dir)
    supported_languages = {}

    for voice_info in tts_voices.values():
        language_code = voice_info.language.family
        if language_code not in supported_languages_codes:
            continue

        try:
            language = supported_languages[language_code]
        except KeyError:
            language = SupportedLanguageInfo(
                name=voice_info.language.name_english,
                code=language_code,
            )
            supported_languages[language_code] = language

        dialect_code = voice_info.language.region
        try:
            dialect = language.dialects[dialect_code]
        except KeyError:
            dialect = SupportedDialectInfo(
                name=voice_info.language.country_english,
                code=dialect_code,
            )
            language.dialects[dialect_code] = dialect
        
        variant_code = voice_info.key
        try:
            variant = dialect.variants[variant_code]
        except KeyError:
            variant = SupportedVariantInfo(
                code=variant_code,
                n_speakers=voice_info.num_speakers,
            )
            dialect.variants[variant_code] = variant

    return supported_languages
    
def display_supported_languages(download_dir: str|Path):
    supported_languages = get_supported_languages(download_dir)
    last_language = ''
    last_dialect = ''
    display_buffer = ''
    language_padding = 15
    dialect_padding = 35
    variation_padding = 35
    n_speakers_padding = 15

    display_buffer += f'| {"Language":<{language_padding}}| {"Dialect":<{dialect_padding}}| {"Variant":<{variation_padding}}| {"Num Speakers":<{n_speakers_padding}}|\n'
    display_buffer += f'|-{"-"*language_padding}|-{"-"*dialect_padding}|-{"-"*variation_padding}|-{"-"*n_speakers_padding}|\n'

    supported_languages = sorted(supported_languages.values(), key=lambda supported_language: supported_language.name)
    for supported_language in supported_languages:
        dialects = sorted(supported_language.dialects.values(), key=lambda dialect: dialect.name)

        for dialect in dialects:
            variants = sorted(dialect.variants.values(), key=lambda variant: variant.code)
            for variant in variants:
                language_name = ''
                dialect_name = ''

                if supported_language.name != last_language:
                    last_language = supported_language.name
                    language_name = supported_language.name
                
                if dialect.name != last_dialect:
                    last_dialect = dialect.name
                    dialect_name = dialect.name
                
                n_speakers = variant.n_speakers
                display_buffer += f'| {language_name:<{language_padding}}| {dialect_name:<{dialect_padding}}| {variant.code:<{variation_padding}}| {n_speakers:<{n_speakers_padding}}|\n'
    
    return display_buffer

def is_supported_language(download_dir: str|Path, language_code: str) -> bool:
    return language_code in get_supported_languages(download_dir)

def is_supported_variant_code(download_dir: str|Path, variant_code: str):
    return variant_code in get_tts_voices(download_dir)