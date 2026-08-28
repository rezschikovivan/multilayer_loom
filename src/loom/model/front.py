from src.loom.model.model_bases import InstanceFactory, Observer, Subject, TextileContainer, TextileType, notifying
from src.loom.model.warp import WarpLines
from src.loom.model.weft import Side, WeftsGrid


class FabricProfile(TextileContainer, Subject, Observer): 
    def __init__(self, textile_type:TextileType):
        TextileContainer.__init__(self, textile_type)
        Subject.__init__(self)
        self.grid = WeftsGrid(textile_type)
        self.lines = WarpLines(textile_type, self.grid)
        self.textile_type_factory = InstanceFactory(TextileType)
        self.lines.register_observer(self)
    
    @property
    def grid_height(self):
        return self.grid.column_height
    @property
    def grid_width(self):
        return self.grid.row_width
    @property
    def lines_count(self):
        return self.lines.lines_count

    def notify(self, subject, *args):
        return self.notify_observers()


    def reduce(self, side:Side, repeat=1):
        self.grid.reduce(side, repeat)

    def increase(self, side:Side, repeat=1):
        self.grid.increase(side, repeat)
    @notifying
    def set_anchor(self, line_index:int, column, target_line):
        self.lines.set_warp_anchor(line_index, column, target_line)

    def get_warp(self, index:int):
        if index <= len(self.lines)-1: 
            return self.lines[index]
        else:
            raise IndexError(f"Невозможно получить основу под индексом {index}, всего существует лишь {len(self.lines)} основ!")

    def get_weft(self, column:int, row:int):
        return self.grid.get_weft(column, row)
    @notifying
    def toggle_weft(self, column_index, row_index):
        weft = self.grid.get_weft(column_index, row_index)
        if weft.is_active:
            self.grid.set_inactive(column_index, row_index)
        else:
            self.grid.set_active(column_index, row_index)

    def _set_textile_type(self, new_textile):
        self.textile_type = new_textile
        self.lines._set_textile_type(self.textile_type)
        self.grid._set_textile_type(self.textile_type)

    def get_grid_size(self)->list[int,int]:
        return [self.grid.row_width, self.grid.column_height]

