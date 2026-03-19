from sudoku_board import SudokuBoard
from sudoku_solver import SudokuSolver
from game_state import GameState, GameScreen, PopUpType
from board_provider import BoardProvider
from typing import Optional, Tuple
import copy
import time

class SudokuGame:
    def __init__(self):
        self.board_provider = BoardProvider()
        self.board: Optional[SudokuBoard] = None
        self.solver = SudokuSolver()
        self.state = GameState()
        
    def start_new_game(self, difficulty: str = "easy") -> None:
        self.board = self.board_provider.get_board(difficulty)
        self.state.reset()
        self.state.difficulty = difficulty
        self.state.current_screen = GameScreen.GAME_PLAY
        self.state.timer_on = True
        
    def make_move(self, x: int, y: int, num: int) -> bool:
        if not self.board or self.board.is_original_cell(x, y):
            return False
            
        if num == 0:
            self.board.clear_cell(x, y)
            self.state.made_move = True
            return True
            
        if self.board.is_valid_move(x, y, num):
            self.board.set_cell(x, y, num)
            self.state.made_move = True
            
            if self.board.is_complete() and self._is_solved_correctly():
                self.state.game_over = True
                
            return True
        else:
            self.board.set_cell(x, y, num)
            self.state.made_move = True
            self.state.increment_mistakes()
            return False
            
    def _is_solved_correctly(self) -> bool:
        if not self.board:
            return False
            
        for y in range(9):
            for x in range(9):
                if not self.board.is_valid_move(x, y, self.board.get_cell(x, y)):
                    return False
        return True
            
    def solve_instant(self) -> bool:
        if self.board:
            return self.solver.solve(self.board)
        return False
        
    def solve_animated(self, callback=None) -> None:
        if not self.board:
            return
            
        def solve_step_by_step(board, delay=0.05):
            empty = self.solver.find_empty(board)
            if not empty:
                return True
                
            y, x = empty
            
            for num in range(1, 10):
                if board.is_valid_move(x, y, num):
                    board.set_cell(x, y, num)
                    
                    if callback:
                        callback()
                    
                    time.sleep(delay)
                    
                    if solve_step_by_step(board, delay):
                        return True
                        
                    board.set_cell(x, y, 0)
                    
                    if callback:
                        callback()
                    
                    time.sleep(delay)
                    
            return False
            
        solve_step_by_step(self.board, 0.05)
        
    def is_solvable(self) -> bool:
        if self.board:
            return self.solver.is_solvable(self.board)
        return False
        
    def get_selected_cell(self) -> Optional[Tuple[int, int]]:
        return self.state.selected_cell
        
    def select_cell(self, x: int, y: int) -> None:
        if self.board and not self.board.is_original_cell(x, y):
            self.state.select_cell(x, y)
        else:
            self.state.deselect_cell()
            
    def deselect_cell(self) -> None:
        self.state.deselect_cell()
        
    def get_time_elapsed(self) -> int:
        return self.state.time_elapsed
        
    def get_mistakes(self) -> int:
        return self.state.mistakes
        
    def is_game_over(self) -> bool:
        return self.state.game_over
        
    def navigate_to_screen(self, screen: GameScreen) -> None:
        self.state.current_screen = screen
        if screen == GameScreen.MAIN_MENU:
            self.state.reset_solver_boards = False