from consts import IDS, MOUSE_OFFSET, COLORS, SCREEN, SND_SWAP_BACK, GEMS, GAME, SWAP_DIRS
import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group, GroupSingle
from pygame.math import Vector2 as vec
from random import choice
from screen_manager import Screen_Manager
from gem_select import Select_Gem
from swap_gem import Swap_Gem
from match import Match
from sprites import Swap_Dirs, Debug_Rect
from graphic import ImageSheet
from resources import BoardPosition
import numpy


class Gem(Sprite):
    def __init__(self, group: Group,
                 gems_img: ImageSheet,
                 board_manager,
                 pos: vec,
                 number: int):
        super().__init__(group)

        self.id = choice(IDS)
        IDS.remove(self.id)
        self._gems_img: ImageSheet = gems_img
        self._board_manager = board_manager
        self._size: vec = GEMS.SIZE
        self._offset: vec = GEMS.OFFSET
        self._bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._new_bpos: BoardPosition = BoardPosition(pos, self._size, self._offset)
        self._number: int = number
        self._speed: int = GEMS.SPEED
        self._direction: vec = vec()
        self._velocity: vec = self._direction * self._speed
        self._ready = True
        self._dist: int = 0
        self._is_falling: bool = False
        self._state: str = 'idle'
        self._frame: int = 0
        self.image: Surface = Surface((GEMS.SIZE.x, GEMS.SIZE.y), pygame.SRCALPHA)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))
        self.rect: Rect = self.image.get_rect(topleft = self._new_bpos.gfx_pos)

        #self.debug_rect = Debug_Rect(self._board_manager.swapdir_group, self.id, self.rect.topleft, self._new_bpos.gfx_pos, self._velocity)

    @property
    def bpos(self) -> BoardPosition:
        return self._bpos
    
    @property
    def new_bpos(self) -> BoardPosition:
        return self._new_bpos
    
    @new_bpos.setter
    def new_bpos(self, value: vec):
        self._new_bpos.pos = value
    
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
    def ready(self) -> bool:
        return self._ready

    def change_pos(self):
        direction: vec = self._new_bpos.pos - self._bpos.pos
        if vec(direction).length() > 0:
            self._direction = vec.normalize(direction)
        self._velocity = self._direction * self._speed
        self._ready = False

    def reset_state(self):
        self._frame = 0
        self._state = 'idle'
        self.image.fill(COLORS.TRANSPARENT)
        self.image.blit(self._gems_img.sheet[self._number-1], (0, 0))

    def _fall(self):
        if self._is_falling: return
        if self._bpos.pos.y == GAME.BOARD_SIZE.y-1: return

        dist = 0
        if self._bpos.pos.y >= 0: start = int(self._bpos.pos.y) + 1
        else: start = 0

        for y in range(start, int(GAME.BOARD_SIZE.y)):
            if self._board_manager.board.gems[int(self._bpos.pos.x)][y] == None:
                dist += 1
        if dist == 0: return
        self._new_bpos.pos = self._bpos.pos + vec(0, dist)
        self._board_manager.match_gems.add_to_matching(self)
        self._is_falling = True
        self.change_pos()
        self._state = 'fall'
    
    def __repr__(self):
        return f'{self._number} <{self.id}>'
    
    def update(self, dt):

        self._dt = dt

        self._fall()

        current_pos = vec(self.rect.topleft)
        distance = vec().distance_to(self._velocity*dt)
        current_pos.move_towards_ip(self._new_bpos.gfx_pos, distance)
        self.rect.topleft = current_pos

        if not self._ready:
            if self.rect.topleft == (int(self._new_bpos.gfx_pos.x), int(self._new_bpos.gfx_pos.y)):
                self._velocity = vec()
                self._bpos.pos = self._new_bpos.pos.copy()
                self._board_manager.board.gems[int(self._bpos.pos.x)][int(self._bpos.pos.y)] = self
                self._ready  = True
                self._is_falling = False
                self.reset_state()

class Create_Board():
    def __init__(self, board_manager,
                 gems_group: Group,
                 gems_sheet: ImageSheet,
                 nr_of_gems: int):
        self._gems_sheet: ImageSheet = gems_sheet
        self._size: vec = GAME.BOARD_SIZE
        self._board_manager = board_manager
        self._nr_of_gems: int = nr_of_gems
        self._gems_group: Group = gems_group
        self._gems: list[Gem] = self._make_board()

    @property
    def gems(self) -> list[Gem]:
        return self._gems
    
    @gems.setter
    def gems(self, value):
        self._gems = value

    def _make_board(self) -> list[Gem]:
        gems = numpy.empty(shape=(int(self._size.x), int(self._size.y)), dtype=object)

        for x in range(int(self._size.y)):
            for y in range(int(self._size.x)):
                number = choice(self.choice_number(gems, vec(x, y), [nr+1 for nr in range(self._nr_of_gems)]))      
                gems[x][y] = Gem(self._gems_group, self._gems_sheet, self._board_manager, vec(x, y), number)
        #print(gems)
        
        return gems.tolist()
        #return gems.tolist()
    
    def choice_number(self, board: list[Gem], pos: vec, candidates: list) -> list[int]:
        x = int(pos.x)
        y = int(pos.y)
        if x-2 >= 0:
            previous_x: list[Gem] = [board[x-1][y].number, board[x-2][y].number]
            if previous_x[0] == previous_x[1]:
                candidates.remove(previous_x[0])
        if y-2 >= 0:
            previous_y = [board[x][y-1].number, board[x][y-2].number]
            if previous_y[0] == previous_y[1]:
                if previous_y[0] in candidates:
                    candidates.remove(previous_y[0])

        return candidates
    
    def add_new_gem(self, pos: vec):
        candidates = [nr+1 for nr in range(GAME.NUMBER_OF_GEMS)]
        return Gem(self._gems_group, self._gems_sheet, self._board_manager, pos, choice(candidates))
    
    def exec_time(func):
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            #print(f'Process : {time.time() - start_time} sec.')
            return result
        return wrapper

    @exec_time
    def shuffle(self, board: list[Gem]) -> numpy.ndarray:
        temp_board = numpy.empty(shape=(int(self._size.x), int(self._size.y)),dtype=object)
        rng = numpy.random.default_rng()
        _board = rng.permuted(numpy.array(board, dtype=Gem))
        _board = rng.permuted(_board, axis=1)
        #print('***')
        #print(_board)
        _board_con = numpy.concatenate(_board)
        for x in range(int(self._size.x)):
            for y in range(int(self._size.y)):
                #rint()
                rng.shuffle(_board_con)
                numbers = self.choice_number(temp_board, vec(x, y), [nr+1 for nr in range(self._nr_of_gems)])
                #print(f'{numbers}', end=' > ')
                for i, gem in enumerate(_board_con):
                    if gem.number in numbers:
                        temp_board[x, y] = gem
                        #print(f'{gem}', end=' > ')
                        _board_con = numpy.delete(_board_con, i, 0)
                        #print(_board_con, end= ' >>> ')
                        temp_board[x, y].new_bpos.pos = vec(x, y)
                        temp_board[x, y].change_pos()
                        break
                else:
                    #print('error!', end=' > ')
                    #print(f'{numbers}', end=' > ')
                    #print(_board_con, end= ' >>> ')
                    temp_board = self.shuffle(board)

        return temp_board

    

class Board_Manager():
    def __init__(self, gems_group: Group, screen_manager: Screen_Manager):
        self._gems_group: Group[Gem] = gems_group
        self._screen_manager: Screen_Manager = screen_manager
        self._anim_group: Group = Group()
        self._board: Create_Board = Create_Board(self,
                                                 self._gems_group,
                                                 ImageSheet('gem_', SCREEN.ELEMENTS),
                                                 GAME.NUMBER_OF_GEMS)
        self._select_gem: Select_Gem = Select_Gem(self._screen_manager)
        self._swapdir_group: GroupSingle = GroupSingle()
        self._pointer_group: GroupSingle = GroupSingle()
        self._swap_gems: Swap_Gem = Swap_Gem(self)
        self._match_gems: Match = Match(self)
        self._overs: list[Gem] = list()
        self._possibles: bool = False
        self._gems_ready = False
        self._match: bool = False
        self._gems_matching: set = set()

    @property
    def screen_manager(self):
        return self._screen_manager

    @property
    def board(self) -> Create_Board:
        return self._board
    
    @board.setter
    def board(self, value):
        self._board = value
    
    @property
    def select_gem(self) -> Select_Gem:
        return self._select_gem

    @property
    def swapdir_group(self) -> GroupSingle:
        return self._swapdir_group
    
    @property
    def anim_group(self) -> Group:
        return self._anim_group
    
    @property
    def possibles(self) -> bool:
        return self._possibles
    
    @possibles.setter
    def possibles(self, value: bool):
        self._possibles = value
    
    @property
    def match_gems(self) -> Match:
        return self._match_gems
    
    @property
    def swap_gems(self) -> Swap_Gem:
        return self._swap_gems
    
    @property
    def match(self) -> bool:
        return self._match
    
    @match.setter
    def match(self, value: bool):
        self._match = value
    
    @property
    def gems_matching(self) -> set:
        return self._gems_matching

    def _detect_pointer_with_gem_collision(self, events, game_status, player):

        if not self._gems_ready: return

        gem: Gem = None
        for _gem in self._gems_group:
            if _gem.rect.collidepoint(*(pygame.mouse.get_pos() - SCREEN.POSITIONS['board'] - MOUSE_OFFSET)):
                gem = _gem

        if player == 'Player':
            for event in events:
                if game_status != 'play':
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
                            Swap_Dirs(self._swapdir_group,
                                        self._select_gem.selected_gem1.bpos,
                                        SWAP_DIRS.ANIM,
                                        SWAP_DIRS.OFFSET,
                                        vec(gem.bpos.pos - self._select_gem.selected_gem1.bpos.pos))

    def _check_swaped_gems(self, gems: set[Gem]) -> bool:
        if len(gems) == 0: return False
        for gem in gems:
            if not gem.ready:
                return True
        return False
    
    def gems_end_moving(self) -> bool:
        for gem in self._gems_group:
            if gem.ready == False:
                return False
        return True
    
    def update(self, events, dt, game_status, player):

        self._gems_ready = self.gems_end_moving()

        self._detect_pointer_with_gem_collision(events, game_status, player)

        self._select_gem.select_group.update(dt)
        self._select_gem.select_group.draw(self._screen_manager.screens.Anim)
        self._swapdir_group.draw(self._screen_manager.screens.Anim)

        if self._select_gem.ready_to_swap:
            self._select_gem.ready_to_swap = False
            self._swap_gems.add_gems(self._select_gem.selected_gem1, self._select_gem.selected_gem2)
            self._swap_gems.swap(None)

        if self._swap_gems.swaping:
            if not self._check_swaped_gems([self._swap_gems.gem1, self._swap_gems.gem2]):
                self._match_gems.add_to_matching(self._swap_gems.gem1)
                self._match_gems.add_to_matching(self._swap_gems.gem2)
                self._match, self._gems_matching = self._match_gems.match()
                if self._match:
                    #print('board_manager > match = true')
                    self._swap_gems.swaping = False
                else:
                    self._swap_gems.swap(SND_SWAP_BACK)
                self._swap_gems.clear_swap()
                self._select_gem.clear()

            if not self.board_is_idle():
                print('board is not idle')
                                

        self._gems_group.update(dt)
        self._anim_group.update(dt)
        self._anim_group.draw(self.screen_manager.screens.Anim)
    
    def board_is_idle(self) -> bool:
        if not self.gems_end_moving(): return False
        if len(self._match_gems.set_matching) > 0:
            self._match_gems.match()
            print(f'{self._match_gems.set_matching=}')
            return False
        return True