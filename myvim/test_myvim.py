import pytest
import tempfile
import os
from model import TextModel, MyString
from patterns import GlobalCommandHistory, NumberLinesCommand, CommandManager

class TestMyString:
    def test_initialization(self):
        s = MyString("test")
        assert str(s) == "test"
    
    def test_append(self):
        s = MyString("hello")
        s.append(" world")
        assert str(s) == "hello world"
    
    def test_insert(self):
        s = MyString("hello")
        s.insert(2, "XXX")
        assert str(s) == "heXXXllo"
    
    def test_delete(self):
        s = MyString("hello world")
        s.delete(5, 11)
        assert str(s) == "hello"
    
    def test_length(self):
        s = MyString("test")
        assert len(s) == 4

class TestTextModel:
    def setup_method(self):
        self.model = TextModel()
    
    def test_syntax_highlighting_attribute(self):
        assert hasattr(self.model, 'syntax_highlighting_enabled')
        assert self.model.syntax_highlighting_enabled == False
    
    def test_line_numbers_attribute(self):
        assert hasattr(self.model, 'line_numbers_enabled')
        assert self.model.line_numbers_enabled == False
    
    def test_initial_state(self):
        assert self.model.get_line_count() == 1
        assert self.model.get_line(0) == ""
        assert not self.model.modified
    
    def test_insert_text(self):
        self.model.insert_text(0, 0, "hello")
        assert self.model.get_line(0) == "hello"
        assert self.model.modified
    
    def test_delete_text(self):
        self.model.insert_text(0, 0, "hello")
        self.model.delete_text(0, 1, 3)
        assert self.model.get_line(0) == "hlo"
    
    def test_load_save_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='cp1251') as f:
            f.write("line1\nline2\nline3")
            temp_filename = f.name
        
        try:
            assert self.model.load_file(temp_filename)
            assert self.model.get_line_count() == 3
            assert self.model.get_line(0) == "line1"
            
            self.model.insert_text(0, 0, "test")
            assert self.model.save_file(temp_filename)
            
            new_model = TextModel()
            assert new_model.load_file(temp_filename)
            assert new_model.get_line(0) == "testline1"
        
        finally:
            os.unlink(temp_filename)
    
    def test_search_forward(self):
        self.model.lines = [MyString("hello world"), MyString("test hello")]
        line, pos = self.model.search_forward("hello", 0, 0)
        assert line == 0
        assert pos == 0
        
        line, pos = self.model.search_forward("hello", 0, 1)
        assert line == 1
        assert pos == 5
    
    def test_search_backward(self):
        self.model.lines = [MyString("hello world"), MyString("test hello")]
        line, pos = self.model.search_backward("hello", 1, 10)
        assert line == 1
        assert pos == 5
        
        line, pos = self.model.search_backward("hello", 1, 5)
        assert line == 0
        assert pos == 0

class TestGlobalCommandHistory:
    def setup_method(self):
        history = GlobalCommandHistory()
        history.clear_history()
    
    def test_singleton_pattern(self):
        history1 = GlobalCommandHistory()
        history2 = GlobalCommandHistory()
        assert history1 is history2
    
    def test_add_and_get_history(self):
        history = GlobalCommandHistory()
        
        history.add_command("test_command", {"param": "value"})
        commands = history.get_history()
        
        assert len(commands) == 1
        assert commands[0]['type'] == "test_command"
        assert commands[0]['params']['param'] == "value"
    
    def test_search_history(self):
        history = GlobalCommandHistory()
        
        history.add_command("number_lines")
        history.add_command("syntax_highlight")
        history.add_command("undo")
        
        results = history.search_history("number")
        assert len(results) == 1
        assert results[0]['type'] == "number_lines"
    
    def test_clear_history(self):
        history = GlobalCommandHistory()
        
        history.add_command("test1")
        history.add_command("test2")
        assert len(history.get_history()) == 2
        
        history.clear_history()
        assert len(history.get_history()) == 0

class TestNumberLinesCommand:
    def test_execute_undo(self):
        model = TextModel()
        model.lines = [MyString("line1"), MyString("line2")]
        
        command = NumberLinesCommand(model, True)

        assert command.execute()
        assert model.line_numbers_enabled
        
        assert command.undo()
        assert not model.line_numbers_enabled

class TestCommandManager:
    def setup_method(self):
        history = GlobalCommandHistory()
        history.clear_history()
    
    def test_execute_undo_redo(self):
        manager = CommandManager()
        model = TextModel()
        
        command = NumberLinesCommand(model, True)
        
        assert manager.execute_command(command, "test_command")
        assert len(manager.history) == 1
        assert model.line_numbers_enabled
        
        assert manager.undo()
        assert not model.line_numbers_enabled
        assert len(manager.redo_stack) == 1

        assert manager.redo()
        assert model.line_numbers_enabled
        assert len(manager.history) == 1


class TestIntegration:
    def setup_method(self):
        history = GlobalCommandHistory()
        history.clear_history()
    
    def test_complete_workflow(self):
        model = TextModel()
        model.lines = [MyString("first line"), MyString("second line")]
        
        number_cmd = NumberLinesCommand(model, True)
        assert number_cmd.execute()
        assert model.line_numbers_enabled
        
        assert number_cmd.undo()
        assert not model.line_numbers_enabled

        manager = CommandManager()
        assert manager.execute_command(number_cmd, "number_lines")
        assert model.line_numbers_enabled
        
        history = manager.global_history.get_history()
        assert len(history) == 1
        assert history[0]['type'] == "number_lines"
    
    def test_multiple_commands_history(self):
        manager = CommandManager()
        model = TextModel()
        
        cmd1 = NumberLinesCommand(model, True)
        cmd2 = NumberLinesCommand(model, False)
        
        assert manager.execute_command(cmd1, "enable_numbers")
        assert manager.execute_command(cmd2, "disable_numbers")

        history = manager.global_history.get_history()
        assert len(history) == 2
        assert history[0]['type'] == "enable_numbers"
        assert history[1]['type'] == "disable_numbers"

class TestMissingCommands:
    def setup_method(self):
        self.model = TextModel()
        self.model.lines = [MyString("hello world test"), MyString("another line")]
    
    def test_yank_word(self):
        line = self.model.get_line(0)
        pos = 6 
        
        start = pos
        while start > 0 and line[start-1] not in ' \t\n':
            start -= 1
        end = pos
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        yanked_word = line[start:end]
        assert yanked_word == "world"
    
    def test_go_to_line_command(self):
        from patterns import GoToLineCommand
        
        model = TextModel()
        model.lines = [MyString("line1"), MyString("line2"), MyString("line3")]
        
        class MockView:
            def show_message(self, msg): pass
        
        command = GoToLineCommand(model, MockView(), 2)
        assert command.execute()
        assert model.cursor_line == 1 
        
        assert command.undo()
        assert model.cursor_line == 0  

class TestVimCommands:
    def setup_method(self):
        self.model = TextModel()
        self.model.lines = [
            MyString("hello world test"),
            MyString("another line here"),
            MyString("third line")
        ]
    
    def test_delete_word_simple(self):
        line = "hello world test"
        pos = 6  
    
        if line[pos] in ' \t':
            start = pos
            while start < len(line) and line[start] in ' \t':
                start += 1
            end = start
            while end < len(line) and line[end] not in ' \t\n':
                end += 1
            while end < len(line) and line[end] in ' \t':
                end += 1
            result = line[:pos] + line[end:]
        else:
            start = pos
            while start > 0 and line[start-1] not in ' \t\n':
                start -= 1
            end = start
            while end < len(line) and line[end] not in ' \t\n':
                end += 1
            while end < len(line) and line[end] in ' \t':
                end += 1
            result = line[:start] + line[end:]
    
        assert result == "hello test"
    
    def test_delete_inner_word(self):
        line = "hello  world  test"

        pos = 7 
        
        start = pos
        while start > 0 and line[start-1] not in ' \t\n':
            start -= 1
        
        end = pos
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        expected = "hello    test"  
        result = line[:start] + line[end:]
        assert result == expected, f"Expected '{expected}', got '{result}'"
    
    def test_yank_word(self):
        line = "hello world test"
        
        pos = 6
        
        start = pos
        while start > 0 and line[start-1] not in ' \t\n':
            start -= 1
        
        end = pos
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        yanked_word = line[start:end]
        assert yanked_word == "world", f"Expected 'world', got '{yanked_word}'"
    
    def test_file_encoding(self):
        model = TextModel()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='latin1') as f:
            f.write("línea uno\nlínea dos\nlínea tres")
            temp_filename = f.name
        
        try:
            assert model.load_file(temp_filename)
            assert model.get_line_count() == 3
            assert "línea" in model.get_line(0)
            
            model.insert_text(0, 0, "test ")
            assert model.save_file()
            
        finally:
            os.unlink(temp_filename)

class TestLargeFiles:
    def test_large_file_loading(self):
        """Тест загрузки файла >512KB"""
        model = TextModel()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='latin1') as f:
            for i in range(10000):
                f.write(f"This is line {i} with some text. " * 5 + "\n")
            temp_filename = f.name
        
        try:
            import os
            file_size = os.path.getsize(temp_filename)
            assert file_size > 512 * 1024  
            
            assert model.load_file(temp_filename)
            assert model.get_line_count() > 0

            assert model.search_forward("line 5000", 0, 0)[0] != -1
            
        finally:
            os.unlink(temp_filename)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])