from loom.model.model_bases import InstanceFactory, TextileContainer, TextileType
from loom.model.warp import WarpLines, x, y
from loom.model.weft import WeftsGrid, Side


class FabricProfile(TextileContainer): 
    def __init__(self, textile_type:TextileType):
        self.wefts = WeftsGrid(textile_type)
        self.warps = WarpLines(textile_type, self.wefts)
        self.textile_type_factory = InstanceFactory(TextileType)
        super().__init__(textile_type)
    
    @property
    def grid_height(self):
        return self.wefts.column_height
    @property
    def grid_width(self):
        return self.wefts.row_width
    @property
    def lines_count(self):
        return self.warps.lines_count

    def reduce(self, side:Side, repeat=1):
        self.wefts.reduce(side, repeat)
    
    def increase(self, side:Side, repeat=1):
        self.wefts.increase(side, repeat)
    
    def set_anchor(self, line_index:int, column:x, target_line:y):
        self.warps.set_warp_anchor(line_index, column, target_line)

    def get_warp(self, index:int):
        return self.warps[index]

    def get_weft(self, column:int, row:int):
        return self.wefts.get_weft(column, row)

    def _set_textile_type(self, new_textile):
        self.warps._set_textile_type(new_textile)
        self.wefts._set_textile_type(new_textile)

    def get_grid_size(self)->list[x,y]:
        return [self.wefts.row_width, self.wefts.column_height]
