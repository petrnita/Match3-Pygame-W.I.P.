import pygame
from pygame import Surface
from pygame.math import Vector2 as vec
from consts import COLORS

class Screen_Props():
    def __init__(self):
        self.width: int = None
        self.height: int = None
        self.tile_size: vec = None
        self.left: int = None
        self.right: int = None
        self.top: int = None
        self.bottom: int = None


class Screen_Layers():
    def __init__(self):
        self.Main: Surface = None
        self.Board: Surface = None
        self.Gems: Surface = None
        self.Anim: Surface = None
        self.Top: Surface = None


class Screen_Manager():
    def __init__(self):
        self.screens = Screen_Layers()
        self.properities = Screen_Props()
        self.properities.width = 1734
        self.properities.height = 1044
        self.properities.tile_size = vec(96, 96)
        self.background: Surface = pygame.image.load('gfx/back.png')
        self.screens.Main = pygame.display.set_mode((self.properities.width, self.properities.height))
        pygame.display.set_caption('Match-3 game tutorial 2026 > Petr Nita <')        
        self.screens.Anim = self.screens.Main.copy().convert_alpha()
        self.screens.Top = self.screens.Main.copy().convert_alpha()
        self.board_image: Surface = pygame.image.load('gfx/board.png')
        self.board_size: vec = vec(self.board_image.get_width(), self.board_image.get_height())
        self.properities.left = self.properities.right = (self.background.get_width() - self.board_size.x) // 2
        self.properities.top = self.properities.bottom = (self.background.get_height() - self.board_size.y) // 2
        self.board_offset: vec = vec(self.properities.left, self.properities.top)      
        self.screens.Board = Surface((self.board_size.x, self.board_size.y), pygame.SRCALPHA)
        self.screens.Board.blit(self.board_image, (0, 0))
        self.screens.Gems = self.screens.Board.copy().convert_alpha()

    def paint_screen(self):
        self.screens.Main.blit(self.background, (0, 0))
        self.screens.Gems.fill(COLORS.TRANSPARENT)
        self.screens.Anim.fill(COLORS.TRANSPARENT)
        self.screens.Top.fill(COLORS.TRANSPARENT)
        

    def draw(self):
        self.screens.Main.blit(self.screens.Board, self.board_offset)
        self.screens.Main.blit(self.screens.Gems, self.board_offset)
        self.screens.Main.blit(self.screens.Anim, (0, 0))
        self.screens.Main.blit(self.screens.Top, (0, 0))

        pygame.display.flip()