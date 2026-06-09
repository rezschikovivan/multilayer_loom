from tkinter import BOTH, RIGHT, SOLID, Tk
from tkinter.ttk import Frame

from loom.view.tab_menu import TopMenu
from loom.view.input_panel import SettingsPanel
from loom.controller.input_feilds import InputFeild
from loom.controller.command import Command

def foo(*args):
    print("Foo Foo")

def bar(*args):
    print("Bar Bar")

class Window():

    def __init__(self):
        self.root = Tk()
        self.config_window()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)# bind exit button click

        self.panel = SettingsPanel(self.root)
        self.menu = TopMenu(self.root)

        self.main_frame = Frame(borderwidth=5, relief=SOLID, padding=[8, 10])
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.bind_Z_btn()

    
    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.root.title("Многослойный ткацкий станок КГУ")
        self.root.geometry("600x400")
        self.root.iconbitmap(default="icon.ico")
        self.root.state('zoomed')# expand on all screen

    def add_feild_to_panel(self, input_feild_class:InputFeild, name:str, receiver):
        self.panel.add_input_feild(input_feild_class, name, receiver)

    def bind_Z_btn(self):
        self.root.bind_all("<Control-z>", Command.manager.unexecute)
        #self.panel.root.bind("<Control-z>", Command.manager.unexecute)
    
    def exit(self):
        """ Catch exit button click """
        self.root.destroy()

    def run(self):
        self.root.mainloop()




