from typing import Tuple, Optional
from sudoku_board import SudokuBoard
import copy

class SudokuSolver:
    @staticmethod
    def find_empty(board: SudokuBoard) -> Optional[Tuple[int, int]]:
        for y in range(9):
            for x in range(9):
                if board.get_cell(x, y) == 0:
                    return (y, x)
        return None
        
    @staticmethod
    def solve(board: SudokuBoard) -> bool:
        empty = SudokuSolver.find_empty(board)
        if not empty:
            return True
            
        y, x = empty
        
        for num in range(1, 10):
            if board.is_valid_move(x, y, num):
                board.set_cell(x, y, num)
                
                if SudokuSolver.solve(board):
                    return True
                    
                board.set_cell(x, y, 0)
                
        return False
        
    @staticmethod
    def is_solvable(board: SudokuBoard) -> bool:
        temp_board = SudokuBoard(copy.deepcopy(board.grid))
        return SudokuSolver.solve(temp_board)