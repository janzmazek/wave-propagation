from tkinter import *
from source.constructor import Constructor
from source.model import Model

# Global constants
WIDTH = 800
HEIGHT = 500
OFFSET = 10
DEFAULT_LENGTH = 100
DEFAULT_WIDTH = 10
DEFAULT_ALPHA = 0.5

class Gui(object):
    def __init__(self):
        # Set object widgets to None
        self.left_frame = None
        self.canvas = None
        self.tools_frame = None
        self.moving_tools = None
        self.deleting_tools = None

        self.master = Tk()
        self.master.title("Wave propagation")
        self.label_message = Label(self.master,
                                   text="Welcome to wave propagation in urban areas simulator."
                                   )
        self.label_message.grid(row=0, column=0, columnspan=1, sticky="we")

        self.add_left_frame()
        self.add_starting_frame()
        # self.master.resizable(0, 0)
        self.master.mainloop()


    def add_left_frame(self):
        self.left_frame = Frame()
        self.left_frame.grid(row=1, column=0, sticky="n", padx=10, pady=10)

    def add_starting_frame(self):
        self.starting_frame = LabelFrame(self.left_frame,
                                         text="Create new network",
                                         bd=2,
                                         relief="ridge",
                                         padx=10,
                                         pady=10
                                         )
        self.starting_frame.pack(fill=BOTH, expand=1)
        verticals_label = Label(self.starting_frame,
                                text="Enter number of verticals:")
        verticals_label.pack()
        self.verticals_entry = Entry(self.starting_frame)
        self.verticals_entry.pack()
        horizontals_label = Label(self.starting_frame,
                                  text="Enter number of horizontals:")
        horizontals_label.pack()
        self.horizontals_entry = Entry(self.starting_frame)
        self.horizontals_entry.pack()
        initial_length_label = Label(self.starting_frame,
                                     text="Enter initial street length (defaults to {0}):".format(DEFAULT_LENGTH)
                                     )
        initial_length_label.pack()
        self.initial_length_entry = Entry(self.starting_frame)
        self.initial_length_entry.pack()
        draw_button = Button(self.starting_frame,
                             text="Draw network",
                             command=self.draw_click)
        draw_button.pack()


    def add_tools_frame(self):
        self.tools_frame = LabelFrame(self.left_frame,
                                      text="Editing tools",
                                      bd=2,
                                      relief="ridge",
                                      padx=10,
                                      pady=10
                                      )
        self.tools_frame.pack(fill=BOTH, expand=1)

    def draw_click(self):
        """
        This method is executed when draw button is clicked.
        """
        verticals = int(self.verticals_entry.get())
        horizontals = int(self.horizontals_entry.get())
        initial_length = self.initial_length_entry.get()
        if initial_length == '':
            initial_length = DEFAULT_LENGTH
        else:
            initial_length = int(initial_length)
        self.constructor = Constructor(horizontals, verticals, initial_length)

        # ========== Changing stage ==========
        if self.tools_frame is not None:
            self.tools_frame.destroy()
        self.add_tools_frame()
        if self.canvas is not None:
            self.canvas.destroy()
        self.add_canvas()
        self.add_moving_tools()
        self.remove_bind()
        self.add_moving_bind()
        # ========== Changing stage ==========

    def add_moving_tools(self):
        self.moving_tools = Frame(self.tools_frame)
        self.moving_tools.pack()
        moving_message = Label(self.moving_tools,
                               text="Drag and drop to move street."
                               )
        moving_message.pack()
        finished_moving_button = Button(self.moving_tools,
                                        text="Finished moving",
                                        command=self.finished_moving_click
                                        )
        finished_moving_button.pack()

    def remove_bind(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1")

    def add_moving_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_move)
        self.canvas.bind("<ButtonRelease-1>", self.release_to_move)

    def finished_moving_click(self):
        # ========== Changing stage ==========
        self.moving_tools.destroy()
        self.add_deleting_tools()
        self.remove_bind()
        self.add_deleting_bind()
        # ========== Changing stage ==========

    def add_deleting_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_delete)

    def add_deleting_tools(self):
        self.deleting_tools = Frame(self.tools_frame)
        self.deleting_tools.pack()
        deleting_message = Label(self.deleting_tools,
                                 text="Click on street to delete it")
        deleting_message.pack()
        finished_deleting_button = Button(self.deleting_tools,
                                          text="Finished deleting",
                                          command=self.finished_deleting_click
                                          )
        finished_deleting_button.pack()

    def finished_deleting_click(self):
        # ========== Changing stage ==========
        self.deleting_tools.destroy()
        self.add_modifying_tools()
        self.remove_bind()
        print("Just removed all binds. Test me.")
        # ========== Changing stage ==========

    def add_modifying_tools(self):
        self.modifying_tools = Frame(self.tools_frame)
        self.modifying_tools.pack()
        modifying_message = Label(self.modifying_tools,
                                  text="Choose default parameters for streets"
                                  )
        modifying_message.pack()
        width_message = Label(self.modifying_tools,
                              text="Width (defaults to {0}):".format(DEFAULT_WIDTH)
                              )
        width_message.pack()
        self.width_entry = Entry(self.modifying_tools)
        self.width_entry.pack()
        alpha_message = Label(self.modifying_tools,
                              text="Absorption coefficient (defaults to {0}):".format(DEFAULT_ALPHA)
                              )
        alpha_message.pack()
        self.alpha_entry = Entry(self.modifying_tools)
        self.alpha_entry.pack()
        modify_button = Button(self.modifying_tools,
                               text="Modify network",
                               command=self.modify_click
                               )
        modify_button.pack()

    def modify_click(self):
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        width = float(width)
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        alpha = float(alpha)
        self.constructor.modify_adjacency(width, alpha)

        # ========== Changing stage ==========
        self.canvas.destroy()
        self.add_canvas(modified=True)
        self.modifying_tools.destroy()
        self.remove_bind()
        self.add_customising_tools()
        self.add_selecting_bind()
        # ========== Changing stage ==========

    def add_customising_tools(self):
        self.selected = None
        self.customising_tools = Frame(self.tools_frame)
        self.customising_tools.pack()
        customising_message = Label(self.customising_tools,
                                    text="Select street to customise."
                                    )
        customising_message.pack()
        width = Label(self.customising_tools, text="Width:")
        width.pack()
        self.width_entry = Entry(self.customising_tools)
        self.width_entry.pack()
        alpha = Label(self.customising_tools, text="Absorption coefficient:")
        alpha.pack()
        self.alpha_entry = Entry(self.customising_tools)
        self.alpha_entry.pack()
        customise_button = Button(self.customising_tools, text="Change", command=self.customise_click)
        customise_button.pack()

    def customise_click(self):
        if self.selected is None:
            print("Nothing selected.")
        else:
            adjacency = self.constructor.get_modified_adjacency()
            alpha = self.alpha_entry.get()
            properties = adjacency[self.selected[0]][self.selected[1]]
            if alpha == '':
                alpha = properties["alpha"]
            alpha = float(alpha)
            width = self.width_entry.get()
            if width == '':
                width = properties["width"]
            width = float(width)
            self.constructor.change_alpha(self.selected[0], self.selected[1], alpha)
            self.constructor.change_width(self.selected[0], self.selected[1], width)

            self.canvas.destroy()
            self.add_canvas(modified=True)
            self.add_selecting_bind()

    def add_selecting_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_select)

    def click_to_select(self, event):
        canvas = event.widget
        self.selected = self.find_nodes(canvas)
        print(self.selected)

    def find_nodes(self, canvas):
        line = canvas.find_withtag("current")
        coordinates = canvas.coords(line)
        point1 = coordinates[0:2]
        point2 = coordinates[2:4]
        index1 = None
        index2 = None
        counter = 0
        positions = self.constructor.get_positions()
        for position in positions:
            if position[0]+OFFSET == point1[0] and position[1]+OFFSET == point1[1]:
                index1 = counter
            elif position[0]+OFFSET == point2[0] and position[1]+OFFSET == point2[1]:
                index2 = counter
            counter += 1
        return (index1, index2)

    def add_canvas(self, modified=False):
        """
        This method creates canvas.
        """
        self.label_message.grid(row=0, column=0, columnspan=2, sticky="we")
        self.canvas = Canvas(self.master, width=WIDTH, height=HEIGHT, bg="AntiqueWhite1")
        self.canvas.grid(row=1, column=1, rowspan=1)
        self.draw_network(modified)

    def draw_network(self, modified):
        """
        This method draws network of streets on canvas.
        """
        if modified:
            adjacency = self.constructor.get_modified_adjacency()
        else:
            adjacency = self.constructor.get_adjacency()
        positions = self.constructor.get_positions()
        for i in range(len(positions)):
            for j in range(i):
                if adjacency[i][j] != 0:
                    x0 = positions[i][0]
                    y0 = positions[i][1]
                    x1 = positions[j][0]
                    y1 = positions[j][1]
                    if modified:
                        alpha = adjacency[i][j]["alpha"]
                        red = hex(int(alpha*255))
                        red = red[-2:] if len(red)==4 else "0{0}".format(red[-1])
                        blue = hex(int((1-alpha)*255))
                        blue = blue[-2:] if len(blue)==4 else "0{0}".format(blue[-1])
                        fill = "#{0}00{1}".format(red, blue)
                        width = adjacency[i][j]["width"]
                    else:
                        fill = "light slate grey"
                        width = 5
                    self.canvas.create_line(x0+OFFSET,
                                            y0+OFFSET,
                                            x1+OFFSET,
                                            y1+OFFSET,
                                            fill=fill,
                                            width=width
                                            )

    def click_to_move(self, event):
        """
        This method is triggered when left mouse button is clicked.
        """
        self.movement = {"move": False,
                         "orientation": None,
                         "start": None,
                         "line_index": None
                         }
        canvas = event.widget
        line = canvas.find_withtag("current")
        if not line: # Execute if tuple is not empty
            self.movement["move"] = False
        else:
            (index1, index2) = self.find_nodes(canvas)
            verticals = self.constructor.get_verticals()
            positions = self.constructor.get_positions()
            orientation = "vertical" if positions[index1][0] == positions[index2][0] else "horizontal"
            start = positions[index1][1] if orientation=="horizontal" else positions[index1][0]
            start = start + OFFSET
            line_index = index1%verticals if orientation=="vertical" else index1//verticals
            self.movement["move"] = True
            self.movement["orientation"] = orientation
            self.movement["start"] = start
            self.movement["line_index"] = line_index

    def release_to_move(self, event):
        """
        This method is triggered when left mouse button is released.
        """
        canvas = event.widget
        line = canvas.find_withtag("current")
        if not line and self.movement["move"] is True:
            start = self.movement["start"]
            line_index = self.movement["line_index"]
            orientation = self.movement["orientation"]
            if orientation=="horizontal":
                end = event.y
                delta = end - start
                self.constructor.move_horizontal_line(line_index, delta)
            else:
                end = event.x
                delta = end - start
                self.constructor.move_vertical_line(line_index, delta)

            # ========== Changing stage ==========
            self.canvas.destroy()
            self.add_canvas()
            self.add_moving_bind()
            # ========== Changing stage ==========
        else:
            print("You released mouse on another line! Oops.")

    def click_to_delete(self, event):
        """
        This method is triggered when left mouse button is clicked.
        """
        canvas = event.widget
        line = canvas.find_withtag("current")
        if not line: # Execute if tuple is not empty
            print("You misclicked!")
        else:
            (index1, index2) = self.find_nodes(canvas)
            self.constructor.delete_connection(index1, index2)

            # ========== Changing stage ==========
            self.canvas.destroy()
            self.add_canvas()
            self.remove_bind()
            self.add_deleting_bind()
            # ========== Changing stage ==========
