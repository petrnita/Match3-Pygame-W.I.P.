from consts import BOARD_IS_IDLE, IDS, MOUSE_OFFSET, COLORS, SCREEN, SND_SWAP_BACK, GEMS, GAME, SWAP_DIRS
import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group, GroupSingle
from pygame.math import Vector2 as vec
from random import choice
from screen_manager import Screen_Manager
from gem_select import Select_Gem
from old_files.swap_gem import Swap_Gem
from match import Match
from sprites import Swap_Dirs, Debug_Rect
from graphic import ImageSheet
from resources import BoardPosition
import numpy as np

from pygame.font import SysFont

pygame.font.init
debugfont = SysFont('Arial', 16, True)

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
        self._board_manager: Board_Manager = board_manager
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
        idtext = debugfont.render(f' {self.id} ', True, '#ffa4d1', "#141313")
        self.image.blit(idtext, (3, 3))
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
        self._ready = False
        direction: vec = self._new_bpos.pos - self._bpos.pos
        if vec(direction).length() > 0:
            self._direction = vec.normalize(direction)
        self._velocity = self._direction * self._speed

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
            if self._board_manager.board[int(self._bpos.pos.x)][y] == None:
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
        idtext = debugfont.render(f' {self.id} ', True, '#ffa4d1', "#141313")
        self.image.blit(idtext, (3, 3))

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
                self._board_manager.set_gem_on_position(self, self._bpos.pos)
                self._ready  = True
                self._is_falling = False
                self.reset_state()

class Board_Creator:
    def make_board(gems_group: Group,
                   board_size: vec,
                   nr_of_gems: int,
                   gems_sheet: ImageSheet,
                   board_manager) -> list[Gem]:
        gems = np.empty(shape=(int(board_size.x), int(board_size.y)), dtype=object)

        for x in range(int(board_size.y)):
            for y in range(int(board_size.x)):
                number = choice(Board_Creator.choice_number(gems, vec(x, y), [nr+1 for nr in range(nr_of_gems)]))      
                gems[x][y] = Gem(gems_group, gems_sheet, board_manager, vec(x, y), number)
        #print(gems)
        
        return gems.tolist()
        #return gems.tolist()
    
    @staticmethod
    def choice_number(board: list[Gem],
                      pos: vec,
                      candidates: list) -> list[int]:
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
    
    def add_new_gem(gems_group: Group,
                    pos: vec,
                    gems_sheet: ImageSheet,
                    board_manager):
        candidates = [nr+1 for nr in range(GAME.NUMBER_OF_GEMS)]
        return Gem(gems_group, gems_sheet, board_manager, pos, choice(candidates))
    
    def exec_time(func):
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            #print(f'Process : {time.time() - start_time} sec.')
            return result
        return wrapper

    @exec_time
    def shuffle(board_size: vec,
                board: list[Gem],
                nr_of_gems: int) -> np.ndarray:
        temp_board = np.empty(shape=(int(board_size.x), int(board_size.y)),dtype=object)
        rng = np.random.default_rng()
        _board = rng.permuted(np.array(board, dtype=Gem))
        _board = rng.permuted(_board, axis=1)
        #print('***')
        #print(_board)
        _board_con = np.concatenate(_board)
        for x in range(int(board_size.x)):
            for y in range(int(board_size.y)):
                #rint()
                rng.shuffle(_board_con)
                numbers = Board_Creator.choice_number(temp_board, vec(x, y), [nr+1 for nr in range(nr_of_gems)])
                #print(f'{numbers}', end=' > ')
                for i, gem in enumerate(_board_con):
                    if gem.number in numbers:
                        temp_board[x, y] = gem
                        #print(f'{gem}', end=' > ')
                        _board_con = np.delete(_board_con, i, 0)
                        #print(_board_con, end= ' >>> ')
                        # temp_board[x, y].new_bpos.pos = vec(x, y)
                        # temp_board[x, y].change_pos()
                        break
                else:
                    #print('error!', end=' > ')
                    #print(f'{numbers}', end=' > ')
                    #print(_board_con, end= ' >>> ')
                    temp_board = Board_Creator.shuffle(board)

        return temp_board

    

class Board_Manager():
    def __init__(self, screen_manager: Screen_Manager):
        self._gems_group: Group[Gem] = Group()
        self._screen_manager: Screen_Manager = screen_manager
        self._anim_group: Group = Group()
        self._board: list[Gem] = Board_Creator.make_board(self._gems_group,
                                                        GAME.BOARD_SIZE,
                                                        GAME.NUMBER_OF_GEMS,
                                                        ImageSheet('gem_', SCREEN.ELEMENTS),
                                                        self)
        self._select_gem: Select_Gem = Select_Gem(self._screen_manager)
        self._swapdir_group: GroupSingle = GroupSingle()
        self._pointer_group: GroupSingle = GroupSingle()
        self._swaping_gem1: Gem = None
        self._swaping_gem2: Gem = None
        self._swaping: bool = False
        self._match_gems: Match = Match(self)
        self._gem_under_mouse: list[Gem] = list()
        self._match: bool = False
        self._ready_to_falling: bool = False
        self._gems_killed: set = None

    @property
    def gems_group(self) -> Group:
        return self._gems_group

    @property
    def screen_manager(self):
        return self._screen_manager

    @property
    def board(self) -> list[Gem]:
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
    def match_gems(self) -> Match:
        return self._match_gems
    
    @property
    def match(self) -> bool:
        return self._match
    
    @match.setter
    def match(self, value: bool):
        self._match = value

    @match.setter
    def match(self, value: bool):
        self._match = value
    
    @property
    def gems_killed(self) -> set:
        return self._gems_killed
    
    @gems_killed.setter
    def gems_killed(self, value: set[Gem]):
        self._gems_killed = value
    
    def set_gem_on_position(self, gem: Gem, pos: vec):
        self._board[int(pos.x)][int(pos.y)] = gem

    def shuffle_board(self):
        self._board = Board_Creator.shuffle(self._board)
        self.rearange_board(self._board)

    def rearange_board(self, new_board: list[Gem]):
        for x in range(int(GAME.BOARD_SIZE.x)):
            for y in range(int(GAME.BOARD_SIZE.y)):
                self._board[x][y] = new_board[x][y]
                self._board[x][y].new_bpos.pos = vec(x, y)
                self._board[x][y].change_pos()

    def get_swaping(self) -> bool:
        return self._swaping

    def _detect_pointer_with_gem_collision(self, events, game_status, player):

        if not self.gems_end_moving(self._board): return

        gem: Gem = None
        for _gem in self._gems_group:
            if _gem.rect.collidepoint(*(pygame.mouse.get_pos() - SCREEN.POSITIONS['board'] - MOUSE_OFFSET)):
                gem = _gem

        if player == 'Player':
            for event in events:
                if game_status != 'play':
                    break
                if not self.get_swaping():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if gem != None:
                            self._select_gem.try_select(gem)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if gem != None and self._select_gem.selected_gem1 != None and gem != self._select_gem.selected_gem1:
                            self._select_gem.try_select(gem, False)
                    if event.type == pygame.MOUSEMOTION:
                        if self._gem_under_mouse != gem:
                            self.swapdir_group.empty()
                            self._gem_under_mouse = gem
                        if self._select_gem.selected_gem1 and self._select_gem.is_neighbor(gem):
                            Swap_Dirs(self._swapdir_group,
                                        self._select_gem.selected_gem1.bpos,
                                        SWAP_DIRS.ANIM,
                                        SWAP_DIRS.OFFSET,
                                        vec(gem.bpos.pos - self._select_gem.selected_gem1.bpos.pos))
    
    def gems_end_moving(self, gems: set[Gem] | list[Gem]) -> bool:
        if len(gems) == 0: return False
        if isinstance(gems[0], list):
            _gems = np.concatenate((gems), dtype=Gem)
        else:
            _gems = gems
        for gem in _gems:
            if gem == None: return False
            if not gem.ready: return False
        return True
    
    def board_is_ready(self) -> bool:
        if not self.gems_end_moving(self._board): return False
        return True

    def update(self, events, dt, game_status, player):

        self._detect_pointer_with_gem_collision(events, game_status, player)

        self._select_gem.select_group.update(dt)
        self._select_gem.select_group.draw(self._screen_manager.Anim)
        self._swapdir_group.draw(self._screen_manager.Anim)

        if self._select_gem.ready_to_swap:
            self._select_gem.ready_to_swap = False
            self.add_gems(self._select_gem.selected_gem1, self._select_gem.selected_gem2)
            self.swap(None)

        if self.get_swaping():
            if self.gems_end_moving([self._swaping_gem1, self._swaping_gem2]):
                self._match_gems.add_to_matching(self._swaping_gem1)
                self._match_gems.add_to_matching(self._swaping_gem2)
                self._match_gems.match(self)
                #self._match, self._gems_killed = self._match_gems.match()
                if self._match:
                    self._swaping = False
                else:
                    self.swap(SND_SWAP_BACK)
                self.clear_swap()
                self._select_gem.clear()

        if self.board_is_ready():
            if len(self._match_gems.set_matching) > 0:
                self._match_gems.match(self)
                #self._match, self._gems_killed = self._match_gems.match()
            else:
                pygame.event.post(pygame.event.Event(BOARD_IS_IDLE))

        self._gems_group.update(dt)
        self._anim_group.update(dt)
        self._gems_group.draw(self._screen_manager.Board)
        self._anim_group.draw(self._screen_manager.Anim)

    def add_gems(self, gem1, gem2):
        self._swaping_gem1 = gem1
        self._swaping_gem2 = gem2

    def swap(self, sound: str=None): 
        self._swaping = not self._swaping
        if sound != None:
            SND_SWAP_BACK.play()
        sel1 = (int(self._swaping_gem1.bpos.pos.x), int(self._swaping_gem1.bpos.pos.y))
        sel2 = (int(self._swaping_gem2.bpos.pos.x), int(self._swaping_gem2.bpos.pos.y))
        self._board[sel1[0]][sel1[1]], self._board[sel2[0]][sel2[1]] = self._board[sel2[0]][sel2[1]], self._board[sel1[0]][sel1[1]]
        self._swapdir_group.empty()
        self._swaping_gem1.new_bpos.pos = self._swaping_gem2.bpos.pos
        self._swaping_gem1.change_pos()
        self._swaping_gem1.state = 'swap'
        self._swaping_gem2.new_bpos.pos = self._swaping_gem1.bpos.pos
        self._swaping_gem2.change_pos()
        self._swaping_gem2.state = 'swap'

    def clear_swap(self):
        self._swaping_gem1 = None
        self._swaping_gem2 = None
        self._swaping = False
    

            