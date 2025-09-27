import pygame

from bomberace import settings
from bomberace.assets import LOADED_ASSETS
from bomberace.player import Player
from bomberace.world import World

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption("Bomberace - Game by Joeffison")

pygame.mixer.music.set_volume(settings.VOLUME_PERCENTAGE)
pygame.mixer.music.load(settings.MUSIC_PATH)
pygame.mixer.music.play(-1, 0.0, 5000)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)

LOADED_ASSETS.init()

player = Player(
    screen, LOADED_ASSETS.PLAYER1_ANIMATIONS, x=settings.TILE_SIZE, y=settings.TILE_SIZE
)

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 2, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 2, 2, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
world = World(
    screen,
    world_data,
    settings.TILE_SIZE,
    LOADED_ASSETS.WALL_SPRITE,
    LOADED_ASSETS.BRICKS_SPRITE,
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(settings.FPS)
    screen.fill(settings.BACKGROUND_COLOR)

    world.update()
    world.draw()

    player.update(world)
    pygame.display.flip()

pygame.quit()
