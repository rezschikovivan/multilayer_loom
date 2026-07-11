from base import Side, Textile, TextileContainer, TextileType, Observer
from weft import WeftsGrid

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
