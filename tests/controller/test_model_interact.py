from unittest import TestCase

from loom.controller import CommandManager, IncreaseWeftsCommand, ReduceWeftsCommand, SetWarpAnchorCommand, ToggleWeftCommand
from loom.model import FabricProfile


class TestSetWarpAnchorCommand(TestCase):
    def setUp(self):    
        self.profile = FabricProfile(None)        
        self.warp_index = 0
        self.column = 0
        self.cmnd = SetWarpAnchorCommand(self.profile, self.warp_index, self.column, 2)

    def test_input_bad_column(self):
        """Проверка исключения при указаниии невозможной колонки"""
        self.assertRaises(ValueError, SetWarpAnchorCommand, self.profile, 0, 10, 1)

    def test_input_big_target_row(self):
        """Проверка установки максимальной точки основы при указаниии очень большой строчки"""
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 0)
        cmnd = SetWarpAnchorCommand(self.profile, self.warp_index, self.column, 219)
        cmnd.execute()
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 2)

    def test_set_anchor_command_execute(self):
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 0)
        self.cmnd.execute()
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 2)

    def test_undo_and_redo(self):
        self.cmnd.execute()
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 2)
        self.cmnd.undo()
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 0)
        self.cmnd.redo()
        self.assertEqual(self.profile.get_warp(self.warp_index)[self.column], 2)

class TestIncreaseWeftsCommand(TestCase):
    def setUp(self):    
        self.profile = FabricProfile(None)
        self.manager = CommandManager()            

    def test_increase_top(self):
        cmnd = IncreaseWeftsCommand(self.profile, "top")
        self.assertEqual(self.profile.grid_height, 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 3)
        cmnd = IncreaseWeftsCommand(self.profile, "top" , 3)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 6)

    def test_increase_bottom(self):
        cmnd = IncreaseWeftsCommand(self.profile, "bottom" )
        self.assertEqual(self.profile.grid_height, 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 3)
        cmnd = IncreaseWeftsCommand(self.profile, "bottom" , 3)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 6)

    def test_increase_right(self):
        cmnd = IncreaseWeftsCommand(self.profile, "right" )
        self.assertEqual(self.profile.grid_width, 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 3)
        cmnd = IncreaseWeftsCommand(self.profile, "right" , 3)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 6)

    def test_increase_left(self):
        cmnd = IncreaseWeftsCommand(self.profile, "left" )
        self.assertEqual(self.profile.grid_width, 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 3)
        cmnd = IncreaseWeftsCommand(self.profile, "left" , 3)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 6)

class TestReduceWeftsCommand(TestCase):
    def setUp(self):             
        self.profile = FabricProfile(None) # 10x10
        IncreaseWeftsCommand(self.profile, "top" , 8).execute()
        IncreaseWeftsCommand(self.profile, "right" , 8).execute()

    def test_reduce_top(self):
        self.assertEqual(self.profile.grid_height, 10)

        cmnd = ReduceWeftsCommand(self.profile, "top" )
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 9)

        cmnd = ReduceWeftsCommand(self.profile, "top" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 7)

        cmnd = ReduceWeftsCommand(self.profile, "top" , 5)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 2)

        cmnd = ReduceWeftsCommand(self.profile, "top" , 3)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 2)


    def test_reduce_bottom(self):
        self.assertEqual(self.profile.grid_height, 10)

        cmnd = ReduceWeftsCommand(self.profile, "bottom" )
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 9)

        cmnd = ReduceWeftsCommand(self.profile, "bottom" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 7)

        cmnd = ReduceWeftsCommand(self.profile, "bottom" , 5)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 2)

        cmnd = ReduceWeftsCommand(self.profile, "bottom" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_height, 2)

    def test_reduce_right(self):
        self.assertEqual(self.profile.grid_width, 10)

        cmnd = ReduceWeftsCommand(self.profile, "right" )
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 9)

        cmnd = ReduceWeftsCommand(self.profile, "right" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 7)

        cmnd = ReduceWeftsCommand(self.profile, "right" , 5)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 2)

        cmnd = ReduceWeftsCommand(self.profile, "right" , 1)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 2)

    def test_reduce_left(self):
        self.assertEqual(self.profile.grid_width, 10)

        cmnd = ReduceWeftsCommand(self.profile, "left" )
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 9)

        cmnd = ReduceWeftsCommand(self.profile, "left" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 7)

        cmnd = ReduceWeftsCommand(self.profile, "LEFT" , 5)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 2)
        
        cmnd = ReduceWeftsCommand(self.profile, "left" , 2)
        cmnd.execute()
        self.assertEqual(self.profile.grid_width, 2)

class TesrToggleWeftCommand(TestCase):
    def setUp(self):
        self.profile = FabricProfile(None)

    def test_toggle(self):
        self.assertEqual(self.profile.get_weft(0,0).is_active, True)

        cmnd = ToggleWeftCommand(self.profile, 0, 0 )
        cmnd.execute()
        self.assertEqual(self.profile.get_weft(0,0).is_active, False)

        cmnd.execute() # повторный вызов приводит к тому же результату
        self.assertEqual(self.profile.get_weft(0,0).is_active, False)

        cmnd1 = ToggleWeftCommand(self.profile, 0, 0 )
        cmnd1.execute()
        self.assertEqual(self.profile.get_weft(0,0).is_active, True)

    def test_undo_redo_true_input(self):
        self.assertEqual(self.profile.get_weft(0,0).is_active, True)

        cmnd = ToggleWeftCommand(self.profile, 0, 0 )
        cmnd.execute()
        self.assertEqual(self.profile.get_weft(0,0).is_active, False)

        cmnd.undo()
        self.assertEqual(self.profile.get_weft(0,0).is_active, True)

        cmnd.redo()
        self.assertEqual(self.profile.get_weft(0,0).is_active, False)

    def test_undo_redo_false_input(self):
        self.profile.grid.set_inactive(1,1)
        self.assertEqual(self.profile.get_weft(1,1).is_active, False)

        cmnd = ToggleWeftCommand(self.profile, 1, 1 )
        cmnd.execute()
        self.assertEqual(self.profile.get_weft(1,1).is_active, True)

        cmnd.undo()
        self.assertEqual(self.profile.get_weft(1,1).is_active, False)

        cmnd.redo()
        self.assertEqual(self.profile.get_weft(1,1).is_active, True)