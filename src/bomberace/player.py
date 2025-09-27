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

        self._speed = 2

        self.bombs = pygame.sprite.Group()
        self.colliding_bombs = pygame.sprite.Group()

        # to avoid getting stuck in walls, this is set only once (instead of by image)
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def collision_rect(self) -> pygame.Rect:
        height_ignored = self.rect.height - settings.TILE_SIZE

        return pygame.Rect(
            self.rect.x,
            self.rect.y + height_ignored,
            self.rect.width - 10,
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

        self._update_colliding_bombs()

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
                self.colliding_bombs.add(bomb)

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

        # checking collisions separately so diagonals won't block movement
        dx, _ = self._validate_no_collisions(world, dx=dx, dy=0)
        _, dy = self._validate_no_collisions(world, dx=0, dy=dy)

        dx, dy = self._validate_cannot_go_through_previous_bomb(dx, dy)

        self.rect.x += dx
        self.rect.y += dy
        self._screen.blit(self.image, self.rect)

    def _validate_no_collisions(
        self, world: World, dx: int, dy: int
    ) -> tuple[int, int]:
        if dx == 0 and dy == 0:
            return dx, dy

        new_rect = pygame.Rect(
            self.collision_rect.x + dx,
            self.collision_rect.y + dy,
            settings.TILE_SIZE,
            settings.TILE_SIZE,
        )

        if world.colliderect(new_rect) or world.collides_with_bombs(
            new_rect, ignore_bombs=self.colliding_bombs
        ):
            dx, dy = 0, 0

        return dx, dy

    def _validate_cannot_go_through_previous_bomb(
        self, dx: int, dy: int
    ) -> tuple[int, int]:
        """
        Prevents moving back when placing multiple bombs.

        Without this, a player could place two consecutive bombs and go back
        through the first one.
        """

        if len(self.colliding_bombs) < 2:
            return dx, dy

        bombs = self.colliding_bombs.sprites()
        last_bomb = bombs[-1]
        previous_bomb = bombs[-2]

        delta_x = previous_bomb.rect.x - last_bomb.rect.x
        if delta_x and (delta_x * dx) > 0:
            dx = 0

        delta_y = previous_bomb.rect.y - last_bomb.rect.y
        if delta_y and (delta_y * dy) > 0:
            dy = 0

        return dx, dy

    def _update_colliding_bombs(self):
        for bomb in self.colliding_bombs:
            if not bomb.rect.colliderect(self.collision_rect):
                self.colliding_bombs.remove(bomb)

    def get_tile_center(self):
        pos = self.collision_rect.center
        grid_x = pos[0] // settings.TILE_SIZE
        grid_y = pos[1] // settings.TILE_SIZE

        center_x = grid_x * settings.TILE_SIZE + settings.TILE_SIZE // 2
        center_y = grid_y * settings.TILE_SIZE + settings.TILE_SIZE // 2
        return center_x, center_y
