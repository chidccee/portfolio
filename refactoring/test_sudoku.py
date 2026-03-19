import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sudoku_board import SudokuBoard
from sudoku_solver import SudokuSolver
from sudoku_game import SudokuGame
from game_state import GameState, GameScreen
from board_provider import BoardProvider

class TestSudokuBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = SudokuBoard()
        
    def test_initial_board_creation(self):
        for y in range(9):
            for x in range(9):
                self.assertEqual(self.board.get_cell(x, y), 0)
                
    def test_valid_move(self):
        self.board.set_cell(0, 0, 1)
        self.assertTrue(self.board.is_valid_move(1, 0, 2))
        
    def test_invalid_move_row(self):
        self.board.set_cell(0, 0, 1)
        self.assertFalse(self.board.is_valid_move(1, 0, 1))
        
    def test_invalid_move_column(self):
        self.board.set_cell(0, 0, 1)
        self.assertFalse(self.board.is_valid_move(0, 1, 1))
        
    def test_invalid_move_block(self):
        self.board.set_cell(0, 0, 1)
        self.assertFalse(self.board.is_valid_move(1, 1, 1))
        
    def test_board_completion(self):
        self.assertFalse(self.board.is_complete())
        
    def test_original_cell_protection(self):
        original_grid = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        board = SudokuBoard(original_grid)
        
        self.assertTrue(board.is_original_cell(0, 0))
        self.assertFalse(board.is_original_cell(1, 0))
        
        board.set_cell(0, 0, 5)
        self.assertEqual(board.get_cell(0, 0), 1)  

    def test_cell_clearing(self):
        board = SudokuBoard()
        board.set_cell(1, 1, 5)
        self.assertEqual(board.get_cell(1, 1), 5)
        
        board.clear_cell(1, 1)
        self.assertEqual(board.get_cell(1, 1), 0)


class TestSudokuSolver(unittest.TestCase):
    
    def setUp(self):
        self.solver = SudokuSolver()
        
    def test_find_empty_cell(self):
        board = SudokuBoard()
        empty_pos = self.solver.find_empty(board)
        self.assertIsNotNone(empty_pos)
        self.assertEqual(empty_pos, (0, 0))  
        
    def test_solve_simple_sudoku(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        board = SudokuBoard(grid)
        
        result = self.solver.solve(board)
        self.assertTrue(result)
        self.assertTrue(board.is_complete())

    def test_is_solvable(self):
        solvable_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        board = SudokuBoard(solvable_grid)
        self.assertTrue(self.solver.is_solvable(board))


class TestSudokuGame(unittest.TestCase):
    
    def setUp(self):
        self.game = SudokuGame()
        
    def test_new_game_initialization(self):
        self.game.start_new_game("easy")
        self.assertIsNotNone(self.game.board)
        self.assertEqual(self.game.state.difficulty, "easy")
        self.assertEqual(self.game.state.current_screen, GameScreen.GAME_PLAY)
        self.assertEqual(self.game.state.mistakes, 0)
        self.assertEqual(self.game.state.time_elapsed, 0)
        
    def test_game_state_transitions(self):
        self.game.navigate_to_screen(GameScreen.MAIN_MENU)
        self.assertEqual(self.game.state.current_screen, GameScreen.MAIN_MENU)
        
        self.game.navigate_to_screen(GameScreen.PLAY_MENU)
        self.assertEqual(self.game.state.current_screen, GameScreen.PLAY_MENU)
        
    def test_valid_game_move(self):
        test_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.game.board = SudokuBoard(test_grid)
        
        result = self.game.make_move(0, 0, 1)
        self.assertTrue(result)
            
    def test_cell_selection(self):
        test_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.game.board = SudokuBoard(test_grid)

        self.game.select_cell(1, 1)
        self.assertEqual(self.game.get_selected_cell(), (1, 1))
        
        self.game.deselect_cell()
        self.assertIsNone(self.game.get_selected_cell())

    def test_invalid_move_in_original_cell(self):
        original_grid = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.game.board = SudokuBoard(original_grid)
        
        result = self.game.make_move(0, 0, 5)
        self.assertFalse(result)  
        self.assertEqual(self.game.board.get_cell(0, 0), 1)


class TestBoardProvider(unittest.TestCase):
    
    def setUp(self):
        self.provider = BoardProvider()
        
    def test_board_generation(self):
        for difficulty in ['easy', 'medium', 'hard', 'veryHard']:
            board = self.provider.get_board(difficulty)
            self.assertIsInstance(board, SudokuBoard)
            self.assertIsNotNone(board.grid)
            
    def test_given_numbers_count(self):
        test_board = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        count = self.provider.count_given_numbers(test_board)
        self.assertEqual(count, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)