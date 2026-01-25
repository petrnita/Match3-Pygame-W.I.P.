import pygame, sys
from pygame import Surface, Rect
from pygame.math import Vector2 as vec
from pygame.mixer import Sound
from graphic import ImageSheet

pygame.init()
pygame.mixer.init()


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


class Screen_Props():
    def __init__(self):
        self.WIDTH = None
        self.HEIGHT = None
        self.TILE_SIZE = None
        self.LEFT = None
        self.RIGHT = None
        self.TOP = None
        self.BOTTOM = None


class Game_Props():
    def __init__(self):
        self.BOARD_SIZE = None
        self.NUMBER_OF_GEMS = None


class Txt_Props():
    def __init__(self):
        self.NO_MORE_MOVES = None
        self.PRESS_ANY_KEY = None


COLORS = Colors()

SND_SWAP_BACK = Sound('snd/swap_back.wav')

TXT = Txt_Props()
TXT.NO_MORE_MOVES = pygame.image.load('gfx/no_more_moves.png')
TXT.PRESS_ANY_KEY = pygame.image.load('gfx/press_any_key.png')

SCREEN = Screen_Props()
SCREEN.WIDTH = 1734
SCREEN.HEIGHT = 1044
SCREEN.TILE_SIZE = vec(96, 96)

BACKGROUND = pygame.image.load('gfx/back.png')

BOARD = Properities()
BOARD.IMAGE = pygame.image.load('gfx/board.png')
BOARD.SIZE = vec(BOARD.IMAGE.get_width(), BOARD.IMAGE.get_height())
SCREEN.LEFT = SCREEN.RIGHT = (BACKGROUND.get_width() - BOARD.SIZE.x) // 2
SCREEN.TOP = SCREEN.BOTTOM = (BACKGROUND.get_height() - BOARD.SIZE.y) // 2
BOARD.OFFSET = vec(SCREEN.LEFT, SCREEN.TOP)

GAME = Game_Props()
GAME.BOARD_SIZE = vec(8, 8)
GAME.NUMBER_OF_GEMS = 7

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