import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import random

from source.components.menu import Menu
from source.components.canvas import Canvas
from source.components.tools import *

# Window parameters
WIDTH = 1000
HEIGHT = 600
SCALE = 1.5

# Adobe flat UI colour scheme
DARK_BLUE = "#2C3E50"
MEDIUM_BLUE = "#2980B9"
LIGHT_BLUE = "#3498DB"
RED = "#E74C3C"
WHITE = "#ECF0F1"

# Colour parameters
CANVAS_BACKGROUND = WHITE

# Dimensions
FRAME_OPTIONS = {"padx":10}

class View(tk.Tk):
    """This class implements the "view" part of the MVC architectural pattern."""

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.title("Probabilistic ray model of energy propagation")

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.canvas = Canvas(self, height=100, width=WIDTH, bg=CANVAS_BACKGROUND)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.toolbar = CreationTools(self, **FRAME_OPTIONS)
        self.toolbar.pack(fill=tk.BOTH, expand=tk.NO)

        self.minsize(width=WIDTH, height=HEIGHT)

        self.controller = None

    def register(self, controller):
        """
        This method registers the controller to send requests to.
        """
        self.controller = controller

    def switch_tools(self, tools):
        """
        This method switches toolbar to requested tools.
        """
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

    def refresh_canvas(self, adjacency, positions, modified, selected=False):
        """
        This method refreshes canvas based on the received data.
        """
        self.canvas.refresh_canvas(adjacency, positions, modified, selected)

    def remove_binds(self):
        """
        This method removes all binds from the canvas.
        """
        self.canvas.remove_binds()

    def add_bind(self, tools):
        """
        This method adds requested bind to canvas.
        """
        if tools == "MovingTools":
            self.canvas.add_moving_bind()
        elif tools == "DeletingTools":
            self.canvas.add_deleting_bind()
        elif tools == "CustomisingTools":
            self.canvas.add_selecting_bind()
        else:
            raise ValueError("No such tools.")

    def show_message(self, title, message):
        """
        This method displays the message box with requested title and a message.
        """
        messagebox.showinfo(title, message)

    def save_as(self, extension):
        """
        This method displays the file dialog box to save file and returns the
        file name.
        """
        filename = filedialog.asksaveasfile(mode='w', defaultextension=extension)
        if filename is None:
            return None
        return filename.name

    def open(self):
        """
        This method displays the file dialog box to open file and returns the
        file name.
        """
        filename = filedialog.askopenfilename()
        if filename == '':
            return None
        return filename

    def resize_window(self, option):
        """
        This method sets new minimal size of the window.
        """
        if option == "small":
            self.minsize(width=int(WIDTH/SCALE), height=int(HEIGHT/SCALE))
        elif option == "medium":
            self.minsize(width=int(WIDTH), height=int(HEIGHT))
        elif option == "large":
            self.minsize(width=int(WIDTH*SCALE), height=int(HEIGHT*SCALE))


    def change_background(self):
        """
        This method changes background colour to some random value.
        """
        red = hex(random.randint(150, 255))[2:]
        green = hex(random.randint(150, 255))[2:]
        blue = hex(random.randint(150, 255))[2:]
        self.canvas.configure(bg="#{0}{1}{2}".format(red, green, blue))
