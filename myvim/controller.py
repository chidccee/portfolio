from patterns import (CommandManager, NumberLinesCommand, 
                     ToggleSyntaxHighlightingCommand, ShowHistoryCommand, 
                     ClearHistoryCommand, SearchHistoryCommand, GlobalCommandHistory)

class TextController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.model = model
        
        self.model.global_history = GlobalCommandHistory()
        
        self.cursor_line = 0
        self.cursor_pos = 0
        self.first_line = 0
        self.mode = "NORMAL"
        self.command_buffer = ""
        self.search_text = ""
        self.last_search = None
        self.last_search_direction = None
        self.running = True
        self.last_key = ''
        self.second_last_key = ''
        self.number_buffer = ""
        self.yank_buffer = ""
        self.replace_char = False
        
        self.command_manager = CommandManager()
    
    def run(self):
        if not self.view.init_screen():
            print("Failed to initialize screen")
            return
        
        try:
            while self.running:
                self._update_display()
                key = self.view.get_input()
                
                if not key:
                    continue
                
                if self.mode == "NORMAL":
                    self._handle_normal_mode(key)
                elif self.mode == "INSERT":
                    self._handle_insert_mode(key)
                elif self.mode == "COMMAND":
                    self._handle_command_mode(key)
                elif self.mode == "SEARCH":
                    self._handle_search_mode(key)
                elif self.mode == "REPLACE_CHAR":
                    self._handle_replace_char_mode(key)
                    
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.view.cleanup()
    
    def _update_display(self):
        total_lines = self.model.get_line_count()
        
        height, _ = self.view.get_screen_size()
        if self.cursor_line < self.first_line:
            self.first_line = self.cursor_line
        elif self.cursor_line >= self.first_line + height - 1:
            self.first_line = self.cursor_line - height + 2
        
        display_lines = []
        for i in range(total_lines):
            display_lines.append(self.model.get_line(i))
        
        message = ""
        if self.mode == "COMMAND":
            message = f":{self.command_buffer}"
        elif self.mode == "SEARCH":
            prefix = "/" if self.last_search_direction == "forward" else "?"
            message = f"{prefix}{self.search_text}"
        elif self.mode == "REPLACE_CHAR":
            message = "Replace character - enter new character"
        
        self.view.set_status(
            self.mode,
            self.model.filename,
            self.cursor_line,
            total_lines,
            message
        )
        
        self.view.display(display_lines, self.cursor_line, self.cursor_pos, self.first_line)
    
    def _handle_normal_mode(self, key):
        self.second_last_key = self.last_key
        self.last_key = key
        
        if key.isdigit():
            self.number_buffer += key
            return
        
        count = 1
        if self.number_buffer:
            try:
                count = int(self.number_buffer)
                self.number_buffer = ""
            except ValueError:
                count = 1
                self.number_buffer = ""
        
        for _ in range(count):
            if not self._execute_normal_command(key):
                break
    
    def _execute_normal_command(self, key):
        if key in ['h', 'KEY_LEFT']:
            self._move_left()
        elif key in ['l', 'KEY_RIGHT']:
            self._move_right()
        elif key in ['k', 'KEY_UP']:
            self._move_up()
        elif key in ['j', 'KEY_DOWN']:
            self._move_down()
        elif key in ['0', 'KEY_HOME', '^']:
            self._move_line_start()
        elif key in ['$', 'KEY_END']:
            self._move_line_end()
        elif key == 'w':
            self._move_word_forward()
        elif key == 'b':
            self._move_word_backward()
        elif key == 'g' and self.last_key == 'g':
            self._move_file_start()
        elif key == 'G':
            if hasattr(self, '_numeric_prefix') and self._numeric_prefix:
                line_num = self._numeric_prefix
                self._go_to_line(line_num)
                self._numeric_prefix = None
            else:
                self._move_file_end()
        elif key == 'KEY_PGUP':
            self._page_up()
        elif key == 'KEY_PGDOWN':
            self._page_down()
        
        elif key == 'x':
            self._delete_char()
        elif key == 'd' and self.last_key == 'd':
            self._delete_line()
        elif key == 'd' and self.last_key == 'w':  
            self._delete_word()
        elif key == 'd' and self.second_last_key == 'd' and self.last_key == 'i' and key == 'w':  # diw
            self._delete_inner_word()
        elif key == 'y' and self.last_key == 'y':
            self._yank_line()
        elif key == 'y' and self.last_key == 'w':  
            self._yank_word()
        elif key == 'p':
            self._paste()
        elif key == 'P':
            self._paste_before()
        elif key == 'u':
            success = self.command_manager.undo()
            if success:
                self.view.show_message("Undo successful")
            else:
                self.view.show_message("Nothing to undo")
        elif key == 'U':
            self._undo_line_changes()
        elif key == 'i':
            self.mode = "INSERT"
        elif key == 'I':
            self._move_line_start()
            self.mode = "INSERT"
        elif key == 'a':
            self._move_right()
            self.mode = "INSERT"
        elif key == 'A':
            self._move_line_end()
            self.mode = "INSERT"
        elif key == 'o':
            self._insert_line_below()
            self.mode = "INSERT"
        elif key == 'O':
            self._insert_line_above()
            self.mode = "INSERT"
        elif key == 'S':
            self._clear_line()
            self.mode = "INSERT"
        elif key == 'r':
            self.mode = "REPLACE_CHAR"
            self.view.show_message("Replace character - enter new character")
            return True
        elif key == ':':
            self.mode = "COMMAND"
            self.command_buffer = ""
            return True
        elif key == '/':
            self.mode = "SEARCH"
            self.search_text = ""
            self.last_search_direction = "forward"
            return True
        elif key == '?':
            self.mode = "SEARCH"
            self.search_text = ""
            self.last_search_direction = "backward"
            return True
        elif key == 'n':
            self._repeat_search()
        elif key == 'N':
            self._repeat_search_reverse()
        else:
            if key not in ['KEY_RESIZE']:
                if self.number_buffer:
                    self.number_buffer = ""
                self.view.show_message(f"Unknown key: {key}")
            return False
        return True
    
    def _handle_insert_mode(self, key):
        if key == 'ESC':
            self.mode = "NORMAL"
        elif key == 'KEY_BACKSPACE':
            self._backspace()
        elif key == 'KEY_ENTER':
            self._split_line()
        elif len(key) == 1:
            self.model.insert_text(self.cursor_line, self.cursor_pos, key)
            self.cursor_pos += 1
    
    def _handle_command_mode(self, key):
        if key == 'ESC':
            self.mode = "NORMAL"
            self.command_buffer = ""
        elif key == 'KEY_ENTER':
            self._execute_command()
        elif key == 'KEY_BACKSPACE':
            if self.command_buffer:
                self.command_buffer = self.command_buffer[:-1]
        elif len(key) == 1:
            self.command_buffer += key
    
    def _handle_search_mode(self, key):
        if key == 'ESC':
            self.mode = "NORMAL"
            self.search_text = ""
        elif key == 'KEY_ENTER':
            self._execute_search()
        elif key == 'KEY_BACKSPACE':
            if self.search_text:
                self.search_text = self.search_text[:-1]
        elif len(key) == 1:
            self.search_text += key
    
    def _handle_replace_char_mode(self, key):
        if key == 'ESC':
            self.mode = "NORMAL"
        elif len(key) == 1 and key not in ['KEY_ENTER', 'KEY_BACKSPACE']:
            line = self.model.get_line(self.cursor_line)
            if self.cursor_pos < len(line):
                self.model.delete_text(self.cursor_line, self.cursor_pos, self.cursor_pos + 1)
                self.model.insert_text(self.cursor_line, self.cursor_pos, key)
            self.mode = "NORMAL"
    
    def _execute_command(self):
        cmd = self.command_buffer.strip()
        self.command_buffer = ""
    
        if cmd.startswith('o '):
            filename = cmd[2:].strip()
            if self.model.load_file(filename):
                self.cursor_line = 0
                self.cursor_pos = 0
                self.mode = "NORMAL"
                self.view.show_message(f"Opened {filename}")
            else:
                self.view.show_message(f"Error opening {filename}")
    
        elif cmd == 'x':
            if self.model.save_file():
                self.running = False
            else:
                self.view.show_message("Error saving file")
    
        elif cmd == 'w':
            if self.model.filename:
                if self.model.save_file():
                    self.view.show_message("File saved")
                else:
                    self.view.show_message("Error saving file")
            else:
                self.view.show_message("No filename")
    
        elif cmd.startswith('w '):
            filename = cmd[2:].strip()
            if self.model.save_file(filename):
                self.view.show_message(f"Saved as {filename}")
            else:
                self.view.show_message("Error saving file")
    
        elif cmd == 'q':
            if not self.model.modified:
                self.running = False
            else:
                self.view.show_message("No write since last change (add ! to override)")
    
        elif cmd == 'q!':
            self.running = False
    
        elif cmd == 'wq' or cmd == 'wq!':
            if self.model.filename:
                if self.model.save_file():
                    self.running = False
                else:
                    self.view.show_message("Error saving file")
            else:
                self.view.show_message("No filename")
    
        elif cmd == 'e!':
            if self.model.filename:
                self.model.load_file(self.model.filename)
                self.cursor_line = 0
                self.cursor_pos = 0
            self.mode = "NORMAL"
    
        elif cmd.isdigit():
            line_num = int(cmd) - 1
            if 0 <= line_num < self.model.get_line_count():
                self.cursor_line = line_num
                self.cursor_pos = 0
            self.mode = "NORMAL"
    
        elif cmd == 'set num' or cmd == 'set number':
            new_state = not self.model.line_numbers_enabled
            number_cmd = NumberLinesCommand(self.model, new_state)
            if self.command_manager.execute_command(number_cmd, f"set_num_{new_state}"):
                status = "enabled" if new_state else "disabled"
                self.view.show_message(f"Line numbers {status}")
    
        elif cmd == 'sy' or cmd == 'syntax':
            new_state = not self.model.syntax_highlighting_enabled
            syntax_cmd = ToggleSyntaxHighlightingCommand(self.model, new_state)
            if self.command_manager.execute_command(syntax_cmd, f"set_syntax_{new_state}"):
                status = "enabled" if new_state else "disabled"
                self.view.show_message(f"Syntax highlighting {status}")
    
        elif cmd == 'history':
            history_cmd = ShowHistoryCommand(self.command_manager.global_history, self.view)
            history_cmd.execute()
    
        elif cmd == 'clearhistory':
            clear_cmd = ClearHistoryCommand(self.command_manager.global_history, self.view)
            self.command_manager.execute_command(clear_cmd, "clear_history")
    
        elif cmd.startswith('searchhistory '):
            search_term = cmd[14:].strip()
            if search_term:
                search_cmd = SearchHistoryCommand(self.command_manager.global_history, self.view, search_term)
                search_cmd.execute()
    
        elif cmd == 'h' or cmd == 'help':
            help_text = "Навигация: h j k l, w b, 0 $, gg G, / ? n N | Редактирование: i I a A o O S, x dw dd, yy yw p, u U | Команды: :w :q :q! :wq :e! :set num :sy :h"
            self.view.show_message(help_text)
            self.mode = "NORMAL"
    
        else:
            if cmd and cmd[-1] == 'G' and cmd[:-1].isdigit():
                line_num = int(cmd[:-1])
                self._go_to_line(line_num)
                self.mode = "NORMAL"
            else:
                self.view.show_message(f"Unknown command: {cmd}")
    
        self.mode = "NORMAL"
    
    def _delete_word(self):
        line = self.model.get_line(self.cursor_line)
        pos = self.cursor_pos
        
        if pos >= len(line):
            return
        
        if line[pos] in ' \t':
            start = pos
            while start < len(line) and line[start] in ' \t':
                start += 1
        else:
            start = pos
            while start > 0 and line[start-1] not in ' \t\n':
                start -= 1
        
        end = start
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        while end < len(line) and line[end] in ' \t':
            end += 1
        
        if start < end:
            self.model.delete_text(self.cursor_line, start, end)
            self.cursor_pos = start
    
    def _delete_inner_word(self):
        line = self.model.get_line(self.cursor_line)
        pos = self.cursor_pos
        
        if pos >= len(line) or line[pos] == ' ':
            return
        
        start = pos
        while start > 0 and line[start-1] not in ' \t\n':
            start -= 1
        
        end = pos
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        if start < end:
            self.model.delete_text(self.cursor_line, start, end)
            self.cursor_pos = start
    
    def _undo_line_changes(self):
        self.model.lines[self.cursor_line] = MyString()
        self.cursor_pos = 0
        self.model.modified = True
        self.view.show_message("Cleared current line")
    
    def _execute_search(self):
        if not self.search_text:
            self.mode = "NORMAL"
            return
        
        if self.last_search_direction == "forward":
            line, pos = self.model.search_forward(
                self.search_text, 
                self.cursor_line, 
                self.cursor_pos + 1 if self.cursor_pos < len(self.model.get_line(self.cursor_line)) else 0
            )
        else:
            line, pos = self.model.search_backward(
                self.search_text,
                self.cursor_line,
                self.cursor_pos
            )
        
        if line != -1:
            self.cursor_line = line
            self.cursor_pos = pos
            self.last_search = self.search_text
            self.view.show_message(f"Found: {self.search_text}")
        else:
            self.view.show_message(f"Pattern not found: {self.search_text}")
        
        self.mode = "NORMAL"
    
    def _repeat_search(self):
        if self.last_search:
            self.search_text = self.last_search
            self.last_search_direction = "forward"
            self._execute_search()
    
    def _repeat_search_reverse(self):
        if self.last_search:
            self.search_text = self.last_search
            self.last_search_direction = "backward"
            self._execute_search()
    
    def _go_to_line(self, line_number):
        if 1 <= line_number <= self.model.get_line_count():
            self.cursor_line = line_number - 1
            self.cursor_pos = 0
            self.view.show_message(f"Jumped to line {line_number}")
        else:
            self.view.show_message(f"Invalid line number: {line_number}")
    
    def _page_up(self):
        height, _ = self.view.get_screen_size()
        self.cursor_line = max(0, self.cursor_line - (height - 2))
        self._adjust_cursor_position()
    
    def _page_down(self):
        height, _ = self.view.get_screen_size()
        max_line = self.model.get_line_count() - 1
        self.cursor_line = min(max_line, self.cursor_line + (height - 2))
        self._adjust_cursor_position()
    
    def _move_up(self):
        if self.cursor_line > 0:
            self.cursor_line -= 1
            self._adjust_cursor_position()
    
    def _move_down(self):
        if self.cursor_line < self.model.get_line_count() - 1:
            self.cursor_line += 1
            self._adjust_cursor_position()
    
    def _move_left(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif self.cursor_line > 0:
            self.cursor_line -= 1
            self.cursor_pos = len(self.model.get_line(self.cursor_line))
    
    def _move_right(self):
        current_len = len(self.model.get_line(self.cursor_line))
        if self.cursor_pos < current_len:
            self.cursor_pos += 1
        elif self.cursor_line < self.model.get_line_count() - 1:
            self.cursor_line += 1
            self.cursor_pos = 0
    
    def _move_line_start(self):
        self.cursor_pos = 0
    
    def _move_line_end(self):
        self.cursor_pos = len(self.model.get_line(self.cursor_line))
    
    def _move_word_forward(self):
        line = self.model.get_line(self.cursor_line)
        pos = self.cursor_pos
        
        while pos < len(line) and line[pos] == ' ':
            pos += 1
        
        while pos < len(line) and line[pos] != ' ':
            pos += 1

        while pos < len(line) and line[pos] == ' ':
            pos += 1
        
        self.cursor_pos = min(pos, len(line))
    
    def _move_word_backward(self):
        line = self.model.get_line(self.cursor_line)
        pos = self.cursor_pos - 1
        
        if pos < 0:
            return
        
        while pos > 0 and line[pos] == ' ':
            pos -= 1
        
        while pos > 0 and line[pos] != ' ':
            pos -= 1
        
        if pos == 0 and line[0] != ' ':
            self.cursor_pos = 0
        else:
            self.cursor_pos = pos + 1
    
    def _move_file_start(self):
        self.cursor_line = 0
        self.cursor_pos = 0
    
    def _move_file_end(self):
        self.cursor_line = self.model.get_line_count() - 1
        self.cursor_pos = len(self.model.get_line(self.cursor_line))
    
    def _adjust_cursor_position(self):
        current_len = len(self.model.get_line(self.cursor_line))
        if self.cursor_pos > current_len:
            self.cursor_pos = current_len
    
    def _delete_char(self):
        line = self.model.get_line(self.cursor_line)
        if self.cursor_pos < len(line):
            self.model.delete_text(self.cursor_line, self.cursor_pos, self.cursor_pos + 1)
    
    def _delete_line(self):
        if self.model.get_line_count() > 1:
            self._yank_line()
            del self.model.lines[self.cursor_line]
            if self.cursor_line >= self.model.get_line_count():
                self.cursor_line = self.model.get_line_count() - 1
            self.cursor_pos = 0
            self.model.modified = True
    
    def _yank_line(self):
        self.yank_buffer = self.model.get_line(self.cursor_line)
        self.view.show_message("Yanked line")
    
    def _yank_word(self):
        line = self.model.get_line(self.cursor_line)
        pos = self.cursor_pos
        
        start = pos
        while start > 0 and line[start-1] not in ' \t\n':
            start -= 1
        end = pos
        while end < len(line) and line[end] not in ' \t\n':
            end += 1
        
        if start < end:
            self.yank_buffer = line[start:end]
            self.view.show_message("Yanked word")
    
    def _paste(self):
        if self.yank_buffer:
            self.model.insert_text(self.cursor_line, self.cursor_pos, self.yank_buffer)
            self.cursor_pos += len(self.yank_buffer)
            self.model.modified = True
    
    def _paste_before(self):
        if self.yank_buffer:
            self.model.insert_text(self.cursor_line, self.cursor_pos, self.yank_buffer)
            self.model.modified = True
    
    def _clear_line(self):
        self.model.lines[self.cursor_line] = MyString()
        self.cursor_pos = 0
        self.model.modified = True
    
    def _backspace(self):
        if self.cursor_pos > 0:
            self.model.delete_text(self.cursor_line, self.cursor_pos - 1, self.cursor_pos)
            self.cursor_pos -= 1
        elif self.cursor_line > 0:
            prev_len = len(self.model.get_line(self.cursor_line - 1))
            current_text = str(self.model.lines[self.cursor_line])
            self.model.lines[self.cursor_line - 1].append(current_text)
            del self.model.lines[self.cursor_line]
            self.cursor_line -= 1
            self.cursor_pos = prev_len
            self.model.modified = True
    
    def _split_line(self):
        current_line = self.model.get_line(self.cursor_line)
        if self.cursor_pos < len(current_line):
            left_part = str(self.model.lines[self.cursor_line])[:self.cursor_pos]
            right_part = str(self.model.lines[self.cursor_line])[self.cursor_pos:]
            self.model.lines[self.cursor_line] = MyString(left_part)
            self.model.lines.insert(self.cursor_line + 1, MyString(right_part))
            self.cursor_line += 1
            self.cursor_pos = 0
        else:
            self.model.lines.insert(self.cursor_line + 1, MyString())
            self.cursor_line += 1
            self.cursor_pos = 0
        self.model.modified = True
    
    def _insert_line_below(self):
        self.model.lines.insert(self.cursor_line + 1, MyString())
        self.cursor_line += 1
        self.cursor_pos = 0
        self.model.modified = True
    
    def _insert_line_above(self):
        self.model.lines.insert(self.cursor_line, MyString())
        self.cursor_pos = 0
        self.model.modified = True