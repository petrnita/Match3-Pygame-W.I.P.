import pygame
from pygame.sprite import Group, GroupSingle
from pygame.math import Vector2 as vec
from random import choice
from gem_select import Select_Gem
from sprites import ImageSheet, \
                    Gem, \
                    Animation, \
                    Swap_Dirs
import numpy as np
from rich import print as print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from debug import debug
console = Console()

class Board_Creator:
    def make_board(gems_group: Group,
                   board_size: vec,
                   nr_of_gems: int,
                   gems_sheet: ImageSheet) -> list[Gem]:
        gems = np.empty(shape=(int(board_size.x), int(board_size.y)), dtype=object)

        for x in range(int(board_size.y)):
            for y in range(int(board_size.x)):
                number = choice(Board_Creator.choice_number(gems, vec(x, y), [nr+1 for nr in range(nr_of_gems)]))      
                gems[x][y] = __class__.add_new_gem(gems_group, gems_sheet, vec(x, y), number)
        
        # for column in range(8):
        #     renderable = [Panel(gem[column]) for gem in gems]
        #     console.print(Columns(renderable, width=11))


        return gems.tolist()
    
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
    
    @staticmethod
    def add_new_gem(gems_group: Group,
                    gems_sheet: ImageSheet,
                    pos: vec,
                    number: int = None):
        from consts import GAME
        candidates = number if number else choice([nr+1 for nr in range(GAME.NUMBER_OF_GEMS)])
        return Gem(gems_group, gems_sheet, pos, candidates)
    
    def exec_time(func):
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            debug(f'shuffle : {time.time() - start_time} sec.')
            return result
        return wrapper

    @exec_time
    def shuffle(board_size: vec,
                board: list[Gem],
                nr_of_gems: int) -> np.ndarray:
        temp_board = np.empty(shape=(int(board_size.x), int(board_size.y)), dtype=object)
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
                    temp_board = Board_Creator.shuffle(board_size, board, nr_of_gems)

        return temp_board

    
class Board_Manager():
    def __init__(self):
        from consts import GAME, SCREEN
        self._gems_group: Group[Gem] = Group()
        self._select_group: GroupSingle = GroupSingle()
        self._swapdir_group: GroupSingle = GroupSingle()
        self._pointer_group: GroupSingle = GroupSingle()
        self._anim_group: Group = Group()               
        self._board: list[Gem] = Board_Creator.make_board(self._gems_group,
                                                        GAME.BOARD_SIZE,
                                                        GAME.NUMBER_OF_GEMS,
                                                        ImageSheet('gem_', SCREEN.ELEMENTS))
        self._select_gem: Select_Gem = Select_Gem(self._select_group)
        self._selected1: Gem = None
        self._selected2: Gem = None
        self._swapped1: Gem = None
        self._swapped2: Gem = None
        self._swapping: bool = False
        self._gem_under_mouse: list[Gem] = list()
        self._matching_queue: set = set()
        self._match: bool = False
        self._gems_killed: set = None
        self._ready_to_falling: bool = False
        self._board_is_idle: bool = False

    @property
    def gems_group(self) -> Group:
        return self._gems_group

    @property
    def board(self) -> list[Gem]:
        return self._board
    
    @board.setter
    def board(self, value):
        self._board = value
    
    @property
    def selected_gem1(self) -> Gem:
        return self._selected1
    
    @selected_gem1.setter
    def selected_gem1(self, value: Gem):
        self._selected1 = value

    @property
    def swapdir_group(self) -> GroupSingle:
        return self._swapdir_group
    
    @property
    def anim_group(self) -> Group:
        return self._anim_group
    
    @property
    def match(self) -> bool:
        return self._match
    
    @match.setter
    def match(self, value: bool):
        self._match = value
    
    @property
    def gems_killed(self) -> set:
        return self._gems_killed
    
    @gems_killed.setter
    def gems_killed(self, value: set[Gem]):
        self._gems_killed = value

    @property
    def board_is_idle(self) -> bool:
        return self._board_is_idle
    
    def set_gem_on_position(self, gem: Gem, pos: vec):
        self._board[int(pos.x)][int(pos.y)] = gem

    def shuffle_board(self):
        from consts import GAME
        self._board = Board_Creator.shuffle(GAME.BOARD_SIZE, self._board, GAME.NUMBER_OF_GEMS)
        self.rearange_board(self._board)

    def rearange_board(self, new_board: list[Gem]):
        from consts import GAME
        for x in range(int(GAME.BOARD_SIZE.x)):
            for y in range(int(GAME.BOARD_SIZE.y)):
                self._board[x][y] = new_board[x][y]
                self._board[x][y].newpos = vec(x, y)
                self._board[x][y].change_pos()

    def select_gem(self, gem, unselect: bool=True):
        self._selected1, self._selected2 = self._select_gem.try_select(gem, unselect)

    def get_swaping(self) -> bool:
        return self._swapping

    def _detect_pointer_with_gem_collision(self, events, game):
        from consts import SCREEN, MOUSE_OFFSET, SWAP_DIRS
        if not self.gems_end_moving(self._board): return

        gem: Gem = None
        for _gem in self._gems_group:
            if _gem.rect.collidepoint(*(pygame.mouse.get_pos() - SCREEN.POSITIONS['board'] - MOUSE_OFFSET)):
                gem = _gem

        if game.current_player == 'Player':
            for event in events:
                if game.game_status != 'play':
                    break
                if not self.get_swaping():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if gem:
                            self.select_gem(gem)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if gem != None and self._selected1 != None and gem != self._selected1:
                            self.select_gem(gem, False)
                    if event.type == pygame.MOUSEMOTION:
                        if self._gem_under_mouse != gem:
                            self.swapdir_group.empty()
                            self._gem_under_mouse = gem
                        if self._selected1 and self._select_gem.is_neighbor(gem):
                            Swap_Dirs(self._swapdir_group,
                                        self._selected1.bpos,
                                        SWAP_DIRS.ANIM,
                                        SWAP_DIRS.OFFSET,
                                        vec(gem.pos - self._selected1.pos))
    
    def gems_end_moving(self, gems: set[Gem] | list[Gem]) -> bool:
        if len(gems) == 0: return False
        _gems = np.concatenate(gems, dtype=Gem)
        for gem in _gems:
            if gem == None: return False
            if not gem.ready: return False
        return True
    
    def board_is_ready(self) -> bool:
        if not self.gems_end_moving(self._board): return False
        return True

    def update(self, events: list, dt, game):
        from consts import BOARD_IS_IDLE_EVENT, SND_SWAP_BACK
        self._detect_pointer_with_gem_collision(events, game)

        if self._select_gem.ready_to_swap:
            self._select_gem.ready_to_swap = False
            self.add_gems(self._selected1, self._selected2)
            self.swap(None)

        if self.get_swaping():
            if self.gems_end_moving([[self._swapped1, self._swapped2]]):
                self.add_to_matching(self._swapped1)
                self.add_to_matching(self._swapped2)
                self.check_match()
                #self._match, self._gems_killed = self._match_gems.match()
                if self._match:
                    self._swapping = False
                else:
                    self.swap(SND_SWAP_BACK)
                self.clear_swap()
                self._select_gem.clear()

        if self.board_is_ready():
            if len(self._matching_queue) > 0:
                debug(f'{self._matching_queue=}')
                self.check_match()
                self._board_is_idle = False
            else:
                self._board_is_idle = True
        else:
            self._board_is_idle = False
            debug(f'{self._board_is_idle=}')

        self._select_group.update(dt)
        self._gems_group.update(self, dt)
        self._anim_group.update(dt)

        self._gems_group.draw(game.screen_manager.Board)
        self._select_group.draw(game.screen_manager.Anim)
        self._swapdir_group.draw(game.screen_manager.Anim)        
        self._anim_group.draw(game.screen_manager.Anim)

    def add_gems(self, gem1, gem2):
        self._swapped1 = gem1
        self._swapped2 = gem2

    def swap(self, sound: str | None=None):
        from consts import SND_SWAP_BACK, SWAPING_EVENT
        self._swapping = not self._swapping
        pygame.event.post(pygame.event.Event(SWAPING_EVENT))
        if sound != None:
            SND_SWAP_BACK.play()
        sel1 = (self._swapped1.posx, self._swapped1.posy)
        sel2 = (self._swapped2.posx, self._swapped2.posy)
        self._board[sel1[0]][sel1[1]], self._board[sel2[0]][sel2[1]] = self._board[sel2[0]][sel2[1]], self._board[sel1[0]][sel1[1]]
        self._swapdir_group.empty()
        self._swapped1.newpos = self._swapped2.pos
        self._swapped1.change_pos()
        self._swapped1.state = 'swap'
        self._swapped2.newpos = self._swapped1.pos
        self._swapped2.change_pos()
        self._swapped2.state = 'swap'

    def clear_swap(self):
        self._swapped1 = None
        self._swapped2 = None
        self._swapping = False

    def add_to_matching(self, gem):
        _gem: Gem = gem
        self._matching_queue.add(_gem)

    def get_matching_queue(self) -> set:
        return self._matching_queue
        
    def _get_neighbor(self, gem, offset: vec):
        from consts import GAME
        _gem: Gem = gem
        bound = GAME.BOARD_SIZE
        if 0 <= _gem.posx + offset.x < bound.x and 0 <= _gem.posy + offset.y < bound.y:
            return self._board[int(_gem.posx + offset.x)][int(_gem.posy + offset.y)]
        return None
    
    def _three_of_kind(self, gem: Gem, axis: list) -> tuple:
        _gem: Gem = gem
        kinds: list = list()
        for neighbor in axis:
            negative: Gem = self._get_neighbor(_gem, neighbor + axis[0])
            center: Gem = self._get_neighbor(_gem, neighbor)
            positive: Gem = self._get_neighbor(_gem, neighbor + axis[2])
            if not None in [negative, center, positive]:
                if negative.number == center.number == positive.number:
                    kinds.extend([negative, center, positive])
        return kinds
    
    def check_match(self) -> list[bool, set]:
        from consts import IDS, GEMS_KILLED_EVENT, SCREEN, KILL_GEM
        self._match = False
        self._gems_killed = set()
        _sorted_matching_queue = reversed(sorted(self._matching_queue, key=lambda gem: gem.posy))
        self._matching_queue = set()
        new_gems = {'0': -1, '1': -1, '2': -1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1}
        self._horizontal: list[vec] = [vec(-1, 0), vec(), vec(1, 0)]
        self._vertical: list[vec] = [vec(0, -1), vec(), vec(0, 1)]
        for gem in _sorted_matching_queue:
            set_same: set[Gem] = set()
            set_same.update(self._three_of_kind(gem, self._horizontal))
            set_same.update(self._three_of_kind(gem, self._vertical))
            if len(set_same) > 2:
                lst_new_gems = list()
                for same in set_same:
                    new_y = new_gems[str(int(same.posx))]
                    IDS.append(same.id)
                    new_gem = Board_Creator.add_new_gem(self._gems_group,
                                                        ImageSheet('gem_', SCREEN.ELEMENTS),
                                                        vec(same.posx, new_y))
                    lst_new_gems.append(new_gem)
                    new_gems[str(int(same.posx))] -= 1
                    Animation(self._anim_group, same.gpos,
                                KILL_GEM.ANIM, KILL_GEM.SPEED, KILL_GEM.OFFSET, KILL_GEM.LOOP)
                    same.kill()
                    self._board[int(same.posx)][int(same.posy)] = None
                pygame.event.post(pygame.event.Event(GEMS_KILLED_EVENT))
                self._match = True
                self._gems_killed = set_same
                debug(f'{set_same=}')
    

            