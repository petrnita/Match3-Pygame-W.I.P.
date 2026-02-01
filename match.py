import pygame
from pygame.math import Vector2 as vec
from consts import SCREEN, GEMS_KILLED_EVENT, IDS, GAME, KILL_GEM
from sprites import Animation
from graphic import ImageSheet

pygame.init()

class Match():
    def __init__(self, board_manager):
        from game_assets import Board_Manager

        self._board_manager: Board_Manager = board_manager
        self._matching_queue: set = set()
        self._threes = 0
        self._horizontal: list[vec] = [vec(-1, 0), vec(), vec(1, 0)]
        self._vertical: list[vec] = [vec(0, -1), vec(), vec(0, 1)]

    @property
    def set_matching(self) -> set:
        return self._matching_queue

    def add_to_matching(self, gem):
        from game_assets import Gem
        _gem: Gem = gem
        self._matching_queue.add(_gem)

    def get_matching_queue(self) -> set:
        return self._matching_queue
        
    def _get_neighbor(self, gem, offset: vec):
        from game_assets import Gem
        _gem: Gem = gem
        bound = GAME.BOARD_SIZE
        if 0 <= _gem.bpos.pos.x + offset.x < bound.x and 0 <= _gem.bpos.pos.y + offset.y < bound.y:
            return self._board_manager.board[int(_gem.bpos.pos.x + offset.x)][int(_gem.bpos.pos.y + offset.y)]
        return None
    
    def _three_of_kind(self, gem, axis: list) -> tuple:
        from game_assets import Gem
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
    
    def match(self, board_manager) -> list[bool, set]:
        from game_assets import Gem, Board_Creator
        board_manager.match = False
        board_manager.gems_killed = set()
        #ret = [False, set()]
        _sorted_matching_queue = reversed(sorted(self._matching_queue, key=lambda gem: gem.bpos.pos.y))
        self._matching_queue = set()
        new_gems = {'0': -1, '1': -1, '2': -1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1}
        for gem in _sorted_matching_queue:
            #self._board_manager.possibles = False
            set_same: set[Gem] = set()
            set_same.update(self._three_of_kind(gem, self._horizontal))
            set_same.update(self._three_of_kind(gem, self._vertical))
            if len(set_same) > 2:
                lst_new_gems = list()
                for same in set_same:
                    new_y = new_gems[str(int(same.bpos.pos.x))]
                    IDS.append(same.id)
                    new_gem = Board_Creator.add_new_gem(self._board_manager.gems_group,
                                                        vec(same.bpos.pos.x, new_y),
                                                        ImageSheet('gem_', SCREEN.ELEMENTS),
                                                        self._board_manager)
                    lst_new_gems.append(new_gem)
                    new_gems[str(int(same.bpos.pos.x))] -= 1
                    Animation(self._board_manager.anim_group, same.bpos.gfx_pos,
                                KILL_GEM.ANIM, KILL_GEM.SPEED, KILL_GEM.OFFSET, KILL_GEM.LOOP)
                    same.kill()
                    self._board_manager.board[int(same.bpos.pos.x)][int(same.bpos.pos.y)] = None
                pygame.event.post(pygame.event.Event(GEMS_KILLED_EVENT))
                board_manager.match = True
                board_manager.gems_killed = set_same
                #ret = [True, set_same]
                print(f'{set_same=}')
                #set_same = set()
        #return ret
