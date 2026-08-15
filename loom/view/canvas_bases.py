from abc import ABC, abstractmethod
from collections.abc import Generator
from tkinter import Canvas, Event, Tk


class Redrawable(ABC):
    """Интерфейс объектов которые перерисовщик Redrawer может перерисовать"""
    @abstractmethod
    def redraw(self):
        """Перерисовать объект"""
        raise NotImplementedError()

class Redrawer:
    """
    Перерисовщик работающий по приниципу 'наблюдателя' и перерисовывает все добавленные объекты 
    реализующие интерфейс Redrawable
    """
    def __init__(self):
        self._to_redraw: list[Redrawable] = []

    def add_redrawable(self, redrawable: Redrawable):
        """Добавляет обьект слушатель для перерисовки"""
        self._to_redraw.append(redrawable)

    def redraw_all(self):
        """Перерисовывает все добавленные объекты"""
        for redrawable in self._to_redraw:
            redrawable.redraw()

    def del_all_redrawable(self):
        """
        Отчищает список объектов для перерисовки, тем самым предотвращая утечки памяти.
        """
        self._to_redraw: list[Redrawable] = []

class ResizableCanvas(Redrawer):
    """Базовый класс для перерисовки канваса при изменении его размеров"""
    def __init__(self, main_root:Tk):
        super().__init__()
        self.main_root = main_root
        self.redraw_duration_ms: int = 100
        self._after_id = None
        self.can_be_redrawed: bool = True
        self.main_root.bind("<Expose>", self.__on_resizing)

    @abstractmethod
    def redraw_on_resize(self):
        """Перерисовывает изображение при изменении размеров окна"""
        raise NotImplementedError()

    def __redraw(self):
        self.can_be_redrawed = False
        self.redraw_on_resize()
        self.can_be_redrawed = True
    
    def __on_resizing(self, event:Event):
        """Срабатывает при изменении размеров окна, планирует в цикле событий перерисовк окна"""
        if event.widget is self.main_root:
            if getattr(self, "_after_id", None):
                self.main_root.after_cancel(self._after_id)
            self._after_id = self.main_root.after(self.redraw_duration_ms, self.__redraw)

class CanvasDepicter(ResizableCanvas):
    """
    Базовый класс холста-посредника обеспечивающего работоспособность всех обьектов на холсте
    """
    def __init__(self, root:Tk, columns, rows):
        if columns <= 0 or rows <= 0:
            raise ValueError(f"Количество колонок:строчек должно быть больше нуля, сейчас {columns}:{rows}")
        super().__init__(root)
        self.canvas = Canvas(root, bg="white", borderwidth=0, highlightthickness=0)
        self.canvas.pack(anchor='center', expand=True, fill='both')
        self.canvas.update()

        self.active_line = None
        self.x_intervale:float = 0
        self.y_intervale:float = 0
        self.radius = 0
        self.rows:int = rows
        self.columns:int = columns
        self.draw_delay_ms = 10

    @property
    def height(self):
        return self.canvas.winfo_height()
    @property
    def width(self):
        return self.canvas.winfo_width()

    def plan_to_draw_profile(self, *args):
        """
        Планирует перерисовать профиль, если поступает еще запрос обновляет таймер.
        Блокирует возможность к сверхбыстрому перерисовыванию (например через зажатые клавиши),
        чтобы предотвратить визуальные баги.
        """
        if self.can_be_redrawed:
            if getattr(self, "_after_id", None):
                self.main_root.after_cancel(self._after_id)
            self._after_id = self.main_root.after(self.draw_delay_ms, self.draw_profile)

    @abstractmethod
    def draw_profile(self):
        raise NotImplementedError()
    @abstractmethod
    def set_selected_warp(self, warp_view):
        raise NotImplementedError()
    @abstractmethod
    def get_canvas(self)->Canvas:
        raise NotImplementedError()
    @abstractmethod
    def set_warp(self, column, row):
        raise NotImplementedError()
    @abstractmethod
    def get_warp(self, warp_index:int):
        raise NotImplementedError()
    @abstractmethod
    def set_weft(self, column, row):
        raise NotImplementedError()
    @abstractmethod
    def get_weft(self, column, row):
        raise NotImplementedError()    

class RainbowColorsGen:
    """Генератор возвращающий цвета ррадуги по очереди"""
    def __init__(self):
        self.colors_generator = self.__color_generator()
        self.rainbow_colors: list = [
                "#ffadad",  "#ffd6a5",  "#fdffb6",  "#caffbf",  
                "#9bf6ff",  "#a0c4ff",  "#bdb2ff",  "#ffc6ff"
                ]

    def next_color(self):
        """Возвращает слкдующий цвет радуги"""
        return next(self.colors_generator)

    def __color_generator(self)->Generator[str]:
        while True:
            yield from self.rainbow_colors

    def __next__(self):
        """Возвращает слкдующий цвет радуги"""
        return self.colors_generator.__next__()
