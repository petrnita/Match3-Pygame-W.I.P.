import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2 as vec
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w')
logger = logging.getLogger(__name__)

from pygame.font import SysFont

pygame.font.init()
debugfont = SysFont('Arial', 16, True)

class Debug_Rect(Sprite):
    font = pygame.font.SysFont('Arial', 14, True)
    def __init__(self, group: Group, id: int,  pos: tuple, new_pos: vec, velocity: vec):
        super().__init__(group)

        self.update(id, pos, new_pos, '#aa2200', velocity)

    def update(self, id: int, pos: tuple, new_pos: vec, color: str, velocity: float):
        self.image = Surface((96, 96), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect, 2)
        gem_info1 = __class__.font.render(f'{id}', True, '#ffe8e2')
        gem_info2 = __class__.font.render(f'{list(new_pos)}', True, '#ffe8e2')
        gem_info3 = __class__.font.render(f'{list(pos)}', True, '#ffe8e2')
        gem_info4 = __class__.font.render(f'{list(velocity)}', True, '#ffe8e2')
        self.image.blit(gem_info1, (2, 2))
        self.image.blit(gem_info2, (2, 18))
        self.image.blit(gem_info3, (2, 34))
        self.image.blit(gem_info4, (2, 50))
        self.rect.topleft = pos    


class BoardPosition():
    def __init__(self, pos: vec, tile_size: vec, offset: vec=vec()):
        self._pos: vec = pos
        self._tile_size: vec = tile_size
        self._offset: vec = offset
        self._gpos: vec = vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset

    @property
    def pos(self) -> vec:
        return self._pos
    
    @pos.setter
    def pos(self, value: vec):
        self._pos = value
        self._gpos = vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset

    @property
    def tile_size(self) -> int:
        return self._tile_size
    
    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value

    @property
    def gpos(self) -> vec:
        return vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset
    
    @property
    def offset(self) -> vec:
        return self._offset


class ImageSheet():
    def __init__(self, name: str, images: dict[Surface]):
        self._images: dict[Surface] = images
        self._sheet = []
        for key, image in self._images.items():
            if name in key:
                self.sheet.append(image)
        self._frames: int = len(self._sheet)

    @property
    def frames(self) -> int:
        return self._frames
    
    @property
    def sheet(self) -> list[Surface]:
        return self._sheet
    

class Gem(Sprite):
    def __init__(self, group: Group,
                 gems_img: ImageSheet,
                 pos: vec,
                 number: int):
        from consts import IDS, \
                            GEMS
        super().__init__(group)

        self.id = np.random.choice(IDS)
        IDS.remove(self.id)
        self._gems_img: ImageSheet = gems_img
        self._size: vec = GEMS.SIZE
        self._offset: vec = GEMS.OFFSET
        self._bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._new_bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._number: int = number
        self._speed: int = GEMS.SPEED
        self._direction: vec = vec()
        self._velocity: vec = self._direction * self._speed
        self._ready = True
        self._dist: int = 0
        self._is_falling: bool = False
        self._state: str = 'idle'
        self._frame: int = 0
        self.image: Surface = Surface((GEMS.SIZE.x, GEMS.SIZE.y), pygame.SRCALPHA)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))
        idtext = debugfont.render(f' {self.id} ', True, '#ffa4d1', "#141313")
        self.image.blit(idtext, (3, 3))
        self.rect: Rect = self.image.get_rect(topleft = self._new_bpos.gpos)

        #self.debug_rect = Debug_Rect(self._board_manager.swapdir_group, self.id, self.rect.topleft, self._new_bpos.gfx_pos, self._velocity)

    @property
    def bpos(self) -> BoardPosition:
        return self._bpos
    
    @property
    def new_bpos(self) -> BoardPosition:
        return self._new_bpos
    
    @new_bpos.setter
    def new_bpos(self, value: vec):
        self._new_bpos.pos = value
    
    @property
    def number(self) -> int:
        return self._number
    
    @property
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str):
        self._state = value
    
    @property
    def ready(self) -> bool:
        return self._ready
    
    @property
    def posx(self) -> int:
        return int(self._bpos.pos.x)
    
    @property
    def posy(self) -> int:
        return int(self._bpos.pos.y)

    @property
    def gposx(self) -> float:
        return self._bpos._gpos.x
    
    @property
    def gposy(self) -> float:
        return self._bpos._gpos.y
    
    @property
    def pos(self) -> vec:
        return self._bpos.pos
    
    @pos.setter
    def pos(self, value: vec):
        self._bpos.pos = value

    @property
    def gpos(self) -> vec:
        return self._bpos._gpos

    @property
    def newpos(self) -> vec:
        return self._new_bpos.pos
    
    @newpos.setter
    def newpos(self, value: vec):
        self._new_bpos.pos = value

    @property
    def newgpos(self) -> vec:
        return self._new_bpos._gpos

    def change_pos(self):
        self._ready = False
        direction: vec = self._new_bpos.pos - self._bpos.pos
        if vec(direction).length() > 0:
            self._direction = vec.normalize(direction)
        self._velocity = self._direction * self._speed

    def reset_state(self):
        from consts import COLORS
        self._frame = 0
        self._state = 'idle'
        self.image.fill(COLORS.TRANSPARENT)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))

    def _fall(self, board_manager):
        from consts import GAME
        if self._is_falling: return
        if self._bpos.pos.y == GAME.BOARD_SIZE.y-1: return

        dist = 0
        if self._bpos.pos.y >= 0: start = int(self._bpos.pos.y) + 1
        else: start = 0

        for y in range(start, int(GAME.BOARD_SIZE.y)):
            if board_manager.board[int(self._bpos.pos.x)][y] == None:
                dist += 1
        if dist == 0: return
        self._new_bpos.pos = self._bpos.pos + vec(0, dist)
        board_manager.add_to_matching(self)
        self._is_falling = True
        self.change_pos()
        self._state = 'fall'
    
    def __repr__(self):
        return f'({self._number})<{self.id:02}>'
    
    def __rich__(self) -> str:
        return f'([bold cyan]{self._number}[/bold cyan])<[yellow]{self.id:02}[/yellow]>'
    
    def update(self, board_manager, dt):
        idtext = debugfont.render(f' {self.id} ', True, '#ffa4d1', "#141313")
        self.image.blit(idtext, (3, 3))

        self._dt = dt

        self._fall(board_manager)

        current_pos = vec(self.rect.topleft)
        distance = vec().distance_to(self._velocity*dt)
        current_pos.move_towards_ip(self._new_bpos.gpos, distance)
        self.rect.topleft = current_pos

        if not self._ready:
            if self.rect.topleft == (int(self._new_bpos.gpos.x), int(self._new_bpos.gpos.y)):
                self._velocity = vec()
                self._bpos.pos = self._new_bpos.pos.copy()
                board_manager.set_gem_on_position(self, self._bpos.pos)
                self._ready  = True
                self._is_falling = False
                self.reset_state()


class Animation(Sprite):
    def __init__(self, group: Group | GroupSingle,
                 pos: vec,
                 sheet_img: ImageSheet,
                 speed: int,
                 offset: vec=vec(),
                 loop: bool=False):
        super().__init__(group)
        self._pos: vec = pos
        self._offset: vec = offset
        self._speed: int = speed
        self._loop: bool = loop
        self._frame: int = 0
        self._anim: ImageSheet = sheet_img
        self._frames: int = self._anim.frames
        self.image: Surface = self._anim.sheet[0]
        self.rect: Rect = self.image.get_rect(topleft=self._pos+self._offset)

    def update(self, dt: float):
        if self._frame < self._frames - 1:
            self._frame += self._speed * dt
        else:
            self._frame = 0
            if not self._loop: self.kill()
        self.image = self._anim.sheet[int(self._frame)].convert_alpha()


class Swap_Dirs(Sprite):
    def __init__(self, group: GroupSingle,
                 pos: BoardPosition,
                 sheet_img: ImageSheet,
                 offset: vec,
                 direction: vec):
        super().__init__(group)
        self._offset: vec = offset
        self._pos: BoardPosition = pos
        self._sheet_img: ImageSheet = sheet_img.sheet
        self._direction: vec = direction
        self._dirs: dict[Surface] = {
            '[0, -1]': self._sheet_img[0],
            '[1, 0]': self._sheet_img[1],
            '[0, 1]': self._sheet_img[2],
            '[-1, 0]': self._sheet_img[3]
        }
        self.image: Surface = self._dirs[str(self._direction)]
        self.rect: Rect = self.image.get_rect(topleft=self._pos.gpos+self._offset)


class Bar(Sprite):
    def __init__(self, group: Group, img_sheet: dict[Surface], bar_type: str, player: str, bar_color: str=''):
        from consts import SCREEN
        super().__init__(group)
        
        self._image_sheet: dict[Surface] = img_sheet
        self._bar_type: str = bar_type
        self._player: str = player
        self._scale = 264/100 if player in ['player', 'cpu'] else 752/100
        self._value: int = 100
        self._old_value: int = 0
        self._min_value: int = -300 if player in ['player', 'time'] else 300
        self._empty: bool = False
        self._direction: int = 1 if player in ['player', 'time'] else -1 
        self._pos: vec = SCREEN.POSITIONS[f'{self._player}_bar_{bar_color}']
        self._img_back: Surface = self._image_sheet[f'{bar_type}_bar_back']
        self._img_progress: Surface = self._image_sheet[f'{bar_type}_bar_{bar_color}']
        self._img_top: Surface = self._image_sheet[f'{bar_type}_bar_top']
        self._img_empty: Surface = self._image_sheet[f'{bar_type}_bar_empty']
        self.image: Surface = Surface(self._img_top.get_size(), pygame.SRCALPHA)
        self.rect: Rect = self.image.get_rect(topleft=self._pos)
        self._empty_image = self.image.copy()
        self._empty_image.blit(self._img_back, (0, 0))

    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = value

    def update(self, dt):
        if self._old_value != self._value:
            if self._empty:
                self._empty = False    
            if self._value > 0:
                bar_width = self._scale * self._value
                offset = (-self._direction * self._scale * 100) + bar_width * self._direction 
            else:
                self._empty = True
            
            if not self._empty:
                self.image = self._empty_image.copy()
                self.image.blit(self._img_progress, (offset, 0))
            else:
                self.image.blit(self._img_empty, (0, 0))
            self.image.blit(self._img_top, (0, 0))
            self._old_value = self._value

class Player_Text(Sprite):
    def __init__(self, group: Group, pos: vec, player: str):
        from consts import SCREEN
        super().__init__(group)
        self._pos: vec = pos
        self._player: str = player
        self._images: dict[Surface] = {
            'default': SCREEN.ELEMENTS[self._player],
            'active': SCREEN.ELEMENTS[f'{self._player}_active']
        }
        self._img: str = 'default'
        self.image: Surface = self._images[self._img].convert_alpha()
        self.rect: Rect = self.image.get_rect(topleft=self._pos)

    def update(self, dt):
        pass

    def swap_image(self):
        self._img = 'default' if self._img == 'active' else 'active'
        self.image = self._images[self._img]


class Text_Fade(Sprite):#
    def __init__(self, group: Group,
                 pos: vec,
                 image: Surface,
                 size_speed: int,
                 fade_speed: int,
                 size_direction: str='grow',
                 fade_direction: str='In',
                 blink_speed: int=0):
        super().__init__(group)
        self._center: vec = vec(pos.x + image.get_width()//2, pos.y + image.get_height()//2)
        self._blink_speed: int = blink_speed
        self._count = 0
        self._img: Surface = image
        if fade_direction == 'In':
            self._fade_direction = fade_speed
            self._alpha = 0
            self._stop_alpha = 255
        else:
            self._fade_direction = -fade_speed
            self._alpha = 255
            self._stop_alpha = 0

        if size_direction == 'grow':
            self._size_direction = size_speed
            self._scale: int = 1
        else:
            self._size_direction = -size_speed
            self._scale: int = 1

        self.image: Surface = self._img.convert_alpha()
        self.rect = self.image.get_rect(center = self._center)

    def update(self, dt):
        if self._alpha * np.sign(self._fade_direction) < self._stop_alpha:    
            self.image = pygame.transform.scale_by(self._img, self._scale).convert_alpha()
            self.image.set_alpha(self._alpha)
            self.rect = self.image.get_rect(center = self._center)
            self._scale += self._size_direction
            self._alpha += self._fade_direction
        else:
            if self._fade_direction < 0:
                self.kill()            

        if self._blink_speed > 0:
            if self._count < self._blink_speed:
                self._count += 1
            else:
                self._count = 0
                if self.image.get_size() == (1, 1):
                    self.image = self._img.convert_alpha()
                    self.rect = self.image.get_rect(center = self._pos)
                else:
                    self.image = Surface((1, 1))




class Fade(Sprite):
    def __init__(self, group: Group, speed: int, direction: str='In'):
        from consts import SCREEN, COLORS, GEMS
        super().__init__(group)
        if direction == 'In':
            self._direction = speed
            self._alpha = 0
            self._stop_alpha = 180
        else:
            self._direction = -speed
            self._alpha = 180
            self._stop_alpha = 0
        self.image: Surface = Surface((SCREEN.SIZE-vec(0, SCREEN.TILE_SIZE.y)), pygame.SRCALPHA)
        self.image.set_alpha(self._alpha)
        pygame.draw.rect(self.image, COLORS.SKIN_MEDIUM, self.image.get_rect())
        self.rect = self.image.get_rect(topleft = GEMS.OFFSET)
        

    def update(self, dt):
        if self._alpha * np.sign(self._direction) < self._stop_alpha:
            self._alpha += self._direction
            self.image.set_alpha(self._alpha)
            return
        
        if self._direction < 0: self.kill()