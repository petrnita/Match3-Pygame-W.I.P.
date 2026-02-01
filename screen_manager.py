import pygame
from pygame import Surface
from consts import COLORS, SCREEN


class Screen_Manager():
    def __init__(self):
        self.Main = pygame.display.set_mode(SCREEN.SIZE)
        pygame.display.set_caption('Match-3 game tutorial 2026 > Petr Nita <')
        self.Board = Surface((SCREEN.ELEMENTS_RECTS['board'].w, SCREEN.ELEMENTS_RECTS['board'].h)).convert_alpha()
        self.Anim = self.Board.copy().convert_alpha()
        self.Top = self.Main.copy().convert_alpha()
        self.debug_shuffle = False

    def paint_screen(self):
        self.Main.blit(SCREEN.IMAGE, (0, 0))
        self.Board.fill(COLORS.TRANSPARENT)
        self.Anim.fill(COLORS.TRANSPARENT)
        self.Top.fill(COLORS.TRANSPARENT)
        
    def draw(self):
        self.Main.blit(self.Board, SCREEN.POSITIONS['board'])
        self.Main.blit(self.Anim, SCREEN.POSITIONS['board'])
        self.Main.blit(SCREEN.ELEMENTS['title'], SCREEN.POSITIONS['title'])
        self.Main.blit(self.Top, (0, 0))



# debug
        pygame.display.flip()
        if self.debug_shuffle:
            self.debug_shuffle = False
            self.print_screen()

    def print_screen(self):
        image = self.Main.subsurface(SCREEN.POSITIONS_RECTS['board'])
        pygame.image.save(image, 'gfx/screenshot.png')


