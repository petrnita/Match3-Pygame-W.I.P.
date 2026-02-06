import pygame, sys
from pygame import Surface
from pygame.sprite import Group, GroupSingle
from pygame.math import Vector2 as vec
from pygame.cursors import Cursor
from game_assets import Board_Manager, Gem
from check_matching import Check_Matching
from sprites import Fade, Player_Text
from sprites import Text_Fade, Swap_Dirs, Bar
from debug import Show_Text

from debug import log, clear
from debug import debug

clear()

class Screen_Manager():
    def __init__(self):
        from consts import SCREEN
        self.Main = pygame.display.set_mode(SCREEN.SIZE)
        pygame.display.set_caption('Match-3 game tutorial 2026 > Petr Nita <')
        self.Board = Surface((SCREEN.ELEMENTS_RECTS['board'].w, SCREEN.ELEMENTS_RECTS['board'].h)).convert_alpha()
        self.Anim = self.Board.copy().convert_alpha()
        self.Top = self.Main.copy().convert_alpha()
        self.debug_shuffle = False

    def paint_screen(self):
        from consts import SCREEN, COLORS
        self.Main.blit(SCREEN.IMAGE, (0, 0))
        self.Board.fill(COLORS.TRANSPARENT)
        self.Anim.fill(COLORS.TRANSPARENT)
        self.Top.fill(COLORS.TRANSPARENT)
        
    def draw(self):
        from consts import SCREEN
        self.Main.blit(self.Board, SCREEN.POSITIONS['board'])
        self.Main.blit(self.Anim, SCREEN.POSITIONS['board'])
        self.Main.blit(SCREEN.ELEMENTS['title'], SCREEN.POSITIONS['title'])
        self.Main.blit(self.Top, (0, 0))

# debug
        pygame.display.flip()
        if self.debug_shuffle:
            self.debug_shuffle = False
            self.print_screen()

    def print_screen(self):
        from consts import SCREEN
        image = self.Main.subsurface(SCREEN.POSITIONS_RECTS['board'])
        pygame.image.save(image, 'gfx/screenshot.png')


class Player():
    def __init__(self):
        self._text: Player_Text = None
        self._find_gem: Gem = None
        self._find_direction: vec = None
        self._swap = False
        self._start_move: bool = True
        self._end_move: bool = False
        self._bars: list[Bar] = []
        self._damage: int = 0
        self._extra_move: bool = False

    @property
    def text(self) -> Player_Text:
        return self._text
    
    @text.setter
    def text(self, value: Player_Text):
        self._text = value
    
    @property
    def find_gem(self) -> Gem:
        return self._find_gem
    
    @find_gem.setter
    def find_gem(self, value: Gem):
        self._find_gem = value
    
    @property
    def find_direction(self) -> vec:
        return self._find_direction
    
    @find_direction.setter
    def find_direction(self, value: vec):
        self._find_direction = value
    
    @property
    def swap(self) -> bool:
        return self._swap
    
    @swap.setter
    def swap(self, value: bool):
        self._swap = value
    
    @property
    def start_move(self) -> bool:
        return self._start_move
    
    @start_move.setter
    def start_move(self, value: bool):
        self._start_move = value

    @property
    def end_move(self) -> bool:
        return self._end_move
    
    @end_move.setter
    def end_move(self, value: bool):
        self._end_move = value
    
    @property
    def bars(self) -> list[Bar]:
        return self._bars
    
    @property
    def damage(self) -> int:
        return self._damage
    
    @damage.setter
    def damage(self, value: int):
        self._damage = value

    @property
    def extra_move(self) -> bool:
        return self._extra_move
    
    @extra_move.setter
    def extra_move(self, value: bool):
        self._extra_move = value

    def swap_image(self, player):
        self.text.swap_image()
        player.text.swap_image()


class GameManager():
    def __init__(self):
        from consts import SCREEN
        import os
        self.clock = pygame.time.Clock()
        self.make_groups()
        self.screen_manager: Screen_Manager = Screen_Manager()
        self.board_manager: Board_Manager = Board_Manager()
        self.game_status = 'start'
        self.current_player: str = 'Player'
        self.player: Player = Player()
        self.player.text = Player_Text(self.text_group, SCREEN.POSITIONS['player'], 'player')
        self.player.start_move = True
        self.swaping = False
        self.cpu: Player = Player()
        self.cpu.text = Player_Text(self.text_group, SCREEN.POSITIONS['cpu'], 'cpu')
        self.cpu.text.swap_image()
        self.player.swap_image(self.cpu)
        self.make_bars()
        self.move_delay = pygame.USEREVENT + 0
        pygame.time.set_timer(self.move_delay, 5000)
        self.gems_are_killed = False
        self.board_is_idle = False
        self.ready_to_move = False
        self.debug_group: Group = Group()
        self.debug_fps = Show_Text(self.debug_group, '', vec(12, 12))
        self.pause = False
        self.change_cursor('hand', True, False)
        Fade(self.fade_group, 2, 'Out')

    def make_groups(self):
        self.fade_group: GroupSingle = GroupSingle()
        self.anim_group: Group = Group()
        self.text_group: Group = Group()
        self.bars_group: Group = Group()

    def make_bars(self):
        from consts import SCREEN
        for bar in range(6):
            self.player.bars.append(Bar(self.bars_group, SCREEN.ELEMENTS, 'battle', 'player', f'{bar+1}'))
            self.cpu.bars.append(Bar(self.bars_group, SCREEN.ELEMENTS, 'battle', 'cpu', f'{bar+1}'))
        self.time_bar = Bar(self.bars_group, SCREEN.ELEMENTS, 'time', 'time', 'progress')

    def update(self, events, dt):
        self.board_manager.update(events, dt, self)
        self.fade_group.update(dt)
        self.text_group.update(dt)
        self.anim_group.update(dt)

        if self.game_status == 'shuffle':
            if self.board_manager.board_is_idle:
                Fade(self.fade_group, 2, 'Out')
                # self.game_status = 'play'

        self.bars_group.update(dt)

        self.debug_group.update(f'FPS: {int(self.clock.get_fps())}')

        # if self.game_status == 'start':
        #     if self.ready_to_move == True:
        #         self.wait(2000)
        #         print('start')

        if self.game_status == 'play' or self.game_status == 'start' or self.game_status == 'shuffle':
            if self.ready_to_move:
                if self.current_player == 'CPU':
                    self.cpu_playing()
                    if self.gems_are_killed:
                        self.gems_are_killed = False
                        self.take_damage(self.cpu, self.player)
                else:
                    self.player_playing()
                    if self.gems_are_killed:
                        self.gems_are_killed = False
                        self.take_damage(self.player, self.cpu)

    def draw(self):   
        self.fade_group.draw(self.screen_manager.Anim)
        self.bars_group.draw(self.screen_manager.Top)
        self.text_group.draw(self.screen_manager.Top)
        self.debug_group.draw(self.screen_manager.Main)
        
    def main_loop(self):
        from consts import GEMS_KILLED_EVENT, BOARD_IS_IDLE_EVENT, SWAPING_EVENT
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
                    pass
                if event.type == self.move_delay:
                    self.ready_to_move = True
                if event.type == GEMS_KILLED_EVENT:
                    self.gems_are_killed = True
                if event.type == BOARD_IS_IDLE_EVENT:
                    self.board_is_idle = True
                if event.type == SWAPING_EVENT:
                    self.swaping = True
                                       
            self.screen_manager.paint_screen()

            if not self.pause:
                self.update(events, dt)

            self.draw()

            self.screen_manager.draw()

    def player_playing(self):
        if not self.board_manager.board_is_idle: return

        if self.player.start_move:
            if not self.game_status == 'start' and not self.game_status == 'shuffle':
                self.player.swap_image(self.cpu)
                log('player swaping image')
            else:
                log('play')
                self.game_status = 'play'
            find_gem, _ = Check_Matching.check(self.board_manager.board)
            if not find_gem:
                self.screen_manager.debug_shuffle = True
                self.shuffle_gems()
                self.game_status = 'shuffle'
                self.wait(4000)
                return
            self.player.start_move = False

        if not self.player.end_move:
            if self.swaping:
                log(f'{self.swaping=}')
                self.swaping = False
                self.player.end_move = True
                self.wait(1000)
                return
        else:
            log(f'{self.player.end_move=}') 
            if self.player.extra_move:
                log('player has extra move')
                self.player.extra_move = False
                self.player.start_move = True
                self.player.end_move = False
                self.wait(2000)
                return 
            
            self.current_player = 'CPU'
            log(f'{self.current_player=}', '[bold blue]CPU[/] is playing')
            self.player.end_move = False

        return
        if self.player.swap:
            debug(f'{self.player.swap=}')
            self.player.swap = False
            self.player.swap_image(self.cpu)
            return

        if self.player.start_move:
            debug(f'{self.player.start_move=}')
            find_gem, _ = Check_Matching.check(self.board_manager.board)
            debug(f'{find_gem=}')
            if not find_gem:
                self.screen_manager.debug_shuffle = True
                self.shuffle_gems()
                self.game_status = 'shuffle'
                self.wait(4000)
                return
            self.player.start_move = False

        if self.board_manager.get_swaping():
            debug(f'{self.board_manager.get_swaping()=}')
            self.player.end_move = True
            self.wait(1000)
            return

        if self.player.end_move:
            debug(f'{self.player.end_move=}')
            self.player.end_move = False
            self.player.start_move = True
            if self.player.extra_move:
                debug(f'{self.player.extra_move=}')
                self.player.extra_move = False
                self.player.end_move = False
                self.wait(2000)
                return            
            self.current_player = 'CPU'
            debug(f'{self.current_player=}')
            self.cpu.swap = True
            self.wait(2000)

    def cpu_playing(self):
        from consts import SWAP_DIRS
        if not self.board_manager.board_is_idle: return

        log('idle')
    
        if self.cpu.start_move:
            if not self.game_status == 'start' and not self.game_status == 'shuffle':
                self.player.swap_image(self.cpu)
                log('CPU swaping image')
            else:
                log('play')
                self.game_status = 'play'
            self.cpu.find_gem, self.cpu.find_direction = Check_Matching.check(self.board_manager.board)
            if not self.cpu.find_gem:
                self.screen_manager.debug_shuffle = True
                self.shuffle_gems()
                self.game_status = 'shuffle'
                self.wait(4000)
                self.cpu.start_move = True
                return
            self.cpu.start_move = False

            self.board_manager.select_gem(self.cpu.find_gem)
            Swap_Dirs(self.board_manager.swapdir_group,
                    self.cpu.find_gem.bpos,
                    SWAP_DIRS.ANIM, SWAP_DIRS.OFFSET,
                    (self.cpu.find_direction))
            self.wait(500, loops=1)
            return
        
        if not self.cpu.end_move:
            swaped_gem = self.board_manager.board[int(self.cpu.find_gem.bpos.pos.x+self.cpu.find_direction[0])][int(self.cpu.find_gem.bpos.pos.y+self.cpu.find_direction[1])]
            self.board_manager.select_gem(swaped_gem)
            if self.cpu.extra_move:
                self.cpu.extra_move = False
                self.wait(2000)
                return
            self.cpu.end_move = True
            self.wait(1000)
            return

        if self.board_manager.board_is_idle:
            self.cpu.start_move = True
            self.cpu.end_move = False
            self.current_player = 'Player'
            log(f'{self.current_player=}', '[bold violet]Player[/] is playing')
            self.player.swap = True
            self.swaping = False
            self.player.start_move = True                  
            self.wait(2000)



        return
        if self.cpu.start_move:
            debug(f'{self.cpu.start_move=}')
            self.cpu.swap = False
            self.cpu.swap_image(self.player)            
            self.cpu.start_move = False
            self.cpu.find_gem, self.cpu.find_direction = Check_Matching.check(self.board_manager.board)
            debug(f'{self.cpu.find_gem=}, {self.cpu.find_direction=}')
            if not self.cpu.find_gem:
                self.screen_manager.debug_shuffle = True
                self.shuffle_gems()
                self.game_status = 'shuffle'
                self.wait(4000)
                self.cpu.start_move = True
                return
            
            self.board_manager.select_gem(self.cpu.find_gem)
            debug('cpu selecting gem1...')
            Swap_Dirs(self.board_manager.swapdir_group,
                    self.cpu.find_gem.bpos,
                    SWAP_DIRS.ANIM, SWAP_DIRS.OFFSET,
                    (self.cpu.find_direction))
            self.wait(500, loops=1)
            return
        else:
            if not self.cpu.end_move:
                gem = self.cpu.find_gem
                direction = self.cpu.find_direction
                self.board_manager.select_gem(self.board_manager.board[int(gem.bpos.pos.x+direction[0])][int(gem.bpos.pos.y+direction[1])], True)
                debug('cpu selecting gem2...')
                if self.cpu.extra_move:
                    self.cpu.extra_move = False
                    self.wait(2000)
                    return
                self.cpu.end_move = True
                self.wait(1000)
                #return

        if not self.cpu.end_move: return

        if self.board_manager.board_is_idle:
            self.cpu.start_move = True
            self.cpu.end_move = False
            self.current_player = 'Player'
            self.player.swap = True                    
            self.wait(2000)

    def take_damage(self, current_player: Player, opponent: Player):
        debug(self.current_player)
        current_player.damage = len(self.board_manager.gems_killed)
        matching = len(self.board_manager.gems_killed)
        if matching == 4:
            current_player.damage *= 2
        elif matching > 4:
            current_player.extra_move = True

        if current_player.damage > 0:
            bar = list(self.board_manager.gems_killed)[0].number
            if bar < 7:
                opponent.bars[bar-1].value -= current_player.damage

    def wait(self, delay: int, loops: int=0):
        pygame.time.set_timer(self.move_delay, delay, loops=loops)
        self.ready_to_move = False

    def shuffle_gems(self):
        from consts import TXT_NO_MOVE
        Fade(self.fade_group, 2)
        Text_Fade(self.text_group,
                  TXT_NO_MOVE.OFFSET,
                  TXT_NO_MOVE.IMAGE,
                  .03,
                  5,
                  size_direction='grow',
                  fade_direction='Out')
        self.board_manager.shuffle_board()
        self.game_status = 'shuffle'

    def print_screen(self):
        from consts import SCREEN
        image = self.screen_manager.Main.subsurface(SCREEN.POSITIONS_RECTS['board'])
        pygame.image.save(image, 'gfx/screenshot.png')

    def change_cursor(self, cursor: str='hand', init: bool=False, reset: bool=False):
        from consts import SCREEN
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
    game_manager.main_loop()
    game_manager.change_cursor(reset=True)
    pygame.quit()
    sys.exit()


