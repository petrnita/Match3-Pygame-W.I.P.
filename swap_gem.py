import pygame
from pygame.mixer import Sound
from consts import *

pygame.mixer.init()

class Swap_Gem():
    def __init__(self, board_manager):
        self._gem1 = None
        self._gem2 = None
        self._board_manager = board_manager
        self._swaping: bool = False

    @property
    def gem1(self):
        return self._gem1
    
    @property
    def gem2(self):
        return self._gem2

    @property
    def swaping(self) -> bool:
        return self._swaping
    
    @swaping.setter
    def swaping(self, value: bool):
        self._swaping = value

    def add_gems(self, gem1, gem2):
        self._gem1 = gem1
        self._gem2 = gem2

    def swap(self, sound: str=None):
        self._swaping = not self._swaping
        if sound != None:
            SND_SWAP_BACK.play()
        sel1 = (int(self._gem1.bpos.pos.x), int(self._gem1.bpos.pos.y))
        sel2 = (int(self._gem2.bpos.pos.x), int(self._gem2.bpos.pos.y))
        self._board_manager.board.gems[sel1[0]][sel1[1]], self._board_manager.board.gems[sel2[0]][sel2[1]] = self._board_manager.board.gems[sel2[0]][sel2[1]], self._board_manager.board.gems[sel1[0]][sel1[1]]
        self._board_manager.swapdir_group.empty()
        self._gem1.new_bpos.pos = self._gem2.bpos.pos
        self._gem1.change_pos()
        self._gem2.new_bpos.pos = self._gem1.bpos.pos
        self._gem2.change_pos()

    def clear_swap(self):
        self._gem1 = None
        self._gem2 = None
        self._swaping = False