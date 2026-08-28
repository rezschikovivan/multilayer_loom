from loom_logger import get_logger
from src.loom.controller import Command
from src.loom.model.front import FabricProfile, Side

# Команы Сетки утков

class WeftGridSizeCommand(Command):
    """Базовый класс для управления сеткой утков"""
    def __init__(self, profile:FabricProfile, side:Side, repeat:int=1):
        super().__init__(profile.grid, side)
        self.profile = profile
        self.side = side
        self.repeat = repeat


class IncreaseWeftsCommand(WeftGridSizeCommand):
    """Команда для приращения размеров сетки утков"""
    def action(self):
        self.profile.increase(self.side, self.repeat)

    def is_changes(self):
        return True
    
class ReduceWeftsCommand(WeftGridSizeCommand):
    """Командада для сокращения сетки утков"""
    def action(self):
        self.profile.reduce(self.side, self.repeat)

    def is_changes(self):
        return self.profile.grid.can_be_reduced(self.side, self.repeat)

# Команды основы

class SetWarpAnchorCommand(Command):
    """Команда устновки якоря основы"""
    def __init__(self, profile:FabricProfile, warp_index:int, column:int, target_row:int):
        if column > profile.grid_width:
            raise ValueError(f"Длинна колонок основы меньше переданной колонки: {column}, длинна основы: {profile.grid_width}")
        if target_row > profile.lines_count:
            get_logger("SetWarpAnchorCommand").warning(
                f"Попытка установить основу на высоте {target_row} завершилась установкой на самую вернею строку, "+
                f"т.к. превышает количество строк: {target_row} > {profile.lines_count}"
                   )
        warp = profile.get_warp(warp_index)
        super().__init__(profile.lines)
        self.profile = profile
        self.warp_index = warp_index
        self.column = column
        self.target_row = target_row
        _, self.curret_row = warp.get_point(warp_index, column)

    def is_changes(self):
        return not (self.curret_row == self.target_row)

    def action(self):
        self.profile.set_anchor(self.warp_index, self.column, self.target_row)

# Команды утка

class ToggleWeftCommand(Command):
    """Класс устаноки состояния утка"""
    def __init__(self, profile:FabricProfile, column, row):
        super().__init__(profile.grid, "right")# т.к. размеры не меняються можно указать любую сторону
        self.profile = profile
        self.column = column
        self.row = row
        self.curr_weft_condition = self.profile.grid.get_weft(self.column, self.row).is_active

    def is_changes(self):
        return True

    def action(self):
        if self.curr_weft_condition is False:
            self.profile.grid.set_active(self.column, self.row)
        else:
            self.profile.grid.set_inactive(self.column, self.row)
