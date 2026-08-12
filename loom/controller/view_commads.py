from abc import ABC, abstractmethod
from tkinter import END, Entry, Variable

from loom.controller import Command, CommandManager


class EnterGetable(ABC):

    def __init__(self):
        self.widget:Entry

    @abstractmethod
    def get_enter(self):
        raise NotImplementedError()

class GetEnterCommand(Command):
    """Command to get user input in Fields. Can reverse changes and reverses.
      Managed by CommandManager"""

    def __init__(
        self, field: EnterGetable, receiver: Variable, manager: CommandManager
    ):
        super().__init__(manager)
        self.field = field
        self.receiver = receiver

    def is_changes(self):
        return not str(self.receiver.get()) == self.field.get_enter()

    def set_states(self):
        self.last_memento = self.receiver.get()
        self.new_memento = self.field.get_enter()
        self.receiver.set(self.new_memento)        

    def undo(self):
        self.receiver.set(self.last_memento)
        self.field.widget.delete(0, END)
        self.field.widget.insert(0, str(self.last_memento))

    def redo(self):
        self.receiver.set(self.new_memento)
        self.field.widget.delete(0, END)
        self.field.widget.insert(0, str(self.new_memento))
