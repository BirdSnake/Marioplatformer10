from pygame import *
import os

import pyganim
from player import BASE_DIR

PLATFORM_WIDTH, PLATFORM_HEIGHT = 32, 32
PLATFORM_COLOR = '#FF6262'

ANIMATION_BLOCK_TELEPORT = [
    fr'{BASE_DIR}/blocks/portal2.png',
    fr'{BASE_DIR}/blocks/portal1.png'
]

ANIMATION_PRINCESS = [
    fr'{BASE_DIR}/blocks/princess_l.png',
    fr'{BASE_DIR}/blocks/princess_r.png'
]

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(fr'blocks/platform.png')
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = image.load(fr'blocks/dieBlock.png')


class BlockTeleport(Platform):
    def __init__(self, x, y, go_x, go_y):
        super().__init__(x, y)
        self.go_x = go_x
        self.go_y = go_y
        bolt_anim = list()
        for anim in ANIMATION_BLOCK_TELEPORT:
            bolt_anim.append((anim, 0.3))
        self.bolt_anim = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.bolt_anim.blit(self.image, (0, 0))

class Princess(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        bolt_anim = list()
        for anim in ANIMATION_PRINCESS:
            bolt_anim.append((anim, 0.8))
            self.bolt_anim = pyganim.PygAnimation(bolt_anim)
            self.bolt_anim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.bolt_anim.blit(self.image, (0, 0))