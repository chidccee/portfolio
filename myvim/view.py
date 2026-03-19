import curses
from adapter import CursesAdapter

class TextView:
    
    def __init__(self, model=None):
        self.adapter = CursesAdapter()
        self.mode = "NORMAL"
        self.filename = ""
        self.current_line = 0
        self.current_col = 0
        self.total_lines = 0
        self.message = ""
        self.model = model
        self.help_mode = False
        self.help_text = ""
    
    def init_screen(self):
        return self.adapter.init_screen()
    
    def cleanup(self):
        self.adapter.cleanup()
    
    def set_status(self, mode, filename, current_line, total_lines, message=""):
        self.mode = mode
        self.filename = filename or "[No Name]"
        self.current_line = current_line
        self.current_col = 0
        self.total_lines = total_lines
        self.message = message
    
    def display(self, lines, cursor_line, cursor_pos, first_line=0):
        height, width = self.adapter.get_screen_size()
        
        self.current_col = cursor_pos

        self.adapter.clear()
        
        if self.mode == "HELP":
            self._display_help(height, width)
            return
        
        display_height = height - 1
        for i in range(display_height):
            line_idx = first_line + i
            if line_idx < len(lines):
                line_text = str(lines[line_idx])
                
                if self.model and self.model.line_numbers_enabled:
                    line_num = f"{line_idx + 1:4d} "
                    display_text = line_num + line_text
                else:
                    display_text = line_text
                
                if len(display_text) > width:
                    display_text = display_text[:width-1]
                
                self.adapter.add_str(i, 0, display_text)
            else:
                self.adapter.add_str(i, 0, "~")
        
        mode_display = self.mode
        if self.mode in ["INSERT", "COMMAND", "SEARCH", "REPLACE_CHAR", "HELP"]:
            mode_display = "-- " + self.mode + " --"
        
        status_parts = [
            mode_display,
            f"{self.filename}",
            f"Line:{self.current_line + 1}/{self.total_lines}",
            f"Col:{cursor_pos + 1}"
        ]
        
        if self.model:
            if self.model.line_numbers_enabled:
                status_parts.append("[NUM]")
            if self.model.syntax_highlighting_enabled:
                status_parts.append("[SYNTAX]")
        
        status_line = " | ".join(status_parts)
        
        if self.message:
            available_space = width - len(status_line) - 3
            if available_space > 10:
                status_line += " | " + self.message[:available_space]
        
        status_line = status_line[:width-1]
        
        self.adapter.add_str(height-1, 0, " " * width)
        self.adapter.add_str(height-1, 0, status_line, curses.A_REVERSE)
        
        cursor_y = cursor_line - first_line
        cursor_x = cursor_pos
        if self.model and self.model.line_numbers_enabled:
            cursor_x += 6
        
        if 0 <= cursor_y < display_height:
            self.adapter.move_cursor(cursor_y, min(cursor_x, width-1))
        
        self.adapter.refresh()

    def get_input(self):
        return self.adapter.get_input()
    
    def get_screen_size(self):
        return self.adapter.get_screen_size()
    
    def show_message(self, message):
        self.message = message
    
    def show_help(self):
        self.mode = "HELP"