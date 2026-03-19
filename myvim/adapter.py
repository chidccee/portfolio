import curses

class CursesAdapter:
    
    def __init__(self):
        self.screen = None
        self._screen_size = (24, 80) 
    
    def init_screen(self):
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(1)
            self.screen.keypad(True)
            self.screen.timeout(100)
            
            height, width = self.screen.getmaxyx()
            self._screen_size = (height, width)
            
            return True
        except Exception as e:
            self._screen_size = (24, 80)
            return False
    
    def cleanup(self):
        try:
            if self.screen:
                curses.nocbreak()
                self.screen.keypad(False)
                curses.echo()
                curses.endwin()
        except Exception as e:
            pass
    
    def get_screen_size(self):
        try:
            if self.screen:
                height, width = self.screen.getmaxyx()
                self._screen_size = (height, width)
        except:
            pass
        return self._screen_size
    
    def clear(self):
        try:
            if self.screen:
                self.screen.clear()
        except:
            pass
    
    def refresh(self):
        try:
            if self.screen:
                self.screen.refresh()
        except:
            pass
    
    def add_str(self, y, x, text, attributes=0):
        try:
            if self.screen and 0 <= y < self.get_screen_size()[0]:
                max_x = self.get_screen_size()[1] - x
                if max_x > 0 and text:
                    display_text = text[:max_x]
                    self.screen.addstr(y, x, display_text, attributes)
        except curses.error:
            pass
    
    def move_cursor(self, y, x):
        try:
            if self.screen:
                height, width = self.get_screen_size()
                if 0 <= y < height and 0 <= x < width:
                    self.screen.move(y, x)
        except:
            pass
    
    def get_input(self):
        if not self.screen:
            return ''
        
        try:
            key = self.screen.getch()
            
            if key == -1:
                return ''
            elif key == curses.KEY_UP:
                return 'KEY_UP'
            elif key == curses.KEY_DOWN:
                return 'KEY_DOWN'
            elif key == curses.KEY_LEFT:
                return 'KEY_LEFT'
            elif key == curses.KEY_RIGHT:
                return 'KEY_RIGHT'
            elif key == curses.KEY_BACKSPACE or key == 127:
                return 'KEY_BACKSPACE'
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                return 'KEY_ENTER'
            elif key == 27:  # ESC
                return 'ESC'
            elif key == curses.KEY_PPAGE:
                return 'KEY_PGUP'
            elif key == curses.KEY_NPAGE:
                return 'KEY_PGDOWN'
            elif key == curses.KEY_HOME:
                return 'KEY_HOME'
            elif key == curses.KEY_END:
                return 'KEY_END'
            elif key == curses.KEY_DC:  
                return 'KEY_DELETE'
            elif 32 <= key <= 126:  
                return chr(key)
            else:
                return ''
        except:
            return ''