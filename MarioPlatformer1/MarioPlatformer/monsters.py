from pygame import *
import pyganim
import os

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = '#2110FF'

BASE_DIR = os.path.dirname(__file__)

ANIMATION_MONSTER_HORYSONTAL = [
    fr'{BASE_DIR}/monsters/fire1.png',
    fr'{BASE_DIR}/monsters/fire2.png',
]

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, max_length_left, max_length_up):
        super().__init__()
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.start_x = x
        self.start_y = y
        self.max_length_left = max_length_left
        self.max_length_up = max_length_up
        self.x_vel = left
        self.y_vel = up
        bolt_anim = list()
        for anim in ANIMATION_MONSTER_HORYSONTAL:
            bolt_anim.append((anim, 0.3))
        self.bolt_anim = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim.play()

    def update(self, platforms):
        self.image.fill(Color(MONSTER_COLOR))
        self.bolt_anim.blit(self.image, (0, 0))

        self.rect.x += self.x_vel
        self.rect.y -= self.y_vel

        self.collide(platforms)

        if abs(self.start_x - self.rect.x) > self.max_length_left:
            self.x_vel = -self.x_vel
        elif abs(self.start_y - self.rect.y) > self.max_length_up:
            self.y_vel = -self.y_vel

    def collide(self, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform) and self != platform:
                self.x_vel = -self.x_vel
                self.y_vel = -self.y_vel

