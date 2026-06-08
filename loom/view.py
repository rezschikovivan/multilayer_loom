from tkinter import Tk, SOLID, W, BOTH, LEFT, RIGHT, Misc
from tkinter.ttk import Frame, Label, Entry, Button


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):# call instead of the constructor
        if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.__init__(*args)
        return cls._instance

def foo(*args):
    print("Foo Foo")

def bar(*args):
    print("Bar Bar")

class Window(Singleton):

    __left_panel = None

    def __init__(self, root:Tk):
        self.__root = root
        self.__root.title("Loom")
        self.__root.geometry("600x400")
        self.__root.iconbitmap(default="icon.ico")

        self.left_panel.add_input_feild("Name", foo)
        self.left_panel.add_input_feild("LastName", bar)

        main_frame = Frame(borderwidth=5, relief=SOLID, padding=[8, 10])
        main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        name_label = Label(main_frame, text="Введите Pyfxtybtимя")
        name_label.grid(row=0, column=0)
        
        name_entry = Entry(main_frame)
        name_entry.grid(row=1, column=0)

    @property
    def left_panel(self)->SettingsPanel:
        if self.__left_panel is None:
            self.__left_panel = SettingsPanel(self.__root, foo)
        return self.__left_panel
    
    def run(self):
        self.__root.mainloop()

class SettingsPanel:
    def __init__(self, root:Tk, listener:callable):
        self.feilds = {}
        self.__root = Frame(master=root, borderwidth=5, relief=SOLID, padding=[8, 10])
        self.__root.pack(side=LEFT, fill=BOTH)
        accept_btn = Button(master=self.__root, text="Принять", command=listener)
        accept_btn.pack(side="bottom")

    def add_input_feild(self, name:str, listener:callable=None):
        self.feilds[name] = Feild(self.__root, name, listener)

# data bean
class Feild:
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

    

