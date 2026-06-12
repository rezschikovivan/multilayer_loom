from tkinter import Misc, W, Variable, END
from tkinter.ttk import Entry, Label
from loom.controller.command import Command
from abc import ABC, abstractmethod

class GetInputCommand(Command):
    """Command to get user input in feilds. Can reverse changes and reverses. Managed by CommandManager"""
    def __init__(self, feild:"InputWiget", receiver:Variable):
        self.feild = feild
        self.receiver = receiver

    def execute(self, *args, **kwds):
        if str(self.receiver.get()) == self.feild.get_data(): return # Do nothing if value wasn`t change
        self.last_state = self.receiver.get()
        self.curr_state = self.feild.get_data()
        self.manager.past_commands.append(self.copy())
        self.receiver.set(self.curr_state)

    def undo(self):
        self.receiver.set(self.last_state)
        self.feild.widget.delete(0, END)
        self.feild.widget.insert(0, str(self.last_state))

    def reverse_undo(self):
        self.receiver.set(self.curr_state)
        self.feild.widget.delete(0, END)
        self.feild.widget.insert(0, str(self.curr_state))

    def copy(self):
        cpy = GetInputCommand(self.feild, self.receiver)
        cpy.last_state = self.last_state
        cpy.curr_state = self.curr_state
        return cpy

class InputWiget(ABC):
    """Wiget each can take user input. Intaracting withs model variables through Command subclass"""
    def __init__(self, root:Misc, name:str, receiver:Variable):
        self._root = root
        self._name = name
        self._command = GetInputCommand(self, receiver)
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
    def validate(newvalue:str)->bool:
        """True or False for inputing char"""
    @abstractmethod
    def create_widget(self)->Entry:
        """Place and returns concrete widget (tkinter) for input"""
    def create_title(self):
        """Place the feild title"""
        self._label = Label(self._root, text=self._name)
        self._label.pack(anchor=W)
    def get_validatcommand(self):
        """Returns correct value for widget validatecommande"""
        return (self._root.register(self.validate), "%P")# set the method as a validation method
    def bind_enter(self):
        """Make the commande listening events"""
        self._input_widget.bind("<Return>", self._command.execute)
        self._input_widget.bind("<FocusOut>", self._command.execute)
    def get_data(self):
        """"Returns correct data from feild"""
        return self._input_widget.get()
    
class IntFeild(InputWiget):
    def create_widget(self):
        widget = Entry(self._root, validate="key", validatecommand=self.get_validatcommand())
        widget.pack()
        return widget
    def validate(self, newvalue:str)->bool:
        if newvalue.isdigit() or newvalue == "": return True
        return False
    def get_data(self):
        data = super().get_data() if super().get_data() != "" else  "0"
        return data

class LetterFeild(InputWiget):
    def create_widget(self):
        widget = Entry(self._root, validate="key", validatecommand=self.get_validatcommand())
        widget.pack()
        return widget
    
    def validate(self, newvalue:str)->bool: 
        if newvalue.isalpha() or newvalue == "": return True
        return False

