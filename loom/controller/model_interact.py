from loom.controller.command import Command, CommandManager, abstractmethod
from loom.model.model import FabricProfile, Side
from loom_logger import get_logger

class WeftGridSizeCommand(Command):
    """Базовый класс для управления сеткой уткоов"""
    def __init__(self, profile:FabricProfile, side:Side, manager:CommandManager, repeat:int=1):
        super().__init__(manager)
        self.profile = profile
        self.side = side
        self.repeat = repeat
    def set_states(self):
        self.last_state = self.profile.wefts._wefts.copy()
        self.grid_action()
        self.new_state = self.profile.wefts._wefts.copy()

    @abstractmethod
    def grid_action(self):
        raise NotImplementedError()

    def undo(self):
        self.profile.wefts.wefts_list = self.last_state

    def redo(self):
        self.profile.wefts.wefts_list = self.new_state

    def is_changes(self):
        return True

class IncreaseWeftsCommand(WeftGridSizeCommand):
    """Команда для приращения размеров сетки утков"""
    def grid_action(self):
        self.profile.increase(self.side, self.repeat)

class ReduceWeftsCommand(WeftGridSizeCommand):
    """Командада для уменьшения сетки утков"""
    def grid_action(self):
        self.profile.reduce(self.side, self.repeat)

class SetWarpAnchorCommand(Command):
    """Команда устновки якоря основы"""
    def __init__(self, profile:FabricProfile, warp_index:int, column:int, target_row:int, manager:CommandManager):
        if column > profile.grid_width:
            raise ValueError(f"Длинна колонок основы меньше переданной колонки: {column}, длинна основы: {profile.grid_width}")
        if target_row > profile.lines_count:
            get_logger("SetWarpAnchorCommand").warning(
                f"Попытка установить основу на высоте {target_row} завершилась установкой на самую вернею строку, "+
                f"т.к. превышает количество строк: {target_row} > {profile.lines_count}"
                   )
        super().__init__(manager)
        self.profile = profile
        self.warp_index = warp_index
        self.column = column
        self.target_row = target_row
        self.curret_anchor:int = self.profile.get_warp(self.warp_index)[self.column]

    def is_changes(self):
        return not (self.curret_anchor == self.target_row)

    def set_states(self):
        self.last_state = self.curret_anchor
        self.profile.set_anchor(self.warp_index, self.column, self.target_row)
        self.new_state = self.profile.get_warp(self.warp_index)[self.column]
        
    def undo(self):
        self.profile.set_anchor(self.warp_index, self.column, self.last_state)

    def redo(self):
        self.profile.set_anchor(self.warp_index, self.column, self.target_row)

class ToggleWeftCommand(Command):
    """Класс устаноки состояния утка"""
    def __init__(self, profile:FabricProfile, column, row, manager):
        super().__init__(manager)
        self.profile = profile
        self.column = column
        self.row = row
        self.curr_weft_condition = self.profile.wefts.get_weft(self.column, self.row).is_active

    def is_changes(self):
        return True

    def set_states(self):
        self.last_state = self.curr_weft_condition
        self.toggle_weft()
        self.new_state = not self.last_state

    def toggle_weft(self):
        if self.last_state is False:
            self.profile.wefts.set_active(self.column, self.row)
        else:
            self.profile.wefts.set_inactive(self.column, self.row)

    def undo(self):
        if self.new_state is False:
            self.profile.wefts.set_active(self.column, self.row)
        else:
            self.profile.wefts.set_inactive(self.column, self.row)

    def redo(self):
        self.toggle_weft()
