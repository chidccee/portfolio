import pygame
import sys
import time
from typing import Tuple
from sudoku_game import SudokuGame
from sudoku_renderer import SudokuRenderer
from game_state import GameScreen, PopUpType
from menu_manager import MenuManager

class SudokuApp:
    def __init__(self):
        pygame.init()
        self.game = SudokuGame()
        self.renderer = SudokuRenderer()
        self.menu_manager = MenuManager()
        self.running = True
        self.last_time_update = time.time()
        self.animating = False  
        
        try:
            pygame.mixer.init()
            self.click_sound = pygame.mixer.Sound("click.ogg")
            self.move_sound = pygame.mixer.Sound("move.ogg")
            self.congratulation_sound = pygame.mixer.Sound("congratulation.ogg")
            self.game_start_sound = pygame.mixer.Sound("gameStart.ogg")
        except:
            print("Sound files not found, continuing without sound")
            self.click_sound = None
            self.move_sound = None
            self.congratulation_sound = None
            self.game_start_sound = None
        
    def run(self) -> None:
        while self.running:
            current_time = time.time()
            
            if current_time - self.last_time_update >= 1 and not self.animating:
                self.game.state.increment_time()
                self.last_time_update = current_time
                
            self._handle_events()
            self._render()
            
        pygame.quit()
        sys.exit()
        
    def _handle_events(self) -> None:
        if self.animating:
            return
            
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(mouse_pos)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(mouse_pos)
                
    def _handle_key_press(self, key: int) -> None:
        if self.animating:
            return
            
        if self.game.state.current_screen == GameScreen.INTRO:
            if key == pygame.K_RETURN and not self.game.state.intro_click:
                self._play_sound(self.click_sound)
                self.game.state.intro_click = True
                self.game.state.current_screen = GameScreen.MAIN_MENU
                
        elif self.game.state.current_screen == GameScreen.GAME_PLAY:
            selected = self.game.get_selected_cell()
            if selected and self.game.state.active_popup == PopUpType.NONE:
                x, y = selected
                
                if pygame.K_1 <= key <= pygame.K_9:
                    num = key - pygame.K_0
                    self.game.make_move(x, y, num)
                    self._play_sound(self.move_sound)
                elif key == pygame.K_0 or key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                    self.game.make_move(x, y, 0)
                    
            if key == pygame.K_SPACE and self.game.state.active_popup == PopUpType.NONE:
                self._play_sound(self.click_sound)
                self.game.state.show_popup(PopUpType.AUTO_SOLVE)
                
        elif self.game.state.current_screen == GameScreen.SOLVER:
            selected = self.game.get_selected_cell()
            if selected:
                x, y = selected
                
                if pygame.K_1 <= key <= pygame.K_9:
                    num = key - pygame.K_0
                    self.game.make_move(x, y, num)
                    self._play_sound(self.move_sound)
                elif key == pygame.K_0 or key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                    self.game.make_move(x, y, 0)
                    
            if key == pygame.K_SPACE and self.game.state.active_popup == PopUpType.NONE:
                if self.game.is_solvable():
                    self._play_sound(self.click_sound)
                    self.game.state.show_popup(PopUpType.AUTO_SOLVE)
                    
    def _handle_mouse_down(self, mouse_pos: Tuple[int, int]) -> None:
        if self.animating:
            return
            
        if (self.game.state.current_screen == GameScreen.GAME_PLAY or 
            self.game.state.current_screen == GameScreen.SOLVER):
            if self.game.state.active_popup == PopUpType.NONE:
                cell = self.menu_manager.get_cell_at_pos(mouse_pos)
                if cell:
                    self.game.select_cell(cell[0], cell[1])
                else:
                    self.game.deselect_cell()
                    
    def _handle_mouse_up(self, mouse_pos: Tuple[int, int]) -> None:
        if self.animating:
            return
            
        if self.game.state.current_screen == GameScreen.MAIN_MENU:
            if self.menu_manager.cursor('onPlayText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.current_screen = GameScreen.PLAY_MENU
                
            elif self.menu_manager.cursor('onSolverText', mouse_pos):
                self._play_sound(self.click_sound)
                self._start_solver()
                
            elif self.menu_manager.cursor('onScoreBoardText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.current_screen = GameScreen.SCORE_BOARD
                
            elif self.menu_manager.cursor('onExitText', mouse_pos):
                self.running = False
                
        elif self.game.state.current_screen == GameScreen.PLAY_MENU:
            if self.menu_manager.cursor('onMainMenuText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.current_screen = GameScreen.MAIN_MENU
                
            elif self.menu_manager.cursor('onEasyText', mouse_pos):
                self._start_new_game('easy')
                
            elif self.menu_manager.cursor('onMediumText', mouse_pos):
                self._start_new_game('medium')
                
            elif self.menu_manager.cursor('onHardText', mouse_pos):
                self._start_new_game('hard')
                
            elif self.menu_manager.cursor('onVeryHardText', mouse_pos):
                self._start_new_game('veryHard')
                
        elif self.game.state.current_screen == GameScreen.SCORE_BOARD:
            if self.menu_manager.cursor('onMainMenuText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.current_screen = GameScreen.MAIN_MENU

        elif self.game.state.current_screen == GameScreen.GAME_PLAY:
            if self.menu_manager.cursor('onGamePlayMainMenuText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.show_popup(PopUpType.EXIT_CONFIRM)
                
        elif self.game.state.current_screen == GameScreen.SOLVER:
            if self.menu_manager.cursor('onGamePlayMainMenuText', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.current_screen = GameScreen.MAIN_MENU
                self.game.state.game_grid_switch = True

        if self.game.state.active_popup != PopUpType.NONE:
            self._handle_popup_click(mouse_pos)
            
    def _handle_popup_click(self, mouse_pos: Tuple[int, int]) -> None:
        if self.animating:
            return
            
        if self.game.state.active_popup == PopUpType.EXIT_CONFIRM:
            if self.menu_manager.cursor('onCancel', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.hide_popup()
            elif self.menu_manager.cursor('onOk', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.hide_popup()
                self.game.state.current_screen = GameScreen.MAIN_MENU
                self.game.state.game_grid_switch = True
                self.game.state.timer_on = False
                
        elif self.game.state.active_popup == PopUpType.AUTO_SOLVE:
            if self.menu_manager.cursor('onCancel', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.hide_popup()
            elif self.menu_manager.cursor('onAutoSolveDirect', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.solve_instant()
                self.game.state.hide_popup()
            elif self.menu_manager.cursor('onAutoSolveAnimation', mouse_pos):
                self._play_sound(self.click_sound)
                self.game.state.hide_popup()
                self._start_animated_solve()
                
    def _start_animated_solve(self) -> None:
        self.animating = True
        
        def update_callback():
            self._render()
            pygame.display.flip()
            pygame.event.pump()
            
        self.game.solve_animated(update_callback)
        self.animating = False
                
    def _start_new_game(self, difficulty: str) -> None:
        self._play_sound(self.click_sound)
        if self.game_start_sound:
            self.game_start_sound.play()
        self.game.start_new_game(difficulty)
        
    def _start_solver(self) -> None:
        self._play_sound(self.click_sound)
        self.game.state.current_screen = GameScreen.SOLVER
        self.game.state.game_grid_switch = True
        if not self.game.state.reset_solver_boards:
            from sudoku_board import SudokuBoard
            self.game.board = SudokuBoard()  
            self.game.state.reset_solver_boards = True
            
    def _play_sound(self, sound) -> None:
        if sound:
            try:
                sound.play()
            except:
                pass
                
    def _render(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        
        if self.game.state.current_screen == GameScreen.INTRO:
            self.renderer.draw_intro(self.game)
            
        elif self.game.state.current_screen == GameScreen.MAIN_MENU:
            self.renderer.draw_main_menu(self.game, mouse_pos)
            
        elif self.game.state.current_screen == GameScreen.PLAY_MENU:
            self.renderer.draw_play_menu(self.game, mouse_pos)
            
        elif self.game.state.current_screen == GameScreen.GAME_PLAY:
            self.renderer.draw_game_board(self.game, mouse_pos)
            
        elif self.game.state.current_screen == GameScreen.SOLVER:
            self.renderer.draw_game_board(self.game, mouse_pos)
            
        elif self.game.state.current_screen == GameScreen.SCORE_BOARD:
            self.renderer.screen.fill(self.renderer.color_manager.get_color('black'))
            sudoku_font = self.renderer.font_manager.load_font(100)
            sudoku_text = sudoku_font.render("SUDOKU", True, self.renderer.color_manager.get_color('white'))
            self.renderer.screen.blit(sudoku_text, (60, 80))
            
            menu_font = self.renderer.font_manager.load_font(30, True)
            menu_text = menu_font.render("[main menu]", True, self.renderer.color_manager.get_color('white'))
            menu_rect = menu_text.get_rect(topleft=(50, 40))
            
            if menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.renderer.screen, self.renderer.color_manager.get_color('white'), 
                               (menu_rect.x, menu_rect.y, menu_rect.width, menu_rect.height))
                menu_text_inverted = menu_font.render("[main menu]", True, self.renderer.color_manager.get_color('black'))
                self.renderer.screen.blit(menu_text_inverted, menu_rect)
            else:
                self.renderer.screen.blit(menu_text, menu_rect)
                
            score_font = self.renderer.font_manager.load_font(40, True)
            score_text = score_font.render("Score Board - Coming Soon", True, self.renderer.color_manager.get_color('white'))
            self.renderer.screen.blit(score_text, (100, 300))
        
        if self.game.state.active_popup != PopUpType.NONE:
            self.renderer.draw_popup(self.game, mouse_pos)
            
        if (self.game.state.current_screen == GameScreen.GAME_PLAY and 
            self.game.is_game_over() and not self.game.state.congrates_played):
            self._play_sound(self.congratulation_sound)
            self.game.state.congrates_played = True
            
        pygame.display.flip()

if __name__ == "__main__":
    app = SudokuApp()
    app.run()