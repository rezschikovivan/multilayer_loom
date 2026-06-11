from tkinter import BOTH, LEFT, SOLID, Tk
from tkinter.ttk import Button, Frame
from loom.controller.command import Command
from loom.controller.input_feilds import InputWiget

class SettingsPanel:
    def __init__(self, root:Tk):
        self.feilds = {}
        self.root = Frame(master=root, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.root.pack(side=LEFT, fill=BOTH)

        
    def add_accept_btn(self, listener:Command):
        accept_btn = Button(master=self.root, text="Принять", command=listener)
        accept_btn.pack(side="bottom")

    def add_input_feild(self, input_feild_class:InputWiget, name:str, receiver):
        self.feilds[name] = input_feild_class(self.root, name, receiver)

