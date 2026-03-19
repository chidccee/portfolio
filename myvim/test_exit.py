#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import TextModel
from view import TextView
from controller import TextController

# Простой тест выхода
model = TextModel()
view = TextView()
controller = TextController(model, view)

print("Testing exit functionality...")
print("This should exit immediately with :q command")

# Симулируем команду выхода
controller.mode = "COMMAND"
controller.command_buffer = "q"
controller._execute_command()

if not controller.running:
    print("SUCCESS: Exit command worked!")
else:
    print("FAILED: Exit command didn't work")