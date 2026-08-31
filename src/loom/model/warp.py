from copy import deepcopy
from enum import Enum
from typing import Iterable
from src.loom.controller.memo import IOriginator, Memento
from src.loom.model.model_bases import IObserver, Side, Subject, Textile, TextileContainer, TextileType, notifying
from src.loom.model.weft import WeftsGrid

#-------- Классы исключений -----------
class TrajectoryError(Exception):
    """Ошибка кодирования траектории нити внутри одной колонки"""

class ZerosEntriesError(TrajectoryError):
    def __str__(self):
        return "Количество нулей должно быть нечётным!"

class AlternationError(TrajectoryError):
    def __str__(self):
        return "Нули должны чередоваться с другими кодами!"

class SequenceLenghtError(TrajectoryError):
    def __str__(self):
        return "Длинна последовательности не может быть меньше одного!"

class NotEndsWithNullError(TrajectoryError):
    def __str__(self):
        return "Последовательность должна закакниваться на ноль!"
#--------------------------------------

class Point(tuple):
    def __new__(cls, column:int, row:int):
        return super().__new__((column, row))

class TrajectoryMode(Enum):
    """
    ## Перечисление с 2-мя состояниями: before, after.
    ### "before" - нить сразу поднимается/опускается.
    В таком режиме для построения линии используется нечетное количество высот и чётное количество элементов (с 0-ми).
    При таком режиме нити траектория будет начинаться с значения высоты.
    ### "after"  - нить сначала проходит вперед и поднимаеться/опускается уже за утком.
    В таком режиме для построения линии используется четное количество высот и нечётное количество элементов (с 0-ми).
    При таком режиме нити траектория будет начинаться с нуля.
    """
    before = "before"
    after = "after"

class ColumnTrajectory(list[int]):
    """ 
    ## Класс кодирующий траекторию нити внутри одной колонки.
    ### Кодирование:
    Используется 3 категории чисел: 
    #### 1. Целые положительные > 0
    Означают насколько поднимается нить вверх.
    #### 2. Ноль 0
    Показывает, что нить переходит над/под утком.
    Позволяет кодировать множественные точки в одной колонке. 
    #### 3. Целые отрицетльные < 0
    Означают насколько опускается нить вниз.
    ### Правила кодирования:
    1. Количество нулей должно быть нечётным.
    2. Последовательность должна заканчиваться на ноль.
    3. Нули должны чередоваться с другими кодами.
    4. Длинна последовательности не может быть меньше одного
    """
    def __init__(self):
        super().__init__((0,))

    @staticmethod
    def inspect_trajectory(points: list[int], is_raises=False)->bool|TrajectoryError:
        """
        Возвращает True если эта кодировка правильная.
        Параметр is_raises показывает вернуть false или бросить исключение,
        если указано false будет возвращено булевое значение.
        """
        if len(points) >  0:
            if (len(points) == 1 and points[0] != 0) or (points[-1] != 0):
                if is_raises:
                    raise NotEndsWithNullError()
                else:
                    return False
        else:
            if is_raises:
                raise SequenceLenghtError()
            else:
                return False
            
        null_entries = points.count(0)
        if null_entries % 2 == 0:
            if is_raises:
                raise ZerosEntriesError()
            else:
                return False
        
        last = points[0]
        for next in points[1:]:
            if (last == 0 and next != 0) or (last != 0 and next == 0):
                last = next
            else:
                if is_raises:
                    raise AlternationError()
                else:
                    return False
                
        return True
    @property
    def heights_iterator(self):
        def gen():
            start = 1 if self.mode == TrajectoryMode.after else 0
            yield from [self[i] for i in range(start, len(self), 2)]
        return gen()
    @property
    def mode(self)->TrajectoryMode:
        return TrajectoryMode.after if self[0] == 0 else TrajectoryMode.before
    @property
    def exit_level(self):
        return sum(self)
    @property
    def enter_level(self):
        return self[0]
            
    def get_across_jumper_index(self, line_index:int, row:int)->int:
        """Возвращает первый попавшийся индекс при котором высота пересекает переданную строчку."""
        rel_row = row - line_index
        height = 0
        for i, v in enumerate(self):
            height += v
            if height == rel_row:
                return i+1
            
    def is_across_level(self, line_index:int,  row:int)->bool:
        rel_level = row - line_index
        start = 1 if self.mode == TrajectoryMode.after else 0
        for i in range(start, len(self), 2):
            if self[i] == rel_level:
                return True
        return False

    def reset_tracery(self, value:Iterable):
        self.clear()
        self.extend(value)

    def add_tracery(self, value:Iterable):
        self.pop()
        self.extend(value)

    def add_after(self):
        ...

    def add_before(self):
        ...

    def set_single_anchor(self, line_index:int, target_row:int):
        """Устанавливает основе одну точку и всегда в режиме 'before'"""
        heights = self.__сalculate_heights(line_index, target_row)
        tracery = self.__arrange_jumpers(TrajectoryMode.before, heights)
        self.reset_tracery(tracery)

    def try_add_multiple_anchors(self, line_index:int, *target_points:int)->tuple[bool, str]:
        """Пытаеться добавить новую точку в колонке. Возвращает булевый отчет об успехе операции"""
        mode = TrajectoryMode.after
        is_apply, msg = self.validate_points(mode, *target_points)
        if not is_apply:
            return False, msg
        heights = self.__сalculate_heights(line_index, *target_points)
        tracery = self.__arrange_jumpers(mode, heights)
        is_valid = self.inspect_trajectory(tracery)
        if is_valid:
            self.add_tracery(tracery)
        return is_valid, str(tracery)

    def validate_points(self, mode:TrajectoryMode, *rows:int)->tuple[bool, str]:
        """Проверяем входные данные точек. В итоге нить должна выйти вправо"""
        if len(rows) > 0: 
                jumpres = (len(rows) + (len(self)//2))
                if mode == TrajectoryMode.after and jumpres % 2 != 0:
                    return False, f"При режиме after должно передаваться чётное количество точек! (переданно {len(rows)})"
                if mode == TrajectoryMode.before and jumpres % 2 == 0:
                    return False, f"При режиме before должно передаваться нечётное количество точек! (переданно {len(rows)})"
                return True, "Ошибок нет"
        else:
            return False,  SequenceLenghtError.__str__()

    def __сalculate_heights(self, line_index:int, *rows:int)->list[int]:
        """Рассчитывает высоты. Возвращает список высот, но это не готовый узор, в нём нету 0-ей."""
        heights = list[int]()
        for row in rows:
            anchor = row - line_index
            if len(heights) > 0:
                anchor = anchor - heights[-1]
            heights.append(anchor)
        return heights

    def __arrange_jumpers(self, mode:TrajectoryMode, heights:list[int])->list[int]:
        """Расставляет нули в нужных местах."""
        tracery = []
        for i, x in enumerate(heights):
            if i:
                tracery.append(0)
            tracery.append(x)
        if mode == TrajectoryMode.after:
            tracery.insert(0, 0)
        tracery.append(0)
        return tracery


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

    def __getitem__(self, key)->int:
        return self.anchor_points[key]

    def __iter__(self):
        return iter(self.anchor_points)

    def get_point(self, warp_index:int, column)->list[int,int]:
        return [column, warp_index + self.anchor_points[column]]

    def get_points(self, warp_index:int = 0)->list[list[int,int]]:
        """При warp_index = 0 вернет список эквивалентный списку относительных точек экземпляра (anchor_points)"""
        points = []
        for i in range(len(self.anchor_points)):
            points.append(self.get_point(warp_index, i))
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
        
    def set_anchor(self, line_index:int, column:int, row:int):
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
        if side not in (Side.left, Side.right):
            raise ValueError(f"Невозможно добавить длинну со стороны {side}, допустимы только: left, right!")
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
        if side not in (Side.left, Side.right):
            raise ValueError(f"Невозможно добавить длинну со стороны {side}, допустимы только: left, right!")
        if target_value >= self.length and target_value > 0:
            raise ValueError(f"Нельзя методом уменьшения добавить длинну. \
                             Целевое значение больше текущего! {target_value} > {self.length}")
        index = -1 if side == Side.right else 0
        for _ in range(self.length - target_value):
            self.anchor_points.pop(index)

class WarpLines(TextileContainer, IObserver, IOriginator, Subject):
    """
    Составной объект основ. Представляет собой множество основ,
    которые содержат относительные данные о своей форме. Количество
    основы на 1 больше чем высота утков.
    """
    def __init__(self, textile_type:TextileType, grid:WeftsGrid):
        super(TextileContainer, self).__init__(textile_type)
        super(Subject, self).__init__()
        self._warps:list[Warp] = []
        grid.register_observer(self)
        for _ in range(grid.column_height+1):
            self._warps.append(Warp(self._textile_type, grid.row_width))

    @property
    def lines_count(self):
        return len(self._warps)
    @property
    def length(self):
        return len(self._warps[0].anchor_points)
    @property
    def warps_list(self):
        return self._warps
    @warps_list.setter
    def warps_list(self, value):
        self._warps = value

    def notify(self, grid:WeftsGrid, side:Side):
        """Получает уведомления при изменении сетки утков."""
        self.update_warps(grid, side)

    def __getitem__(self, key)->Warp:
        return self.get_warp(key)

    def __len__(self):
        return len(self._warps)
    @notifying
    def update_warps(self, grid:WeftsGrid, side:Side):
        """Обновляет все хранимые основы и гарантирует, что обновлены будут все экземпляры"""
        wefts_add_one = grid.column_height+1
        if wefts_add_one > self.lines_count:#   высота увеличелась 
            self.increase(side, wefts_add_one-self.lines_count)  
        elif wefts_add_one < self.lines_count:# высота уменьшилась
            self.reduce(side, self.lines_count-wefts_add_one)

        for i in range(len(self._warps)):# обновляет все основы
            self._warps[i].update(i, grid, side)
    
    def get_warp(self, line_index):
        if line_index <= len(self)-1: 
            return self._warps[line_index]
        else:
            raise IndexError(f"Невозможно получить основу под индексом {line_index}, всего существует лишь {len(self)} основ!")
    
    def _set_textile_type(self, new_textile):
        if self.textile_type is not new_textile:
            self._textile_type = new_textile
            for w in self._warps:
                w._textile_type = self.textile_type

    def increase(self, side, repeats=1):
        for _ in range(repeats):
            if side == Side.top:
                self._warps.append(Warp(self._textile_type, self.length))
            elif side == Side.bottom:
                self._warps.insert(0, Warp(self._textile_type, self.length))
            else:
                raise ValueError(f"Невозможно добавить основы со стороны {side}, допустимы только: top, bottom!")

    def reduce(self, side, repeats=1):
        if side not in (Side.top, Side.bottom):
            raise ValueError(f"Невозможно добавить основы со стороны {side}, допустимы только: top, bottom!")
        if self.lines_count <= 1:
            return
        index = -1 if side == Side.top else 0
        for _ in range(repeats):
            self._warps.pop(index)

    def set_warp_anchor(self, line_index:int, column:int, target_line:int):
        warp = self._warps[line_index]
        warp.set_anchor(line_index, column, target_line)
        warp.update_anchors(line_index, self.lines_count-1)

    @notifying
    def set_memento(self, memento:Memento):
        self._warps = memento.get_state(self)

    def create_memento(self):
        return Memento(self, deepcopy(self._warps))
