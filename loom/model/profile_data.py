from tkinter import IntVar
from abc import ABC, abstractmethod

class ClickArea:
    def __init__(self):
        ...

class TextileElement(ABC):
    """Интерфейс для любого элемента ткани: составного и индивидуального"""
    def __init__(self):
        super().__init__()

class Weft(TextileElement):
    """Утóк"""
    def __init__(self, is_active=True):
        self.is_active = is_active

class Warp(TextileElement):
    """Основа"""
    def __init__(self, stoke_number:int):
        self.anchor_points = []
        self.stoke_number: int = stoke_number
    def set_anchor(self, point:ClickArea):
        ...
    
class CompositeTextileElement(TextileElement):
    @abstractmethod
    def __init__(self): super().__init__()
    @abstractmethod
    def add_element(self, element: "TextileElement"): pass
    @abstractmethod
    def remove_element(self, element:"TextileElement"): pass

class Reed(CompositeTextileElement):
    """Бедро, столбец утков (weft), составной элемент"""
    def __init__(self):
        self.wefts = []
    def add_element(self, weft:Weft):
        self.wefts.append(weft)
    def remove_element(self, weft:Weft):
        self.wefts.remove(weft)

class FabricGrid(CompositeTextileElement):
    """Корневой составной обьект двумерного представления ткани"""
    def __init__(self):
        self.reeds = []
    def add_element(self, reed:Reed):
        self.reeds.append(reed)
    def remove_element(self, reed:Reed):
        self.reeds.remove(reed)

