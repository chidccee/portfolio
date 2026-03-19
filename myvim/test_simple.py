# test_simple.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import TextModel
from view import TextView

def simple_test():
    print("=== ПРОСТОЙ ТЕСТ ОТОБРАЖЕНИЯ ===")
    
    model = TextModel()
    view = TextView()
    
    if not view.init_screen():
        print("Failed to initialize screen")
        return
    
    try:
        # Тест 1: Простое сообщение
        view.message = "TEST MESSAGE 123"
        view.set_status("NORMAL", "test.txt", 1, 5, "")
        view.display(["Line 1", "Line 2", "Line 3"], 1, 0, 0)
        input("Нажми Enter...")
        
        # Тест 2: Другое сообщение
        view.message = "HISTORY: cmd1, cmd2"
        view.set_status("NORMAL", "test.txt", 1, 5, "")
        view.display(["Line 1", "Line 2", "Line 3"], 1, 0, 0)
        input("Нажми Enter для выхода...")
        
    finally:
        view.cleanup()

if __name__ == "__main__":
    simple_test()