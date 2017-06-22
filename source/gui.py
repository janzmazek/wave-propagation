from tkinter import *
from tkinter import filedialog
import json
from source.editingTools import *
from source.networkCanvas import NetworkCanvas
from source.constructor import Constructor

# Global constants
WIDTH = 600
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
        self.constructor = False

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
        self.add_main_menu()
        self.add_left_frame()
        self.add_right_frame()
        self.add_starting_frame()
        self.master.resizable(0,0)
        self.master.iconbitmap('py.ico')
        self.master.mainloop()

    def add_main_menu(self):
        # create main menu

        self.menubar = Menu(self.master)

        # Create file menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_click)
        self.file_menu.add_command(label="Save", command=self.save_click)

        # create Window menu
        window_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=window_menu)
        window_menu.add_command(label="Small", command=lambda: self.change_window("small"))
        window_menu.add_command(label="Medium", command=lambda: self.change_window("medium"))
        window_menu.add_command(label="Big", command=lambda: self.change_window("big"))

        # Create Tools menu
        tools_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Move streets", command=lambda: self.change_tool("move"))
        tools_menu.add_command(label="Delete streets", command=lambda: self.change_tool("delete"))
        tools_menu.add_command(label="Modify network", command=lambda: self.change_tool("modify"))
        tools_menu.add_command(label="Customise streets", command=lambda: self.change_tool("customise"))

        # create Help menu
        help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.hello)

        # display the menu
        self.master.config(menu=self.menubar)

    def hello(self):
        print("Hello")

    def change_window(self, window):
        if self.canvas and self.tools_frame:
            if window == "small":
                self.canvas.config(width=WIDTH/1.5//1, height=HEIGHT/1.5//1)
            elif window == "medium":
                self.canvas.config(width=WIDTH, height=HEIGHT)
            elif window == "big":
                self.canvas.config(width=1.5*WIDTH//1, height=1.5*HEIGHT//1)


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
        horizontals = int(self.horizontals_entry.get())//1
        verticals = int(self.verticals_entry.get())//1
        initial_length = self.initial_length_entry.get()
        if initial_length == '':
            initial_length = DEFAULT_LENGTH
        initial_length = int(initial_length//1)
        self.add_canvas_and_tools()
        self.constructor = Constructor(horizontals, verticals, initial_length)
        self.network_canvas = NetworkCanvas(self.canvas, self.constructor)
        editing_tools = MovingTools(self.network_canvas, self.tools_frame)

    def open_click(self):
        filename = filedialog.askopenfilename()
        if filename is None:
            return
        with open(filename, "r") as file:
            invalues = json.load(file)
        horizontals = invalues["horizontals"]
        verticals = invalues["verticals"]
        modified_adjacency = invalues["modified_adjacency"]

        self.add_canvas_and_tools()
        self.constructor = Constructor(horizontals, verticals)
        self.constructor.import_network(invalues)
        self.network_canvas = NetworkCanvas(self.canvas, self.constructor)
        if modified_adjacency is None:
            ModifyingTools(self.network_canvas, self.tools_frame)
        else:
            ModelTools(self.network_canvas, self.tools_frame)

    def add_canvas_and_tools(self):
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


    def save_click(self):
        if self.canvas and self.tools_frame:
            filename = filedialog.asksaveasfile(mode='w', defaultextension=".json")
            if filename is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            self.constructor.export_network(filename.name)
        else:
            print("Nothing to save!")

    def change_tool(self, tool):
        self.add_canvas_and_tools()
        if self.constructor:
            if tool=="move":
                pass
            elif tool=="delete":
                pass
            elif tool=="modify":
                pass
            elif tool=="customise":
                pass
