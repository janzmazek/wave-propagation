import tkinter as tk

# Default values
DEFAULT_HORIZONTALS = 4
DEFAULT_VERTICALS = 6
DEFAULT_LENGTH = 100
DEFAULT_WIDTH = 5
DEFAULT_ALPHA = 0.03
DEFAULT_BETA = 1e-3
DEFAULT_THRESHOLD = 2

# Dimensions
ENTRY_WIDTH = 4
PADX = 10

class CreationTools(tk.LabelFrame):
    """This class of methods implements creation tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(CreationTools, self).__init__(view, *args, text="Create grid", **kwargs)
        self.view = view

        horizontals_label = tk.Label(self,
                                     text="Horizontal streets [{0}]:".format(DEFAULT_HORIZONTALS),
                                     padx=PADX
                                     )
        horizontals_label.pack(side=tk.LEFT)

        self.horizontals_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.horizontals_entry.pack(side=tk.LEFT)

        verticals_label = tk.Label(self,
                                   text="Vertical streets [{0}]:".format(DEFAULT_VERTICALS),
                                   padx=PADX
                                   )
        verticals_label.pack(side=tk.LEFT)

        self.verticals_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.verticals_entry.pack(side=tk.LEFT)

        initial_length_label = tk.Label(self,
                                        text="Street lengths [{0}]:".format(
                                        DEFAULT_LENGTH),
                                        padx=PADX
                                        )
        initial_length_label.pack(side=tk.LEFT)
        self.initial_length_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.initial_length_entry.pack(side=tk.LEFT)
        draw_button = tk.Button(self,
                                text="Draw network",
                                padx=PADX,
                                command=self.click
                                )
        draw_button.pack(side=tk.LEFT)

    def click(self):
        """
        This method is triggered when the "draw" button is clicked.
        """
        horizontals = self.horizontals_entry.get()
        if horizontals == '':
            horizontals = DEFAULT_HORIZONTALS
        verticals = self.verticals_entry.get()
        if verticals == '':
            verticals = DEFAULT_VERTICALS
        initial_length = self.initial_length_entry.get()
        if initial_length == '':
            initial_length = DEFAULT_LENGTH

        self.view.controller.done_creating(horizontals, verticals, initial_length)


class MovingTools(tk.LabelFrame):
    """This class of methods implements moving tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(MovingTools, self).__init__(view, *args, text="Move streets", **kwargs)
        self.view = view

        moving_message = tk.Label(self,
                                  text="Drag and drop to move street.",
                                  padx=PADX
                                  )
        moving_message.pack(side=tk.LEFT)
        done_moving_button = tk.Button(self,
                                           text="Done moving",
                                           command=self.click
                                           )
        done_moving_button.pack(side=tk.LEFT)

    def click(self):
        """
        This method is triggered when the "done moving" button is clicked.
        """
        self.view.controller.done_moving()

class DeletingTools(tk.LabelFrame):
    """This class of methods implements deleting tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(DeletingTools, self).__init__(view, *args, text="Delete streets", **kwargs)
        self.view = view

        deleting_message = tk.Label(self,
                                 text="Click to delete street.",
                                 padx=PADX
                                 )
        deleting_message.pack(side=tk.LEFT)
        done_deleting_button = tk.Button(self,
                                         text="Done deleting",
                                         command=self.click
                                         )
        done_deleting_button.pack(side=tk.LEFT)

    def click(self):
        """
        This method is triggered when the "done deleting" button is clicked.
        """
        self.view.controller.done_deleting()

class ModifyingTools(tk.LabelFrame):
    """This class of methods implements modifying tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(ModifyingTools, self).__init__(
            view, *args, text="Select default parameters for streets", **kwargs)
        self.view = view

        width_message = tk.Label(self,
                                 text="Width [{0}]:".format(DEFAULT_WIDTH),
                                 padx=PADX
                                 )
        width_message.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.width_entry.pack(side=tk.LEFT)
        alpha_message = tk.Label(self,
                                 text="Wall absorption [{0}]:".format(DEFAULT_ALPHA),
                                 padx=PADX
                                 )
        alpha_message.pack(side=tk.LEFT)
        self.alpha_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.alpha_entry.pack(side=tk.LEFT)
        beta_message = tk.Label(self,
                                 text="Air absorption [{0}]:".format(DEFAULT_BETA),
                                 padx=PADX
                                 )
        beta_message.pack(side=tk.LEFT)
        self.beta_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.beta_entry.pack(side=tk.LEFT)
        modify_button = tk.Button(self,
                                  text="Modify network",
                                  command=self.click
                                  )
        modify_button.pack(side=tk.LEFT)

    def click(self):
        """
        This method is triggered when the "modify network" button is clicked.
        """
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        beta = self.beta_entry.get()
        if beta == '':
            beta = DEFAULT_BETA
        self.view.controller.done_modifying(width, alpha, beta)

class CustomisingTools(tk.LabelFrame):
    """This class of methods implements customising tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(CustomisingTools, self).__init__(view, *args, text="Customise streets", **kwargs)
        self.view = view

        customising_message = tk.Label(self,
                                       text="Click to select street.",
                                       padx=PADX
                                       )
        customising_message.pack(side=tk.LEFT)
        width = tk.Label(self,
                         text="Width [{0}]:".format(DEFAULT_WIDTH),
                         padx=PADX
                         )
        width.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.width_entry.pack(side=tk.LEFT)
        alpha = tk.Label(self,
                         text="Wall absorption [{0}]:".format(DEFAULT_ALPHA),
                         padx=PADX
                         )
        alpha.pack(side=tk.LEFT)
        self.alpha_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.alpha_entry.pack(side=tk.LEFT)
        beta = tk.Label(self,
                         text="Air absorption [{0}]:".format(DEFAULT_BETA),
                         padx=PADX
                         )
        beta.pack(side=tk.LEFT)
        self.beta_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.beta_entry.pack(side=tk.LEFT)
        customise_button = tk.Button(self,
                                     text="Customise",
                                     command=self.customise_click
                                     )
        customise_button.pack(side=tk.LEFT)
        done_customising_button = tk.Button(self,
                                            text="Finished customising",
                                            command=self.done_customising
                                            )
        done_customising_button.pack(side=tk.LEFT)

    def customise_click(self):
        """
        This method is triggered when the "customise" button is clicked.
        """
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        beta = self.beta_entry.get()
        if beta == '':
            beta = DEFAULT_BETA

        self.view.controller.customise_click(width, alpha, beta)

    def done_customising(self):
        """
        This method is triggered when the "done customising" button is clicked.
        """
        self.view.controller.done_customising()

class ModelTools(tk.LabelFrame):
    """This class of methods implements model tools in the toolbar."""
    def __init__(self, view, *args, **kwargs):
        super(ModelTools, self).__init__(view, *args, text="Choose model parameters", **kwargs)
        self.view = view

        starting_label = tk.Label(self, text="Source:", padx=PADX )
        starting_label.pack(side=tk.LEFT)
        self.starting_entry_1 = tk.Entry(self, width=ENTRY_WIDTH)
        self.starting_entry_1.pack(side=tk.LEFT)
        self.starting_entry_2 = tk.Entry(self, width=ENTRY_WIDTH)
        self.starting_entry_2.pack(side=tk.LEFT)
        ending_label = tk.Label(self, text="Receiver:", padx=PADX)
        ending_label.pack(side=tk.LEFT)
        self.ending_entry_1 = tk.Entry(self, width=ENTRY_WIDTH)
        self.ending_entry_1.pack(side=tk.LEFT)
        self.ending_entry_2 = tk.Entry(self, width=ENTRY_WIDTH)
        self.ending_entry_2.pack(side=tk.LEFT)
        threshold_label = tk.Label(self,
                                   text="Threshold [{0}]:".format(DEFAULT_THRESHOLD),
                                   padx=PADX
                                   )
        threshold_label.pack(side=tk.LEFT)
        self.threshold_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.threshold_entry.pack(side=tk.LEFT)
        height_label = tk.Label(self,
                                text="Height:",
                                padx=PADX
                                )
        height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.height_entry.pack(side=tk.LEFT)
        compute_button = tk.Button(self,
                                   text="Compute",
                                   command=self.compute_click
                                   )
        compute_button.pack(side=tk.LEFT)
        export_button = tk.Button(self,
                                  text="Compute all",
                                  command=self.compute_all_click
                                  )
        export_button.pack(side=tk.LEFT)

    def compute_click(self):
        """
        This method is triggered when the "compute" button is clicked.
        """
        starting_1 = self.starting_entry_1.get()
        starting_2 = self.starting_entry_2.get()
        ending_1 = self.ending_entry_1.get()
        ending_2 = self.ending_entry_2.get()
        threshold = self.threshold_entry.get()
        height = self.height_entry.get()
        if threshold == '':
            threshold = DEFAULT_THRESHOLD
        if height == '':
            height = False
        source = (starting_1, starting_2)
        receiver = (ending_1, ending_2)
        self.view.controller.compute_click(source, receiver, threshold, height)
    def compute_all_click(self):
        """
        This method is triggered when the "compute all" button is clicked.
        """
        starting_1 = self.starting_entry_1.get()
        starting_2 = self.starting_entry_2.get()
        threshold = self.threshold_entry.get()
        height = self.height_entry.get()
        if threshold == '':
            threshold = DEFAULT_THRESHOLD
        if height == '':
            height = False
        source = (starting_1, starting_2)
        self.view.controller.compute_all_click(source, threshold, height)
