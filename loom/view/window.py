from platform import system
from tkinter import PhotoImage, Tk

from loom.controller.command import CommandManager
from loom.model.model import FabricProfile
from loom.view.canvas_panel import CanvasPanel
from loom.view.tab_menu import TabMenu


class Window:
    """Main program window"""

    def __init__(self, profile:FabricProfile):
        self.root = Tk()
        self.config_window()
        self.config_grid()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # bind exit button click
        self.manager = CommandManager()

        self.menu = TabMenu(self.root)

        self.canvas = CanvasPanel(self.root, profile, self.manager)
        
        self.bind_z_y_btns()

    def config_grid(self):
        for r in range(10):
            self.root.columnconfigure(index=r, weight=1)
        for r in range(10):
            self.root.rowconfigure(index=r, weight=1)

    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.root.title("Многослойный ткацкий станок КГУ")
        icon = PhotoImage(file="icon.png")
        self.root.iconphoto(True, icon)
        self.root.geometry("600x400")  # set usual size

        platform = system()
        if platform == "Windows":
            self.root.state("zoomed")
        if platform == "Linux":
            w = self.root.winfo_screenwidth()
            h = self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}")  # set fullscreen size

    def bind_z_y_btns(self):
        """Bind undo and reverse undo buttons"""
        self.root.bind_all("<Control-z>", self.manager.undo)
        self.root.bind_all("<Control-y>", self.manager.redo)

    def exit(self):
        """Catch exit button click"""
        self.root.destroy()

    def run(self):
        """Start app"""
        self.root.mainloop()
