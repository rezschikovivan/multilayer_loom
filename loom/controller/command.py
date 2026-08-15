from abc import ABC, abstractmethod
from tkinter import Event

from loom.controller.memo import Memento, Originator


class Command(ABC):
    """Abstract interface of "command" pattern"""

    def __init__(self, originator:Originator, *memento_args):
        self.manager = CommandManager()
        self._originator = originator
        self.memento_args = memento_args
        self.last_memento: Memento = None
        self.new_memento:  Memento = None

    def execute(self, *args, **kwds):
        """Execute request and update states"""
        if not self.is_changes():
            return
        self.last_memento = self._originator.create_memento(*self.memento_args)
        self.action()
        self.new_memento = self._originator.create_memento(*self.memento_args)
        self.update_command_manager()
        
    @abstractmethod
    def is_changes(self)->bool:
        """
        Возвращает True если команда несет какие либо изменения в состояние системы
        иначе False. Реализация по умолчанию всегда восвращает True.
        """
        return True

    @abstractmethod
    def action(self):
        """
        Выполняет действие производимое над объектом-хозяином
        """
        raise NotImplementedError()
    
    def undo(self):
        """Отменяте выполнение команды"""
        self._originator.set_memento(self.last_memento)
    
    def redo(self):
        """Отменяет отмену выполнения команды"""
        self._originator.set_memento(self.new_memento)
    
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

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CommandManager(metaclass=Singleton):
    """Manager each allows methods to manage the commands"""

    def __init__(self):
        self.past_commands = BottomlessStack(50)
        self.future_commands = BottomlessStack(50)

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
