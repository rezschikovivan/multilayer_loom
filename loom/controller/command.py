from abc import ABC, abstractmethod
from tkinter import END, Event, Variable


class BottomlessStack:
    """Stack with auto clearing. If len arcoss the max_len, first item is deleting."""

    def __init__(self, max_len=10):
        self.enum = []
        self.max_len = max_len

    def __getitem__(self, key):
        return self.enum[key]

    def append(self, item):
        if len(self.enum) >= self.max_len:
            self.enum.pop(0)
        self.enum.append(item)

    def __iter__(self):
        return self.enum.__iter__()

    def pop(self, index=-1):
        return self.enum.pop(index)

    def __len__(self):
        return self.enum.__len__()

    def clear(self):
        self.enum.clear()


class CommandManager:
    """Manager each allows methods to manage the commands"""

    def __init__(self):
        self.past_commands = BottomlessStack()
        self.future_commands = BottomlessStack()

    def undo(self, event: Event):
        """Unexecute last command CTRL+Z"""
        if len(self.past_commands) >= 1:
            cmnd: Command = self.past_commands.pop()
            cmnd.undo()
            self.future_commands.append(cmnd)

    def redo(self, event: Event):
        """Unexecute last unexecute command CTRL+Y"""
        if len(self.future_commands) >= 1:
            cmnd: Command = self.future_commands.pop()
            cmnd.redo()
            self.past_commands.append(cmnd)


class Command(ABC):
    """Abstract interface of "command" pattern"""

    def __init__(self, manager: CommandManager):
        self.manager = manager
        self.last_state = None
        self.curr_state = None

    @abstractmethod
    def execute(self, *args, **kwds):
        """Execute request and update states"""

    @abstractmethod
    def undo(self):
        """Reverse execute effect"""

    @abstractmethod
    def redo(self):
        """Reverse undo effect"""


class EnterGetable(ABC):
    @abstractmethod
    def get_enter(self):
        pass


class GetEnterCommand(Command):
    """Command to get user input in Fields. Can reverse changes and reverses.
      Managed by CommandManager"""

    def __init__(
        self, field: EnterGetable, receiver: Variable, manager: CommandManager
    ):
        super().__init__(manager)
        self.field = field
        self.receiver = receiver

    def execute(self, *args, **kwds):
        if str(self.receiver.get()) == self.field.get_enter():
            return  # Do nothing if value wasn`t change
        self.last_state = self.receiver.get()
        self.curr_state = self.field.get_enter()
        self.manager.future_commands.clear()
        self.manager.past_commands.append(self)
        self.receiver.set(self.curr_state)

    def undo(self):
        self.receiver.set(self.last_state)
        self.field.widget.delete(0, END)
        self.field.widget.insert(0, str(self.last_state))

    def redo(self):
        self.receiver.set(self.curr_state)
        self.field.widget.delete(0, END)
        self.field.widget.insert(0, str(self.curr_state))
