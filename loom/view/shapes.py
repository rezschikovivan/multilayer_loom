from loom.view.canvas_bases import CanvasDepicter, Redrawable
from abc import abstractmethod

from tkinter import Event

# Базовые классы визуальных элементов холста

class GridableView(Redrawable):
    """
    Базовый класс описывабщий графические обьекты на холсте.
    Которые можно расположить по сетке колонок и строчек.
    """
    def __init__(self, depicter:CanvasDepicter, column, row):
        self.depicter = depicter
        self.column = column
        self.row = row
        self.depicter.add_redrawable(self)
        self.cnvs = depicter.get_canvas()
        self.redraw()
        self.cnvs.update()

    @property
    def x_step(self)->float:
        return self.column*self.depicter.x_intervale
    @property
    def y_step(self)->float:
        return self.row*self.depicter.y_intervale

    def redraw(self):
        """Перерисовывает объект"""
        self.id = self.draw()
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
    
# Конкретные подклассы

class WarpView(GridableView):
    """Визуал описывающий основу"""
    def __init__(self, depicter:CanvasDepicter, column, row, color:str):
        self.level = depicter.rows - row
        self.color = color
        self.tint_color:str = ""
        self.is_tinted: bool = False
        self.tint_precent:int = 50
        super().__init__(depicter, column, row)

    def on_click_left(self, event):
        self.depicter.set_current_warp(self)
        
    def on_click_right(self, event):
        self.depicter.get_warp(self.level)

    def draw(self):
        x0 = 0
        y0 = self.y_step+(0.5*self.depicter.y_intervale)
        x1 = self.depicter.canvas.winfo_width()
        y1 = self.y_step+(0.5*self.depicter.y_intervale)
        o_id = self.cnvs.create_line(x0, y0, x1, y1, fill=self.color, width=self.depicter.y_intervale*0.1)
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

class WeftView(GridableView):
    """Визуал описывающий уток"""
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


class ClickArea(GridableView):
    """Визуал описывающий зону для нажатия"""
    def on_click_right(self, event:Event):
        pass

    def on_click_left(self, event:Event):
        self.depicter.set_warp(self.column, self.row)

    def draw(self):
        x0 = self.x_step-self.depicter.radius
        y0 = self.y_step-self.depicter.radius+self.depicter.y_intervale
        x1 = self.x_step+self.depicter.radius
        y1 = self.y_step+self.depicter.radius
        o_id =  self.cnvs.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="#FFFFFF")
        self.cnvs.create_text((x0+x1)*0.5, (y0+y1)*0.5, text=f"c{self.column-1}:r{self.depicter.rows-self.row}")
        self.cnvs.tag_lower(o_id)
        return o_id

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