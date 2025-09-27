import xml.etree.ElementTree as ElementTree

import pygame

from bomberace import settings


def load_sprite_sheet(path, frame_width, frame_height):
    sprite_sheet = pygame.image.load(path).convert_alpha()
    sheet_rect = sprite_sheet.get_rect()

    frames = []
    for x in range(0, sheet_rect.width, frame_width):
        for y in range(0, sheet_rect.height, frame_height):
            frame = sprite_sheet.subsurface(x, y, frame_width, frame_height)
            frames.append(frame)

    return frames


def load_sprites_row(
    sprite_sheet, frame_width, frame_height, from_x, from_y, num_sprites
):
    frames = []
    for i in range(num_sprites):
        frame = sprite_sheet.subsurface(
            from_x + frame_width * i, from_y, frame_width, frame_height
        )
        frames.append(frame)

    return frames


def split_kenney_sprite_sheet(sprite_sheet_path, sprite_sheet_xml_path):
    sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()

    with open(sprite_sheet_xml_path, "rb") as xml_file:
        root = ElementTree.fromstring(xml_file.read())

    frames = {}
    response = []
    for subtexture in root.findall("SubTexture"):
        name = subtexture.get("name")
        x = int(subtexture.get("x"))
        y = int(subtexture.get("y"))
        width = int(subtexture.get("width"))
        height = int(subtexture.get("height"))

        ratio = width / settings.TILE_SIZE

        # Extract the exact image/frame
        frame = sheet_image.subsurface(x, y, width, height)

        # scale to fit to tile_size
        frame = pygame.transform.scale(frame, (settings.TILE_SIZE, height // ratio))

        # padding = 3
        # frame = frame.subsurface(padding, 20 + padding, 75 - padding, 80 - padding)

        frames[name] = frame
        if "walk" in name:
            response.append(frame)

    return response


def flip_horizontally(images: list[pygame.Surface]):
    for image in images:
        yield pygame.transform.flip(image, True, False)


def collide_mask(
    left: pygame.rect.Rect,
    right: pygame.rect.Rect,
    leftmask: pygame.mask.Mask,
    rightmask: pygame.mask.Mask,
):
    """collision detection between two rects, using masks."""
    xoffset = right[0] - left[0]
    yoffset = right[1] - left[1]

    return leftmask.overlap(rightmask, (xoffset, yoffset))
