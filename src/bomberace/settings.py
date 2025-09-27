from pathlib import Path

FPS = 60

TILE_SIZE = 50
TILES_X_COUNT = 15
TILES_Y_COUNT = 13

SCREEN_WIDTH = TILES_X_COUNT * TILE_SIZE
SCREEN_HEIGHT = TILES_Y_COUNT * TILE_SIZE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

VOLUME_PERCENTAGE = 1

# assets
ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"

MUSIC_PATH = ASSETS_DIR / "fight.wav"

BRICKS_SPRITES_PATH = ASSETS_DIR / "stone_packed.png"
WALL_SPRITES_PATH = ASSETS_DIR / "rock_packed.png"

# animations
PLAYER1_SPRITES_PATH = ASSETS_DIR / "character_maleAdventurer_sheetHD.png"
PLAYER1_SPRITES_XML_PATH = ASSETS_DIR / "character_maleAdventurer_sheetHD.xml"

## keeping the original file structure to reduce initial setup efforts for others
_BOMB_SPRITES_DIR = (
    ASSETS_DIR
    / "free-no-redistribution"
    / "craftpix-778120-free-robot-sprite"
    / "PNG_Bodyparts&Spriter_Animations"
    / "Robot1"
    / "Bomb"
)
BOMB_SPRITES_PATH = [
    _BOMB_SPRITES_DIR / f"bomb_000{10 - layer_index}_Layer-{layer_index}.png"
    for layer_index in range(1, 11)
]

# Colors
BACKGROUND_COLOR = (132, 198, 105)
