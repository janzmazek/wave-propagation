from tkinter import *
from tkinter import messagebox
from source.model import Model

DEFAULT_LENGTH = 100
DEFAULT_WIDTH = 10
DEFAULT_ALPHA = 0.5

class EditingTools(object):
    """docstring for EditingTools."""
    def __init__(self, network_canvas, tools_frame):
        self.network_canvas = network_canvas
        self.tools_frame = tools_frame


class MovingTools(EditingTools):
    """docstring for MovingTools."""
    def __init__(self, network_canvas, tools_frame):
        super(MovingTools, self).__init__(network_canvas, tools_frame)
        self.moving_tools = Frame(self.tools_frame)
        self.moving_tools.pack()
        moving_message = Label(self.moving_tools,
                               text="Drag and drop to move street."
                               )
        moving_message.pack()
        finished_moving_button = Button(self.moving_tools,
                                        text="Finished moving",
                                        command=self.click
                                        )
        finished_moving_button.pack()

        (self.funcid1, self.funcid2) = self.network_canvas.add_moving_bind()

    def delete(self):
        self.moving_tools.destroy()
        self.moving_tools = None

    def click(self):
        self.delete()
        self.network_canvas.remove_moving_bind(self.funcid1, self.funcid2)
        DeletingTools(self.network_canvas, self.tools_frame)

class DeletingTools(EditingTools):
    """docstring for DeletingTools."""
    def __init__(self, network_canvas, tools_frame):
        super(DeletingTools, self).__init__(network_canvas, tools_frame)
        self.deleting_tools = Frame(self.tools_frame)
        self.deleting_tools.pack()
        deleting_message = Label(self.deleting_tools,
                                 text="Click on street to delete it")
        deleting_message.pack()
        finished_deleting_button = Button(self.deleting_tools,
                                          text="Finished deleting",
                                          command=self.click
                                          )
        finished_deleting_button.pack()

        self.funcid = self.network_canvas.add_deleting_bind()

    def delete(self):
        self.deleting_tools.destroy()

    def click(self):
        self.delete()
        self.network_canvas.remove_deleting_bind(self.funcid)
        ModifyingTools(self.network_canvas, self.tools_frame)

class ModifyingTools(EditingTools):
    """docstring for ModifyingTools."""
    def __init__(self, network_canvas, tools_frame):
        super(ModifyingTools, self).__init__(network_canvas, tools_frame)
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
                               command=self.click
                               )
        modify_button.pack()

    def delete(self):
        self.modifying_tools.destroy()

    def click(self):
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        width = float(width)
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        alpha = float(alpha)

        self.delete()
        self.network_canvas.modify_network(width, alpha)
        self.network_canvas.refresh_network()
        CustomisingTools(self.network_canvas, self.tools_frame)

class CustomisingTools(EditingTools):
    """docstring for CustomisingTools."""
    def __init__(self, network_canvas, tools_frame):
        super(CustomisingTools, self).__init__(network_canvas, tools_frame)
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
        customise_button = Button(self.customising_tools,
                                  text="Change",
                                  command=self.customise_click
                                  )
        customise_button.pack()
        finished_customising_button = Button(self.customising_tools,
                                             text="Finished customising",
                                             command=self.finished_click
                                             )
        finished_customising_button.pack()

        self.funcid = self.network_canvas.add_selecting_bind()

    def delete(self):
        self.customising_tools.destroy()

    def customise_click(self):
        width = self.width_entry.get()
        if width == '':
            width = False
        else:
            width = float(width)
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = False
        else:
            alpha = float(alpha)
        selected = self.network_canvas.selected
        if selected is None:
            print("Nothing selected...")
        else:
            self.network_canvas.customise_network(width, alpha)
        self.network_canvas.refresh_network()


    def finished_click(self):
        self.delete()
        self.network_canvas.refresh_network()
        self.network_canvas.draw_nodes()
        self.network_canvas.remove_selecting_bind(self.funcid)
        ModelTools(self.network_canvas, self.tools_frame)

class ModelTools(EditingTools):
    """docstring for ModelTools."""
    def __init__(self, canvas, tools_frame):
        super(ModelTools, self).__init__(canvas, tools_frame)
        self.model_tools = Frame(self.tools_frame)
        self.model_tools.pack()
        starting_label = Label(self.model_tools, text="Select starting point.")
        starting_label.grid(row=0, column=0)
        self.starting_entry = Entry(self.model_tools, width=5)
        self.starting_entry.grid(row=0, column=1)
        ending_label = Label(self.model_tools, text="Select ending point.")
        ending_label.grid(row=2, column=0)
        self.ending_entry = Entry(self.model_tools, width=5)
        self.ending_entry.grid(row=2, column=1)
        threshold_label = Label(self.model_tools, text="Choose threshold (defaults to 2).")
        threshold_label.grid(row=3, column=0)
        self.threshold_entry = Entry(self.model_tools, width=5)
        self.threshold_entry.grid(row=3, column=1)
        compute_button = Button(self.model_tools, text="Compute power", command=self.click)
        compute_button.grid(row=4, column=0, columnspan=2)

    def delete(self):
        self.model_tools.destroy()

    def click(self):
        starting = int(self.starting_entry.get())
        ending = int(self.ending_entry.get())
        threshold = self.threshold_entry.get()
        if threshold == '':
            threshold = 2
        threshold = int(threshold)
        model = Model(self.network_canvas.constructor.get_modified_adjacency())
        model.set_source(starting)
        model.set_receiver(ending)
        power = model.solve(threshold)
        messagebox.showinfo("Result", "Power percentage: {0}".format(power))
