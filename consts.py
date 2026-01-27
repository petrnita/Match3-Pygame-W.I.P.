import pygame, sys, json
from pygame import Surface, Rect
from pygame.math import Vector2 as vec
from pygame.mixer import Sound
from graphic import ImageSheet

pygame.init()
pygame.mixer.init()


class Slices():
    @classmethod
    def get_positions(cls, filename: str) -> dict[vec]:
        with open(filename, 'r') as file:
            data = json.load(file)
        positions = {}
        for d in data['meta']['slices']:
            bounds = d['keys'][0]['bounds']
            positions[d['name']] = vec(bounds['x'], bounds['y'])
        return positions
    
    @classmethod
    def get_images(cls, filename: str, picture: str) -> list[dict[Surface], dict[Rect]]:
        picture = pygame.image.load(picture)
        with open(filename, 'r') as file:
            data = json.load(file)
        pictures = {}
        rects = {}
        for d in data['meta']['slices']:
            bounds = d['keys'][0]['bounds']
            pictures[d['name']] = Surface.subsurface(picture, Rect(bounds['x'],
                                                                   bounds['y'],
                                                                   bounds['w'],
                                                                   bounds['h']))
            rects[d['name']] = Rect(bounds['x'],
                                    bounds['y'],
                                    bounds['w'],
                                    bounds['h'])
        return [pictures, rects]


class Screen_Layout():
    def __init__(self):
        self._IMAGE: Surface = pygame.image.load('gfx/screen_back.png')
        self._WIDTH: int = self.IMAGE.get_width()
        self._HEIGHT: int = self.IMAGE.get_height()
        self._SIZE: tuple = (self._WIDTH, self._HEIGHT)
        self._slices: Slices = Slices()
        self._POSITIONS: dict[vec] = self._slices.get_positions('json/screen_layout.json')
        self._ELEMENTS, self._ELEMENTS_RECTS = self._slices.get_images('json/elements.json', 'gfx/elements.png')
        self._TILE_SIZE: vec = vec(self._ELEMENTS_RECTS['gem_1'].w, self._ELEMENTS_RECTS['gem_1'].h)

    @property
    def IMAGE(self) -> Surface:
        return self._IMAGE

    @property
    def SIZE(self) -> tuple:
        return self._SIZE
    
    @property
    def TILE_SIZE(self) -> vec:
        return self._TILE_SIZE
    
    @TILE_SIZE.setter
    def TILE_SIZE(self, value: vec):
        self._TILE_SIZE = value

    @property
    def POSITIONS(self) -> dict[vec]:
        return self._POSITIONS
    
    @property
    def ELEMENTS(self) -> dict[Surface]:
        return self._ELEMENTS
    
    @property
    def ELEMENTS_RECTS(self) -> dict[Rect]:
        return self._ELEMENTS_RECTS
    

class Elements():
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
        self.SKIN_MEDIUM = '#806d5b'


class Game_Props():
    def __init__(self):
        self.BOARD_SIZE = None
        self.NUMBER_OF_GEMS = None


class Txt_Props():
    def __init__(self):
        self.NO_MORE_MOVES = None
        self.PRESS_ANY_KEY = None

SCREEN = Screen_Layout()

COLORS = Colors()

SND_SWAP_BACK = Sound('snd/swap_back.wav')

GAME = Game_Props()
GAME.BOARD_SIZE = vec(8, 8)
GAME.NUMBER_OF_GEMS = 9

GEMS = Elements()
GEMS.SIZE = SCREEN.TILE_SIZE
GEMS.OFFSET = vec(0, GEMS.SIZE.y)
GEMS.SPEED = 480

SELECT = Elements()
SELECT.SIZE = vec(SCREEN.ELEMENTS_RECTS['select_anim_0'].w, SCREEN.ELEMENTS_RECTS['select_anim_0'].h) 
SELECT.OFFSET = vec(SCREEN.POSITIONS['select_offset']-SCREEN.POSITIONS['board']-GEMS.OFFSET)
SELECT.ANIM = ImageSheet('select_anim_', SCREEN.ELEMENTS)
SELECT.SPEED = 32
SELECT.LOOP = True

KILL_GEM = Elements()
KILL_GEM.SIZE = vec(SCREEN.ELEMENTS_RECTS['gem_1'].w, SCREEN.ELEMENTS_RECTS['gem_1'].h)
KILL_GEM.OFFSET = GEMS.OFFSET
KILL_GEM.ANIM = ImageSheet('kill_gem_', SCREEN.ELEMENTS)
KILL_GEM.SPEED = 32
KILL_GEM.LOOP = False

SWAP_DIRS = Elements()
SWAP_DIRS.SIZE = vec(SCREEN.ELEMENTS_RECTS['swap_dir_0'].w, SCREEN.ELEMENTS_RECTS['swap_dir_0'].h)
SWAP_DIRS.OFFSET = vec(SCREEN.POSITIONS['dirs_offset']-SCREEN.POSITIONS['board']-GEMS.OFFSET)
SWAP_DIRS.ANIM = ImageSheet('swap_dir_', SCREEN.ELEMENTS)

TXT_NO_MOVE = Elements()
TXT_NO_MOVE.IMAGE = SCREEN.ELEMENTS['no_move']
TXT_NO_MOVE.OFFSET = SCREEN.POSITIONS['no_move']