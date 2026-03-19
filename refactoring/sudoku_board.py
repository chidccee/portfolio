from typing import List, Tuple, Optional
import copy

class SudokuBoard:
    def __init__(self, grid: Optional[List[List[int]]] = None):
        self.grid = grid or [[0 for _ in range(9)] for _ in range(9)]
        self.original = copy.deepcopy(self.grid)
        
    def is_valid_move(self, x: int, y: int, num: int) -> bool:
        if num == 0:
            return True
            
        temp_grid = copy.deepcopy(self.grid)
        temp_grid[y][x] = 0
        
        for i in range(9):
            if temp_grid[y][i] == num:
                return False
                
        for i in range(9):
            if temp_grid[i][x] == num:
                return False

        box_x = x // 3
        box_y = y // 3
        for j in range(box_y * 3, (box_y + 1) * 3):
            for k in range(box_x * 3, (box_x + 1) * 3):
                if temp_grid[j][k] == num:
                    return False
                    
        return True
        
    def is_complete(self) -> bool:
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return False
        return True
        
    def is_original_cell(self, x: int, y: int) -> bool:
        return self.original[y][x] != 0
        
    def reset(self) -> None:
        self.grid = copy.deepcopy(self.original)
        
    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]
        
    def set_cell(self, x: int, y: int, value: int) -> None:
        if not self.is_original_cell(x, y):
            self.grid[y][x] = value
            
    def clear_cell(self, x: int, y: int) -> None:
        if not self.is_original_cell(x, y):
            self.grid[y][x] = 0