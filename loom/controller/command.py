from abc import ABC, abstractmethod
from loom.utils import BottomlessStack
from tkinter import END, Event

class CommandManager():
    def __init__(self):
        self.past_commands = BottomlessStack()
        self.future_commands = BottomlessStack()
    def unexecute(self, event:Event):
        """Unexecute last command"""
        if len(self.past_commands) >= 1:
            cmnd: "Command" = self.past_commands.pop()
            cmnd.undo()
        
class Command(ABC):
    """Abstract interface of "command" pattern """
    manager = CommandManager()
    def __init__(self):
        self.last_state = None
    @abstractmethod
    def execute(self, *args, **kwds):
        """Execute command and update self.last_state"""
    @abstractmethod
    def undo(self):
        """Reverse execute effect"""
    @abstractmethod
    def copy(self):
        """Returns object copy"""

