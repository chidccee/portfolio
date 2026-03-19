import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import TextModel
from view import TextView
from controller import TextController

def main():
    model = TextModel()
    view = TextView()
    controller = TextController(model, view)
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not model.load_file(filename):
            print(f"Error opening file: {filename}")
            return 1
    
    controller.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())