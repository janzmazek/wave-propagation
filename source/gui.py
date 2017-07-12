from tkinter import *
from tkinter import filedialog
import json
from source.editingTools import *

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

        # Main widgets
        self.left_frame = False
        self.right_frame = False
        self.tools_frame = False
        self.canvas = False

        # Entry widgets
        self.horizontals_entry = False
        self.verticals_entry = False
        self.initial_length_entry = False

        # Initial state
        self.add_main_menu()
        self.add_left_frame()
        self.add_right_frame()
        self.add_canvas()
        self.add_tools()
        self.tools = CreationTools(self.tools_frame, self.canvas)

        self.master.resizable(0,0)
        self.master.iconbitmap('py.ico')
        self.master.mainloop()

    def add_main_menu(self):
        """
        This method creates main menu.
        """

        self.menubar = Menu(self.master)

        # Create file menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open",
                                   command=lambda: self.file_click("open")
                                   )
        self.file_menu.add_command(label="Save",
                                   command=lambda: self.file_click("save")
                                   )
        self.file_menu.add_command(label="Export image",
                                   command=lambda: self.file_click("export")
                                   )

        # create Window menu
        window_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window",
                                 menu=window_menu
                                 )
        window_menu.add_command(label="Small",
                                command=lambda: self.window_click("small")
                                )
        window_menu.add_command(label="Medium",
                                command=lambda: self.window_click("medium")
                                )
        window_menu.add_command(label="Big",
                                command=lambda: self.window_click("big")
                                )

        # Create Tools menu
        tools_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools",
                                 menu=tools_menu
                                 )
        tools_menu.add_command(label="Create newtork",
                               command=lambda: self.tools_click("create")
                               )
        tools_menu.add_command(label="Delete street",
                               command=lambda: self.tools_click("delete")
                               )
        tools_menu.add_command(label="Modify network",
                               command=lambda: self.tools_click("modify")
                               )
        tools_menu.add_command(label="Customise streets",
                               command=lambda: self.tools_click("customise")
                               )

        # create Help menu
        help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

        # display the menu
        self.master.config(menu=self.menubar)

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

    def add_canvas(self):
        """
        This method destroys canvas if already instantiated and creates a new
        one.
        """
        if self.canvas:
            self.canvas.destroy()
        self.canvas = Canvas(self.right_frame,
                             width=WIDTH,
                             height=HEIGHT,
                             bg="AntiqueWhite1"
                             )
        self.canvas.pack()

    def add_tools(self):
        """
        This method destroys tools frame if already instantiated and creates a
        new one.
        """
        if self.tools_frame:
            self.tools_frame.destroy()
        self.tools_frame = LabelFrame(self.left_frame,
                                      text="Editing tools",
                                      bd=2,
                                      relief="ridge",
                                      padx=10,
                                      pady=10
                                      )
        self.tools_frame.pack(fill=BOTH, expand=1)

    def file_click(self, file_option):
        """
        This method is executed when one of the "file" menu options is clicked.
        """
        if file_option=="open":
            filename = filedialog.askopenfilename()
            if filename is None:
                return
            with open(filename, "r") as file:
                invalues = json.load(file)
            horizontals = invalues["horizontals"]
            verticals = invalues["verticals"]
            modified_adjacency = invalues["modified_adjacency"]

            self.constructor = Constructor(horizontals, verticals)
            self.constructor.open_network(invalues)
            self.network_canvas = NetworkCanvas(self.canvas, self.constructor)

            self.add_tools()
            if modified_adjacency is None:
                self.tools = ModifyingTools(self.tools_frame,
                                            self.constructor,
                                            self.network_canvas
                                            )
            else:
                self.tools = ModelTools(self.tools_frame,
                                        self.constructor,
                                        self.network_canvas
                                        )

        if not self.canvas or not self.tools_frame:
            return # next options not available in starting window
        if file_option=="save":
            filename = filedialog.asksaveasfile(mode='w',
                                                defaultextension=".json"
                                                )
            if filename is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            self.constructor.save_network(filename.name)
        elif file_option=="export":
            filename = filedialog.asksaveasfile(mode='w',
                                                defaultextension=".html"
                                                )
            if filename is None:
                return
            self.constructor.export_network(filename.name)

    def tools_click(self, tool):
        """
        This method is executed when one of the "tools" menu options is clicked.
        """
        if not self.tools.network_canvas:
            return
        tools_frame = self.tools.tools_frame
        constructor = self.tools.constructor
        network_canvas = self.tools.network_canvas
        self.add_tools()
        if tool=="create":
            self.tools.network_canvas.unmodify_network()
            CreationTools(self.tools_frame, self.canvas, network_canvas)
            self.tools.network_canvas = False
        elif tool=="delete":
            self.tools.network_canvas.unmodify_network()
            DeletingTools(self.tools_frame, constructor, network_canvas)
        elif tool=="modify":
            self.tools.network_canvas.unmodify_network()
            ModifyingTools(self.tools_frame, constructor, network_canvas)
        elif tool=="customise":
            if self.tools.network_canvas.modified is True:
                CustomisingTools(self.tools_frame, constructor, network_canvas)
            else:
                self.tools.network_canvas.unmodify_network()
                ModifyingTools(self.tools_frame, constructor, network_canvas)

    def window_click(self, window):
        """
        This method is executed when one of the "window" menu options is
        clicked.
        """
        if window == "small":
            self.canvas.config(width=WIDTH/1.5//1, height=HEIGHT/1.5//1)
        elif window == "medium":
            self.canvas.config(width=WIDTH, height=HEIGHT)
        elif window == "big":
            self.canvas.config(width=1.5*WIDTH//1, height=1.5*HEIGHT//1)
