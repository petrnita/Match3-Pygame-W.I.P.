from pygame.math import Vector2 as vec
from consts import *
from graphic import Kill_Gem

class Match():
    def __init__(self, board_manager):
        self._board_manager = board_manager
        self._set_matching: set = set()
        self._threes = 0
        self._horizontal: list[vec] = [vec(-1, 0), vec(), vec(1, 0)]
        self._vertical: list[vec] = [vec(0, -1), vec(), vec(0, 1)]

    @property
    def set_matching(self) -> set:
        return self._set_matching

    def add_to_matching(self, gem):
        self._set_matching.add(gem)
        
    def _get_neighbor(self, gem, offset: vec):
        bound = vec(GAME_BOARD_SIZE.x, GAME_BOARD_SIZE.y)
        if 0 <= gem.bpos.pos.x + offset.x < bound.x and 0 <= gem.bpos.pos.y + offset.y < bound.y:
            return self._board_manager.board.gems[int(gem.bpos.pos.x + offset.x)][int(gem.bpos.pos.y + offset.y)]
        return None
    
    def _three_of_kind(self, gem, axis: list) -> tuple:
        kinds: list = list()
        for neighbor in axis:
            negative = self._get_neighbor(gem, neighbor + axis[0])
            center = self._get_neighbor(gem, neighbor)
            positive = self._get_neighbor(gem, neighbor + axis[2])
            if not None in [negative, center, positive]:
                if negative.number == center.number == positive.number:
                    kinds.extend([negative, center, positive])
        return kinds
    
    def match(self) -> bool:
        ret = False
        set_match = reversed(sorted(self._set_matching, key=lambda gem: gem.bpos.pos.y))
        self._set_matching = set()
        new_gems = {'0': -1, '1': -1, '2': -1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1}
        for gem in set_match:
            self._board_manager.possibles = False
            set_same = set()
            set_same.update(self._three_of_kind(gem, self._horizontal))
            set_same.update(self._three_of_kind(gem, self._vertical))
            if len(set_same) > 2:
                lst_new_gems = list()
                for same in set_same:
                    new_y = new_gems[str(int(same.bpos.pos.x))]
                    new_gem = self._board_manager.board.add_new_gem(vec(same.bpos.pos.x, new_y), lst_new_gems)
                    lst_new_gems.append(new_gem)
                    new_gems[str(int(same.bpos.pos.x))] -= 1
                    Kill_Gem(self._board_manager.anim_group, same.bpos.gfx_pos, 32)
                    same.kill()
                    self._board_manager.board.gems[int(same.bpos.pos.x)][int(same.bpos.pos.y)] = None
                ret = True
        return ret
