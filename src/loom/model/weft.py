from copy import deepcopy

from src.loom.controller.memo import IOriginator, Memento
from src.loom.model.model_bases import InstanceFactory, Side, Textile, TextileContainer, TextileType, WeftGridSubject, notifying


class Weft(Textile):
    """
    Утóк. Класс приспособленец, поддерживает два состояния утка: активное и неактивное.
    Экземпляры получать через фабрику, для конроля количества экземпляров.
    """
    def __init__(self, is_active:bool, textile_type:"TextileType"):
        self.is_active = is_active
        super().__init__(textile_type)
    def __str__(self)->str:
        """Возвращает строковое предстваление одной длинны для любого состоянния"""
        if self.is_active:
            return f"Weft<{self.is_active}> {id(self)}"
        else:
            return f"Weft<{self.is_active}>{id(self)}"
    
    def __repr__(self)->str:
        return self.__str__()


class WeftsGrid(TextileContainer, WeftGridSubject, IOriginator):
    """
    Составной объект описывабщий сетку утков.
    Реализует интерфейс для управления сеткой.
    Для получения экземпляров утка используеться
    фабрика. По умолчанию сетку 2х2 (по умолчанию минимально возможный размер).
    """
    def __init__(self, textile_type:TextileType, columns:int=2, rows:int=2, min_size:int=2):
        if columns <= 0 or rows <= 0: 
            raise AttributeError("Невозможно создать сетку с такимим размерами!")
        self._wefts:list[list[Weft]] = []
        self._weft_factory = InstanceFactory(Weft)
        self.minsize = min_size
        TextileContainer.__init__(self, textile_type)
        WeftGridSubject.__init__(self)
        for _ in range(columns): # задает начальную сетку
             self._wefts.append([self._weft_factory.get_instance(True, self._textile_type) for _ in range(rows)])

    def __str__(self)->str:
        stroke = ""
        #header
        for i in range(self.row_width):
            stroke += f"    [ {self.get_weft(i, self.column_height-1)},   "
        #body
        for i in range(self.column_height-1, 1, -1):
            stroke += "\n"
            for j in range(self.row_width):
                stroke += f"      {self.get_weft(j, i)},   "
        stroke += "\n"
        #down
        for i in range(self.row_width):
            stroke += f"      {self.get_weft(i,0)} ] ,"
        return "[\n" + stroke[:len(stroke)-1] + "\n]"
    
    def __repr__(self):
        return f"WeftsGrid<{self.row_width}x{self.column_height}> {id(self)}"

    @property
    def column_height(self)->int:
        return self._wefts[0].__len__()
    @property
    def row_width(self)->int:
        return self._wefts.__len__()

    def get_wefts_list(self)->list:
        return self._wefts

    def set_wefts_list(self, new_wefts:list, side:Side):
        if new_wefts != self._wefts:
            self._wefts = new_wefts
            self.notify_observers(self, Side(side))
    
    def _set_textile_type(self, new_textile):
        if self.textile_type is not new_textile:
            self._textile_type = new_textile
            for i in self._wefts:
                for w in i:
                    w._textile_type = self.textile_type
    
    def set_active(self, column_index:int, row_index:int):
        self._set_weft(column_index, row_index,self._weft_factory.get_instance(True, self._textile_type))

    def set_inactive(self, column_index:int, row_index:int):
        self._set_weft(column_index, row_index,self._weft_factory.get_instance(False, self._textile_type))

    def get_weft(self, column_index:int, row_index:int):
        return self._wefts[column_index][-(row_index+1)]

    def _set_weft(self, column_index:int, row_index:int, weft:Weft):
        self._wefts[column_index][-(row_index+1)] = weft
    @notifying
    def increase(self, side:Side|str, repeat:int=1):
        side = Side(side)
        if side in (Side.left, Side.right):
            self.__increment_column(side, repeat)
        elif side in (Side.top, Side.bottom):
            self.__increment_row(side, repeat)
        return side
    @notifying
    def reduce(self, side:Side|str, repeat:int=1):
        side = Side(side)
        if not self.can_be_reduced(side, repeat):
            raise ValueError(
                f"Нельзя уменьшить размеры сетки утков меньше минимального: {self.minsize} по любой из сторон. "+
                  f"Текущее состояние: {self.__repr__()}, попытка уменьшить на {repeat} со стороны {side}")
        if side in (Side.left, Side.right):
            self.__decrement_column(side, repeat)
        elif side in (Side.top, Side.bottom):
            self.__decrement_row(side, repeat)
        return side

    def can_be_reduced(self, side:Side|str, repeat:int = 1)->bool:
        side = Side(side)
        if side in (Side.bottom, Side.top) and self.column_height - repeat < self.minsize:
            return False
        elif side in (Side.right, Side.left) and self.row_width - repeat < self.minsize:
            return False
        return True

    def __increment_column(self, side:"Side", repeat:int ):
        """Добавляет новую колонку утков по указанной стороне"""
        if side not in (Side.left, Side.right): 
            raise AttributeError("Cannot add column on 'bottom' or 'top'")
        for _ in range(repeat):
            new_column = [self._weft_factory.get_instance(True, self._textile_type) for _ in range(self.column_height)] 
            if side == Side.right:
                self._wefts.append(new_column)
            elif side == Side.left:
                self._wefts.insert(0, new_column)

    def __decrement_column(self, side:"Side", repeat:int):
        """Убирает новую колонку утков по указанной стороне"""
        if side not in (Side.left, Side.right):
            raise AttributeError("Cannot add column on 'bottom' or 'top'")
        for _ in range(repeat):
            if side == Side.right:
                self._wefts.pop()
            elif side == Side.left:
                self._wefts.pop(0)

    def __increment_row(self, side:"Side", repeat:int):
        """Добавляет строчку утков по указанной стороне"""
        if side not in (Side.top, Side.bottom): 
            raise AttributeError("Cannot add row on 'left' or 'right'") 
        for _ in range(repeat):
            if side == Side.top:
                for column in self._wefts:
                    column.insert(0, self._weft_factory.get_instance(True, self._textile_type))
            elif side == Side.bottom:
                for column in self._wefts:
                    column.append(self._weft_factory.get_instance(True, self._textile_type))

    def __decrement_row(self, side:"Side", repeat:int):
        """Убирает строчку утков по указанной стороне"""
        if side not in (Side.top, Side.bottom): 
            raise AttributeError("Cannot add row on 'left' or 'right'") 
        for _ in range(repeat):
            if side == Side.top:
                for column in self._wefts:
                    column.pop(0)
            elif side == Side.bottom:
                for column in self._wefts:
                    column.pop()
    @notifying
    def set_memento(self, memento: Memento):
        self._wefts, side = memento.get_state(self)
        return side

    def create_memento(self, side:Side)->Memento:
        return Memento(self, [deepcopy(self._wefts), Side(side)])

