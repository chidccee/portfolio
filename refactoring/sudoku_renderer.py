import pygame
import time
from typing import Tuple, Optional
from sudoku_game import SudokuGame
from game_state import GameScreen, PopUpType

class ColorManager:
    @staticmethod
    def get_color(color_name: str) -> Tuple[int, int, int]:
        colors = {
            'green': (40, 160, 30),
            'black': (20, 20, 20),
            'white': (240, 240, 240),
            'dimWhite': (150, 150, 150),
            'red': (170, 10, 10),
            'orange': (190, 80, 20),
            'grey': (80, 80, 80),
            'dimGrey': (40, 40, 40),
            'veryDimGrey': (30, 30, 30)
        }
        return colors.get(color_name, (0, 0, 0))

class FontManager:
    def __init__(self):
        self.fonts = {}
        
    def load_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = f"{size}_{bold}"
        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.SysFont("Arial", size, bold=bold)
            except:
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]

class SudokuRenderer:
    def __init__(self, screen_width: int = 600, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("~SUDOKU~")
        
        self.color_manager = ColorManager()
        self.font_manager = FontManager()
        
        self.cell_size = 66
        self.board_start_x = 2
        self.board_start_y = 100
        self.board_size = self.cell_size * 9
        
    def draw_intro(self, game) -> None:
        if game.state.grid_switch:
            self._draw_grid_animation('main')
            game.state.grid_switch = False

        sudoku_font = self.font_manager.load_font(100)
        sudoku_text = sudoku_font.render("SUDOKU", True, self.color_manager.get_color('red'))
        self.screen.blit(sudoku_text, (60, 120))
        
        line_font = self.font_manager.load_font(30)
        line_text = line_font.render("press [ENTER]", True, self.color_manager.get_color('green'))
        self.screen.blit(line_text, (200, 600))
        
    def draw_main_menu(self, game, mouse_pos: Tuple[int, int]) -> None:
        self.screen.fill(self.color_manager.get_color('black'))
        
        sudoku_font = self.font_manager.load_font(100)
        sudoku_text = sudoku_font.render("SUDOKU", True, self.color_manager.get_color('white'))
        self.screen.blit(sudoku_text, (60, 120))
        
        play_font = self.font_manager.load_font(50, True)
        solver_font = self.font_manager.load_font(50, True)
        score_font = self.font_manager.load_font(50, True)
        exit_font = self.font_manager.load_font(50, True)
        
        play_text = play_font.render("-: PLAY :-", True, self.color_manager.get_color('white'))
        play_rect = play_text.get_rect(center=(300, 330))
        
        solver_text = solver_font.render("-: SOLVER :-", True, self.color_manager.get_color('white'))
        solver_rect = solver_text.get_rect(center=(300, 430))
        
        score_text = score_font.render("-: SCORE BOARD :-", True, self.color_manager.get_color('white'))
        score_rect = score_text.get_rect(center=(300, 530))
        
        exit_text = exit_font.render("-: EXIT :-", True, self.color_manager.get_color('white'))
        exit_rect = exit_text.get_rect(center=(300, 630))
        
        if play_rect.collidepoint(mouse_pos):
            play_font_big = self.font_manager.load_font(65, True)
            play_text_big = play_font_big.render("-: PLAY :-", True, self.color_manager.get_color('white'))
            play_rect_big = play_text_big.get_rect(center=(300, 330))
            self.screen.blit(play_text_big, play_rect_big)
        else:
            self.screen.blit(play_text, play_rect)
            
        if solver_rect.collidepoint(mouse_pos):
            solver_font_big = self.font_manager.load_font(65, True)
            solver_text_big = solver_font_big.render("-: SOLVER :-", True, self.color_manager.get_color('white'))
            solver_rect_big = solver_text_big.get_rect(center=(300, 430))
            self.screen.blit(solver_text_big, solver_rect_big)
        else:
            self.screen.blit(solver_text, solver_rect)
            
        if score_rect.collidepoint(mouse_pos):
            score_font_big = self.font_manager.load_font(65, True)
            score_text_big = score_font_big.render("-: SCORE BOARD :-", True, self.color_manager.get_color('white'))
            score_rect_big = score_text_big.get_rect(center=(300, 530))
            self.screen.blit(score_text_big, score_rect_big)
        else:
            self.screen.blit(score_text, score_rect)
            
        if exit_rect.collidepoint(mouse_pos):
            exit_font_big = self.font_manager.load_font(65, True)
            exit_text_big = exit_font_big.render("-: EXIT :-", True, self.color_manager.get_color('white'))
            exit_rect_big = exit_text_big.get_rect(center=(300, 630))
            self.screen.blit(exit_text_big, exit_rect_big)
        else:
            self.screen.blit(exit_text, exit_rect)
            
    def draw_play_menu(self, game, mouse_pos: Tuple[int, int]) -> None:
        self.screen.fill(self.color_manager.get_color('black'))
        
        sudoku_font = self.font_manager.load_font(100)
        sudoku_text = sudoku_font.render("SUDOKU", True, self.color_manager.get_color('white'))
        self.screen.blit(sudoku_text, (60, 120))
        
        menu_font = self.font_manager.load_font(30, True)
        menu_text = menu_font.render("[main menu]", True, self.color_manager.get_color('white'))
        menu_rect = menu_text.get_rect(topleft=(50, 40))
        
        if menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), 
                           (menu_rect.x, menu_rect.y, menu_rect.width, menu_rect.height))
            menu_text_inverted = menu_font.render("[main menu]", True, self.color_manager.get_color('black'))
            self.screen.blit(menu_text_inverted, menu_rect)
        else:
            self.screen.blit(menu_text, menu_rect)
        
        easy_font = self.font_manager.load_font(50, True)
        medium_font = self.font_manager.load_font(50, True)
        hard_font = self.font_manager.load_font(50, True)
        very_hard_font = self.font_manager.load_font(50, True)

        easy_text = easy_font.render("-: EASY :-", True, self.color_manager.get_color('white'))
        easy_rect = easy_text.get_rect(center=(300, 330))
        
        medium_text = medium_font.render("-: MEDIUM :-", True, self.color_manager.get_color('white'))
        medium_rect = medium_text.get_rect(center=(300, 430))

        hard_text = hard_font.render("-: HARD :-", True, self.color_manager.get_color('white'))
        hard_rect = hard_text.get_rect(center=(300, 530))
        
        very_hard_text = very_hard_font.render("-: VERY HARD :-", True, self.color_manager.get_color('white'))
        very_hard_rect = very_hard_text.get_rect(center=(300, 630))
        
        if easy_rect.collidepoint(mouse_pos):
            easy_font_big = self.font_manager.load_font(65, True)
            easy_text_big = easy_font_big.render("-: EASY :-", True, self.color_manager.get_color('white'))
            easy_rect_big = easy_text_big.get_rect(center=(300, 330))
            self.screen.blit(easy_text_big, easy_rect_big)
        else:
            self.screen.blit(easy_text, easy_rect)
            
        if medium_rect.collidepoint(mouse_pos):
            medium_font_big = self.font_manager.load_font(65, True)
            medium_text_big = medium_font_big.render("-: MEDIUM :-", True, self.color_manager.get_color('white'))
            medium_rect_big = medium_text_big.get_rect(center=(300, 430))
            self.screen.blit(medium_text_big, medium_rect_big)
        else:
            self.screen.blit(medium_text, medium_rect)
            
        if hard_rect.collidepoint(mouse_pos):
            hard_font_big = self.font_manager.load_font(65, True)
            hard_text_big = hard_font_big.render("-: HARD :-", True, self.color_manager.get_color('white'))
            hard_rect_big = hard_text_big.get_rect(center=(300, 530))
            self.screen.blit(hard_text_big, hard_rect_big)
        else:
            self.screen.blit(hard_text, hard_rect)
            
        if very_hard_rect.collidepoint(mouse_pos):
            very_hard_font_big = self.font_manager.load_font(65, True)
            very_hard_text_big = very_hard_font_big.render("-: VERY HARD :-", True, self.color_manager.get_color('white'))
            very_hard_rect_big = very_hard_text_big.get_rect(center=(300, 630))
            self.screen.blit(very_hard_text_big, very_hard_rect_big)
        else:
            self.screen.blit(very_hard_text, very_hard_rect)
            
    def draw_game_board(self, game, mouse_pos: Tuple[int, int]) -> None:
        if game.state.game_grid_switch:
            self._draw_grid_animation('gamePlay')
            game.state.game_grid_switch = False

        self.screen.fill(self.color_manager.get_color('black'))
        
        self._draw_grid()
        
        self._draw_numbers(game)
        
        self._highlight_selected_cell(game)
        
        self._draw_game_info(game)
        
        menu_font = self.font_manager.load_font(30, True)
        menu_text = menu_font.render("[main menu]", True, self.color_manager.get_color('white'))
        menu_rect = menu_text.get_rect(topleft=(20, 20))
        
        if menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), 
                           (menu_rect.x, menu_rect.y, menu_rect.width, menu_rect.height))
            menu_text_inverted = menu_font.render("[main menu]", True, self.color_manager.get_color('black'))
            self.screen.blit(menu_text_inverted, menu_rect)
        else:
            self.screen.blit(menu_text, menu_rect)
            
        space_font = self.font_manager.load_font(30)
        space_text = space_font.render("Press [SPACE] to Autosolve", True, self.color_manager.get_color('grey'))
        self.screen.blit(space_text, (110, 725))
        
    def draw_popup(self, game, mouse_pos: Tuple[int, int]) -> None:
        if game.state.active_popup == PopUpType.EXIT_CONFIRM:
            self._draw_exit_confirm_popup(mouse_pos)
        elif game.state.active_popup == PopUpType.AUTO_SOLVE:
            self._draw_autosolve_popup(mouse_pos)
            
    def _draw_exit_confirm_popup(self, mouse_pos: Tuple[int, int]) -> None:
        s = pygame.Surface((600, 200), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.screen.blit(s, (0, 300))
        
        query_font = self.font_manager.load_font(25, True)
        query_text = query_font.render("Are you sure? You will lose your progress !", True, self.color_manager.get_color('white'))
        self.screen.blit(query_text, (50, 340))
        
        cancel_font = self.font_manager.load_font(30, True)
        ok_font = self.font_manager.load_font(30, True)
        
        cancel_text = cancel_font.render("[CANCEL]", True, self.color_manager.get_color('white'))
        cancel_rect = cancel_text.get_rect(topleft=(130, 420))
        
        ok_text = ok_font.render("[OK]", True, self.color_manager.get_color('white'))
        ok_rect = ok_text.get_rect(topleft=(400, 420))
        
        if cancel_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), cancel_rect)
            cancel_text_inverted = cancel_font.render("[CANCEL]", True, self.color_manager.get_color('black'))
            self.screen.blit(cancel_text_inverted, cancel_rect)
        else:
            self.screen.blit(cancel_text, cancel_rect)
            
        if ok_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), ok_rect)
            ok_text_inverted = ok_font.render("[OK]", True, self.color_manager.get_color('black'))
            self.screen.blit(ok_text_inverted, ok_rect)
        else:
            self.screen.blit(ok_text, ok_rect)
            
    def _draw_autosolve_popup(self, mouse_pos: Tuple[int, int]) -> None:
        s = pygame.Surface((600, 250), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.screen.blit(s, (0, 300))
        
        query_font = self.font_manager.load_font(24, True)
        query_text = query_font.render("Are you sure? You don't want to solve on your own!", True, self.color_manager.get_color('white'))
        self.screen.blit(query_text, (10, 320))
        
        cancel_font = self.font_manager.load_font(30, True)
        solution_font = self.font_manager.load_font(30, True)
        animation_font = self.font_manager.load_font(30, True)
        
        cancel_text = cancel_font.render("[CANCEL]", True, self.color_manager.get_color('white'))
        cancel_rect = cancel_text.get_rect(topleft=(130, 420))
        
        solution_text = solution_font.render("[SOLUTION]", True, self.color_manager.get_color('white'))
        solution_rect = solution_text.get_rect(topleft=(320, 380))
        
        animation_text = animation_font.render("[ANIMATION]", True, self.color_manager.get_color('white'))
        animation_rect = animation_text.get_rect(topleft=(310, 470))
        
        if cancel_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), cancel_rect)
            inverted_text = cancel_font.render("[CANCEL]", True, self.color_manager.get_color('black'))
            self.screen.blit(inverted_text, cancel_rect)
        else:
            self.screen.blit(cancel_text, cancel_rect)
            
        if solution_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), solution_rect)
            inverted_text = solution_font.render("[SOLUTION]", True, self.color_manager.get_color('black'))
            self.screen.blit(inverted_text, solution_rect)
        else:
            self.screen.blit(solution_text, solution_rect)
            
        if animation_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.color_manager.get_color('white'), animation_rect)
            inverted_text = animation_font.render("[ANIMATION]", True, self.color_manager.get_color('black'))
            self.screen.blit(inverted_text, animation_rect)
        else:
            self.screen.blit(animation_text, animation_rect)
                
    def _draw_grid_animation(self, where: str) -> None:
        self.screen.fill(self.color_manager.get_color('black'))
        
        if where == 'main':
            thickness, thinness = 6, 3
            for step in range(0, 801, 15):
                for ver_pos in range(4, 600, 600//9):
                    pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                                   (ver_pos, 0), (ver_pos, min(step, 800)), thinness)
                for hor_pos in range(100, 700, 600//9):
                    pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                                   (0, hor_pos), (min(step, 600), hor_pos), thinness)
                pygame.display.update()
                
        elif where == 'gamePlay':
            thickness, thinness = 6, 3
            for step in range(100, 699, 12):
                for ver_pos in range(2, 596, 66):
                    pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                                   (ver_pos, 100), (ver_pos, min(step, 698)), thinness)
                for hor_pos in range(100, 694, 66):
                    pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                                   (2, hor_pos), (min(step, 600), hor_pos), thinness)
                pygame.display.update()
                
    def _draw_grid(self) -> None:
        thickness, thinness = 6, 3
        
        for i in range(10):
            x = self.board_start_x + i * self.cell_size
            line_thickness = thinness if i % 3 != 0 else thickness
            pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                           (x, self.board_start_y), (x, self.board_start_y + self.board_size), line_thickness)
                           
        for i in range(10):
            y = self.board_start_y + i * self.cell_size
            line_thickness = thinness if i % 3 != 0 else thickness
            pygame.draw.line(self.screen, self.color_manager.get_color('dimGrey'),
                           (self.board_start_x, y), (self.board_start_x + self.board_size, y), line_thickness)
                           
    def _draw_numbers(self, game) -> None:
        if not game.board:
            return
            
        number_font = self.font_manager.load_font(35)
        original_font = self.font_manager.load_font(45)
        
        for y in range(9):
            for x in range(9):
                cell_value = game.board.get_cell(x, y)
                if cell_value != 0:
                    pos_x = self.board_start_x + x * self.cell_size + (self.cell_size - 20) // 2
                    pos_y = self.board_start_y + y * self.cell_size + (self.cell_size - 35) // 2
                    
                    if game.board.is_original_cell(x, y):
                        number_text = original_font.render(str(cell_value), True, self.color_manager.get_color('grey'))
                    else:
                        if game.board.is_valid_move(x, y, cell_value):
                            number_text = number_font.render(str(cell_value), True, self.color_manager.get_color('white'))
                        else:
                            number_text = number_font.render(str(cell_value), True, self.color_manager.get_color('red'))
                    
                    self.screen.blit(number_text, (pos_x, pos_y))
                    
    def _highlight_selected_cell(self, game) -> None:
        selected = game.get_selected_cell()
        if selected:
            x, y = selected
            rect = pygame.Rect(
                self.board_start_x + x * self.cell_size + 2,
                self.board_start_y + y * self.cell_size + 2,
                self.cell_size - 4,
                self.cell_size - 4
            )
            pygame.draw.rect(self.screen, self.color_manager.get_color('grey'), rect, 3)
            
    def _draw_game_info(self, game) -> None:
        time_font = self.font_manager.load_font(35)
        mistakes_font = self.font_manager.load_font(25)
        
        time_elapsed = game.get_time_elapsed()
        minutes = time_elapsed // 60
        seconds = time_elapsed % 60
        time_text = time_font.render(f"{minutes}:{seconds:02d}", True, self.color_manager.get_color('white'))
        self.screen.blit(time_text, (450, 30))
        
        mistakes = game.get_mistakes()
        mistakes_text = mistakes_font.render(f"Mistakes: {mistakes}", True, self.color_manager.get_color('white'))
        self.screen.blit(mistakes_text, (400, 70))
        
        if game.is_game_over():
            win_font = self.font_manager.load_font(40, True)
            win_text = win_font.render("You Win!", True, self.color_manager.get_color('green'))
            self.screen.blit(win_text, (200, 750))