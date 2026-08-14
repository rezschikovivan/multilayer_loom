from abc import abstractmethod
from tkinter import DISABLED, Event
from tkinter.font import Font

from loom.controller import Command
from loom.view.canvas_bases import CanvasDepicter, Redrawable

# Базовые классы визуальных элементов холста

class BaseView(Redrawable):
    def __init__(self, depicter:CanvasDepicter):
        self.depicter = depicter
        self.depicter.add_redrawable(self)
        self.cnvs = depicter.get_canvas()
        self.redraw()
        self.cnvs.update()

    def redraw(self):
        """Перерисовывает объект"""
        self.id = self.draw()
        if not isinstance(self.id, (int, str)):
            raise TypeError("Метод draw подкласса BaseView должен возвращать идентефикатор рисунка на холсте: int или str")
        self.cnvs.tag_bind(self.id, "<Button-1>", self.on_click_left)
        self.cnvs.tag_bind(self.id, "<Button-3>", self.on_click_right)

    @abstractmethod
    def draw(self)-> str|int:
        """Отрисовывает фигуру и возвращет её идентифекатор в tkinter"""
        raise NotImplementedError()
    @abstractmethod
    def on_click_right(self, event:Event):
        """Обрабатывает нажатие правой кнопки мыши"""
        raise NotImplementedError()
    @abstractmethod
    def on_click_left(self, event:Event):
        """Обрабатывает нажатие левой кнопки мыши"""
        raise NotImplementedError()

class GridableView(BaseView):
    """
    Базовый класс описывабщий графические обьекты на холсте.
    Которые можно расположить по сетке колонок и строчек.
    """
    def __init__(self, depicter:CanvasDepicter, column, row):
        self.column = column
        self.row = row
        super().__init__(depicter)

    @property
    def x_step(self)->float:
        return self.column*self.depicter.x_intervale
    @property
    def y_step(self)->float:
        return self.row*self.depicter.y_intervale
    
# Конкретные подклассы

class WeftButton(BaseView):
    side_coeff = 0.05
    def __init__(self, depicter, x, y, cmnd_side, is_increase:bool, command:Command):
        self.x = x
        self.y = y
        self.is_increase = is_increase
        self.cmnd_side = cmnd_side
        self.command = command
        super().__init__(depicter)
    
    @property
    def side_size(self)->float:
        return self.get_side_size(self.depicter.x_intervale, self.depicter.y_intervale)
    
    @classmethod
    def get_side_size(cls, x_intervale:float, y_intervale:float):
        return round(min(x_intervale, y_intervale)*cls.side_coeff)
    
    def draw(self):
        x0 = round(self.x)
        y0 = round(self.y)
        x1 = self.x+self.side_size
        y1 = self.y+self.side_size
        sign = "+" if self.is_increase else "−"
        o_id = self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#C5C5C5", outline="#000000", activefill="#AFAFAF")
        self.cnvs.create_text(x0+(round(x1-x0))/2, y0+(round(y1-y0))/2, text=sign, state=DISABLED,font=Font(size=int(self.side_size)))
        return o_id

    def on_click_right(self, event):
        pass

    def on_click_left(self, event):
        self.command.execute()

class WeftView(GridableView):
    """Визуал описывающий уток"""
    radius_coeff = 0.04
    def __init__(self, depicter:CanvasDepicter, column, row):
        super().__init__(depicter, column, row)

    def on_click_left(self, event):
        self.depicter.set_weft(self.column, self.row)

    def on_click_right(self, event):
        self.depicter.get_weft(self.column, self.row)

    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step-self.depicter.radius
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.radius
        o_id = self.cnvs.create_oval(x0, y0, x1, y1, outline="#000000", fill="#FFFFFF", width=1.5)
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"{self.column-1}:{self.depicter.rows-self.row}")
        return o_id

class WarpView(GridableView):
    """Визуал описывающий основу"""
    thickness_coefficient = WeftView.radius_coeff*2
    tint_precent = 50
    def __init__(self, depicter:CanvasDepicter, column, row, color:str):
        self.level = depicter.rows - row
        self.color = color
        self.tint_color:str = ""
        self.is_tinted: bool = False
        super().__init__(depicter, column, row)

    def on_click_left(self, event):
        self.depicter.set_selected_warp(self)
        
    def on_click_right(self, event):
        self.depicter.get_warp(self.level)

    def draw(self):
        x0 = 0
        y0 = self.y_step+(0.5*self.depicter.y_intervale)
        x1 = self.depicter.canvas.winfo_width()
        y1 = self.y_step+(0.5*self.depicter.y_intervale)
        o_id = self.cnvs.create_line(x0, y0, x1, y1, fill=self.color, width=self.depicter.y_intervale*self.thickness_coefficient)
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"index: {self.level}", fill="#FF0000")
        return o_id

    def change_color(self):
        """Меняет цвет этой основы при выборе/отмене выбора"""
        if self.is_tinted:
            self.is_tinted = False
            self._untint()
        else:
            self.is_tinted = True
            self._tint()
    
    def _tint(self) -> str:
        """Устанавливает текущий цвет на затемнённый от обычного"""
        if self.tint_color == "":
            curr_color = self.color.lstrip('#')
            
            r = int(curr_color[0:2], 16)
            g = int(curr_color[2:4], 16)
            b = int(curr_color[4:6], 16)

            factor = 1 - (self.tint_precent / 100.0)
            
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))

            self.tint_color = f"#{r:02x}{g:02x}{b:02x}"
        self.cnvs.itemconfigure(self.id, fill=self.tint_color)

    def _untint(self):
        """Устанавливает цвет на страндартный"""
        self.cnvs.itemconfigure(self.id, fill=self.color)

class ClickArea(GridableView):
    """Визуал описывающий зону для нажатия"""
    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step-self.depicter.radius+self.depicter.y_intervale
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.radius
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.column-1}:r{self.depicter.rows-self.row}")
        self.cnvs.tag_lower(o_id)
        return o_id
    
    def on_click_right(self, event:Event):
        pass

    def on_click_left(self, event:Event):
        self.depicter.set_warp(self.column, self.row)

class BottomClickArea(ClickArea):
    """Визуал описывающий нижнею зону для нажатий"""
    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step+self.depicter.radius
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.y_intervale
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.column-1}:r{0}")
        self.cnvs.tag_lower(o_id)
        return o_id
    
class TopClickArea(ClickArea):
    """Визуал описывающий верхнию зону для нажатий"""
    def draw(self):
        x0 = self.x_step - self.depicter.radius
        y0 = 0
        x1 = self.x_step + self.depicter.radius
        y1 = self.depicter.y_intervale-self.depicter.radius
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.column-1}:r{self.depicter.rows}")
        self.cnvs.tag_lower(o_id)
        return o_id