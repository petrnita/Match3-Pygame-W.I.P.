import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2 as vec
import numpy as np
from consts import COLORS, SCREEN, GEMS
from resources import BoardPosition
from graphic import ImageSheet
    

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
        self.rect: Rect = self.image.get_rect(topleft=self._pos.gfx_pos+self._offset)


class Bar(Sprite):
    def __init__(self, group: Group, img_sheet: dict[Surface], bar_type: str, player: str, bar_color: str=''):
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