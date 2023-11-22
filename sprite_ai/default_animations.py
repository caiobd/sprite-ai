from sprite_ai.sprite_sheet.animation import Animation

ANIMATIONS = {
    "idle": Animation(0, 0, 0.2),
    "walking": Animation(0, 3, 0.2),
    "jumping": Animation(2, 4, 0.2),
    "playing": Animation(30, 33, 0.2),
    "sliding": Animation(19, 21, 0.2),
    "thinking": Animation(14, 17, 0.2),
    "appearing": Animation(26, 29, 1),
    "playing": Animation(29, 33, 0.2),
    "walking_upright": Animation(33, 36, 0.2),
    "laying_down": Animation(17, 17, 0.2),
}
