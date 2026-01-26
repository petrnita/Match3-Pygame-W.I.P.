from consts import TXT
import pygame, sys
from pygame.sprite import Group
from pygame.math import Vector2 as vec
from screen_manager import Screen_Manager
from game_assets import Board_Manager
from check_matching import Check_Matching
from sprites import Fade_In
from sprites import Text_Sprite
from debug import Show_Text


class GameManager():
    
    def __init__(self):
        self.screen_manager: Screen_Manager = Screen_Manager()
        self.clock = pygame.time.Clock()
        self.gems_group: Group = Group()
        self.fade_group: Group = Group()
        self.text_group: Group = Group()
        self.board_manager = Board_Manager(self.gems_group, self.screen_manager)
        self.check_board = pygame.USEREVENT + 1
        pygame.time.set_timer(self.check_board, 3000)
        self.game_status = 'start'
        self.debug_group: Group = Group()
        self.debug_fps = Show_Text(self.debug_group, '', vec(12, 12))

    def update(self, events, dt):
        if self.game_status == 'start':
            if self.screen_manager.gems_offset.y < 0:
                self.screen_manager.gems_offset.y += 400 * dt
            else:
                self.screen_manager.gems_offset.y = 0
                self.game_status = 'play'
            
        self.board_manager.update(events, dt, self.game_status)
        self.fade_group.update(dt)
        self.text_group.update(dt)

        self.debug_group.update(f'FPS: {self.clock.get_fps():.2f}')

    def draw(self):
        self.gems_group.draw(self.screen_manager.screens.Board)        
        self.fade_group.draw(self.screen_manager.screens.Anim)
        self.text_group.draw(self.screen_manager.screens.Anim)

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
                if event.type == self.check_board:        
                    if self.game_status != 'game_over':
                        if self.board_manager.check_gems_ready() and not self.board_manager._swap_gems.swaping:
                            if not Check_Matching.check(self.board_manager.board.gems):
                                self.game_status = 'game_over'
                                Fade_In(self.fade_group, self.screen_manager, 2)
                                Text_Sprite(self.text_group,
                                            vec(self.screen_manager.screens.Board_con.get_width()//2,
                                                self.screen_manager.screens.Board_con.get_height()//2-32),
                                                TXT.NO_MORE_MOVES)
                                Text_Sprite(self.text_group,
                                            vec(self.screen_manager.screens.Board_con.get_width()//2,
                                                self.screen_manager.screens.Board_con.get_height()//2+32),
                                                TXT.PRESS_ANY_KEY,
                                                24)

                    
            self.screen_manager.paint_screen()

            self.update(events, dt)

            self.draw()

            self.screen_manager.draw()


if __name__ == '__main__':
    game_manager: GameManager = GameManager()
    game_manager.main_loop()
    pygame.quit()
    sys.exit()