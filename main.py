from consts import SCREEN, SWAP_DIRS, TXT_NO_MOVE, SELECT
import pygame, sys
from pygame.sprite import Group, GroupSingle
from pygame.math import Vector2 as vec
from pygame.cursors import Cursor
from screen_manager import Screen_Manager
from game_assets import Board_Manager, Gem
from gem_select import Select_Gem
from check_matching import Check_Matching
from sprites import Fade, Player_Text, Debug_Rect
from sprites import Text_Fade, Swap_Dirs, Bar, Animation
from debug import Show_Text
import numpy as np


class GameManager():
    
    def __init__(self):
        from game_assets import Gem
        self.screen_manager: Screen_Manager = Screen_Manager()
        self.clock = pygame.time.Clock()
        self.gems_group: Group = Group()
        self.fade_group: GroupSingle = GroupSingle()
        self.anim_group: Group = Group()
        self.text_group: Group = Group()
        self.bars_group: Group = Group()
        self.game_status = 'play'
        self.player: str = 'Player'
        self.player_text: Player_Text = Player_Text(self.text_group, SCREEN.POSITIONS['player'], 'player')
        self.player_text.swap_image()
        self.cpu_text: Player_Text = Player_Text(self.text_group, SCREEN.POSITIONS['cpu'], 'cpu')
        self.board_manager = Board_Manager(self.gems_group, self.screen_manager)
        self.cpu_find_gem: Gem = None
        self.cpu_find_direction: vec = None
        self.player_start_move: bool = True
        self.cpu_start_move: bool = True
        self.end_swap = False
        self.player_bars: list[Bar] = []
        self.cpu_bars: list[Bar] = []
        self.time_bar: Bar = None
        self.make_bars()
        self.move_delay = pygame.USEREVENT + 0
        self.ready_to_move = False
        self.debug_group: Group = Group()
        self.debug_fps = Show_Text(self.debug_group, '', vec(12, 12))
        self.check_move_counter: int = 0
        self.find_gem = None
        self.bar_counter = 100
        self.pause = False
        self.change_cursor('hand', True, False)
        Fade(self.fade_group, 2, 'Out')

    def make_bars(self):
        for bar in range(6):
            self.player_bars.append(Bar(self.bars_group, SCREEN.ELEMENTS, 'battle', 'player', f'{bar+1}'))
            self.cpu_bars.append(Bar(self.bars_group, SCREEN.ELEMENTS, 'battle', 'cpu', f'{bar+1}'))
        self._time_bar = Bar(self.bars_group, SCREEN.ELEMENTS, 'time', 'time', 'progress')

    def update(self, events, dt):
        self.board_manager.update(events, dt, self.game_status)
        self.fade_group.update(dt)
        self.text_group.update(dt)
        self.anim_group.update(dt)
        if self.bar_counter > 0:
            self.bar_counter -= .6
        else:
            self.help_counter = 0

        if self.game_status == 'shuffle':
            if self.board_manager.check_all_gems_ready():
                Fade(self.fade_group, 2, 'Out')
                self.game_status = 'play'
                self.bar_counter = 100

        self.bars_group.update(self.bar_counter)

        self.debug_group.update(f'FPS: {int(self.clock.get_fps())}')

        if self.player == 'CPU':
            self.cpu_playing()
        else:
            self.player_playing()

    def draw(self):
        self.gems_group.draw(self.screen_manager.screens.Board)     
        self.fade_group.draw(self.screen_manager.screens.Anim)
        self.bars_group.draw(self.screen_manager.screens.Top)
        self.text_group.draw(self.screen_manager.screens.Top)
        self.debug_group.draw(self.screen_manager.screens.Main)
        
    def main_loop(self):
        run: bool = True
        while run:

            dt = self.clock.tick(60) / 1000
            
            events = [event for event in pygame.event.get()]
            
            for event in events:
                
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if self.game_status == 'game_over':
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_s:
                        self.print_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.dict)
                    pass
                if event.type == self.move_delay:
                    self.ready_to_move = True
                    print(f'{self.ready_to_move=}')
                                       
            self.screen_manager.paint_screen()

            if not self.pause:
                self.update(events, dt)

            self.draw()

            self.screen_manager.draw()

    def player_playing(self):
        if not self.board_manager.check_all_gems_ready(): return
        
        if self.player_start_move:
            find_gem, _ = Check_Matching.check(self.board_manager.board.gems)
            if not find_gem:
                self.shuffle_gems()
                self.game_status = 'shuffle'
                return
            self.player_start_move = False
        else:
            if self.board_manager.swap_gems.swaping:
                self.end_swap = False
                print('>>>>>>>')
                self.player_start_move = True 
                self.ready_to_move = False                
                self.player = 'CPU'
                self.cpu_text.swap_image()
                self.player_text.swap_image()
                find_gem, _ = Check_Matching.check(self.board_manager.board.gems)
                if not find_gem:
                    self.shuffle_gems()
                    self.game_status = 'shuffle'
                pygame.time.set_timer(self.move_delay, 2000, loops=1)
                print(f'{pygame.event.poll()=}')
                print('pygame.time.set_timer(self.move_delay, 2000, loops=1)')

    def cpu_playing(self):
        if not self.board_manager.check_all_gems_ready(): return

        if self.cpu_start_move:
            find_gem, _ = Check_Matching.check(self.board_manager.board.gems)
            if not find_gem:
                self.shuffle_gems()
                self.game_status = 'shuffle'
                return
            
            if self.ready_to_move:
                self.cpu_start_move = False
                self.ready_to_move = False
                pygame.time.set_timer(self.move_delay, 500, loops=1)
                self.cpu_find_gem, self.cpu_find_direction = Check_Matching.check(self.board_manager.board.gems)
                if not self.cpu_find_gem:
                    self.player = 'Player'   
                    self.shuffle_gems()
                    self.game_status = 'shuffle'
                    return
                self.print_screen() 
                self.board_manager.select_gem.selected_gem1 = self.cpu_find_gem
                Animation(self.board_manager.select_gem.select_group, self.cpu_find_gem.bpos.gfx_pos,
                        SELECT.ANIM, SELECT.SPEED, SELECT.OFFSET, SELECT.LOOP)
                Swap_Dirs(self.board_manager.swapdir_group,
                        self.cpu_find_gem.bpos,
                        SWAP_DIRS.ANIM, SWAP_DIRS.OFFSET,
                        (self.cpu_find_direction))
           
        else:
            if self.ready_to_move:
                self.board_manager.select_gem.try_select(self.board_manager.board.gems[int(self.cpu_find_gem.bpos.pos.x+self.cpu_find_direction[0])][int(self.cpu_find_gem.bpos.pos.y+self.cpu_find_direction[1])], None)                 
                self.cpu_start_move = True
                self.player = 'Player'
                self.player_text.swap_image()
                self.cpu_text.swap_image()
    
    def shuffle_gems(self):
        Fade(self.fade_group, 2)
        Text_Fade(self.text_group,
                  TXT_NO_MOVE.OFFSET,
                  TXT_NO_MOVE.IMAGE,
                  .03,
                  5,
                  size_direction='grow',
                  fade_direction='Out')
        self.board_manager.board.gems = self.board_manager.board.shuffle(self.board_manager.board.gems)
        self.game_status = 'shuffle'

    def print_screen(self):
        print(SCREEN.ELEMENTS_RECTS['board'])
        print(self.screen_manager.screens.Board.get_rect())
        image = self.screen_manager.screens.Main.subsurface(SCREEN.POSITIONS_RECTS['board'])
        pygame.image.save(image, 'gfx/screenshot.png')

    def change_cursor(self, cursor: str, init: bool=False, reset: bool=False):
        if init:
            default = Cursor(pygame.SYSTEM_CURSOR_ARROW)

            surf = SCREEN.ELEMENTS['hand_cursor']
            hand = Cursor((SCREEN.ELEMENTS_RECTS['hand_cursor'].w//2, SCREEN.ELEMENTS_RECTS['hand_cursor'].h//2), surf)

            self.cursors = {
                'default': default,
                'hand': hand
                }

        if reset:
            pygame.mouse.set_cursor(self.cursors['default'])
            return

        pygame.mouse.set_cursor(self.cursors[cursor])


if __name__ == '__main__':
    game_manager: GameManager = GameManager()
    print(np.array(pygame.event.get()))
    game_manager.main_loop()
    game_manager.change_cursor(reset=True)
    pygame.quit()
    sys.exit()