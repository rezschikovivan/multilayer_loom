import os
import sys
from platform import system
from tkinter import PhotoImage, Tk

from loom.controller.command import CommandManager
from loom.model import FabricProfile
from loom.view.canvas_panel import CanvasPanel
from loom.view.tab_menu import TabMenu


class Window:
    """Main program window"""

    def __init__(self, profile:FabricProfile):
        self.root = Tk()
        self.config_window()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # bind exit button click

        self.menu = TabMenu(self.root)
        self.canvas = CanvasPanel(self.root, profile)
        
        self.bind_z_y_btns()

    def config_window(self):
        """Adjusts the window size, title, and icon"""
        self.root.title("Многослойный ткацкий станок КГУ")
        self.root.configure(bg="white")
        icon = PhotoImage(file=self._get_resource_path("icon.png"))
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
        manager = CommandManager()
        self.root.bind_all("<Control-z>", manager.undo)
        self.root.bind_all("<Control-y>", manager.redo)

    def _get_resource_path(self, filename):
        """
        Получает абсолютный путь к файлу ресурса.
        Работает и при запуске .py, и при запуске собранного .exe.
        """
        if hasattr(sys, '_MEIPASS'):
            # Путь внутри временной папки PyInstaller
            base_path = sys._MEIPASS
        else:
            # Обычный путь при разработке
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename)
    def exit(self):
        """Catch exit button click"""
        self.root.destroy()

    def run(self):
        """Start app"""
        self.root.mainloop()

