from consts import SCREEN, SWAP_DIRS, TXT_NO_MOVE
import pygame, sys
from pygame.sprite import Group, GroupSingle
from pygame.math import Vector2 as vec
from screen_manager import Screen_Manager
from game_assets import Board_Manager
from check_matching import Check_Matching
from sprites import Fade_In, Debug_Rect
from sprites import Text_Sprite, Swap_Dirs
from debug import Show_Text


class GameManager():
    
    def __init__(self):
        self.screen_manager: Screen_Manager = Screen_Manager()
        self.clock = pygame.time.Clock()
        self.gems_group: Group = Group()
        self.fade_group: Group = GroupSingle()
        self.text_group: Group = Group()
        self.board_manager = Board_Manager(self.gems_group, self.screen_manager)
        self.check_board = pygame.USEREVENT + 1
        pygame.time.set_timer(self.check_board, 3000)
        self.game_status = 'play'
        self.debug_group: Group = Group()
        self.debug_fps = Show_Text(self.debug_group, '', vec(12, 12))
        self.help_counter: int = 0
        self.find_gem = None

    def update(self, events, dt):
        self.board_manager.update(events, dt, self.game_status)
        self.fade_group.update(dt)
        self.text_group.update(dt)

        self.debug_group.update(f'FPS: {self.clock.get_fps():.2f}')

    def draw(self):
        self.gems_group.draw(self.screen_manager.screens.Board)        
        self.fade_group.draw(self.screen_manager.screens.Anim)
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.help_counter = 0
                    if self.find_gem:
                        self.find_gem.fade_help = False
                        self.find_gem_gem = None
                        self.fade_group.empty()
                if event.type == self.check_board:        
                    if self.game_status != 'game_over':
                        if self.board_manager.check_gems_ready() and not self.board_manager._swap_gems.swaping:
                            self.find_gem, direction_help = Check_Matching.check(self.board_manager.board.gems)
                            if not self.find_gem:
                                self.game_status = 'game_over'
                                Fade_In(self.fade_group, 2)
                                Text_Sprite(self.text_group, TXT_NO_MOVE.OFFSET, TXT_NO_MOVE.IMAGE)
                                # Text_Sprite(self.text_group,
                                #             vec(self.screen_manager.screens.Board_con.get_width()//2,
                                #                 self.screen_manager.screens.Board_con.get_height()//2+32),
                                #                 TXT.PRESS_ANY_KEY,
                                #                 24)
                            else:
                                self.help_counter += 1
                                print(f'{self.help_counter=}')
                            if self.help_counter == 3:
                                self.find_gem.fade_help = True
                                self.board_manager.help_gem = self.find_gem
                                Debug_Rect(self.fade_group, self.find_gem.rect.topleft)
                                self.help_counter = 0
                                Swap_Dirs(self.fade_group,
                                            self.find_gem.bpos,
                                            SWAP_DIRS.ANIM,
                                            SWAP_DIRS.OFFSET,
                                            (direction_help))
                                       
            self.screen_manager.paint_screen()

            self.update(events, dt)

            self.draw()

            self.screen_manager.draw()


if __name__ == '__main__':
    game_manager: GameManager = GameManager()
    game_manager.main_loop()
    pygame.quit()
    sys.exit()