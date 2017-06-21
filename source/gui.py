from tkinter import *
from source.editingTools import *

# Global constants

WIDTH = 800
HEIGHT = 500


class Gui(object):
    """
    This class of methods is a graphic user interface for wave propagation
    algorithm.
    """
    def __init__(self):
        # Initial state
        self.master = Tk()
        self.master.title("Wave propagation")

        # Main widgets
        self.left_frame = False
        self.right_frame = False
        self.starting_frame = False
        self.editing_tools = False
        self.canvas = False

        # Entry widgets
        self.horizontals_entry = False
        self.verticals_entry = False
        self.initial_length_entry = False

        # Initial state
        self.add_left_frame()
        self.add_right_frame()
        self.add_starting_frame()
        self.master.resizable(0,0)
        self.master.iconbitmap('py.ico')
        self.master.mainloop()

    def add_left_frame(self):
        """
        This method creates 'left frame', container of 'starting frame' and
        'tools frame'.
        """
        self.left_frame = Frame()
        self.left_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

    def add_right_frame(self):
        """
        This method creates 'right frame', container of drawing canvas.
        """
        self.right_frame = Frame()
        self.right_frame.grid(row=0, column=1, sticky="n")

    def add_starting_frame(self):
        """
        This method creates 'starting frame' for constructing initial network
        grid.
        """
        self.starting_frame = LabelFrame(self.left_frame,
                                         text="Create new network",
                                         bd=2,
                                         relief="ridge",
                                         padx=10,
                                         pady=10
                                         )
        self.starting_frame.pack(fill=BOTH, expand=1)

        horizontals_label = Label(self.starting_frame,
                                  text="Horizontal streets:")
        horizontals_label.grid(row=0, column=0)

        self.horizontals_entry = Entry(self.starting_frame, width=5)
        self.horizontals_entry.grid(row=0, column=1)

        verticals_label = Label(self.starting_frame,
                                text="Vertical streets:")
        verticals_label.grid(row=1, column=0)

        self.verticals_entry = Entry(self.starting_frame, width=5)
        self.verticals_entry.grid(row=1, column=1)

        initial_length_label = Label(self.starting_frame,
                                     text="Street lengths (defaults to {0}):".format(DEFAULT_LENGTH)
                                     )
        initial_length_label.grid(row=2, column=0)
        self.initial_length_entry = Entry(self.starting_frame, width=5)
        self.initial_length_entry.grid(row=2, column=1)
        draw_button = Button(self.starting_frame,
                            text="Draw network",
                            command=self.draw_click)
        draw_button.grid()

    def draw_click(self):
        """
        This method is executed when draw button is clicked.
        """
        horizontals = int(self.horizontals_entry.get())
        verticals = int(self.verticals_entry.get())
        initial_length = self.initial_length_entry.get()
        if initial_length == '':
            initial_length = DEFAULT_LENGTH
        initial_length = int(initial_length)

        if self.canvas and self.tools_frame:
            self.canvas.destroy()
            self.tools_frame.destroy()
        self.canvas = Canvas(self.right_frame, width=WIDTH, height=HEIGHT, bg="AntiqueWhite1")
        self.canvas.pack()
        self.tools_frame = LabelFrame(self.left_frame,
                                      text="Editing tools",
                                      bd=2,
                                      relief="ridge",
                                      padx=10,
                                      pady=10
                                      )
        self.tools_frame.pack(fill=BOTH, expand=1)
        editing_tools = MovingTools(self.canvas, self.tools_frame, horizontals, verticals, initial_length)