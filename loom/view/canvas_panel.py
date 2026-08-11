from loom.view.canvas_bases import RainbowColorsGen, CanvasDepicter
from loom.model import FabricProfile, Side, Observer, WeftsGrid 
from loom.view.shapes import WarpView, ClickArea, TopClickArea, BottomClickArea, WeftView, WeftsButton
from loom.controller.model_interact import CommandManager, ReduceWeftsCommand, IncreaseWeftsCommand
from tkinter import Tk

class CanvasPanel(CanvasDepicter, Observer):
    def __init__(self, root:Tk, profile:FabricProfile, manager:CommandManager):
        self.profile = profile
        self.manager = manager
        self.profile.register_grid_listener(self)
        super().__init__(root, profile.grid_width, profile.grid_height)
        self.draw_profile()

    @property
    def HEIGHT(self):
        return self.canvas.winfo_height()
    @property
    def WIDTH(self):
        return self.canvas.winfo_width()

    def notify(self, grid:WeftsGrid, side):
        self.columns = grid.row_width
        self.rows = grid.column_height
        print(self.profile.grid)
        self.draw_profile()

    def set_selected_warp(self, warp_view:"WarpView"):
        """Устанавливает основу как выбранную"""
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
        self.radius = ((0.05 * self.y_intervale) + (0.05 * self.x_intervale ))/2

    def draw_profile(self):
        self.can_be_redrawed = False
        self.del_all_redrawable()
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
        self.__make_buttons_kit(self.x_intervale*0.5, self.y_intervale*0.25, Side.top)
        self.can_be_redrawed = True

    def draw_buttons(self):
        # РАЗМЕЩАТЬ КНОПКИ ПО УГЛАМ ЦИКЛОМ
        for i in range(1, self.columns+1, self.columns-1):# вверху сетки ->- внизу сетки
            x = self.x_intervale*i*0.5
            y = self.y_intervale*i*0.25
            self.__make_buttons_kit(x,y)
        
                    

    def __make_buttons_kit(self, x, y, cmnd_side:Side):
        """Принимает координаты правой нижней точки кнопок"""
        btn_h = WeftsButton.height_coeff*self.y_intervale
        btn_w = WeftsButton.width_coeff*self.x_intervale
        self.__draw_button(x-btn_w, y-btn_h, cmnd_side, True)
        self.__draw_button(x-(2*btn_w), y-(2*btn_h), cmnd_side, False)

    def __draw_button(self, x, y, cmnd_side:Side, is_increase:bool):
        """Создает одну кнопку"""
        action = IncreaseWeftsCommand(self.profile, cmnd_side, self.manager) if is_increase else ReduceWeftsCommand(self.profile, cmnd_side, self.manager)
        WeftsButton(self, x,y, cmnd_side, is_increase, action)
        
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



