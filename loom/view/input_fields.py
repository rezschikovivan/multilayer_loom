from tkinter import Misc, Variable
from tkinter.ttk import Entry, Label

from loom.controller.command import (
    CommandManager,
    EnterGetable,
    GetEnterCommand,
    abstractmethod,
)


class EntryField(EnterGetable):
    """Widget each can take user input. Intaracting withs model variables through
      Command subclass"""

    def __init__(
        self, root: Misc, name: str, receiver: Variable, manager: CommandManager
    ):
        self._root = root
        self._name = name
        self.receiver = receiver
        self.manager = manager
        self.create_title()
        self.get_validatcommand()
        self._input_widget = self.create_widget()
        self.bind_enter()

    @property
    def name(self):
        return self._name

    @property
    def widget(self):
        return self._input_widget

    @abstractmethod
    def validate(self, newvalue: str) -> bool:
        """True or False for inputing char"""

    @abstractmethod
    def create_widget(self) -> Entry:
        """Place and returns concrete widget (tkinter) for input"""

    def create_title(self):
        """Place the Field title"""
        self._label = Label(self._root, text=self._name)
        self._label.pack(anchor="w")

    def get_validatcommand(self):
        """Returns correct value for widget validatecommande"""
        return (
            self._root.register(self.validate),
            "%P",
        )  # set the method as a validation method

    def bind_enter(self):
        """Make the commande listening events"""
        self._input_widget.bind("<Return>", self.take_input)
        self._input_widget.bind("<FocusOut>", self.take_input)

    def take_input(self, event):
        GetEnterCommand(self, self.receiver, self.manager).execute()

    def get_enter(self):
        """ "Returns correct data from Field"""
        return self._input_widget.get()


class IntField(EntryField):
    def create_widget(self):
        widget = Entry(
            self._root, validate="key", validatecommand=self.get_validatcommand()
        )
        widget.pack(fill="x")
        return widget

    def validate(self, newvalue: str) -> bool:
        if newvalue.isdigit() or newvalue == "":
            return True
        return False

    def get_enter(self):
        data = super().get_enter()
        return data if data != "" else "0"


class LetterField(EntryField):
    def create_widget(self):
        widget = Entry(
            self._root, validate="key", validatecommand=self.get_validatcommand()
        )
        widget.pack(fill="x")
        return widget

    def validate(self, newvalue: str) -> bool:
        if newvalue.isalpha() or newvalue == "":
            return True
        return False
