from tkinter import IntVar
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def notify(sekf, grid:WeftsGrid):
        pass

class Subject:
    def __init__(self):
        self.observers: list[Observer] = []
    def register_observer(self, o: Observer):
        self.observers.append(o)
    def remove_observer(self, o: Observer):
        self.observers.remove(o)
    def notify_observers(self, grid:WeftsGrid):
        for o in self.observers:
            o.notify(grid)

class Weft:
    """Утóк"""
    def __init__(self, is_active:bool):
        self.is_active = is_active
        
class WeftsGrid(Subject):
    def __init__(self, rows:int=2, columns:int=2):
        self.wefts = [[Weft(True) for _ in range(columns)]]*rows
        super().__init__()
    @property
    def columns_lenght(self)->int:
        return self.wefts[0].__len__()
    
    def set_active(self, row:int, column:int):...
    def set_inactive(self, row:int, column:int):...

    def increment_column(self):
        self.wefts.append([Weft(True)*self.columns_lenght]) 
        self.notify_observers(self)
    def decrement_column(self):
        if self.columns_lenght > 1:
            for row in self.wefts:
                
            self.wefts.pop()
            self.notify_observers(self)
    def increment_row(self):
        self.rows += 1
        self.notify_observers(self)
    def decrement_row(self):
        if self.rows > 1:
            self.rows -= 1
            self.notify_observers(self)



class Warp():
    """Основа"""
    def __init__(self, stroke_number:int):
        self.stroke_number: int = stroke_number
        self.anchor_points = []
    def set_anchor(self, point):
        ...


class Reed():
    """Бедро, столбец утков (weft), составной элемент"""
    def __init__(self, grid:WeftsGrid):
        grid.register_observer(self)

    def notify(sekf, grid:WeftsGrid): ...

    def __init__(self, height:int):
        self._wefts = []
        self._click_areas = []
        for _ in range(height):
            self.add_weft(Weft())

    def add_weft(self):
        self._wefts.append(Weft())
        
    def remove_weft(self, weft:Weft=None):
        if weft is None: self._wefts.pop()
        else: self._wefts.remove(weft)

# class FabricGrid():
#     """Корневой составной обьект двумерного представления ткани"""
#     def __init__(self, height:int=2, width:int=2):
#         self.reeds = []
#         self.create_grid(height, width)

#     def create_grid(self, height, width):
#         for _ in range(width):
#             self.add(Reed(height))

#     def add(self, reed:Reed):
#         self.reeds.append(reed)
#     def remove(self, reed:Reed):
#         self.reeds.remove(reed)

a = WeftsGrid()

print(1)