from consts import TXT, BACKGROUND, COLORS, BOARD, SCREEN
import pygame, sys
from pygame.math import Vector2 as vec
from screen_data import ScreenLayout
from game_assets import Board_Manager
from check_matching import Check_Matching
from sprites import Fade_In
from sprites import Text_Sprite


class GameManager():
    
    def __init__(self):
        self.screen_layout: ScreenLayout = ScreenLayout()
        self.clock = pygame.time.Clock()
        self.gems_group = pygame.sprite.Group()
        self.fade_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.Group()
        self.board_manager = Board_Manager(self.gems_group, self.screen_layout)
        self.check_board = pygame.USEREVENT + 1
        pygame.time.set_timer(self.check_board, 3000)
        self.game_status = 'play'
        
    def paint_screen(self):
        self.screen_layout.screen.blit(BACKGROUND, (0, 0))
        self.screen_layout.top_screen.fill(COLORS.TRANSPARENT)
        self.screen_layout.board_screen.blit(BOARD.IMAGE, (0, 0))

    def update(self, events, dt):
        self.board_manager.update(events, dt, self.game_status)
        self.fade_group.update(dt)
        self.text_group.update(dt)

    def draw(self):
        self.gems_group.draw(self.screen_layout.board_screen)
        self.board_manager.anim_group.draw(self.screen_layout.screen)
        self.screen_layout.screen.blit(self.screen_layout.board_screen, BOARD.OFFSET)
        self.fade_group.draw(self.screen_layout.top_screen)
        self.text_group.draw(self.screen_layout.top_screen)
        self.screen_layout.screen.blit(self.screen_layout.top_screen, (0, 0))

        pygame.display.flip()
        
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
                if self.game_status != 'game_over':
                    if event.type == self.check_board and self.board_manager._check_moving_of_gems(self.board_manager.match_gems.set_matching):
                        if not Check_Matching.check(self.board_manager.board.gems):
                            self.game_status = 'game_over'
                            Fade_In(self.fade_group, 2)
                            Text_Sprite(self.text_group, vec(SCREEN.WIDTH//2, SCREEN.HEIGHT//2-32), TXT.NO_MORE_MOVES)
                            Text_Sprite(self.text_group, vec(SCREEN.WIDTH//2, SCREEN.HEIGHT//2+32), TXT.PRESS_ANY_KEY, 24)

                    
            self.paint_screen()

            self.update(events, dt)

            self.draw()


if __name__ == '__main__':
    game_manager: GameManager = GameManager()
    game_manager.main_loop()
    pygame.quit()
    sys.exit()