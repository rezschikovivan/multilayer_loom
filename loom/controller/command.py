from abc import ABC, abstractmethod
from loom.utils import BottomlessStack
from tkinter import END, Event

class CommandManager():
    """Manager each allows to manage the commands"""
    def __init__(self):
        self.past_commands = BottomlessStack()
        self.future_commands = BottomlessStack()
    def unexecute(self, event:Event):
        """Unexecute last command CTRL+Z"""
        if len(self.past_commands) >= 1:
            cmnd: "Command" = self.past_commands.pop()
            cmnd.undo()
            self.future_commands.append(cmnd)
    def reverse_unexecute(self, event:Event):
        """Unexecute last unexecute command CTRL+Y"""
        if len(self.future_commands) >= 1:
            cmnd: "Command" = self.future_commands.pop()
            cmnd.reverse_undo()
            self.past_commands.append(cmnd)
class Command(ABC):
    """Abstract interface of "command" pattern """
    manager = CommandManager()
    def __init__(self):
        self.last_state = None
        self.curr_state = None
    @abstractmethod
    def execute(self, *args, **kwds):
        """Execute request and update states"""
    @abstractmethod
    def undo(self):
        """Reverse execute effect"""
    @abstractmethod
    def reverse_undo(self):
        """Reverse undo effect"""
    @abstractmethod
    def copy(self):
        """Returns object copy"""

