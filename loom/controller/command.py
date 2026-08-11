from abc import ABC, abstractmethod
from tkinter import Event

class Command(ABC):
    """Abstract interface of "command" pattern"""

    def __init__(self, manager: "CommandManager"):
        self.manager = manager
        self.last_state = None
        self.new_state = None


    def execute(self, *args, **kwds):
        """Execute request and update states"""
        if not self.is_changes():
            return
        self.set_states()
        self.update_command_manager()
        
    @abstractmethod
    def is_changes(self)->bool:
        """
        Возвращает True если команда несет какие либо изменения в состояние системы
        иначе False. Реализация по умолчанию всегда восвращает True.
        """
        return True
    @abstractmethod
    def set_states(self):
        """
        Записывает состояние до и после изменения в перменнные last_state и new_state соответсвтенно, 
        a так же применяет изменения к системе
        """
        raise NotImplementedError()
    @abstractmethod
    def undo(self):
        """Reverse execute effect"""
        raise NotImplementedError()
    @abstractmethod
    def redo(self):
        """Reverse undo effect"""
        raise NotImplementedError()
    
    def update_command_manager(self):
        self.manager.future_commands.clear()
        self.manager.past_commands.append(self)


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
        self.past_commands = BottomlessStack(30)
        self.future_commands = BottomlessStack(30)

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
