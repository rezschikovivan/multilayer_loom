from loom.model.model_bases import InstanceFactory, Side, Subject, Textile, TextileContainer, TextileType
from loom_logger import get_logger
class Weft(Textile):
    """
    Утóк. Класс приспособленец, поддерживает два состояния утка: активное и неактивное.
    Экземпляры получать через фабрику, для конроля количества экземпляров.
    """
    def __init__(self, is_active:bool, textile_type:"TextileType"):
        self.is_active = is_active
        super().__init__(textile_type)
    def __str__(self)->str:
        return f"Weft<{self.is_active}>{id(self)}"
    def __repr__(self)->str:
        return self.__str__()


class WeftsGrid(TextileContainer, Subject):
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
        super().__init__(textile_type)
        for _ in range(columns): # задает начальную сетку
             self._wefts.append([self._weft_factory.get_instance(True, self._textile_type) for _ in range(rows)])

    def __str__(self)->str:
        stroke = ""
        #header
        for i in range(self.row_width):
            stroke += f"    [ {self.get_weft(i,0)}   "
        #body
        for i in range(1,self.column_height-1):
            stroke += "\n"
            for _ in range(self.row_width):
                stroke += f"      {self.get_weft(i,0)}   "
        stroke += "\n"
        #down
        for i in range(self.row_width):
            stroke += f"      {self.get_weft(i,0)} ],"
        return "[\n" + stroke[:len(stroke)-1] + "\n]"
    def __repr__(self):
        return self.__str__()

    @property
    def column_height(self)->int:
        return self._wefts[0].__len__()
    @property
    def row_width(self)->int:
        return self._wefts.__len__()
    @property
    def wefts_list(self):
        return self._wefts
    @wefts_list.setter
    def wefts_list(self, value):
        self._wefts = value
    
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

    def _set_weft(self, column_index:int, row_index:int, value:Weft):
        self._wefts[column_index][-(row_index+1)] = value

    def increase(self, side:"Side", repeat:int=1):
        side = Side(side)
        if side in (Side.left, Side.right):
            self._increment_column(side, repeat)
        elif side in (Side.top, Side.bottom):
            self._increment_row(side, repeat)

    def reduce(self, side:"Side", repeat:int=1):
        side = Side(side)
        if side in (Side.left, Side.right):
            if repeat > self.row_width:
                repeat = self.row_width - self.minsize
                get_logger("WeftsGrid").warning(f"Попытка удалить утки в ноль по горизонтали привела к уменьшению сетки утков до минимально возможной: {self.minsize}x{self.minsize}")
            self._decrement_column(side, repeat)
        elif side in (Side.top, Side.bottom):
            if repeat > self.column_height:
                repeat = self.column_height - self.minsize
                get_logger("WeftsGrid").warning(f"Попытка удалить утки в ноль по горизонтали привела к уменьшению сетки утков до минимально возможной: {self.minsize}x{self.minsize}")
            self._decrement_row(side, repeat)

    def _increment_column(self, side:"Side", repeat:int ):
        """Добавляет новую колонку утков по указанной стороне"""
        if side not in (Side.left, Side.right): 
            raise AttributeError("Cannot add column on 'bottom' or 'top'")
        for _ in range(repeat):
            new_column = [self._weft_factory.get_instance(True, self._textile_type) for _ in range(self.column_height)] 
            if side == Side.right:
                self._wefts.append(new_column)
            elif side == Side.left:
                self._wefts.insert(0, new_column)
        self.notify_observers(self, side)

    def _decrement_column(self, side:"Side", repeat:int):
        """Убирает новую колонку утков по указанной стороне"""
        if side not in (Side.left, Side.right):
            raise AttributeError("Cannot add column on 'bottom' or 'top'")
        for _ in range(repeat):
            if side == Side.right:
                self._wefts.pop()
            elif side == Side.left:
                self._wefts.pop(0)
        self.notify_observers(self, side)

    def _increment_row(self, side:"Side", repeat:int):
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
        self.notify_observers(self, side)

    def _decrement_row(self, side:"Side", repeat:int):
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
        self.notify_observers(self, side)
