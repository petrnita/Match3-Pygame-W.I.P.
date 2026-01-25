from consts import *
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group, GroupSingle
from random import choice
from screen_data import ScreenLayout
from graphic import ImageSheet
from gem_select import Select_Gem
from swap_gem import Swap_Gem
from match import Match
from graphic import Swap_Dirs
from resources import BoardPosition


class Gem(Sprite):
    def __init__(self, group: Group,
                 gems_img: ImageSheet,
                 board_manager,
                 pos: vec,
                 number: int):
        super().__init__(group)
        self._gems_img: ImageSheet = gems_img
        self._board_manager = board_manager
        self._size: vec = SCR_TILE_SIZE
        self._offset: vec = GEM_OFFSET
        self._bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._new_bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._number: int = number
        self._speed: int = GEM_SPEED
        self._direction: vec = vec()
        self._velocity: vec = self._direction * self._speed
        self._end_moving: bool = True
        self._dist: int = 0
        self._is_falling: bool = False
        self._state: str = 'idle'
        self._frame: int = 0
        self.image: Surface = Surface((GEM_SIZE.x, GEM_SIZE.y), pygame.SRCALPHA)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))
        self.rect: Rect = self.image.get_rect(topleft = self._new_bpos.gfx_pos)

    @property
    def bpos(self) -> BoardPosition:
        return self._bpos
    
    @property
    def new_bpos(self) -> BoardPosition:
        return self._new_bpos
    
    @property
    def number(self) -> int:
        return self._number
    
    @property
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str):
        self._state = value
    
    @property
    def end_moving(self) -> bool:
        return self._end_moving

    def change_pos(self):
        self._direction = vec.normalize(self._new_bpos.pos - self._bpos.pos)
        self._velocity = self._direction * self._speed
        self._end_moving = False

    def reset_state(self):
        self._frame = 0
        self._state = 'idle'
        self.image.fill(TRANSPARENT)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))

    def _fall(self):
        if self._is_falling: return
        if self._bpos.pos.y == GAME_BOARD_SIZE.y-1: return

        dist = 0
        if self._bpos.pos.y >= 0: start = int(self._bpos.pos.y) + 1
        else: start = 0

        for y in range(start, int(GAME_BOARD_SIZE.y)):
            if self._board_manager.board.gems[int(self._bpos.pos.x)][y] == None:
                dist += 1
        if dist == 0: return
        self._new_bpos.pos = self._bpos.pos + vec(0, dist)
        self._board_manager.match_gems.add_to_matching(self)
        self._is_falling = True
        self.change_pos()
        self._state = 'fall'

    def _is_on_target(self) -> bool:
        dx, dy = self._direction
        if dx == 0:
            y = self._new_bpos.gfx_pos.y
            if dy < 0 and self.rect.y < y or dy > 0 and self.rect.y > y:
                self.rect.y = y
                return True
        elif dy == 0:
            x = self._new_bpos.gfx_pos.x
            if dx < 0 and self.rect.x < x or dx > 0 and self.rect.x > x:
                self.rect.x = x
                return True
        return False
    
    def update(self, dt):

        self._fall()

        if self._direction == vec(): return

        self.rect.topleft += self._velocity * dt

        if not self._is_on_target(): return

        self._direction = vec()
        self._bpos.pos = self._new_bpos.pos.copy()
        self._end_moving = True
        self._board_manager.board.gems[int(self._bpos.pos.x)][int(self._bpos.pos.y)] = self
        self._is_falling = False
        self.reset_state()


class Create_Board():
    def __init__(self, board_manager,
                 gems_group: Group):
        self._gems_sheet = ImageSheet(GEMS_IMAGE, GEM_SIZE)
        self._size: vec = GAME_BOARD_SIZE
        self._board_manager = board_manager
        self._nr_of_gems = GAME_NUMBER_OF_GEMS
        self._gems_group: Group = gems_group
        self._gems: list[Gem] = self._make_board()

    @property
    def gems(self) -> list[Gem]:
        return self._gems

    def _make_board(self) -> list[Gem]:
        gems: list[Gem] = [[None for x in range(int(self._size.x))] for y in range(int(self._size.y))]

        for x in range(int(self._size.y)):
            for y in range(int(self._size.x)):
                candidates: list[int] = [nr+1 for nr in range(self._nr_of_gems)]
                if x-2 >= 0:
                    previous_x: list[Gem] = [gems[x-1][y].number, gems[x-2][y].number]
                    if previous_x[0] == previous_x[1]:
                        candidates.remove(previous_x[0])
                if y-2 >= 0:
                    previous_y = [gems[x][y-1].number, gems[x][y-2].number]
                    if previous_y[0] == previous_y[1]:
                        if previous_y[0] in candidates:
                            candidates.remove(previous_y[0])
                gems[x][y] = Gem(self._gems_group, self._gems_sheet, self._board_manager, vec(x, y), choice(candidates))
                                 
        return gems
    
    def add_new_gem(self, pos: vec):
        candidates = [nr+1 for nr in range(GAME_NUMBER_OF_GEMS)]
        return Gem(self._gems_group, self._gems_sheet, self._board_manager, pos, choice(candidates))
    

class Board_Manager():
    def __init__(self, gems_group: Group, screen_layout: ScreenLayout):
        self._gems_group: Group = gems_group
        self._screen_layout: ScreenLayout = screen_layout
        self._board: Create_Board = Create_Board(self, self._gems_group)
        self._select_gem: Select_Gem = Select_Gem()
        self._swapdir_group: GroupSingle = GroupSingle()
        self._pointer_group: GroupSingle = GroupSingle()
        self._anim_group: Group = Group()
        self._swap_gems: Swap_Gem = Swap_Gem(self)
        self._match_gems: Match = Match(self)
        self._overs: list[Gem] = list()
        self._possibles: bool = False

    @property
    def board(self) -> Create_Board:
        return self._board

    @property
    def swapdir_group(self) -> GroupSingle:
        return self._swapdir_group
    
    @property
    def possibles(self) -> bool:
        return self._possibles
    
    @possibles.setter
    def possibles(self, value: bool):
        self._possibles = value

    @property
    def anim_group(self) -> Group:
        return self._anim_group
    
    @property
    def match_gems(self) -> Match:
        return self._match_gems

    def _detect_pointer_with_gem_collision(self, events, game_status):
        if not self._check_moving_of_gems(self._match_gems.set_matching): return

        gem = None
        for _gem in self._gems_group:
            if _gem.rect.collidepoint(*(pygame.mouse.get_pos() - vec(SCR_LEFT, SCR_TOP))):
                gem = _gem

        for event in events:
            if game_status == 'game_over':
                break
            if not self._swap_gems.swaping:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gem != None:
                        self._select_gem.try_select(gem)
                if event.type == pygame.MOUSEBUTTONUP:
                    if gem != None and self._select_gem.selected_gem1 != None and gem != self._select_gem.selected_gem1:
                        self._select_gem.try_select(gem, False)
                if event.type == pygame.MOUSEMOTION:
                    if gem and not gem in self._overs:
                        gem.state = 'over'
                        if len(self._overs) > 0:
                            self._overs[0].state = 'idle'
                            self._overs[0].reset_state()
                        self._overs.clear()
                        self._overs.append(gem)
                    if self._select_gem.selected_gem1 and self._select_gem.is_neighbor(gem):
                        Swap_Dirs(self._swapdir_group, self._select_gem.selected_gem1.bpos,
                                vec(gem.bpos.pos - self._select_gem.selected_gem1.bpos.pos))
                    else:
                        self._swapdir_group.empty()

    def _check_moving_of_gems(self, gems: set[Gem]) -> bool:
        if len(gems) == 0: return True
        for gem in gems:
            if not gem.end_moving:
                return False
        return True
    
    def update(self, events, dt, game_status):
        self._detect_pointer_with_gem_collision(events, game_status)

        self._select_gem.select_group.update(dt)
        self._anim_group.update(dt)
        self._select_gem.select_group.draw(self._screen_layout.top_screen)
        self._swapdir_group.draw(self._screen_layout._top_screen)
        self._anim_group.draw(self._screen_layout._top_screen)

        if self._select_gem.ready_to_swap:
            self._select_gem.ready_to_swap = False
            self._swap_gems.add_gems(self._select_gem.selected_gem1, self._select_gem.selected_gem2)
            self._swap_gems.swap(None)

        if self._swap_gems.swaping:
            if self._check_moving_of_gems([self._swap_gems.gem1, self._swap_gems.gem2]):
                self._match_gems.add_to_matching(self._swap_gems.gem1)
                self._match_gems.add_to_matching(self._swap_gems.gem2)
                if self._match_gems.match():
                    self._swap_gems.swaping = False
                else:
                    self._swap_gems.swap(SND_SWAP_BACK)
                self._swap_gems.clear_swap()
                self._select_gem.clear()

        if self._check_moving_of_gems(self._match_gems.set_matching):
            if len(self._match_gems.set_matching) > 0:
                self._match_gems.match()

        self._gems_group.update(dt)

