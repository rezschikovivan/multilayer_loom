from abc import ABC, abstractmethod
from enum import Enum

Side = Enum("Sides", ("Right","Left", "Top", "Bottom"))


class Observer(ABC):
    @abstractmethod
    def notify(sekf, grid:"WeftsGrid"):
        pass

class Subject:
    def __init__(self):
        self.observers: list[Observer] = []
    def register_observer(self, o: Observer):
        self.observers.append(o)
    def remove_observer(self, o: Observer):
        self.observers.remove(o)
    def notify_observers(self, grid:"WeftsGrid"):
        for o in self.observers:
            o.notify(grid)

class Weft:
    """Утóк. Синглтон класс приспособленец, поддерживает два состояния утка: активное и неактивное"""
    _active_instace = None
    _disactive_instance = None
    def __new__(cls, is_active_arg:bool):
        if is_active_arg:
            if cls._active_instace is None: 
                cls._active_instace = super().__new__(cls)
            return cls._active_instace
        else: 
            if cls._disactive_instance is None: 
                cls._disactive_instance = super().__new__(cls)
            return cls._disactive_instance
    def __init__(self, is_active:bool):
        self.is_active = is_active
    def __str__(self)->str:
        return f"Weft <{self.is_active}> {id(self)}"
    def __repr__(self)->str:
        return self.__str__()

class WeftsGrid(Subject):
    """Grid to manage wefts matrix. Columns - X; Rows - Y"""
    def __init__(self, columns:int=2, rows:int=2):        
        self.wefts:list[list[Weft]] = []
        for _ in range(columns):
            self.wefts.append([Weft(True) for _ in range(rows)])
        
        super().__init__()
    def __str__(self)->str:
        stroke = f""
        #header
        for i in range(self.row_width):
            stroke += f"    [ {self.wefts[i][0]}   "
        #body
        for _ in range(1,self.column_height-1):
            stroke += "\n"
            for _ in range(self.row_width):
                stroke += f"      {self.wefts[i][0]}   "
        stroke += "\n"
        #down
        for i in range(self.row_width):
            stroke += f"      {self.wefts[i][0]} ],"
        
        return "[\n" + stroke[:len(stroke)-1] + "\n]"
    
    def __repr__(self):
        return self.__str__()

    @property
    def column_height(self)->int:
        return self.wefts[0].__len__()
    @property
    def row_width(self)->int:
        return self.wefts.__len__()
    
    def set_active(self, row_index:int, column_index:int):
        self.wefts[row_index][column_index] = Weft(True)
    def set_inactive(self, row_index:int, column_index:int):
        self.wefts[row_index][column_index] = Weft(False)

    def increase(self, side:"Side"):
        if side in (Side.Left, Side.Right):
            self.increase_column(side)
        elif side in (Side.Top, Side.Bottom):
            self.increase_row(side)

    def reduce(self, side:"Side"):
        if side in (Side.Left, Side.Right) and self.row_width > 1:
            self.reduce_column(side)
        elif side in (Side.Top, Side.Bottom) and self.column_height > 1:
            self.reduce_row(side)
        
    def increase_column(self, side:"Side"):
        """Add new wefts column at side"""
        if side not in (Side.Left, Side.Right): raise AttributeError("Cannot add column on 'Bottom' or 'Top'")
        new_column = [Weft(True) for _ in range(self.column_height)] 
        if side == Side.Right:
            self.wefts.append(new_column)
        elif side == Side.Left:
            self.wefts.insert(0, new_column)
        self.notify_observers(self)

    def reduce_column(self, side:"Side"):
        """Remove the wefts column at side"""
        if side not in (Side.Left, Side.Right): raise AttributeError("Cannot add column on 'Bottom' or 'Top'")
        if side == Side.Right:
            self.wefts.pop()
        elif side == Side.Left:
            self.wefts.pop(0)
        self.notify_observers(self)

    def increase_row(self, side:"Side"):
        """Add new wefts row at side"""
        if side not in (Side.Top, Side.Bottom): raise AttributeError("Cannot add row on 'Left' or 'Right'") 
        if side == Side.Top:
            for column in self.wefts:
                column.insert(0, Weft(True))
        elif side == Side.Bottom:
            for column in self.wefts:
                column.append(Weft(True))
        self.notify_observers(self)

    def reduce_row(self, side:"Side"):
        """Remove the wefts row at side"""
        if side not in (Side.Top, Side.Bottom): raise AttributeError("Cannot add row on 'Left' or 'Right'") 
        if side == Side.Top:
            for column in self.wefts:
                column.pop(0)
        elif side == Side.Bottom:
            for column in self.wefts:
                column.pop()
        self.notify_observers(self)
