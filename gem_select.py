from pygame.sprite import GroupSingle
from pygame.math import Vector2 as vec
from consts import SELECT
from sprites import Animation

class Select_Gem():
    def __init__(self):
        from game_assets import Gem
        self._select_group: GroupSingle = GroupSingle()
        self._selected_gem1: Gem = None
        self._selected_gem2: Gem = None
        self._ready_to_swap: bool =  False

    @property
    def select_group(self) -> GroupSingle:
        return self._select_group

    @property
    def selected_gem1(self):
        return self._selected_gem1
    
    @property
    def selected_gem2(self):
        return self._selected_gem2
    
    @property
    def ready_to_swap(self) -> bool:
        return self._ready_to_swap
    
    @ready_to_swap.setter
    def ready_to_swap(self, value: bool):
        self._ready_to_swap = value

    def try_select(self, gem, unselect: bool=True):
        if unselect:
            if gem == self._selected_gem1:
                self._selected_gem1 = None
                self._unselect()
                return
            
        if self._selected_gem1 == None:
            self._selected_gem1 = gem
            self._select()
            return
        
        if self.is_neighbor(gem):
            self._selected_gem2 = gem
            self._ready_to_swap = True
            self._unselect()
        else:
            self._unselect()
            self._selected_gem1 = gem
            self._select()

    def is_neighbor(self, gem) -> bool:
        if gem == None: return False
        if self._selected_gem1.bpos.pos - gem.bpos.pos in [vec(-1, 0), vec(1, 0), vec(0, -1), vec(0, 1)]:
            return True
        return False
    
    def _select(self):
        Animation(self._select_group, self._selected_gem1.bpos.gfx_pos,
                  SELECT.ANIM, SELECT.SPEED, SELECT.OFFSET, SELECT.LOOP)

    def _unselect(self):
        self._select_group.empty()

    def clear(self):
        self._selected_gem1 = None
        self._selected_gem2 = None
        self._ready_to_swap = False