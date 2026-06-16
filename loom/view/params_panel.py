from tkinter import BOTH, LEFT, SOLID, Tk
from tkinter.ttk import Button, Frame
from typing import Dict

from loom.controller.command import Command
from loom.controller.input_feilds import InputWiget, IntFeild
from loom.model.profile_data import Profile

class ParametrsPanel:
    """Left user input pannel"""
    def __init__(self, root:Tk, profile:Profile):
        self.root = Frame(master=root, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.root.grid(row=0, column=0, rowspan=10, sticky="nsew")

        self.profile = profile

        self.feilds:Dict[str,InputWiget] = {}
        self.add_input_feild(IntFeild, "Height", self.profile.height)
        self.add_input_feild(IntFeild, "Width", self.profile.width)
        self.add_accept_btn()
        
    def add_accept_btn(self):
        """Button to accept settings chandes"""
        accept_btn = Button(master=self.root, text="Accept")# input accepting by <FocusOut> from entry event 
        accept_btn.pack(side="bottom")

    def add_input_feild(self, input_feild_class:InputWiget, name:str, receiver):
        """Create and place input feild on panel"""
        self.feilds[name] = input_feild_class(self.root, name, receiver)