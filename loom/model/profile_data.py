from loom.model.wefts import Weft, WeftsGrid



class Warp():
    """Основа"""
    def __init__(self, stroke_number:int):
        self.stroke_number: int = stroke_number
        self.anchor_points = []
    def set_anchor(self, point):
        ...


class Reed():
    """Бедро, столбец утков (weft), составной элемент"""
    def __init__(self, grid:"WeftsGrid"):
        grid.register_observer(self)

    def notify(sekf, grid:"WeftsGrid"): ...

    def __init__(self, height:int):
        self._wefts = []
        self._click_areas = []
        for _ in range(height):
            self.add_weft(Weft())

    def add_weft(self):
        self._wefts.append(Weft())
        
    def remove_weft(self, weft:"Weft"=None):
        if weft is None: self._wefts.pop()
        else: self._wefts.remove(weft)
