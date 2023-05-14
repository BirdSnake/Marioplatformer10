"""Настройки проекта"""
import time

import pygame

pygame.font.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500

FPS = 25
BLOCK = 20
CUP_HEIGHT = BLOCK
CUP_WIDTH = BLOCK // 2

SIDE_FREQ = 0.15
DOWN_FREQ = 0.1

SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK) - 5

FIGURE_WIDTH = 5
FIGURE_HEIGHT = 5

"""Цвета: синий, зеленый, красный, желтый"""
COLORS = ((0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0))

WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK  = (0, 0, 0)

BORDER_COLOR = WHITE
BG_COLOR = BLACK
TXT_COLOR = WHITE
TITLE_COLOR = COLORS[3]
INFO_COLOR = COLORS[0]

LAST_MOVE_DOWN = time.time()
LAST_SIDE_MOVE = time.time()
LAST_FALL = time.time()
GOING_DOWN = False
GOING_LEFT = False
GOING_RIGHT = False
POINTS = 0

BASIC_FONT = pygame.font.SysFont('arial', 20)
BIG_FONT = pygame.font.SysFont('verdana', 45)

FPS_CLOCK = pygame.time.Clock()
DISPLAY_SURF = pygame.display.set_mode(WINDOW_WIDTH, WINDOW_HEIGHT)
