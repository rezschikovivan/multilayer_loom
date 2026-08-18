from abc import abstractmethod
from tkinter import DISABLED, Event
from tkinter.font import Font

#from math import 
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
    @property
    def model_row(self):
        return self.depicter.rows - self.row
    @property
    def model_column(self):
        return (self.column-1)
# Конкретные подклассы

class GridButton(BaseView):
    """
    # Визуал кнопок взаимодействия с сеткой
    Описывает квадратную кнопку в рамках холста с командой на уменьшение или увеличение сетки утков
    ### Конструктор: 
    WeftButton( depicter:CanvasDepicter, x:float, y:float, cmnd_side:Side|str, is_increase:bool, command:Command )
    ### Значение x, y аргуметов:
    Задают положение левого верхнего угла кнопки 
    """
    side_coeff = 0.03
    btns_on_side = 3
    def __init__(self, depicter, floor:int, is_on_left:bool, is_increase:bool, command:Command):
        self.floor = floor
        self.is_increase = is_increase
        self.is_on_left = is_on_left
        self.command = command
        super().__init__(depicter)
    
    @property
    def side_size(self)->float:
        return self.get_side_size(self.depicter.width, self.depicter.height)
    
    @classmethod
    def get_side_size(cls, wi_width:float, wi_height:float):
        return round(min(wi_width, wi_height)*cls.side_coeff)
    
    def draw(self):
        y_step = self.depicter.height / (self.btns_on_side+1)
        x0 = self.side_size if  self.is_on_left else (self.depicter.width - (self.side_size*2))
        y0 = y_step*self.floor + (self.side_size if not self.is_increase else 0)
        x1 = x0*2 if  self.is_on_left else self.depicter.width-self.side_size
        y1 = y_step*self.floor + (0 if not self.is_increase else -self.side_size)
        sign = "+" if self.is_increase else "−"
        o_id = self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#C5C5C5", outline="#000000", activefill="#AFAFAF")
        t_id = self.cnvs.create_text(max(x0, x1)-(max(x0, x1)-min(x0, x1))/2, max(y0, y1)-(max(y0, y1)-min(y0, y1))/2,
                              text=sign, state=DISABLED, font=Font(size=int(self.side_size)))
        self.cnvs.tag_raise(o_id)
        self.cnvs.tag_raise(t_id)
        return o_id

    def on_click_right(self, event):
        pass

    def on_click_left(self, event):
        if self.depicter.can_be_redrawed:
            self.command.execute()

class WeftView(GridableView):
    """Визуал описывающий уток"""
    radius_coeff = 0.06
    def __init__(self, depicter:CanvasDepicter, column, row):
        super().__init__(depicter, column, row)

    def on_click_left(self, event):
        self.depicter.left_click_weft(self.model_column, self.model_row)

    def on_click_right(self, event):
        self.depicter.right_click_weft(self.model_column, self.model_row)

    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step-self.depicter.radius
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.radius
        o_id = self.cnvs.create_oval(x0, y0, x1, y1, outline="#000000", fill="#FFFFFF", width=1.5)
        #self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"{self.model_column}:{self.model_row}",state=DISABLED)
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
        
    @property
    def tag(self):
        return f"warp{self.level}"

    def on_click_left(self, event):
        self.depicter.select_warp(self)
        
    def on_click_right(self, event):
        self.depicter.right_click_warp(self.level)

    def draw(self):
        self.draw_warp()
        return self.tag

    def draw_warp(self):
        y_step = self.depicter.y_intervale* (self.row)
        last_point = (0, 0)
        next_point = (0, y_step+(0.5*self.depicter.y_intervale))
        for i, rel_anchor in enumerate(self.depicter.get_warp(self.level), 1):
            last_point = next_point
            next_point = (self.depicter.x_intervale*i, self.anchor_to_y(rel_anchor))
            self.create_line(*last_point, *next_point)
        last_point = next_point
        next_point = (self.depicter.canvas.winfo_width(), y_step+(0.5*self.depicter.y_intervale))
        self.create_line(*last_point, *next_point)

    def anchor_to_y(self, anchor:int)->float:
        if anchor < 0:
            return self.depicter.y_intervale*(abs(anchor)+self.row)+(0.5*self.depicter.y_intervale)
        elif anchor == 0:
            return (self.depicter.y_intervale*self.row) + (0.5*self.depicter.y_intervale)
        elif anchor > 0:
            return self.depicter.height - self.depicter.y_intervale*(self.level+anchor) - (0.5*self.depicter.y_intervale) 

    def create_line(self, x0, y0, x1, y1):
        color = self.color if not self.is_tinted else self.tint_color or self._tint()
        o_id = self.cnvs.create_line(x0, y0, x1, y1, fill=color, width=self.depicter.y_intervale*self.thickness_coefficient, tags=(self.tag,))
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
        return self.tint_color

    def _untint(self):
        """Устанавливает цвет на страндартный"""
        self.cnvs.itemconfigure(self.id, fill=self.color)

# Зоны нажатия

class ClickArea(GridableView):
    """Визуал описывающий зону для нажатия"""
    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step-self.depicter.radius+self.depicter.y_intervale
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.radius
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        #self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.model_column}:r{self.model_row}")
        self.cnvs.tag_lower(o_id)
        return o_id
    
    def on_click_right(self, event:Event):
        pass

    def on_click_left(self, event:Event):
        self.depicter.left_click_warp(self.model_column, self.model_row)

class BottomClickArea(ClickArea):
    """Визуал описывающий нижнею зону для нажатий"""
    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step+self.depicter.radius
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.y_intervale
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        #self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.model_column}:r{0}")
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
        #self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.model_column}:r{self.depicter.rows}")
        self.cnvs.tag_lower(o_id)
        return o_id
    def on_click_left(self, event:Event):
        self.depicter.left_click_warp(self.model_column, self.model_row+1)