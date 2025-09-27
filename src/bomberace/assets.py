import pygame

from bomberace import settings, utils


class LoadedAssets:
    PLAYER1_ANIMATIONS: dict[str, list]
    BOMB_ANIMATIONS: dict[str, list]

    WALL_SPRITE: pygame.Surface
    BRICKS_SPRITE: pygame.Surface

    def init(self):
        self.PLAYER1_ANIMATIONS = self._build_player_animations()
        self.BOMB_ANIMATIONS = self._build_bomb_animations()

        self.WALL_SPRITE = self._load_wall_sprite()
        self.BRICKS_SPRITE = self._load_bricks_sprite()

    @staticmethod
    def _build_player_animations() -> dict[str, list]:
        animations = {
            "walking_right": utils.split_kenney_sprite_sheet(
                settings.PLAYER1_SPRITES_PATH, settings.PLAYER1_SPRITES_XML_PATH
            )
        }

        flipped_walking_images = utils.flip_horizontally(animations["walking_right"])
        animations["walking_left"] = list(flipped_walking_images)

        return animations

    def _build_bomb_animations(self) -> dict[str, list]:
        return {
            "idle": [
                self._load_image_to_fit(bomb_sprite)
                for bomb_sprite in settings.BOMB_SPRITES_PATH[:2]
            ],
            "exploding": [
                self._load_image_to_fit(bomb_sprite)
                for bomb_sprite in settings.BOMB_SPRITES_PATH[2:]
            ],
            "fire": [self._load_image_to_fit(settings.BOMB_SPRITES_PATH[-2])],
        }

    @staticmethod
    def _load_image_to_fit(path):
        image = pygame.image.load(path).convert_alpha()

        # discard any transparency to save on what has to be scaled
        rect = image.get_bounding_rect()
        cropped_image = image.subsurface(rect)

        return pygame.transform.scale(
            cropped_image, (settings.TILE_SIZE, settings.TILE_SIZE)
        )

    @staticmethod
    def _load_wall_sprite():
        wall_sprite_sheet = pygame.image.load(
            settings.WALL_SPRITES_PATH
        ).convert_alpha()

        sprite_size = 18
        wall = utils.load_sprites_row(
            wall_sprite_sheet, sprite_size, sprite_size, 0, sprite_size * 2, 1
        )[0]

        return pygame.transform.scale(wall, (settings.TILE_SIZE, settings.TILE_SIZE))

    @staticmethod
    def _load_bricks_sprite():
        bricks_sprite_sheet = pygame.image.load(
            settings.BRICKS_SPRITES_PATH
        ).convert_alpha()

        sprite_size = 18
        brick = utils.load_sprites_row(
            bricks_sprite_sheet,
            sprite_size,
            sprite_size,
            sprite_size * 8,
            sprite_size * 2,
            1,
        )[0]

        return pygame.transform.scale(brick, (settings.TILE_SIZE, settings.TILE_SIZE))


LOADED_ASSETS = LoadedAssets()
