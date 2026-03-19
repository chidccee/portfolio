from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class Command(ABC):
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass

class NumberLinesCommand(Command):
    def __init__(self, model, enabled=True):
        self.model = model
        self.enabled = enabled
        self.previous_state = None
    
    def execute(self) -> bool:
        self.previous_state = self.model.line_numbers_enabled
        self.model.line_numbers_enabled = self.enabled
        return True
    
    def undo(self) -> bool:
        if self.previous_state is not None:
            self.model.line_numbers_enabled = self.previous_state
            return True
        return False

class ToggleSyntaxHighlightingCommand(Command):
    def __init__(self, model, enabled=True):
        self.model = model
        self.enabled = enabled
        self.previous_state = None
    
    def execute(self) -> bool:
        self.previous_state = getattr(self.model, 'syntax_highlighting_enabled', False)
        self.model.syntax_highlighting_enabled = self.enabled
        return True
    
    def undo(self) -> bool:
        if self.previous_state is not None:
            self.model.syntax_highlighting_enabled = self.previous_state
            return True
        return False

class GlobalCommandHistory:
    _instance = None
    _history: List[Dict[str, Any]] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalCommandHistory, cls).__new__(cls)
        return cls._instance
    
    def add_command(self, command_type: str, params: Dict[str, Any] = None):
        history_item = {
            'type': command_type,
            'params': params or {},
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self._history.append(history_item)
        
        if len(self._history) > 100:
            self._history.pop(0)
    
    def get_history(self, limit: int = None):
        if limit:
            return self._history[-limit:]
        return self._history.copy()
    
    def clear_history(self):
        self._history.clear()
    
    def search_history(self, search_term: str):
        return [item for item in self._history if search_term.lower() in item['type'].lower()]


class CommandManager:
    def __init__(self):
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
        self.global_history = GlobalCommandHistory()
    
    def execute_command(self, command: Command, command_type: str = "unknown") -> bool:
        if command.execute():
            self.history.append(command)
            self.redo_stack.clear()
            self.global_history.add_command(command_type)
            return True
        return False
    
    def undo(self) -> bool:
        if self.history:
            command = self.history.pop()
            if command.undo():
                self.redo_stack.append(command)
                self.global_history.add_command("undo")
                return True
        return False
    
    def redo(self) -> bool:
        if self.redo_stack:
            command = self.redo_stack.pop()
            if command.execute():
                self.history.append(command)
                self.global_history.add_command("redo")
                return True
        return False


class ShowHistoryCommand(Command):
    def __init__(self, global_history: GlobalCommandHistory, view, limit=10):
        self.global_history = global_history
        self.view = view
        self.limit = limit
    
    def execute(self) -> bool:
        history = self.global_history.get_history(self.limit)
        if not history:
            self.view.show_message("No command history")
            return True
        
        message = f"Last {len(history)} commands: "
        for i, item in enumerate(history, 1):
            cmd_type = item['type']
            if cmd_type == 'set_num_True':
                cmd_type = 'num_on'
            elif cmd_type == 'set_num_False':
                cmd_type = 'num_off'
            message += f"{cmd_type}"
            if i < len(history):
                message += ", "
        
        self.view.show_message(message)
        return True
    
    def undo(self) -> bool:
        return False

class ClearHistoryCommand(Command):
    def __init__(self, global_history: GlobalCommandHistory, view):
        self.global_history = global_history
        self.view = view
        self.previous_history = None
    
    def execute(self) -> bool:
        self.previous_history = self.global_history.get_history()
        self.global_history.clear_history()
        self.view.show_message("Command history cleared")
        return True
    
    def undo(self) -> bool:
        if self.previous_history:
            for item in self.previous_history:
                self.global_history.add_command(item['type'], item['params'])
            self.view.show_message("Command history restored")
            return True
        return False
    
class SearchHistoryCommand(Command):
    def __init__(self, global_history: GlobalCommandHistory, view, search_term):
        self.global_history = global_history
        self.view = view
        self.search_term = search_term
    
    def execute(self) -> bool:
        results = self.global_history.search_history(self.search_term)
        if not results:
            self.view.show_message(f"No commands found for: {self.search_term}")
            return True
        
        message = f"Found {len(results)} commands for '{self.search_term}': "
        for i, item in enumerate(results, 1):
            cmd_type = item['type']
            if cmd_type == 'set_num_True':
                cmd_type = 'num_on'
            elif cmd_type == 'set_num_False':
                cmd_type = 'num_off'
            message += f"{cmd_type}"
            if i < len(results):
                message += ", "
        
        self.view.show_message(message)
        return True
    
    def undo(self) -> bool:
        return False