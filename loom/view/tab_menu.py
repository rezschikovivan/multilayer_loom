from tkinter import Tk, Menu

class TabMenu:
    """Top menu battons object"""
    def __init__(self, root:Tk):
        self.__root = root
        self.__root.option_add("*tearOff", False)
        self.menu = Menu()

        self.add_file_tab()

        self.__root.config(menu=self.menu)

    def add_file_tab(self):
        file_menu = Menu()
        file_menu.add_cascade(label="New")
        file_menu.add_cascade(label="Open")
        file_menu.add_cascade(label="Save")
        self.menu.add_cascade(label="File", menu=file_menu)