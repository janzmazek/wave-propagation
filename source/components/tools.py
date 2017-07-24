import tkinter as tk

DEFAULT_HORIZONTALS = 4
DEFAULT_VERTICALS = 6
DEFAULT_LENGTH = 100
DEFAULT_WIDTH = 10
DEFAULT_ALPHA = 0.1
DEFAULT_THRESHOLD = 2

ENTRY_WIDTH = 4
PADX = 10

class CreationTools(tk.LabelFrame):
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
        This method is executed when draw button is clicked.
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
        self.view.controller.done_moving()

class DeletingTools(tk.LabelFrame):
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
        self.view.controller.done_deleting()

class ModifyingTools(tk.LabelFrame):
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
                                 text="Absorption coefficient [{0}]:".format(DEFAULT_ALPHA),
                                 padx=PADX
                                 )
        alpha_message.pack(side=tk.LEFT)
        self.alpha_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.alpha_entry.pack(side=tk.LEFT)
        modify_button = tk.Button(self,
                                  text="Modify network",
                                  command=self.click
                                  )
        modify_button.pack(side=tk.LEFT)

    def click(self):
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA
        self.view.controller.done_modifying(width, alpha)

class CustomisingTools(tk.LabelFrame):
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
                         text="Absorption coefficient [{0}]:".format(DEFAULT_ALPHA),
                         padx=PADX
                         )
        alpha.pack(side=tk.LEFT)
        self.alpha_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.alpha_entry.pack(side=tk.LEFT)
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
        width = self.width_entry.get()
        if width == '':
            width = DEFAULT_WIDTH
        alpha = self.alpha_entry.get()
        if alpha == '':
            alpha = DEFAULT_ALPHA

        self.view.controller.customise_click(width, alpha)

    def done_customising(self):
        self.view.controller.done_customising()

class ModelTools(tk.LabelFrame):
    def __init__(self, view, *args, **kwargs):
        super(ModelTools, self).__init__(view, *args, text="Choose model parameters", **kwargs)
        self.view = view

        starting_label = tk.Label(self,
                                  text="Starting point.",
                                  padx=PADX
                                  )
        starting_label.grid(row=0, column=0)
        self.starting_entry_1 = tk.Entry(self, width=ENTRY_WIDTH)
        self.starting_entry_1.grid(row=0, column=1)
        self.starting_entry_2 = tk.Entry(self, width=ENTRY_WIDTH)
        self.starting_entry_2.grid(row=0, column=2)
        ending_label = tk.Label(self,
                                text="Eding point.",
                                padx=PADX
                                )
        ending_label.grid(row=1, column=0)
        self.ending_entry_1 = tk.Entry(self, width=ENTRY_WIDTH)
        self.ending_entry_1.grid(row=1, column=1)
        self.ending_entry_2 = tk.Entry(self, width=ENTRY_WIDTH)
        self.ending_entry_2.grid(row=1, column=2)
        threshold_label = tk.Label(self,
                                   text="Threshold [{0}]:".format(DEFAULT_THRESHOLD),
                                   padx=PADX
                                   )
        threshold_label.grid(row=0, column=3)
        self.threshold_entry = tk.Entry(self, width=ENTRY_WIDTH)
        self.threshold_entry.grid(row=0, column=4)
        compute_button = tk.Button(self,
                                   text="Power",
                                   command=self.compute_click
                                   )
        compute_button.grid(row=1, column=3)
        export_button = tk.Button(self,
                                  text="Power plot",
                                  command=self.compute_all_click
                                  )
        export_button.grid(row=1, column=4)

    def compute_click(self):
        starting_1 = self.starting_entry_1.get()
        starting_2 = self.starting_entry_2.get()
        ending_1 = self.ending_entry_1.get()
        ending_2 = self.ending_entry_2.get()
        threshold = self.threshold_entry.get()
        if threshold == '':
            threshold = 2
        self.view.controller.compute_click(starting_1,
                                           starting_2,
                                           ending_1,
                                           ending_2,
                                           threshold
                                           )
    def compute_all_click(self):
        starting_1 = self.starting_entry_1.get()
        starting_2 = self.starting_entry_2.get()
        if starting_1 == '':
            starting_1 = False
            self.view.show_message("Error", "Fill source node 1.")
            raise ValueError("Fill source node 1.")
        if starting_2 == '':
            starting_2 = False
            self.view.show_message("Error", "Fill source node 2.")
            raise ValueError("Fill source node 2.")
        starting_1 = int(starting_1)
        starting_2 = int(starting_2)
        threshold = self.threshold_entry.get()
        if threshold == '':
            threshold = 2
        threshold = int(threshold)
        self.view.controller.compute_all_click(starting_1, starting_2, threshold)
