from loom.view.window import Window
from loom.model.profile_data import Profile
from loom.controller.input_feilds import IntFeild

win = Window()
params = Profile()


from tkinter.ttk import Label
from tkinter import IntVar

he = IntVar()
we = IntVar()

win.add_feild_to_parametrs(IntFeild, "Высота (Y)", he)
win.add_feild_to_parametrs(IntFeild, "Ширина (X)", we)

lbl_H = Label(win.main_frame, textvariable=he)
lbl_H.pack()
lbl_W = Label(win.main_frame, textvariable=we)
lbl_W.pack()

win.run()
