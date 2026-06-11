from tkinter import Misc, W, Variable, END
from tkinter.ttk import Entry, Label
from loom.controller.command import Command
from abc import ABC, abstractmethod

class GetInputCommand(Command):
    def __init__(self, feild:"InputWiget", receiver:Variable):
        self.feild = feild
        self.receiver = receiver

    def execute(self, *args, **kwds):
        if str(self.receiver.get()) == self.feild.get_data(): return # Do nothing if value wasn`t change
        self.last_state = self.receiver.get()
        self.manager.past_commands.append(self.copy())
        self.receiver.set(self.feild.get_data())

    def undo(self):
        self.receiver.set(self.last_state)
        self.feild.widget.delete(0, END)
        self.feild.widget.insert(0, str(self.receiver.get()))

    def copy(self):
        cpy = GetInputCommand(self.feild, self.receiver)
        cpy.last_state = self.last_state
        return cpy

class InputWiget(ABC):
    def __init__(self, root:Misc, name:str, receiver:Variable):
        self._root = root
        self._name = name
        self._receiver = receiver
        self._command = GetInputCommand(self, self._receiver)
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
        pass
    @abstractmethod
    def create_widget(self)->Entry:
        pass
    def create_title(self):
        self._label = Label(self._root, text=self._name)
        self._label.pack(anchor=W)
    def get_validatcommand(self):
        return (self._root.register(self.validate), "%P")# set the method as a validation method

    def bind_enter(self):
        self._input_widget.bind("<Return>", self._command.execute)
        self._input_widget.bind("<FocusOut>", self._command.execute)
    def get_data(self):
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

