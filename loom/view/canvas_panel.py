from loom.view.canvas_bases import RainbowColorsGen, CanvasDepicter
from loom.model.model import FabricProfile, Side
from loom.view.shapes import WarpView, ClickArea, TopClickArea, BottomClickArea, WeftView
from tkinter import Tk

class CanvasPanel(CanvasDepicter):
    def __init__(self, root:Tk, profile:FabricProfile):
        profile.wefts.increase(Side.top, 8)
        profile.wefts.increase(Side.right, 4)
        super().__init__(root, profile.grid_width, profile.grid_height)
        self.draw_profile()

    @property
    def HEIGHT(self):
        return self.canvas.winfo_height()
    @property
    def WIDTH(self):
        return self.canvas.winfo_width()

    def set_current_warp(self, warp_view:"WarpView"):
        if self.active_line is warp_view:
            self.active_line.change_color()# возвращаем предыдущий цвет основе
            self.active_line = None
            return
        if self.active_line is not None:
            self.active_line.change_color()# возвращаем предыдущий цвет основе
        warp_view.change_color()
        self.active_line = warp_view
        print(self.active_line)

    def redraw_on_resize(self):
        self.canvas.delete("all")
        self.calculate_size_values()
        self.redraw_all()

    def calculate_size_values(self):
        self.x_intervale = self.WIDTH / (self.columns+1)
        self.y_intervale = self.HEIGHT / (self.rows+1)
        self.radius = (0.05 * self.y_intervale) + (0.05 * self.x_intervale )

    def draw_profile(self):
        self.can_be_redrawed = False
        self.canvas.delete("all")
        self.calculate_size_values()
        rainbow = RainbowColorsGen()

        self.__create_warp_view(0, 0, rainbow.next_color())# распологаем самую верхнюю линию основы (нулевую)
        for r in range(1, self.rows+1):
            self.y_step = r*self.y_intervale
            self.__create_warp_view(0, r, rainbow.next_color())
            for c in range(1, self.columns+1):
                self.x_step = c*self.x_intervale
                # распологаем кнопки и утки
                self.__create_click_area(c, r)#первыми распологать зоны для нажатий
                self.__create_weft_view(c, r)
        self.can_be_redrawed = True

    def get_canvas(self):
        return self.canvas

    def set_warp(self, column, row):
        print("Warp set")

    def get_warp(self, warp_index):
        print("Warp get")

    def set_weft(self, column, row):
        print("Weft set")

    def get_weft(self, column, row):
        print("Weft set")

    def __create_weft_view(self, column, row):
        WeftView(self, column, row)

    def __create_warp_view(self, column, row, color):
        WarpView(self, column, row, color)

    def __create_click_area(self, column:int, row:int):
        if row == 1:           # распологаем самый верхний ряд кнопок
            TopClickArea(self, column, row)
        if row == self.columns:# распологаем самый нижний  ряд кнопок
            BottomClickArea(self, column, row)
        else:
            ClickArea(self, column, row)



