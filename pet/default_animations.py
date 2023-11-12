from pet.sprite_sheet.animation import Animation

ANIMATIONS = {
    "idle": Animation(0, 0, 0.2),
    "walking": Animation(0, 3, 0.2),
    "jumping": Animation(2, 4, 0.2),
    "playing": Animation(30, 33, 0.2),
    "sliding": Animation(19, 21, 0.2),
    "thinking": Animation(14, 17, 0.2),
    "appearing": Animation(26, 29, 2),
}