#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from patterns import GlobalCommandHistory

def test_history():
    print("=== ТЕСТ ИСТОРИИ КОМАНД ===")
    
    history = GlobalCommandHistory()
    history.clear_history()
    
    # Добавляем тестовые команды
    commands = [
        "set_num_True",
        "undo", 
        "redo",
        "set_num_False",
        "number_lines"
    ]
    
    for cmd in commands:
        history.add_command(cmd)
        print(f"Added: {cmd}")
    
    # Проверяем историю
    print("\n=== ВСЯ ИСТОРИЯ ===")
    all_history = history.get_history()
    for i, item in enumerate(all_history, 1):
        print(f"{i}. [{item['timestamp']}] {item['type']}")
    
    print("\n=== ПОИСК В ИСТОРИИ ===")
    search_results = history.search_history("set")
    for i, item in enumerate(search_results, 1):
        print(f"{i}. {item['type']}")

if __name__ == "__main__":
    test_history()