from numbers import Number
from typing import TypeVar

from loom.model.base import Observer, Side, Textile, TextileContainer, TextileType
from loom.model.weft import WeftsGrid

x = TypeVar("x",bound=Number)
y = TypeVar("y",bound=Number)

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
        return f"Warp {id(self)} <{self.__str__()}>"

    def get_points(self, warp_index:int = 0)->list[list[x,y]]:
        """При warp_index = 0 вернет список эквивалентный списку относительных точек (anchor_points)"""
        points = []
        for i in range(len(self.anchor_points)):
            points.append([i, warp_index + self.anchor_points[i]])
        return points
    @property
    def length(self):
        return len(self.anchor_points)

    def update(self, line_index:int,  wefts_grid:WeftsGrid, side:Side):
        """
        Обновляет основу на соответствие переданным данным. В зависимости от переданной стороны
        добавит или уберет с неё длинну. Относитеьлно index будет рассчитывать выход точек за
        рамки сетки wefts_grid.
        """
        self.update_anchors(line_index, wefts_grid.column_height)
        lines_length = wefts_grid.row_width
        if self.length < lines_length:
            self._add_length(lines_length, side)
        if self.length > lines_length:
            self._remove_length(lines_length, side)

    def update_anchors(self, warp_index:int, wefts_height:int):
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
            elif anchor_pos > wefts_height:# если якорь ухдит за рамку сверху
                # относительная координата для самой верхней строчки
                # вычесляется: максимальный индекс строки - базовый индекс основы  
                self.anchor_points[i] = wefts_height - warp_index
        
    def set_anchor(self, line_index:int, column:x, row:y):
        """
        Устанавливает основу по переданным координатам. 
        Сохраняет относительную координату от индекса линии до точки.
        """
        if column > self.length-1: 
            raise ValueError("Невозможно установить позицию для основы на" \
                             f"длинне {column}, т.к. она превышает длинну основы!" \
                             "Обновите основу (update) и попробуйте снова")
        if column < 0 or row < 0:
            raise ValueError("В качестве аргументов column:x, row:y следует указывать позитивные" \
            "числа т.к. они соответствуют координатам точек привязки (начиная от 0).")
        self.anchor_points[column] = row - line_index

    def _add_length(self, target_value:int, side:Side):
        "Путем добавления приводит длинну к указанному значению"
        if target_value <= self.length:
            raise ValueError(f"Нельзя методом добавляения уменьшить длинну. \
                             Целевое значение меньше текущего! {target_value} < {self.length}")
        for _ in range(target_value - self.length):
            if side == Side.left:
                self.anchor_points.insert(0, 0)
            elif  side == Side.right:
                self.anchor_points.append(0)

    def _remove_length(self, target_value:int, side:Side):
        "Путем удаления приводит длинну к переданному значению"
        if target_value >= self.length and target_value > 0:
            raise ValueError(f"Нельзя методом уменьшения добавить длинну. \
                             Целевое значение больше текущего! {target_value} > {self.length}")
        index = -1 if side == Side.right else 0
        for _ in range(self.length - target_value):
            self.anchor_points.pop(index)

class WarpsLines(TextileContainer, Observer):
    """
    Составной объект основ. Представляет сосбой множество основ,
    которые содержат относительные данные о своей форме. Количество
    основы на 1 больше чем высота утков.
    """
    def __init__(self, textile_type:TextileType, wefts_grid:WeftsGrid):
        super().__init__(textile_type)
        self.warps:list[Warp] = []
        wefts_grid.register_observer(self)
        for _ in range(wefts_grid.column_height+1):
            self.warps.append(Warp(self._textile_type, wefts_grid.row_width))

    def notify(self, grid:WeftsGrid, side:Side):
        """Получает уведомления при изменении сетки утков."""
        self.update_warps(grid, side)

    def update_warps(self, grid:WeftsGrid, side:Side):
        """Обновляет все хранимые основы и гарантирует, что обновлены будут все экземпляры"""
        wefts_add_one = grid.column_height+1
        if wefts_add_one > self.lines_count:#   высота увеличелась 
            self.increase(side, wefts_add_one-self.lines_count)  
        elif wefts_add_one < self.lines_count:# высота уменьшилась
            self.reduce(side, self.lines_count-wefts_add_one)

        for i in range(len(self.warps)):# обновляет все основы
            self.warps[i].update(i, grid, side)
    
    def get_warp(self, line_index):
        return self.warps[line_index]
    
    def _set_textile_type(self, new_textile):
        for w in self.warps:
            w._textile_type = new_textile

    @property
    def lines_count(self):
        return len(self.warps)
    @property
    def warps_length(self):
        return len(self.warps[0].anchor_points)

    def increase(self, side, repeats=1):
        for _ in range(repeats):
            if side == Side.top:
                self.warps.append(Warp(self._textile_type, self.warps_length))
            elif side == Side.bottom:
                self.warps.insert(0, Warp(self._textile_type, self.warps_length))
            else:
                raise ValueError(f"Невозможно добавить основы со стороны {side}, допустимы только: top, bottom!")

    def reduce(self, side, repeats=1):
        if side not in (Side.top, Side.bottom):
            raise ValueError(f"Невозможно добавить основы со стороны {side}, допустимы только: top, bottom!")
        if self.lines_count <= 1:
            return
        index = -1 if side == Side.top else 0
        for _ in range(repeats):
            self.warps.pop(index)

    def set_warp_anchor(self, line_index:int, column:x, target_line:y):
        warp = self.warps[line_index]
        warp.set_anchor(line_index, column, target_line)
        warp.update_anchors(line_index, self.lines_count-1)

