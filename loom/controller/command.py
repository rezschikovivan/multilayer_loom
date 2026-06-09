from abc import ABC, abstractmethod
from loom.utils import BottomlessStack
from tkinter import END

class CommandManager():
    def __init__(self):
        self.past_commands = BottomlessStack()
        self.future_commands = BottomlessStack()
    def unexecute(self, event, *args, **kwds):
        print("unexecute")
        if len(self.past_commands) >= 1:
            cmnd = self.past_commands.pop()
            cmnd.undo()
            cmnd.feild.widget.delete(0, END)
            cmnd.feild.widget.insert(0, str(cmnd.receiver.get()))

        
class Command(ABC):
    manager = CommandManager()
    def __init__(self):
        self.last_state = None
    @abstractmethod
    def execute(self, *args, **kwds):
        pass
    @abstractmethod
    def undo(self):
        pass
    @abstractmethod
    def copy(self):
        pass

