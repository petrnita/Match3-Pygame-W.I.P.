import pygame, sys
from pygame import Surface, Rect
from pygame.math import Vector2 as vec
from pygame.mixer import Sound
from pygame.font import SysFont
from graphic import ImageSheet
from enum import Enum

pygame.init()
pygame.mixer.init()
pygame.font.init()


class Properities():
    def __init__(self):
        self.IMAGE: Surface = None
        self.SIZE: vec = None
        self.ANIM: ImageSheet = None
        self.OFFSET: vec = None
        self.SPEED: int = None
        self.LOOP: bool = None


class Colors():
    def __init__(self):
        self.TRANSPARENT = (0, 0, 0, 0)
        self.SKIN_MEDIUM = '#e8c4a3'

        
COLORS = Colors()

SND_SWAP_BACK = Sound('snd/swap_back.wav')

TXT_NO_MORE_MOVES = pygame.image.load('gfx/no_more_moves.png')
TXT_PRESS_ANY_KEY = pygame.image.load('gfx/press_any_key.png')

SCR_WIDTH = 1734
SCR_HEIGHT = 1044

BACKGROUND = pygame.image.load('gfx/back.png')

BOARD = Properities()
BOARD.IMAGE = pygame.image.load('gfx/board.png')
BOARD.SIZE = vec(BOARD.IMAGE.get_width(), BOARD.IMAGE.get_height())
SCR_LEFT = SCR_RIGHT = (BACKGROUND.get_width() - BOARD.SIZE.x) // 2
SCR_TOP = SCR_BOTTOM = (BACKGROUND.get_height() - BOARD.SIZE.y) // 2
BOARD.OFFSET = vec(SCR_LEFT, SCR_TOP)

SCR_TILE_SIZE = vec(96, 96)

GAME_BOARD_SIZE = vec(8, 8)
GAME_NUMBER_OF_GEMS = 7

GEMS = Properities()
GEMS.IMAGE = pygame.image.load('gfx/gems.png')
GEMS.SIZE = vec(96, 96)
GEMS.OFFSET = vec(12, 12)
GEMS.SPEED = 480

SELECT = Properities()
SELECT.IMAGE = pygame.image.load('gfx/select_anim.png')
SELECT.SIZE = vec(128, 128)
SELECT.ANIM = ImageSheet(SELECT.IMAGE, SELECT.SIZE)
SELECT.OFFSET = vec(-16, -16) + BOARD.OFFSET
SELECT.SPEED = 32
SELECT.LOOP = True

KILL_GEM = Properities()
KILL_GEM.IMAGE = pygame.image.load('gfx/kill_gem.png')
KILL_GEM.SIZE = vec(96, 96)
KILL_GEM.ANIM = ImageSheet(KILL_GEM.IMAGE, KILL_GEM.SIZE)
KILL_GEM.OFFSET = BOARD.OFFSET
KILL_GEM.SPEED = 32
KILL_GEM.LOOP = False

SWAP_DIRS = Properities()
SWAP_DIRS.IMAGE = pygame.image.load('gfx/swap_dirs.png')
SWAP_DIRS.SIZE = vec(192, 192)
SWAP_DIRS.OFFSET = vec(-48, -48)