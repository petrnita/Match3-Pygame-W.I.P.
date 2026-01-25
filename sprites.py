from consts import *
from pygame.sprite import Group, GroupSingle, Sprite
from resources import BoardPosition


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
            self._frame += 1 * self._speed * dt
        else:
            self._frame = 0
            if not self._loop: self.kill()

        self.image = self._anim.sheet[int(self._frame)].convert_alpha()


class Swap_Dirs(Sprite):
    img = SWAP_DIRS.IMAGE
    def __init__(self, group: GroupSingle,
                 pos: BoardPosition,
                 direction: vec):
        super().__init__(group)
        self._gfx: vec = SCR_TILE_SIZE
        self._offset: vec = SWAP_DIRS.OFFSET
        self._pos: BoardPosition = pos
        self._direction: vec = direction
        self.images = ImageSheet(self.img, SWAP_DIRS.SIZE)
        self._dirs: dict[Surface] = {
            '[0, -1]': self.images.sheet[0],
            '[1, 0]': self.images.sheet[1],
            '[0, 1]': self.images.sheet[2],
            '[-1, 0]': self.images.sheet[3]
        }
        self.image: Surface = self._dirs[str(self._direction)]
        self.rect: Rect = self.image.get_rect(topleft=self._pos.gfx_pos+self._offset+vec(SCR_LEFT, SCR_TOP))


class Text_Sprite(Sprite):
    def __init__(self, group: Group, pos: vec, image: Surface, blink_speed: int=0):
        super().__init__(group)
        self._pos: vec = pos
        self._blink_speed: int = blink_speed
        self._count = 0
        self._img = image
        self.image: Surface = self._img.convert_alpha()
        self.rect = self.image.get_rect(center = self._pos)

    def update(self, dt):
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


class Fade_In(Sprite):
    def __init__(self, group: Group, speed: int):
        super().__init__(group)
        self._alpha = 0
        self._speed: int = speed
        self.image: Surface = Surface((BOARD_BACK.get_width(), BOARD_BACK.get_height()), pygame.SRCALPHA)
        pygame.draw.rect(self.image, SKIN_MEDIUM, self.image.get_rect())
        self.rect = self.image.get_rect(topleft = (SCR_LEFT, SCR_TOP))
        self.image.set_alpha(self._alpha)

    def update(self, dt):
        if self._alpha < 180:
            self._alpha += self._speed
            self.image.set_alpha(self._alpha)