from base import TextileContainer, TextileType, InstanceFactory
from weft import WeftsGrid
from warp import WarpsLines

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
