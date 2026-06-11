from tkinter import BOTH, RIGHT, SOLID, Tk
from tkinter.ttk import Frame
from abc import ABC, abstractmethod

from loom.view.tab_menu import TopMenu
from loom.view.input_panel import SettingsPanel
from loom.controller.input_feilds import InputWiget
from loom.controller.command import Command

class Window():

    def __init__(self):
        self.root = Tk()
        self.config_window()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)# bind exit button click

        self.panel = SettingsPanel(self.root)
        self.menu = TopMenu(self.root)

        self.main_frame = Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.bind_Z_btn()

    
    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.root.title("Многослойный ткацкий станок КГУ")
        #self.root.iconbitmap(default="icon.ico", bitmap="icon.ico")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}")# set fullscreen

    def add_feild_to_panel(self, input_feild_class:InputWiget, name:str, receiver):
        self.panel.add_input_feild(input_feild_class, name, receiver)

    def bind_Z_btn(self):
        self.root.bind_all("<Control-z>", Command.manager.unexecute)
        #self.panel.root.bind("<Control-z>", Command.manager.unexecute)
    
    def exit(self):
        """ Catch exit button click """
        self.root.destroy()

    def run(self):
        self.root.mainloop()




