import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import random

from source.components.menu import Menu
from source.components.canvas import Canvas
from source.components.tools import *

WIDTH = 1000
HEIGHT = 600
SCALE = 1.5
CANVAS_BACKGROUND = "cadet blue"
FRAME_OPTIONS = {"padx":10}

class View(tk.Tk):
    """docstring for View."""

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.title("Probabilistic Wave Propagation Model")

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.canvas = Canvas(self, height=100, width=WIDTH, bg=CANVAS_BACKGROUND)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.toolbar = CreationTools(self, **FRAME_OPTIONS)
        self.toolbar.pack(fill=tk.BOTH, expand=tk.NO)

        self.minsize(width=WIDTH, height=HEIGHT)

        self.controller = None

    def register(self, controller):
        self.controller = controller

    def switch_tools(self, tools):
        self.toolbar.pack_forget()
        self.toolbar.destroy()
        self.remove_binds()
        if tools == "CreationTools":
            self.toolbar = CreationTools(self, **FRAME_OPTIONS)
        elif tools == "MovingTools":
            self.toolbar = MovingTools(self, **FRAME_OPTIONS)
            self.add_bind(tools)
        elif tools == "DeletingTools":
            self.toolbar = DeletingTools(self, **FRAME_OPTIONS)
            self.add_bind(tools)
        elif tools == "ModifyingTools":
            self.toolbar = ModifyingTools(self, **FRAME_OPTIONS)
        elif tools == "CustomisingTools":
            self.toolbar = CustomisingTools(self, **FRAME_OPTIONS)
            self.add_bind(tools)
        elif tools == "ModelTools":
            self.toolbar = ModelTools(self, **FRAME_OPTIONS)
        else:
            raise ValueError("No such tools.")
        self.toolbar.pack(fill=tk.BOTH, expand=tk.NO)

    def refresh_canvas(self, adjacency, positions, modified, selected=False,
                       numbered=False):
        self.canvas.refresh_canvas(adjacency, positions, modified, selected, numbered)

    def remove_binds(self):
        self.canvas.remove_binds()

    def add_bind(self, tools):
        if tools == "MovingTools":
            self.canvas.add_moving_bind()
        elif tools == "DeletingTools":
            self.canvas.add_deleting_bind()
        elif tools == "CustomisingTools":
            self.canvas.add_selecting_bind()
        else:
            raise ValueError("No such tools.")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def save_as(self, extension):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=extension)
        return filename.name

    def open(self):
        filename = filedialog.askopenfilename()
        return filename

    def resize_window(self, option):
        if option == "small":
            self.minsize(width=int(WIDTH/SCALE), height=int(HEIGHT/SCALE))
        elif option == "medium":
            self.minsize(width=int(WIDTH), height=int(HEIGHT))
        elif option == "large":
            self.minsize(width=int(WIDTH*SCALE), height=int(HEIGHT*SCALE))


    def change_background(self):
        red = hex(random.randint(150, 255))[2:]
        green = hex(random.randint(150, 255))[2:]
        blue = hex(random.randint(150, 255))[2:]
        self.canvas.configure(bg="#{0}{1}{2}".format(red, green, blue))
