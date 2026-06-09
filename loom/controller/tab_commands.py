from loom.controller.command import Command

class SaveCommand(Command):
    def execute(self, *args, **kwds):
        return super().execute(*args, **kwds)
    def undo(self):
        return super().undo()
