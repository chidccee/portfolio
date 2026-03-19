import pygame
from typing import Tuple, Optional

class MenuManager:
    def __init__(self, screen_width: int = 600, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def cursor(self, text: str, mouse_pos: Tuple[int, int]) -> bool:
        x, y = mouse_pos

        if text == 'onMainMenuText':
            return 50 < x < 250 and 35 < y < 80

        elif text == 'onGamePlayMainMenuText':
            return 20 < x < 220 and 15 < y < 60

        elif text == 'onPlayText' or text == 'onEasyText':
            return 180 < x < 400 and 300 < y < 360

        elif text == 'onSolverText' or text == 'onMediumText':
            return 150 < x < 500 and 400 < y < 460

        elif text == 'onScoreBoardText':
            return 80 < x < 500 and 500 < y < 560

        elif text == 'onHardText':
            return 180 < x < 400 and 500 < y < 560

        elif text == 'onVeryHardText':
            return 100 < x < 480 and 600 < y < 660

        elif text == 'onCancel':
            return 130 < x < 270 and 415 < y < 460

        elif text == 'onOk':
            return 400 < x < 460 and 415 < y < 460

        elif text == 'onAutoSolveDirect':
            return 320 < x < 490 and 385 < y < 420

        elif text == 'onAutoSolveAnimation':
            return 310 < x < 510 and 480 < y < 520

        elif text == 'onExitText':
            return 180 < x < 400 and 600 < y < 660

        return False
        
    def get_cell_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        board_start_x, board_start_y, cell_size = 2, 100, 66
        x, y = pos
        
        if (board_start_x <= x <= board_start_x + cell_size * 9 and
            board_start_y <= y <= board_start_y + cell_size * 9):
            
            cell_x = (x - board_start_x) // cell_size
            cell_y = (y - board_start_y) // cell_size
            
            if 0 <= cell_x < 9 and 0 <= cell_y < 9:
                return (cell_x, cell_y)
                
        return None