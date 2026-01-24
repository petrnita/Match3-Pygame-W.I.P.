from consts import *
from pygame import Surface
from pygame.sprite import Sprite, GroupSingle


class BoardPosition():
    def __init__(self, pos: vec, tile_size: vec, offset: vec=vec()):
        self._pos: vec = pos
        self._tile_size: vec = tile_size
        self._offset: vec = offset
        self._gfx_pos: vec = vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset

    @property
    def pos(self) -> vec:
        return self._pos
    
    @pos.setter
    def pos(self, value: vec):
        self._pos = value
        self._gfx_pos = vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset

    @property
    def tile_size(self) -> int:
        return self._tile_size
    
    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value

    @property
    def gfx_pos(self) -> vec:
        return vec(self._pos.elementwise()*self._tile_size.elementwise()) + self._offset
    
    @property
    def offset(self) -> vec:
        return self._offset
    

class Mouse_Pointer(Sprite):
    def __init__(self, group: GroupSingle):
        super().__init__(group)
        self._gem = None
        self._pos = pygame.mouse.get_pos() - vec(SCR_LEFT, SCR_TOP)
        self.image = Surface((1, 1))
        self.rect = self.image.get_rect(topleft = self._pos)

    def update(self):
        self._pos = pygame.mouse.get_pos() - vec(SCR_LEFT, SCR_TOP)
        self.rect.topleft = self._pos