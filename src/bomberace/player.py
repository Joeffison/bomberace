import pygame

from bomberace import settings
from bomberace.assets import LOADED_ASSETS
from bomberace.sprites import Bomb
from bomberace.world import World


class Player:
    def __init__(
        self,
        screen: pygame.Surface,
        animations: dict[str, list[pygame.Surface]],
        x: int,
        y: int,
    ):
        self._screen = screen
        self._animations = animations

        self._animation_index = 0
        self._animation_tick = 0
        self._direction = "walking_right"
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bombs = pygame.sprite.Group()
        self.colliding_bomb = None
        self._speed = 2

        # to avoid getting stuck in walls, this is set only once (instead of by image)
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def collision_rect(self) -> pygame.Rect:
        height_ignored = self.rect.height - settings.TILE_SIZE

        return pygame.Rect(
            self.rect.x,
            self.rect.y + height_ignored,
            settings.TILE_SIZE,
            settings.TILE_SIZE,
        )

    @property
    def current_animation(self) -> list[pygame.Surface]:
        return self._animations[self._direction]

    @property
    def image(self):
        return self.current_animation[self._animation_index]

    def update(self, world: World):
        # pygame.draw.rect(self._screen, (255, 255, 255), self.rect, 2)
        dx, dy = 0, 0
        walk_cooldown = 5
        self._animation_tick += 1

        if self._animation_tick > walk_cooldown:
            self._animation_tick = 0
            self._animation_index += 1
            self._animation_index %= len(self.current_animation)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and len(self.bombs) <= 5000:
            bomb_pos = self.get_tile_center()
            bomb = Bomb(bomb_pos[0], bomb_pos[1], LOADED_ASSETS.BOMB_ANIMATIONS)
            if world.add_bomb(bomb):
                self.bombs.add(bomb)
                self.colliding_bomb = bomb

        if key[pygame.K_s]:
            dy = self._speed
        if key[pygame.K_w]:
            dy = -self._speed
        if key[pygame.K_a]:
            dx = -self._speed
            self._direction = "walking_left"
        if key[pygame.K_d]:
            dx = self._speed
            self._direction = "walking_right"

        if self.colliding_bomb and not self.collision_rect.colliderect(
            self.colliding_bomb.rect
        ):
            self.colliding_bomb = None

        my_bombs = [self.colliding_bomb] if self.colliding_bomb else None
        new_x_rect = pygame.Rect(
            self.collision_rect.x + dx,
            self.collision_rect.y,
            settings.TILE_SIZE,
            settings.TILE_SIZE,
        )
        if dx != 0 and (
            world.colliderect(new_x_rect, self.mask)
            or world.collides_with_bombs(new_x_rect, my_bombs)
        ):
            dx = 0

        new_y_rect = pygame.Rect(
            self.collision_rect.x,
            self.collision_rect.y + dy,
            settings.TILE_SIZE,
            settings.TILE_SIZE,
        )
        if dy != 0 and (
            world.colliderect(new_y_rect, self.mask)
            or world.collides_with_bombs(new_y_rect, my_bombs)
        ):
            dy = 0

        self.rect.x += dx
        self.rect.y += dy
        self._screen.blit(self.image, self.rect)

    def get_tile_center(self):
        pos = self.collision_rect.center
        grid_x = pos[0] // settings.TILE_SIZE
        grid_y = pos[1] // settings.TILE_SIZE

        center_x = grid_x * settings.TILE_SIZE + settings.TILE_SIZE // 2
        center_y = grid_y * settings.TILE_SIZE + settings.TILE_SIZE // 2
        return center_x, center_y
