from loom.model.model_bases import InstanceFactory, Observer, TextileContainer, TextileType
from loom.model.warp import WarpLines
from loom.model.weft import Side, WeftsGrid


class FabricProfile(TextileContainer): 
    def __init__(self, textile_type:TextileType):
        self.grid = WeftsGrid(textile_type)
        self.lines = WarpLines(textile_type, self.grid)
        self.textile_type_factory = InstanceFactory(TextileType)
        super().__init__(textile_type)
    
    @property
    def grid_height(self):
        return self.grid.column_height
    @property
    def grid_width(self):
        return self.grid.row_width
    @property
    def lines_count(self):
        return self.lines.lines_count

    def register_grid_listener(self, listener:Observer):
        self.grid.register_observer(listener)

    def reduce(self, side:Side, repeat=1):
        self.grid.reduce(side, repeat)
    
    def increase(self, side:Side, repeat=1):
        self.grid.increase(side, repeat)
    
    def set_anchor(self, line_index:int, column, target_line):
        self.lines.set_warp_anchor(line_index, column, target_line)

    def get_warp(self, index:int):
        return self.lines[index]

    def get_weft(self, column:int, row:int):
        return self.grid.get_weft(column, row)

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

