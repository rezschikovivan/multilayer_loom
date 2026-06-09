from loom.view.window import Window
from loom.model.config_params import Configuration
from loom.controller.input_feilds import IntFeild

win = Window()
params = Configuration()


from tkinter.ttk import Label
from tkinter import IntVar

he = IntVar()
we = IntVar()

win.add_feild_to_panel(IntFeild, "Высота (Y)", he)
win.add_feild_to_panel(IntFeild, "Ширина (X)", we)

lbl_H = Label(win.main_frame, textvariable=he)
lbl_H.pack()
lbl_W = Label(win.main_frame, textvariable=we)
lbl_W.pack()

win.run()
