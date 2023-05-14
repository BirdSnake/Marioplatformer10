from pygame import *
import os

import blocks
import pyganim
from MarioPlatformer1.MarioPlatformer import monsters

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = '#888888'

MOVE_EXTRA_SPEED = 2.5
JUMP_EXTRA_POWER = 1
ANIMATION_SUPER_SPEED_DELAY = 0.05

JUMP_POWER = 10
GRAVITY = 0.35

ANIMATION_DELAY = 0.1
BASE_DIR = os.path.dirname(__file__) # Полный путь к каталогу с файлами

ANIMATION_RIGHT = [
    (fr'{BASE_DIR}/mario/r1.png'),
    (fr'{BASE_DIR}/mario/r2.png'),
    (fr'{BASE_DIR}/mario/r3.png'),
    (fr'{BASE_DIR}/mario/r4.png'),
    (fr'{BASE_DIR}/mario/r5.png')
]

ANIMATION_LEFT = [
    (fr'{BASE_DIR}/mario/l1.png'),
    (fr'{BASE_DIR}/mario/l2.png'),
    (fr'{BASE_DIR}/mario/l3.png'),
    (fr'{BASE_DIR}/mario/l4.png'),
    (fr'{BASE_DIR}/mario/l5.png')
]

ANIMATION_JUMP_LEFT = [(fr'{BASE_DIR}/mario/jl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [(fr'{BASE_DIR}/mario/jr.png', 0.1)]

ANIMATION_JUMP = [(fr'{BASE_DIR}/mario/j.png', 0.1)]
ANIMATION_STAY = [(fr'{BASE_DIR}/mario/0.png', 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_vel = 0
        self.start_x = x

        self.y_vel = 0
        self.start_y = y

        self.on_ground = False

        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR)) # Прозрачный фон

        """Анимация движения вправо"""
        bolt_anim = []
        bolt_anim_super_speed = list()
        for animation in ANIMATION_RIGHT:
            bolt_anim.append((animation, ANIMATION_DELAY))
            bolt_anim_super_speed.append((animation, ANIMATION_SUPER_SPEED_DELAY))
        self.bolt_anim_right = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_right.play()

        self.bolt_anim_right_super_speed = pyganim.PygAnimation(bolt_anim_super_speed)
        self.bolt_anim_right_super_speed.play()

        """Анимация движения влево"""
        bolt_anim = []
        bolt_anim_super_speed = list()
        for animation in ANIMATION_LEFT:
            bolt_anim.append((animation, ANIMATION_DELAY))
            bolt_anim_super_speed.append((animation, ANIMATION_SUPER_SPEED_DELAY))
        self.bolt_anim_left = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_left.play()

        self.bolt_anim_left_super_speed = pyganim.PygAnimation(bolt_anim_super_speed)
        self.bolt_anim_left_super_speed.play()

        """Анимация неподвижности"""
        self.bolt_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.bolt_anim_stay.play()
        self.bolt_anim_stay.blit(self.image, (0, 0)) # Стоим по умолчанию

        """Анимация прыжка влево"""
        self.bolt_anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.bolt_anim_jump_left.play()

        """Анимация прыжка вправо"""
        self.bolt_anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.bolt_anim_jump_right.play()

        """Анимация прыжка вверх"""
        self.bolt_anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.bolt_anim_jump.play()

    def update(self, left, right, up, running, platforms):
        if up:
            if self.on_ground:
                self.y_vel = -JUMP_POWER
                if running and (left or right):
                    self.y_vel -= JUMP_EXTRA_POWER
            self.image.fill(Color(COLOR))
            self.bolt_anim_jump.blit(self.image, (0, 0))

        if left:
            self.x_vel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running: # Если ускорены
                self.x_vel -= MOVE_EXTRA_SPEED
                if not up:
                    self.bolt_anim_left_super_speed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.bolt_anim_left.blit(self.image, (0, 0))
            if up:
                self.bolt_anim_jump_left.blit(self.image, (0, 0))

        if right:
            self.x_vel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.x_vel += MOVE_EXTRA_SPEED
                if not up:
                    self.bolt_anim_right_super_speed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.bolt_anim_right.blit(self.image, (0, 0))
            if up:
                self.bolt_anim_jump_right.blit(self.image, (0, 0))

        if not (left or right):
            self.x_vel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.bolt_anim_stay.blit(self.image, (0, 0))

        if not self.on_ground:
            self.y_vel += GRAVITY

        self.on_ground = False
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)

        self.rect.x += self.x_vel
        self.collide(self.x_vel, 0, platforms)

    def collide(self, x_vel, y_vel, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if isinstance(platform, blocks.BlockDie) or isinstance(platform, monsters.Monster):
                    self.die()

                elif isinstance(platform, blocks.BlockTeleport): # Проверка столкновения с телепортом
                    self.teleporting(platform.go_x, platform.go_y)

                if x_vel > 0:
                    self.rect.right = platform.rect.left
                if x_vel < 0:
                    self.rect.left = platform.rect.right

                if y_vel > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.y_vel = 0

                if y_vel < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

    def die(self):
        time.wait(500)
        self.teleporting(self.start_x, self.start_y)

    def teleporting(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y