from tkinter import BOTH, RIGHT, SOLID, Tk
from tkinter.ttk import Frame

from loom.utils import Singleton
from loom.view.top_menu import TopMenu
from loom.view.input_panel import SettingsPanel
from loom.controller.controller import SeetingsListener

def foo(*args):
    print("Foo Foo")

def bar(*args):
    print("Bar Bar")

class Window(Singleton):

    def __init__(self):
        self.__root = Tk()
        self.config_window()
        self.__root.protocol("WM_DELETE_WINDOW", self.exit)# bind exit button click

        self.panel = SettingsPanel(self.__root, SeetingsListener())
        self.menu = TopMenu(self.__root)

        self.panel.add_input_feild("Name", foo)
        self.panel.add_input_feild("LastName", bar)

        main_frame = Frame(borderwidth=5, relief=SOLID, padding=[8, 10])
        main_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    
    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.__root.title("Loom")
        self.__root.geometry("600x400")
        self.__root.iconbitmap(default="icon.ico")
        self.__root.state('zoomed')# expand on all screen
    
    def exit(self):
        """ Catch exit button click """
        self.__root.destroy()

    def run(self):
        self.__root.mainloop()




