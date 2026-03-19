from typing import Tuple, Optional
from enum import Enum

class GameScreen(Enum):
    INTRO = 1
    MAIN_MENU = 2
    PLAY_MENU = 3
    GAME_PLAY = 4
    SOLVER = 5
    SCORE_BOARD = 6

class PopUpType(Enum):
    NONE = 0
    EXIT_CONFIRM = 1
    AUTO_SOLVE = 2

class GameState:
    def __init__(self):
        self.current_screen = GameScreen.INTRO
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.time_elapsed: int = 0
        self.mistakes: int = 0
        self.is_paused: bool = False
        self.game_over: bool = False
        self.difficulty: str = "easy"
        self.active_popup = PopUpType.NONE
        self.grid_switch = True
        self.game_grid_switch = True
        self.intro_click = False
        self.reset_time = True
        self.timer_on = False
        self.made_move = False
        self.congrates_played = False
        self.reset_solver_boards = False
        
    def select_cell(self, x: int, y: int) -> None:
        self.selected_cell = (x, y)
        
    def deselect_cell(self) -> None:
        self.selected_cell = None
        
    def increment_time(self) -> None:
        if not self.is_paused and not self.game_over and self.timer_on:
            self.time_elapsed += 1
            
    def increment_mistakes(self) -> None:
        self.mistakes += 1
        
    def reset(self) -> None:
        self.selected_cell = None
        self.time_elapsed = 0
        self.mistakes = 0
        self.is_paused = False
        self.game_over = False
        self.timer_on = False
        self.reset_time = True
        self.congrates_played = False
        
    def show_popup(self, popup_type: PopUpType) -> None:
        self.active_popup = popup_type
        
    def hide_popup(self) -> None:
        self.active_popup = PopUpType.NONE