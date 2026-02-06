import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
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

def debug(debug):
    import time
    import numpy
    with open('log.txt', mode='a') as file:
        now = time.strftime('%H:%M:%S', time.gmtime())
        if isinstance(debug, list):
            for row in debug:
                file.writelines(f'{now} > {debug}\n')
        elif isinstance(debug, numpy.ndarray):
            file.writelines(f'{now} >\n')
            file.writelines(f'{debug}\n')
        else:
            file.writelines(f'{now} > {debug}\n')


from rich.console import Console

console = Console()

def log(message: str, headline: str=''):
    if headline != '':
        console.rule(headline, align='left')
    console.log(message)

def clear():
    console.clear()