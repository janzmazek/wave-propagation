import tkinter as tk
from PIL import ImageTk

OFFSET = 20

class Canvas(tk.Canvas):
    def __init__(self, view, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.view = view

        self.background_image = False

    def set_background(self, filename):
        self.background_image = ImageTk.PhotoImage(file=filename)

    def remove_background(self):
        self.background_image = False

    def refresh_canvas(self, adjacency, positions, modified, selected, numbered):
        self.delete("all")
        if self.background_image:
            self.create_image(0, 0, image=self.background_image, anchor='nw', tags="background")
        if adjacency is not None and positions is not None:
            self.draw_streets(adjacency, positions, modified)
        if selected:
            self.select_street(positions, selected)
        if numbered:
            self.draw_junctions(positions)

    def draw_streets(self, adjacency, positions, modified):
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
                    self.create_line(x0+OFFSET,
                                     y0+OFFSET,
                                     x1+OFFSET,
                                     y1+OFFSET,
                                     fill=fill,
                                     width=width
                                     )

    def select_street(self, positions, selected):
        index1 = selected[0]
        index2 = selected[1]
        x0 = positions[index1][0]
        y0 = positions[index1][1]
        x1 = positions[index2][0]
        y1 = positions[index2][1]
        self.create_line(x0+OFFSET, y0+OFFSET, x1+OFFSET, y1+OFFSET, fill="green", width=10)


    def draw_junctions(self, positions):
        def circle(x, y, r, **kwargs):
            self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        node = 0
        for position in positions:
            circle(position[0]+OFFSET,
                   position[1]+OFFSET,
                   10,
                   outline="gray",
                   fill="gray",
                   width=2)
            self.create_text(position[0]+OFFSET,
                             position[1]+OFFSET,
                             text="{0}".format(node)
                             )
            node += 1

    def remove_binds(self):
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")

    def add_moving_bind(self):
        self.bind("<Button-1>", self.click_to_move)
        self.bind("<ButtonRelease-1>", self.release_to_move)

    def add_deleting_bind(self):
        self.bind("<Button-1>", self.click_to_delete)

    def add_selecting_bind(self):
        self.bind("<Button-1>", self.click_to_select)

    def click_to_move(self, event):
        """
        This method is triggered when left mouse button is clicked.
        """
        canvas = event.widget
        handle = canvas.find_withtag("current") # returns tuple of handle
        tag = canvas.gettags("current") # returns tuple of tags ("current", "background")
        if not handle or "background" in tag:
            self.view.controller.click_to_move(False, False)
            return
        coordinates = canvas.coords(handle)
        endpoints = (coordinates[0:2], coordinates[2:4])
        self.view.controller.click_to_move(endpoints, OFFSET)

    def release_to_move(self, event):
        """
        This method is triggered when left mouse button is released.
        """
        canvas = event.widget
        handle = canvas.find_withtag("current")
        tag = canvas.gettags("current")
        if handle and "background" not in tag:
            self.view.controller.release_to_move(False)
            return
        endpoints = (event.x, event.y)
        self.view.controller.release_to_move(endpoints)

    def click_to_delete(self, event):
        """
        This method is triggered when left mouse button is clicked.
        """
        canvas = event.widget
        handle = canvas.find_withtag("current")
        tag = canvas.gettags("current")
        if not handle or "background" in tag:
            self.view.controller.click_to_delete(False, False)
            return
        coordinates = canvas.coords(handle)
        endpoints = (coordinates[0:2], coordinates[2:4])
        self.view.controller.click_to_delete(endpoints, OFFSET)

    def click_to_select(self, event):
        canvas = event.widget
        handle = canvas.find_withtag("current")
        tag = canvas.gettags("current")
        if not handle or "background" in tag:
            self.view.controller.click_to_select(False, False)
            return
        coordinates = canvas.coords(handle)
        endpoints = (coordinates[0:2], coordinates[2:4])
        self.view.controller.click_to_select(endpoints, OFFSET)
