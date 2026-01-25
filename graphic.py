from consts import *
from pygame import Surface


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
    


