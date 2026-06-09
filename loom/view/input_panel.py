from tkinter import BOTH, LEFT, SOLID, Misc, Tk, W
from tkinter.ttk import Button, Entry, Frame, Label

class SettingsPanel:
    def __init__(self, root:Tk, listener:callable):
        self.feilds = {}
        self.__root = Frame(master=root, borderwidth=5, relief=SOLID, padding=[8, 10])
        self.__root.pack(side=LEFT, fill=BOTH)
        accept_btn = Button(master=self.__root, text="Принять", command=listener)
        accept_btn.pack(side="bottom")

    def add_input_feild(self, name:str, listener:callable=None):
        self.feilds[name] = InputFeild(self.__root, name, listener)

# data bean
class InputFeild:
    name:str
    label:Label
    entry:Entry
    def __init__(self, root:Misc, name:str, listener:callable=None):
        self.name = name
        self.label = Label(root, text=self.name)
        self.label.pack(anchor=W)
        
        self.entry = Entry(root)
        self.entry.pack()

        if listener is not None:
            self.add_handler(listener)

    def add_handler(self, handler:callable):
        self.entry.bind("<Return>", handler)