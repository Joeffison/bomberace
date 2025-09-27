import logging

import pygame

from bomberace.sprites import Brick, Fire, Wall

logger = logging.getLogger(__name__)


class World:
    def __init__(self, screen, level_data, tile_size, wall, brick):
        self._screen = screen
        self._level_data = level_data
        self._tile_size = tile_size
        self._wall = wall
        self._brick = brick
        self.walls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()

        self.setup_world()

    def setup_world(self):
        for y, row in enumerate(self._level_data):
            for x, tile in enumerate(row):
                coordinates = (x * self._tile_size, y * self._tile_size)
                if tile == 1:
                    wall = Wall(coordinates[0], coordinates[1], self._wall)
                    self.walls.add(wall)
                elif tile == 2:
                    brick = Brick(coordinates[0], coordinates[1], self._brick)
                    self.bricks.add(brick)
                elif tile != 0:
                    logger.error(f"Unknown tile type {tile}")
                    continue

    def draw(self):
        self.walls.draw(self._screen)
        self.bricks.draw(self._screen)
        self.bombs.draw(self._screen)

        for bomb in self.bombs:
            bomb.fire.draw(self._screen)

    def add_bomb(self, bomb) -> bool:
        if self.collides_with_bombs(bomb.rect):
            return False

        self.bombs.add(bomb)

        bomb.add_on_exploding_callback(lambda: self._on_bomb_exploding(bomb))
        bomb.add_on_exploded_callback(lambda: self._on_bomb_exploded(bomb))
        return True

    def _on_bomb_exploding(self, bomb):
        fire_rects = [
            pygame.Rect(
                bomb.rect.x,
                bomb.rect.y + self._tile_size,
                self._tile_size,
                self._tile_size,
            ),
            pygame.Rect(
                bomb.rect.x,
                bomb.rect.y - self._tile_size,
                self._tile_size,
                self._tile_size,
            ),
            pygame.Rect(
                bomb.rect.x + self._tile_size,
                bomb.rect.y,
                self._tile_size,
                self._tile_size,
            ),
            pygame.Rect(
                bomb.rect.x - self._tile_size,
                bomb.rect.y,
                self._tile_size,
                self._tile_size,
            ),
        ]

        for rect in fire_rects:
            collides_with_walls = any(wall for wall in self.walls if wall.collide(rect))
            if not collides_with_walls:
                fire = Fire(rect.x, rect.y, bomb._animations["fire"][0])
                bomb.add_fire(fire)

    def _on_bomb_exploded(self, bomb):
        pygame.sprite.groupcollide(bomb.fire, self.bricks, True, True)
        self.bombs.remove(bomb)

    def colliderect(
        self, rect: pygame.Rect, mask: pygame.mask.Mask
    ) -> pygame.sprite.Sprite | None:
        for wall in self.walls:
            if wall.collide(rect, mask):
                return wall

        for brick in self.bricks:
            if brick.collide(rect, mask):
                return brick

        return None

    def collides_with_bombs(self, rect: pygame.Rect, mybombs: list = None) -> bool:
        bombs = self.bombs
        if mybombs:
            bombs = (bomb for bomb in self.bombs if bomb not in mybombs)

        return any(bomb for bomb in bombs if bomb.rect.colliderect(rect))

    def update(self):
        self.bombs.update()
