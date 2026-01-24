from consts import *
import sys
from screen_data import ScreenLayout
from game_assets import Board_Manager


class GameManager():
    
    def __init__(self):
        self.screen_layout: ScreenLayout = ScreenLayout()
        self.clock = pygame.time.Clock()
        self.gems_group = pygame.sprite.Group()
        self.board_manager = Board_Manager(self.gems_group, self.screen_layout)

    def paint_screen(self):
        self.screen_layout.screen.blit(BACKGROUND, (0, 0))
        self.screen_layout.top_screen.fill(TRANSPARENT)
        self.screen_layout.board_screen.blit(BOARD_BACK, (0, 0))

    def update(self, events, dt):
        self.board_manager.update(events, dt)

    def draw(self):
        self.gems_group.draw(self.screen_layout.board_screen)
        self.board_manager.anim_group.draw(self.screen_layout.screen)
        self.screen_layout.screen.blit(self.screen_layout.board_screen, (SCR_LEFT, SCR_TOP))
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
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    
            self.paint_screen()

            self.update(events, dt)

            self.draw()


if __name__ == '__main__':
    game_manager: GameManager = GameManager()
    game_manager.main_loop()
    pygame.quit()
    sys.exit()