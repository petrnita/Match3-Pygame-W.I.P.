import pygame
from pygame.math import Vector2 as vec

pygame.init()

TRANSPARENT = (0, 0, 0, 0)
BLACK_DARK = '#3b3b3b'
BLACK_LIGHT = '#535353'
SKIN_MEDIUM = '#e8c4a3'

SND_SWAP_BACK = 'snd/swap_back.wav'

SCR_WIDTH = 1734
SCR_HEIGHT = 1044

BACKGROUND = pygame.image.load('gfx/back.png')
BOARD_BACK = pygame.image.load('gfx/board.png')
SCR_LEFT = SCR_RIGHT = (BACKGROUND.get_width() - BOARD_BACK.get_width()) // 2
SCR_TOP = SCR_BOTTOM = (BACKGROUND.get_height() - BOARD_BACK.get_height()) // 2
SCR_TILE_SIZE = vec(96, 96)

GAME_BOARD_SIZE = vec(8, 8)
GAME_NUMBER_OF_GEMS = 7

GEM_SHEET_IMAGE = 'gfx/gems.png'
GEM_SIZE = vec(96, 96)
GEM_OFFSET = vec(12, 12)
GEM_SPEED = 480

SELECT_IMAGE = 'gfx/select_anim.png'
SELECT_SIZE = vec(128, 128)

KILL_GEM_IMAGE = 'gfx/kill_gem.png'
KILL_GEM_SIZE = vec(96, 96)

SWAP_DIRS_IMAGE = 'gfx/swap_dirs.png'
SWAP_DIRS_SIZE = vec(192, 192)
SWAP_DIRS_OFFSET = vec(-48, -48)