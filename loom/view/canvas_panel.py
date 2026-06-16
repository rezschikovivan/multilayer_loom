from loom.model.profile_data import Profile

from tkinter import Canvas, Frame, SOLID
from tkinter.ttk import Button

class CanvasPanel:
    def __init__(self, root, profile:Profile):
        self.root = Frame(master=root, borderwidth=1, relief=SOLID)
        self.root.grid(row=0, column=1,columnspan=5, rowspan=10, sticky="nsew")
        self.profile = profile
        self.root = Canvas(self.root)
        FabricGrid(self.root, self.profile)

class FabricGrid:
    def __init__(self, root, profile:Profile):
        self.profile_settings = profile
        self.root = root
        #self.create_grid(self.profile_settings.width.get(), self.profile_settings.height.get())
        self.create_grid(3,3)

    def create_grid(self, x:int, y:int):
        for c in range(x):
            for r in range(y):
                btn = Button(text=f"{r},{c}")
                btn.grid(row=r, column=c)
#основа
class Warp:
    def __init__(self, layer:int):
        self.base_layer = layer # level at which the warp enters and exist fabric profile

#уток
class Weft:
    def __init__(self):
        self.involved = False   # participates in weaving