from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generic, TypeVar

Side = Enum("Sides", ("right","left", "top", "bottom"))

class Observer(ABC):
    @abstractmethod
    def notify(self, grid:"WeftsGrid", side:Side):
        pass

class Subject:
    def __init__(self):
        self.observers: list[Observer] = []
    def register_observer(self, o: Observer):
        self.observers.append(o)
    def remove_observer(self, o: Observer):
        self.observers.remove(o)
    def notify_observers(self, grid:"WeftsGrid", side:Side):
        for o in self.observers:
            o.notify(grid, side)

class TextileType:
    pass

class Textile(ABC):
    """Базовый класс для всех элементов ткани"""
    def __init__(self, textile_type:"TextileType"):
        self._textile_type:"TextileType" = textile_type
        super().__init__()

class TextileContainer(Textile):
    """
    Интерфейс составных объектов текстиля 
    """
    @abstractmethod
    def increase(self, side:Side, target_value:int=1):
        raise NotImplementedError()
    @abstractmethod
    def reduce(self, side:Side, target_value:int=1):
        raise NotImplementedError()

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

FactoryProduct = TypeVar("FactoryProduct")

class InstanceFactory(Generic[FactoryProduct]):
    """
    Экземпляры фабрики предоставляют единую точку доступа
    для получения экземпляров агрегируемого класса. \n
    Фабрика возвращает одинаковый экземпляр для одинаковых 
    аргументов метода get_instance.\n
    Подобный инструмент позволяет экономить память при
    наличии множества подобных объектов не требующих
    идентичности.
    """
    def __init__(self, class_to_instantiate:FactoryProduct):
        self._instances:list[FactoryProduct] = []
        self._keys: list[list[Any]] = []
        self.cls_to_instantiate = class_to_instantiate
    def get_instance(self, *constructor_args)->FactoryProduct:
        """Возвращает экземпляр соответствующий переданным аргументам"""
        if constructor_args in self._keys:
            return self.__get_inst_by_key(constructor_args)
        try:
            instance = self.cls_to_instantiate(*constructor_args)
        except TypeError:
            raise KeyError(f"Не валидные аргументы: {constructor_args}," + 
                           f"для создания экземпляра класса {self.cls_to_instantiate.__name__}")
        self.__append_inst(constructor_args, instance)
        return instance
    
    def __get_inst_by_key(self, key:list)->FactoryProduct:
        if key in self._keys:
            return self._instances[self._keys.index(key)]
        else: 
            raise KeyError("Не удалось получить экземпляр по этому ключу")
    
    def __append_inst(self, key:list, inst:FactoryProduct):
        self._keys.append(key)
        self._instances.append(inst)

class WeftsGrid(TextileContainer, Subject):
    """
    Составной объект описывабщий сетку утков.
    Реализует интерфейс для управления сеткой.
    Для получения экземпляров утка используеться
    фабрика. По умолчанию создаёт сетку 2х2.
    """
    def __init__(self, textile_type:TextileType, columns:int=2, rows:int=2):
        if columns <= 0 or rows <= 0: 
            raise AttributeError("Невозможно создать сетку с такимим размерами!")
        self._wefts:list[list[Weft]] = []
        self._weft_factory = InstanceFactory(Weft)
        super().__init__(textile_type)
        for _ in range(columns): # задает начальную сетку
            self._wefts.append([self._weft_factory.get_instance(True, self._textile_type) for _ in range(rows)])

    def __str__(self)->str:
        stroke = ""
        #header
        for i in range(self.row_width):
            stroke += f"    [ {self.get_weft(i,0)}   "
        #body
        for _ in range(1,self.column_height-1):
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
    
    def set_active(self, column_index:int, row_index:int):
        self._set_weft(column_index, row_index,self._weft_factory.get_instance(True, self._textile_type))
    def set_inactive(self, row_index:int, column_index:int):
        self._set_weft(column_index, row_index,self._weft_factory.get_instance(False, self._textile_type))

    def get_weft(self, column_index:int, row_index:int):
        return self._wefts[column_index][-(row_index+1)]

    def _set_weft(self, column_index:int, row_index:int, value:Weft):
        self._wefts[column_index][-(row_index+1)] = value

    def increase(self, side:"Side", repeat:int=1):
        if side in (Side.left, Side.right):
            self._increment_column(side, repeat)
        elif side in (Side.top, Side.bottom):
            self._increment_row(side, repeat)

    def reduce(self, side:"Side", repeat:int=1):
        if side in (Side.left, Side.right) and self.row_width > 1:
            self._decrement_column(side, repeat)
        elif side in (Side.top, Side.bottom) and self.column_height > 1:
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

class Warp(Textile):
    """
    Основа. Класс компонент для WarpsLines. 
    Хранит относительную позицию основы.
    """
    def __init__(self, textile_type:TextileType, length:int):
        self.anchor_points = list[int]()
        for _ in range(length):
            self.anchor_points.append(0)
        super().__init__(textile_type)

    def __str__(self)->str:
        return str(self.anchor_points)

    def __repr__(self)->str:
        return f"Warp {id(self)} <{self.__str__()}> "

    def get_points(self, line_index:int = 0)->list:
        points = []
        for i in range(len(self.anchor_points)):
            points.append([i, line_index + self.anchor_points[i]])
        return points
    @property
    def length(self):
        return len(self.anchor_points)

    def update(self, line_index:int,  wefts_grid:WeftsGrid, side:Side):
        "Обновляет основу на соответствие переданным данным"
        if side in (Side.top, Side.bottom):
            self.update_anchors(line_index, wefts_grid.column_height)
        lines_length = wefts_grid.row_width
        if len(self.anchor_points) < lines_length:
            self._add_length(self.lines_length, side)
        if len(self.anchor_points) > lines_length:
            self._remove_length(self.lines_length, side)

    def update_anchors(self, warp_index:int, wefts_count:int):
        """
        Если какие-то якоря выходя за рамки, то устанавливает их на 
        соответствующий предел
        """
        for i in range(len(self.anchor_points)):
            anchor_pos = warp_index + self.anchor_points[i]
            if anchor_pos < 0: # если якорь ухдит за рамку снизу
                # индекс строки показывает расстояние до нуля (самой нижней точки)
                # когда нужно установить основу на самую нижнюю позицию
                # достаточно указать в качестве позиции индекс строки с 
                # отрицательным знаком
                self.anchor_points[i] = -warp_index
            elif anchor_pos > wefts_count:# если якорь ухдит за рамку сверху
                # относительная координата для самой верхней строчки
                # вычесляется: максимальный индекс строки - базовый индекс основы  
                self.anchor_points[i] = self.lines_max_index - warp_index
                
    def set_anchor(self, warp_index:int, column:int, row:int):
        "Устанавливает основу по переданным координатам"
        if column > len(self.anchor_points)-1: 
            raise ValueError("Невозможно установить позицию для основы на" \
                             f"длинне {column}, т.к. она превышает длинну основы!" \
                             "Обновите основу (update) и попробуйте снова")
        self.anchor_points[column] = row - warp_index

    def _add_length(self, value:int, side:Side):
        "Добавляет длинну со стороны"
        index = -1 if side == Side.right else 0
        for _ in range(value - len(self.anchor_points)):
            self.anchor_points.insert(index, 0)

    def _remove_length(self, value:int, side:Side):
        "Убирает длинну со стороны"
        index = -1 if side == Side.right else 0
        for _ in range(len(self.anchor_points) - value):
            self.anchor_points.pop(index)

class WarpsLines(TextileContainer, Observer):
    """
    Составной объект основ. Представляет сосбой множество основ,
    которые содержат относительные данные о своей форме. 
    """
    def __init__(self, textile_type:TextileType, wefts_grid:WeftsGrid):
        super().__init__(textile_type)
        self.warps = list[Warp]()
        for i in range(wefts_grid.column_height+1):
            self.warps.append(Warp(self._textile_type, wefts_grid.row_width))

    def notify(self, grid:WeftsGrid, side:Side):
        if grid.column_height+1 > self.lines_count:#   высота увеличелась 
            self.increase(side, grid.column_height+1)  
        elif grid.column_height+1 < self.lines_count:# высота уменьшилась
            self.reduce(side, grid.column_height+1)
        for i in range(len(self.warps)):# обновляет все основы
            self.warps[i].update(i, grid, side)
    
    def get_warp(self, line_index):
        return self.warps[-(line_index+1)]
    
    @property
    def lines_count(self):
        return len(self.warps)
    @property
    def warps_length(self):
        return len(self.warps[0])

    def increase(self, side, repeats = 1):
        for _ in range(repeats):
            if side == Side.top:
                self.warps.append(Warp(self._textile_type, self.warps_length))
            elif side == Side.bottom:
                self.warps.insert(0, Warp(self._textile_type, self.warps_length))

    def reduce(self, side, repeats = 1):
        if side in (Side.top, Side.bottom):
            index = -1 if side == Side.top else 0
            for _ in range(repeats):
                self.warps.pop(index)

class FabricProfile(TextileContainer): 
    def __init__(self, textile_type:TextileType):
        self.wefts = WeftsGrid(textile_type)
        self.warps = WarpsLines(textile_type, self.wefts.row_width)
        self.fabric_type_factory = InstanceFactory(TextileType)
        super().__init__(textile_type)

    def reduce(self, side, target_value = 1):
        return super().reduce(side, target_value)
    
    def increase(self, side, target_value = 1):
        return super().increase(side, target_value)
