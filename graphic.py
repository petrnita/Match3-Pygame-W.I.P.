import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group, GroupSingle
from pygame.math import Vector2 as vec
from consts import *
from resources import BoardPosition

pygame.init()

class ImageSheet():
    def __init__(self, sheet_img: Surface, frame_size: vec):
        self._sheet_img: Surface = sheet_img
        self._frame_size: vec = frame_size
        self._sheet = []
        self._frames = self._sheet_img.get_width() // int(self._frame_size.x)
        for x in range(self._frames):
            clip: Surface = Surface.subsurface(self._sheet_img, (x*self._frame_size.x, 0, self._frame_size.x, self._frame_size.y))
            self._sheet.append(clip)

    @property
    def frames(self) -> int:
        return self._frames
    
    @property
    def sheet(self) -> list[Surface]:
        return self._sheet
    

class Animation(Sprite):
    def __init__(self, group: Group | GroupSingle,
                 pos: vec,
                 speed: int,
                 offset: vec=vec(),
                 loop: bool=False):
        super().__init__(group)
        self._pos: vec = pos
        self._offset: vec = offset
        self._speed: int = speed
        self._loop: bool = loop
        self._frame: int = 0

    def update(self, dt: float):
        if self._frame < self._frames - 1:
            self._frame += 1 * self._speed * dt
        else:
            self._frame = 0
            if not self._loop: self.kill()

        self.image = self._anim[int(self._frame)].convert_alpha()


class Select(Animation):
    _sheet: ImageSheet = ImageSheet(SELECT_IMAGE, SELECT_SIZE)
    def __init__(self, group: GroupSingle,
                 pos: vec,
                 speed: int,
                 offset: vec=vec(),
                 loop: bool=False):
        super().__init__(group, pos, speed, offset, loop)
        self._anim: list[Surface] = self._sheet.sheet
        self._frames: int = self._sheet.frames
        self.image: Surface = self._anim[0]
        self.rect: Rect = self.image.get_rect(topleft=self._pos+self._offset+vec(SCR_LEFT, 0)+vec(0, SCR_TOP))


class Kill_Gem(Animation):
    _sheet: ImageSheet = ImageSheet(KILL_GEM_IMAGE, KILL_GEM_SIZE)
    def __init__(self, group: Group,
                 pos: BoardPosition,
                 speed: int,
                 offset: vec=vec(),
                 loop: bool=False):
        super().__init__(group, pos, speed, offset, loop)
        self._anim: list[Surface] = self._sheet.sheet
        self._frames: int = self._sheet.frames
        self.image: Surface = self._anim[0]
        self.rect: Rect = self.image.get_rect(topleft=self._pos+self._offset+vec(SCR_LEFT, 0)+vec(0, SCR_TOP))


class Swap_Dirs(Sprite):
    img = SWAP_DIRS_IMAGE
    def __init__(self, group: GroupSingle,
                 pos: BoardPosition,
                 direction: vec):
        super().__init__(group)
        self._gfx: vec = SCR_TILE_SIZE
        self._offset: vec = SWAP_DIRS_OFFSET
        self._pos: BoardPosition = pos
        self._direction: vec = direction
        self.images = ImageSheet(self.img, SWAP_DIRS_SIZE)
        self._dirs: dict[Surface] = {
            '[0, -1]': self.images.sheet[0],
            '[1, 0]': self.images.sheet[1],
            '[0, 1]': self.images.sheet[2],
            '[-1, 0]': self.images.sheet[3]
        }
        self.image: Surface = self._dirs[str(self._direction)]
        self.rect: Rect = self.image.get_rect(topleft=self._pos.gfx_pos+self._offset+vec(SCR_LEFT, 0)+vec(0, SCR_TOP))
