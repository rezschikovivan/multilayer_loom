from tkinter import SOLID, Tk
from tkinter.ttk import Button, Frame, Label

from loom.model.profile_data import Profile
from loom.view.input_fields import EntryField, IntField


class ParametrsPanel:
    """left user input pannel"""

    def __init__(self, root: Tk, profile: Profile, manager):
        self.root = Frame(master=root, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.root.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.manager = manager
        self.profile = profile

        self.Fields: dict[str, EntryField] = {}
        self.add_input_field(IntField, "Height", self.profile.height)
        self.add_input_field(IntField, "Width", self.profile.width)

        lbl_h = Label(self.root, textvariable=self.profile.height)
        lbl_h.pack()
        lbl_w = Label(self.root, textvariable=self.profile.width)
        lbl_w.pack()
        self.add_accept_btn()

    def add_accept_btn(self):
        """Button to accept settings chandes"""
        accept_btn = Button(
            master=self.root, text="Accept"
        )  # input accepting by <FocusOut> from entry event
        accept_btn.pack(side="bottom")

    def add_input_field(self, input_field_class: EntryField, name: str, receiver):
        """Create and place input field on panel"""
        self.Fields[name] = input_field_class(self.root, name, receiver, self.manager)
