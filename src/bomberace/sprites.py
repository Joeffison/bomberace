import pygame

from bomberace.utils import collide_mask


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self, rect: pygame.Rect, mask: pygame.mask.Mask | None = None) -> bool:
        if not rect.colliderect(self.rect):
            return False

        if mask:
            return collide_mask(self.rect, rect, self.mask, mask)

        return True


class Wall(GameSprite):
    pass


class Brick(GameSprite):
    pass


class Fire(GameSprite):
    pass


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, power=1):
        super().__init__()
        self._animations = animations
        self._power = power

        self._animation_index = 0
        self._animation_tick = 0
        self._explosion_tick = 0

        self._current_animation = self._animations["idle"]
        self.image = self._current_animation[self._animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.exploding = False
        self._on_exploding = []
        self._on_exploded = []
        self.fire = pygame.sprite.Group()

    def update(self):
        animation_cooldown = 5 if not self.exploding else 20
        self._animation_tick += 1
        if self._animation_tick > animation_cooldown:
            self._animation_tick = 0
            self._animation_index += 1

        if not self.exploding:
            self._animation_index %= len(self._current_animation)
            explosion_cooldown = 100
            self._explosion_tick += 1
            if self._explosion_tick >= explosion_cooldown:
                self.start_explosion()
        else:
            if self._animation_index == len(self._current_animation):
                for callback in self._on_exploded:
                    callback()
                return

        self.image = self._current_animation[self._animation_index]
        self.fire.update()

    def start_explosion(self):
        if self.exploding:
            return

        self.exploding = True
        self._current_animation = self._animations["exploding"]
        self._animation_index = 0
        self._animation_tick = 0
        self._explosion_tick = 0
        for callback in self._on_exploding:
            callback()

    def add_fire(self, fire):
        self.fire.add(fire)

    def add_on_exploding_callback(self, callback):
        self._on_exploding.append(callback)

    def add_on_exploded_callback(self, callback):
        self._on_exploded.append(callback)
