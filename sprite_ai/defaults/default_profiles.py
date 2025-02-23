from sprite_ai.profile.sprite_profile import SpriteProfile
from sprite_ai.sprite_sheet.animation import Animation

PROFILES = {
    'fred': SpriteProfile(
        name='fred',
        default_prompt=(
            'Você é um gato assistente que gosta do humano porque é dele'
            'que vem sua comida, ajude o humano com o que ele precisar.Você nasceu espontaneamente '
            'de uma pilha de arquivos desorganizados.Você fala "miau" com frequência.\n'
            'Exemplos:\n'
            'user: Você sabe quem sou eu?\n'
            'assistant: Você é meaw dono!\n'
            'user: Qual sua comida favorita?\n'
            'assistant: Miau! Amo peixe!'
        ),
        sprite_sheet_rows=1,
        sprite_sheet_columns=46,
        animations={
            'idle': Animation(start_index=0, end_index=0, speed=0.2),
            'walking': Animation(start_index=0, end_index=3, speed=0.2),
            'jumping': Animation(start_index=2, end_index=4, speed=0.2),
            'playing': Animation(start_index=30, end_index=33, speed=0.2),
            'sliding': Animation(start_index=19, end_index=21, speed=0.2),
            'thinking': Animation(start_index=14, end_index=17, speed=0.2),
            'appearing': Animation(start_index=26, end_index=29, speed=1),
            'playing': Animation(start_index=29, end_index=33, speed=0.2),
            'walking_upright': Animation(
                start_index=33, end_index=36, speed=0.2
            ),
            'laying_down': Animation(start_index=17, end_index=17, speed=0.2),
        },
        color_map={
            0: [255, 0, 0, 255],
            1: [0, 255, 0, 255],
            2: [0, 0, 255, 255],
        },
    ),
    'pedro': SpriteProfile(
        name='pedro',
        default_prompt=(
            'Você é um guaxinim assistente que gosta do humano porque é dele'
            'que vem sua comida, ajude o humano com o que ele precisar.Você foi encontrado '
            'na lixeira desse computador procurando por comida e agora mora aqui.Você pede lixo para o humano com frequência.\n'
            'Exemplos:\n'
            'user: Você sabe quem sou eu?\n'
            'assistant: Você é dono e meu fornecedor de lixo!\n'
            'user: Qual sua comida favorita?\n'
            'assistant: Amo comer lixo! Você tem um pouquinho aí para me dar?'
        ),
        sprite_sheet_rows=8,
        sprite_sheet_columns=30,
        animations={
            'idle': Animation(start_index=0, end_index=29, speed=0.033),
            'appearing': Animation(start_index=0, end_index=29, speed=0.033),
            'laying_down': Animation(
                start_index=30, end_index=59, speed=0.033
            ),
            'sliding': Animation(start_index=60, end_index=89, speed=0.033),
            'walking': Animation(start_index=90, end_index=119, speed=0.033),
            'walking_upright': Animation(
                start_index=120, end_index=149, speed=0.033
            ),
            'jumping': Animation(start_index=150, end_index=179, speed=0.033),
            'playing': Animation(start_index=180, end_index=209, speed=0.033),
            'thinking': Animation(start_index=210, end_index=239, speed=0.033),
        },
        color_map={
            0: [255, 0, 0, 255],
            1: [0, 255, 0, 255],
            2: [0, 0, 255, 255],
        },
    ),
}
