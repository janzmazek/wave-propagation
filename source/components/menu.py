import tkinter as tk

class Menu(tk.Menu):
    def __init__(self, view, *args, **kwargs):
        super(Menu, self).__init__(view, *args, **kwargs)
        self.view = view

        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_file_menu()

        self.window_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Window", menu=self.window_menu)
        self.add_window_menu()

        self.tools_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Tools", menu=self.tools_menu)
        self.add_tools_menu()

        self.help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=self.help_menu)
        self.add_help_menu()

    def add_file_menu(self):
        self.file_menu.add_command(label="Import network",
                                   command=lambda: self.view.controller.file_click("import_network")
                                   )
        self.file_menu.add_command(label="Export network",
                                   command=lambda: self.view.controller.file_click("export_network")
                                   )
        self.file_menu.add_command(label="Draw network",
                                   command=lambda: self.view.controller.file_click("draw_network")
                                   )
        self.file_menu.add_command(label="Set background",
                                   command=lambda: self.view.controller.file_click("set_background"),
                                   )
        self.file_menu.add_command(label="Remove background",
                                   command=lambda: self.view.controller.file_click("remove_background"),
                                   )

    def add_window_menu(self):
        self.window_menu.add_command(label="Small",
                                     command=lambda: self.view.controller.window_click("small")
                                     )
        self.window_menu.add_command(label="Medium",
                                     command=lambda: self.view.controller.window_click("medium")
                                     )
        self.window_menu.add_command(label="Large",
                                     command=lambda: self.view.controller.window_click("large")
                                     )

    def add_tools_menu(self):
        self.tools_menu.add_command(label="Create network",
                                    command=lambda: self.view.controller.tools_click("CreationTools")
                                    )
        self.tools_menu.add_command(label="Move streets",
                                    command=lambda: self.view.controller.tools_click("MovingTools")
                                    )
        self.tools_menu.add_command(label="Delete street",
                                    command=lambda: self.view.controller.tools_click("DeletingTools")
                                    )
        self.tools_menu.add_command(label="Modify network",
                                    command=lambda: self.view.controller.tools_click("ModifyingTools")
                                    )
        self.tools_menu.add_command(label="Customise streets",
                                    command=lambda: self.view.controller.tools_click("CustomisingTools")
                                    )

    def add_help_menu(self):
        self.help_menu.add_command(label="About", command=lambda: self.view.controller.about_click())
        self.help_menu.add_command(label="I don't like background", command=self.view.change_background)
