class MyString:
    
    def __init__(self, text=""):
        self._text = text
    
    def __str__(self):
        return self._text
    
    def __len__(self):
        return len(self._text)
    
    def __getitem__(self, index):
        return self._text[index]
    
    def append(self, text):
        self._text += text
    
    def insert(self, index, text):
        if index > len(self._text):
            self._text += text
        else:
            self._text = self._text[:index] + text + self._text[index:]
    
    def delete(self, start, end):
        if start < len(self._text):
            end = min(end, len(self._text))
            self._text = self._text[:start] + self._text[end:]


class TextModel:
    
    def __init__(self):
        self.lines = [MyString()]
        self.filename = None
        self.modified = False
        self.line_numbers_enabled = False
        self.syntax_highlighting_enabled = False
        self.global_history = None
    
    def load_file(self, filename):
        try:
            encodings = ['latin1', 'iso-8859-1', 'cp1251', 'cp866']
            
            for encoding in encodings:
                try:
                    with open(filename, 'r', encoding=encoding, errors='strict') as f:
                        content = f.read()
                    
                    content = content.replace('\x00', '')
                    lines = content.split('\n')
                    
                    if lines and lines[-1] == '':
                        lines = lines[:-1]
                    
                    self.lines = [MyString(line) for line in lines]
                    
                    if not self.lines:
                        self.lines = [MyString("")]
                    
                    self.filename = filename
                    self.modified = False
                    return True
                    
                except UnicodeDecodeError:
                    continue
            
            print(f"Error: File {filename} encoding not supported")
            return False
            
        except Exception as e:
            print(f"Error loading file {filename}: {e}")
            return False
    
    def save_file(self, filename=None):
        if filename:
            self.filename = filename
        if not self.filename:
            return False
        try:
            with open(self.filename, 'w', encoding='latin1', errors='replace') as f:
                f.write('\n'.join(str(line) for line in self.lines))
            self.modified = False
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def insert_text(self, line_num, pos, text):
        if 0 <= line_num < len(self.lines):
            self.lines[line_num].insert(pos, text)
            self.modified = True
    
    def delete_text(self, line_num, start, end):
        if 0 <= line_num < len(self.lines):
            self.lines[line_num].delete(start, end)
            self.modified = True
    
    def get_line(self, line_num):
        if 0 <= line_num < len(self.lines):
            return str(self.lines[line_num])
        return ""
    
    def get_line_count(self):
        return len(self.lines)
    
    def search_forward(self, text, start_line, start_pos):
        for i in range(start_line, len(self.lines)):
            line_text = str(self.lines[i])
            search_start = start_pos if i == start_line else 0
            pos = line_text.find(text, search_start)
            if pos != -1:
                return i, pos
        return -1, -1
    
    def search_backward(self, text, start_line, start_pos):
        for i in range(start_line, -1, -1):
            line_text = str(self.lines[i])
            end_pos = len(line_text) if i != start_line else start_pos
            pos = line_text.rfind(text, 0, end_pos)
            if pos != -1:
                return i, pos
        return -1, -1