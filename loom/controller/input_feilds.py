from tkinter import Misc, W, Variable
from tkinter.ttk import Entry, Label
from loom.controller.command import Command

class GetInputCommand(Command):
    def __init__(self, feild:"InputFeild", receiver:Variable):
        self.feild = feild
        self.receiver = receiver
        self.last_state = None

    def execute(self, *args, **kwds):
        self.last_state = self.receiver.get()
        self.manager.past_commands.append(self.copy())
        self.receiver.set(self.feild.get_data())

    def undo(self):
        if self.last_state is not None:
            self.receiver.set(self.last_state)

    def copy(self):
        cpy = GetInputCommand(self.feild, self.receiver)
        cpy.last_state = self.last_state
        return cpy

class InputFeild:
    def __init__(self, root:Misc, name:str, receiver:Variable):
        self.__root = root
        self.__name = name
        self.__receiver = receiver
        self.__command = GetInputCommand(self, self.__receiver)
        self.create_title()
        self.create_input_widget()
        self.bind_command()
    @property
    def name(self):
        return self.__name
    @property
    def widget(self):
        return self.__input_widget
    
    def create_title(self):
        self.__label = Label(self.__root, text=self.__name)
        self.__label.pack(anchor=W)

    def create_input_widget(self):
        check = (self.__root.register(self.check), "%P")# set the method as a validation method
        self.__input_widget = Entry(self.__root, validate="key", validatecommand=check)
        self.__input_widget.pack()

    def bind_command(self):
        self.__input_widget.bind("<Return>", self.__command.execute)

    def check(newvalue:str)->bool:# any literal
        return True

    def get_data(self):
        return self.__input_widget.get()

    
class IntFeild(InputFeild):
    def check(self, newvalue:str)->bool:
        if newvalue.isdigit() or newvalue == "": return True
        return False
class LetterFeild(InputFeild):
    def check(self, newvalue:str)->bool: 
        if newvalue.isalpha() or newvalue == "": return True
        return False

