from loom.model.wefts import WeftsGrid

class Warp:
    """Основа."""
    def __init__(self, stroke_number:int):
        self.stroke_number: int = stroke_number
        self.anchor_points = []

    def set_anchor(self, row:int, column:int):
        ...

class WarpGrid:
    ...

class FabricProfile:
    def __init__(self):
        self.wefts_grid = WeftsGrid()

    