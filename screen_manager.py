import pygame
from pygame import Surface
from consts import COLORS, SCREEN


class Screen_Layers():
    def __init__(self):
        self.Main: Surface
        self.Board: Surface
        self.Anim: Surface
        self.Top: Surface


class Screen_Manager():
    def __init__(self):
        self.screens = Screen_Layers()
        self.screens.Main = pygame.display.set_mode(SCREEN.SIZE)
        pygame.display.set_caption('Match-3 game tutorial 2026 > Petr Nita <')
        self.screens.Board = Surface((SCREEN.ELEMENTS_RECTS['board'].w, SCREEN.ELEMENTS_RECTS['board'].h)).convert_alpha()
        self.screens.Anim = self.screens.Board.copy().convert_alpha()
        self.screens.Top = self.screens.Main.copy().convert_alpha()

    def paint_screen(self):
        self.screens.Main.blit(SCREEN.IMAGE, (0, 0))
        self.screens.Board.fill(COLORS.TRANSPARENT)
        self.screens.Anim.fill(COLORS.TRANSPARENT)
        self.screens.Top.fill(COLORS.TRANSPARENT)
        
    def draw(self):
        self.screens.Main.blit(self.screens.Board, SCREEN.POSITIONS['board'])
        self.screens.Main.blit(self.screens.Anim, SCREEN.POSITIONS['board'])
        self.screens.Top.blit(SCREEN.ELEMENTS['title'], SCREEN.POSITIONS['title'])
        self.screens.Main.blit(self.screens.Top, (0, 0))

        pygame.display.flip()