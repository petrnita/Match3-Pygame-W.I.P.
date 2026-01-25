from consts import *


class ScreenLayout():
    def __init__(self):
        self._screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
        pygame.display.set_caption('Match-3 game tutorial 2026 > Petr Nita <')
        self._board_screen: Surface = Surface((BOARD.SIZE.x, BOARD.SIZE.y), pygame.SRCALPHA)
        self._top_screen: Surface = self._screen.copy().convert_alpha()
    
    @property
    def screen(self) -> Surface:
        return self._screen
    
    @property
    def board_screen(self) -> Surface:
        return self._board_screen
    
    @property
    def top_screen(self) -> Surface:
        return self._top_screen