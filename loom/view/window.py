from tkinter import BOTH, RIGHT, SOLID, Tk
from tkinter.ttk import Frame

from loom.view.tab_menu import TabMenu
from loom.view.input_panel import ParametrsPanel
from loom.controller.input_feilds import InputWiget
from loom.controller.command import Command

class Window():
    """Main program window"""
    def __init__(self):
        self.root = Tk()
        self.config_window()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)# bind exit button click

        self.parametrs_panel = ParametrsPanel(self.root)
        self.menu = TabMenu(self.root)

        self.main_frame = Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.bind_Z_Y_btns()

    
    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.root.title("Многослойный ткацкий станок КГУ")
        #self.root.iconbitmap(default="icon.ico", bitmap="icon.ico")# On linux doesn`t work
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}")# set fullscreen size

    def add_feild_to_parametrs(self, input_feild_class:InputWiget, name:str, receiver):
        self.parametrs_panel.add_input_feild(input_feild_class, name, receiver)

    def bind_Z_Y_btns(self):
        """Bind undo and reverse undo buttons"""
        self.root.bind_all("<Control-z>", Command.manager.unexecute)
        self.root.bind_all("<Control-y>", Command.manager.reverse_unexecute)
    
    def exit(self):
        """ Catch exit button click """
        self.root.destroy()

    def run(self):
        """Start app"""
        self.root.mainloop()




