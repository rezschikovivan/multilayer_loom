from math import sqrt
from tkinter import Tk

from src.loom.controller import IncreaseWeftsCommand, ReduceWeftsCommand, SetWarpAnchorCommand
from src.loom.model import FabricProfile, IObserver, Side
from src.loom.model.warp import Warp
from src.loom.view.canvas_bases import CanvasDepicter, RainbowColorsGen
from src.loom.view.shapes import BottomClickArea, ClickArea, GridButton, TopClickArea, WarpView, WeftView


class CanvasPanel(CanvasDepicter, IObserver):
    def __init__(self, root:Tk, profile:FabricProfile):
        self.profile = profile
        self.profile.register_observer(self)
        super().__init__(root, profile.grid_width, profile.grid_height)
        self.draw_profile()

    def notify(self, profile:FabricProfile, *args):
        self.columns = profile.grid_width
        self.rows = profile.grid_height
        self.plan_to_draw_profile()

    def select_warp(self, warp_view:"WarpView"):
        """Устанавливает основу как выбранную, при выборе выбранной основы отменяет выбор"""
        if warp_view is None:
            raise ValueError("Основа не может быть выбрана, т.к. передали None!")
        if self.active_line is warp_view:# ткнули на уже выбранную
            self.unselect_warp()
            return
        if self.active_line is not None:
            self.active_line.change_color()#возвращаем цвет прошлой
        warp_view.change_color()
        self.active_line = warp_view

    def unselect_warp(self):
        if self.active_line:
            self.active_line.change_color()
        self.active_line = None

    def redraw_on_resize(self):
        """Перерисовывает существующие объекты"""
        self.canvas.delete("all")
        self.calculate_size_values()
        self.redraw_all()

    def calculate_size_values(self):
        """Расчитывает размеры для текущего окна"""
        self.x_intervale = self.width / (self.columns+1)
        self.y_intervale = self.height / (self.rows+1)
        self.radius = WeftView.radius_coeff * sqrt((self.y_intervale*2) * (self.x_intervale))

    def draw_profile(self):
        """Рисует профиль создавая объекты соответствующие модели"""
        self.can_be_redrawed = False
        self.del_all_redrawable()
        self.canvas.delete("all")
        self.calculate_size_values()
        rainbow = RainbowColorsGen()

        self.__create_warp_view(0, 0, rainbow.next_color())# распологаем самую верхнюю линию основы (нулевую)
        for r in range(1, self.rows+1):
            self.y_step = r*self.y_intervale
            warp = self.__create_warp_view(0, r, rainbow.next_color())
            if  self.active_line and self.rows - r == self.active_line.level:
                warp._tint()
            for c in range(1, self.columns+1):
                self.x_step = c*self.x_intervale
                # распологаем зоны нажатия и утки
                self.__create_weft_view( c, r)
                self.__create_click_area(c, r)
        self.draw_buttons()
        self.can_be_redrawed = True

    def draw_buttons(self):
        """Создаёт кнопки слева и справа"""

        for i, side in enumerate((Side.top, Side.left, Side.bottom), 1):
            self.__make_buttons_kit(i, True, side)

        for i, side in enumerate((Side.top, Side.right, Side.bottom), 1):
            self.__make_buttons_kit(i, False, side)
        
    def get_canvas(self):
        return self.canvas

    def get_warp(self, warp_index)->Warp:
        return self.profile.get_warp(warp_index)

    def left_click_warp(self, column, row):
        if self.active_line:
            SetWarpAnchorCommand(self.profile, self.active_line.level, column, row).execute()
            #self.profile.set_anchor(self.active_line.level, column, row)
            print(self.profile.get_warp(self.active_line.level))

    def right_click_warp(self, warp_index):
        print("Warp get")

    def left_click_weft(self, column, row):
        print("Weft set1")

    def right_click_weft(self, column, row):
        print("Weft set2")

    def __create_weft_view(self, column, row):
        return WeftView(self, column, row)

    def __create_warp_view(self, column, row, color):
        return WarpView(self, column, row, color)

    def __create_click_area(self, column:int, row:int):
        if row == 1:           # распологаем самый верхний ряд кнопок
            TopClickArea(self, column, row)
        if row == self.rows:# распологаем самый нижний  ряд кнопок
            BottomClickArea(self, column, row)
        else:
            ClickArea(self, column, row)

    def __make_buttons_kit(self, floor:int, is_on_left:bool, cmnd_side:Side):
        """Принимает координаты левой верхней точки набора кнопок и строну для взаимодействия"""
        self.__create_button(floor, is_on_left, cmnd_side, True)
        self.__create_button(floor, is_on_left, cmnd_side, False)

    def __create_button(self, floor:int, is_on_left:bool, cmnd_side:Side, is_increase:bool):
        """Создает одну кнопку"""
        if is_increase:
            action = IncreaseWeftsCommand(self.profile, cmnd_side)
        else:
            action = ReduceWeftsCommand(self.profile, cmnd_side)
        GridButton(self, floor, is_on_left, is_increase, action)
