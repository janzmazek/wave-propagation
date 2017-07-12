from tkinter import *
from tkinter import messagebox
from source.model import Model


DEFAULT_LENGTH = 100
DEFAULT_WIDTH = 10
DEFAULT_ALPHA = 0.5

class EditingTools(object):
    """This class of methods constructs tools widget for GUI."""
    def __init__(self, network_canvas, tools_frame):
        self.network_canvas = network_canvas
        self.tools_frame = tools_frame
        self.tools = False

        # delete binds
        self.network_canvas.selected = False
        self.network_canvas.delete_binds()
        self.network_canvas.refresh_network()


class MovingTools(EditingTools):
    """This child class implements moving tools."""
    def __init__(self, network_canvas, tools_frame):
        network_canvas.draw_network()
        super(MovingTools, self).__init__(network_canvas, tools_frame)
        self.tools = Frame(self.tools_frame)
        self.tools.pack()
        moving_message = Label(self.tools,
                               text="Drag and drop to move street."
                               )
        moving_message.pack()
        finished_moving_button = Button(self.tools,
                                        text="Finished moving",
                                        command=self.click
                                        )
        finished_moving_button.pack()

        self.network_canvas.add_moving_bind()

    def click(self):
        """
        This method is executed on button click and creates tools frame
        following current tools frame.
        """
        self.tools.destroy()
        self.tools = False
        DeletingTools(self.network_canvas, self.tools_frame)

class DeletingTools(EditingTools):
    """This child class implements deleting tools."""
    def __init__(self, network_canvas, tools_frame):
        super(DeletingTools, self).__init__(network_canvas, tools_frame)
        self.network_canvas.refresh_network()
        self.tools = Frame(self.tools_frame)
        self.tools.pack()
        deleting_message = Label(self.tools,
                                 text="Click on street to delete it")
        deleting_message.pack()
        finished_deleting_button = Button(self.tools,
                                          text="Finished deleting",
                                          command=self.click
                                          )
        finished_deleting_button.pack()

        self.network_canvas.add_deleting_bind()

    def click(self):
        """
        This method is executed on button click and creates tools frame
        following current tools frame.
        """
        self.tools.destroy()
        ModifyingTools(self.network_canvas, self.tools_frame)

class ModifyingTools(EditingTools):
    """This child class implements modifying tools."""
    def __init__(self, network_canvas, tools_frame):
        super(ModifyingTools, self).__init__(network_canvas, tools_frame)
        self.network_canvas.refresh_network()
        self.tools = Frame(self.tools_frame)
        self.tools.pack()
        modifying_message = Label(self.tools,
                                  text="Choose default parameters for streets"
                                  )
        modifying_message.pack()
        width_message = Label(self.tools,
                              text="Width (defaults to {0}):".format(DEFAULT_WIDTH)
                              )
        width_message.pack()
        self.width_entry = Entry(self.tools)
        self.width_entry.pack()
        alpha_message = Label(self.tools,
                              text="Absorption coefficient (defaults to {0}):".format(DEFAULT_ALPHA)
                              )
        alpha_message.pack()
        self.alpha_entry = Entry(self.tools)
        self.alpha_entry.pack()
        modify_button = Button(self.tools,
                               text="Modify network",
                               command=self.click
                               )
        modify_button.pack()

    def click(self):
        """
        This method is executed on button click and creates tools frame
        following current tools frame.
        """
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        width = float(width)
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        alpha = float(alpha)
        if width < 0:
            messagebox.showinfo("Error", "Width must be a positive number.")
            raise ValueError("Width must be a positive number.")

        if alpha < 0 or alpha > 1:
            messagebox.showinfo(
                "Error", "Absorption coefficient must be between 0 and 1")
            raise ValueError(
                "Absorption coefficient must be between 0 and 1")

        self.network_canvas.modify_network(width, alpha)
        self.tools.destroy()
        CustomisingTools(self.network_canvas, self.tools_frame)

class CustomisingTools(EditingTools):
    """This child class implements customising tools."""
    def __init__(self, network_canvas, tools_frame):
        super(CustomisingTools, self).__init__(network_canvas, tools_frame)
        self.network_canvas.refresh_network()
        self.tools = Frame(self.tools_frame)
        self.tools.pack()
        customising_message = Label(self.tools,
                                    text="Select street to customise."
                                    )
        customising_message.pack()
        width = Label(self.tools, text="Width:")
        width.pack()
        self.width_entry = Entry(self.tools)
        self.width_entry.pack()
        alpha = Label(self.tools, text="Absorption coefficient:")
        alpha.pack()
        self.alpha_entry = Entry(self.tools)
        self.alpha_entry.pack()
        customise_button = Button(self.tools,
                                  text="Change",
                                  command=self.customise_click
                                  )
        customise_button.pack()
        finished_customising_button = Button(self.tools,
                                             text="Finished customising",
                                             command=self.finished_click
                                             )
        finished_customising_button.pack()

        self.network_canvas.add_selecting_bind()

    def customise_click(self):
        """
        This method is executed on customise button click and customises
        network with specified data.
        """
        if self.network_canvas.selected is False:
            messagebox.showinfo("Error", "Nothing selected")
            raise ValueError("Nothing selected")
        else:
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

            if width is not False and width < 0:
                messagebox.showinfo("Error", "Width must be a positive number.")
                raise ValueError("Width must be a positive number.")
            if alpha is not False and (alpha < 0 or alpha > 1):
                messagebox.showinfo(
                    "Error", "Absorption coefficient must be between 0 and 1")
                raise ValueError(
                    "Absorption coefficient must be between 0 and 1")

            self.network_canvas.customise_network(width, alpha)
            self.network_canvas.selected = None
            self.network_canvas.refresh_network()


    def finished_click(self):
        """
        This method is executed on button click and creates tools frame
        following current tools frame.
        """
        self.tools.destroy()
        ModelTools(self.network_canvas, self.tools_frame)

class ModelTools(EditingTools):
    """This child class implements model tools."""
    def __init__(self, canvas, tools_frame):
        super(ModelTools, self).__init__(canvas, tools_frame)
        self.network_canvas.refresh_network()
        self.network_canvas.draw_nodes()
        self.tools = Frame(self.tools_frame)
        self.tools.pack()
        starting_label = Label(self.tools,
                               text="Select starting point."
                               )
        starting_label.grid(row=0, column=0)
        self.starting_entry_1 = Entry(self.tools, width=5)
        self.starting_entry_1.grid(row=0, column=1)
        self.starting_entry_2 = Entry(self.tools, width=5)
        self.starting_entry_2.grid(row=0, column=2)
        ending_label = Label(self.tools,
                             text="Select ending point."
                             )
        ending_label.grid(row=2, column=0)
        self.ending_entry_1 = Entry(self.tools, width=5)
        self.ending_entry_1.grid(row=2, column=1)
        self.ending_entry_2 = Entry(self.tools, width=5)
        self.ending_entry_2.grid(row=2, column=2)
        threshold_label = Label(self.tools,
                                text="Choose threshold (defaults to 2)."
                                )
        threshold_label.grid(row=3, column=0)
        self.threshold_entry = Entry(self.tools, width=12)
        self.threshold_entry.grid(row=3, column=1, columnspan=2)
        compute_button = Button(self.tools,
                                text="Compute power",
                                command=self.click
                                )
        compute_button.grid(row=4, column=0, columnspan=3)

    def click(self):
        """
        This method is executed on button click and computes the result of
        wave propagation model.
        """
        starting_1 = self.starting_entry_1.get()
        starting_2 = self.starting_entry_2.get()
        if starting_1 == '':
            starting_1 = False
            messagebox.showinfo("Error", "Fill source node 1.")
            raise ValueError("Fill source node 1.")
        if starting_2 == '':
            starting_2 = False
            messagebox.showinfo("Error", "Fill source node 2.")
            raise ValueError("Fill source node 2.")
        starting_1 = int(starting_1)//1
        starting_2 = int(starting_2)//1

        ending_1 = self.ending_entry_1.get()
        ending_2 = self.ending_entry_2.get()
        if ending_1 == '':
            ending_1 = False
            messagebox.showinfo("Error", "Fill source node 1.")
            raise ValueError("Fill source node 1.")
        if ending_2 == '':
            ending_2 = False
            messagebox.showinfo("Error", "Fill source node 2.")
            raise ValueError("Fill source node 2.")
        ending_1 = int(ending_1)//1
        ending_2 = int(ending_2)//1

        threshold = self.threshold_entry.get()
        if threshold == '':
            threshold = 2
        threshold = int(threshold)//1
        model = Model(self.network_canvas.constructor.get_modified_adjacency())
        model.set_source(starting_1, starting_2)
        model.set_receiver(ending_1, ending_2)
        power = model.solve(threshold)
        messagebox.showinfo("Result", "Power percentage: {0}".format(power))
