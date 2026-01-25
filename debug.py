import pygame
from pygame import Surface
from pygame.sprite import Rect, Sprite, Group
from pygame.math import Vector2 as vec
from pygame.font import SysFont

pygame.font.init()

FPS_FONT = SysFont('Arial', 32, True)

class Show_Text(Sprite):
    def __init__(self, group: Group, text: str, pos: vec):
        super().__init__(group)
        self._text: str = text
        self._pos: vec = pos
        self._color = '#dd2222'
        self.image: Surface = FPS_FONT.render(self._text, True, self._color)
        self.rect: Rect = self.image.get_rect(topleft = self._pos)

    def update(self, text: str):
        self.image = FPS_FONT.render(text, True, self._color)
        self.rect = self.image.get_rect(topleft = self._pos)