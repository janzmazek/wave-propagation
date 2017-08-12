import tkinter as tk
from PIL import ImageTk

# Adobe flat UI colour scheme
DARK_BLUE = "#2C3E50"
MEDIUM_BLUE = "#2980B9"
LIGHT_BLUE = "#3498DB"
RED = "#E74C3C"
WHITE = "#ECF0F1"

# Colour parameters
STREET_COLOUR = DARK_BLUE
JUNCTION_COLOUR = MEDIUM_BLUE
SELECTED_COLOUR = LIGHT_BLUE

# Dimensions
OFFSET = 20
STROKE_WIDTH = 5

# Max absorption displays as red colour
MAX_ABSORPTION = 0.1

class Canvas(tk.Canvas):
    """This class implements canvas of "view" part of the MVC pattern."""
    def __init__(self, view, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.view = view

        self.background_image = False

    def set_background(self, filename):
        """
        This setter method sets the background image attribute.
        """
        self.background_image = ImageTk.PhotoImage(file=filename)

    def remove_background(self):
        """
        This method removes the background image attribute.
        """
        self.background_image = False

    def refresh_canvas(self, adjacency, positions, modified, selected):
        """
        This method refreshes canvas based on the received data.
        """
        self.delete("all")
        if self.background_image:
            self.create_image(0, 0, image=self.background_image, anchor='nw', tags="background")
        if adjacency is not None and positions is not None:
            self.__draw_streets(adjacency, positions, modified)
        if selected:
            self.__select_street(positions, selected)
        self.__draw_junctions(positions)

    def __draw_streets(self, adjacency, positions, modified):
        """
        This private method draws lines on canvas based on the received data.
        """
        def get_hex_fill(coefficient, max_absorption):
            red = hex(int(coefficient/max_absorption*255))
            red = red[-2:] if len(red)==4 else "0{0}".format(red[-1])
            blue = hex(int((1-coefficient/max_absorption)*255))
            blue = blue[-2:] if len(blue)==4 else "0{0}".format(blue[-1])
            fill = "#{0}00{1}".format(red, blue)
            return fill

        if modified:
            for i in range(len(positions)): # draw wall absorption
                for j in range(i):
                    if adjacency[i][j] != 0:
                        [xi, yi] = positions[i]
                        [xj, yj] = positions[j]
                        alpha = adjacency[i][j]["alpha"]
                        alpha_fill = get_hex_fill(alpha, MAX_ABSORPTION)
                        width = adjacency[i][j]["width"]
                        self.__draw_stroke(xi+OFFSET, yi+OFFSET,
                                           xj+OFFSET, yj+OFFSET,
                                           stroke=alpha_fill, width=width
                                           )
        for i in range(len(positions)): # draw streets
            for j in range(i):
                if adjacency[i][j] != 0:
                    [xi, yi] = positions[i]
                    [xj, yj] = positions[j]
                    if modified:
                        beta = adjacency[i][j]["beta"]
                        beta_fill = get_hex_fill(beta, MAX_ABSORPTION)
                        width = adjacency[i][j]["width"]
                    else:
                        beta_fill = STREET_COLOUR
                        width = 5
                    self.create_line(xi+OFFSET, yi+OFFSET, xj+OFFSET, yj+OFFSET,
                                     width=width, fill=beta_fill
                                     )

    def __select_street(self, positions, selected):
        """
        This private method draws a street with with specified colour based on
        received data.
        """
        index1 = selected[0]
        index2 = selected[1]
        x0 = positions[index1][0]
        y0 = positions[index1][1]
        x1 = positions[index2][0]
        y1 = positions[index2][1]
        self.create_line(x0+OFFSET, y0+OFFSET, x1+OFFSET, y1+OFFSET,
                         fill=SELECTED_COLOUR, width=10)

    def __draw_stroke(self, x0, y0, x1, y1, stroke, width):
        if stroke:
            offset = width/2
            if x0==x1:
                self.create_line(x0-offset, y0,
                                 x1-offset, y1,
                                 width=STROKE_WIDTH, fill=stroke,
                                 tags="background"
                                 )
                self.create_line(x0+offset, y0,
                                 x1+offset, y1,
                                 width=STROKE_WIDTH, fill=stroke,
                                 tags="background"
                                 )
            elif y0==y1:
                self.create_line(x0, y0-offset,
                                 x1, y1-offset,
                                 width=STROKE_WIDTH, fill=stroke,
                                 tags="background"
                                 )
                self.create_line(x0, y0+offset,
                                 x1, y1+offset,
                                 width=STROKE_WIDTH, fill=stroke,
                                 tags="background"
                                 )


    def __draw_junctions(self, positions):
        """
        This private method draws circles with text inside based on the received
        data.
        """
        def circle(x, y, r, **kwargs):
            self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        node = 0
        for position in positions:
            circle(position[0]+OFFSET,
                   position[1]+OFFSET,
                   10,
                   outline=JUNCTION_COLOUR,
                   fill=JUNCTION_COLOUR,
                   width=2)
            self.create_text(position[0]+OFFSET,
                             position[1]+OFFSET,
                             text="{0}".format(node)
                             )
            node += 1

    def remove_binds(self):
        """
        This method removes all binds from canvas.
        """
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")

    def add_moving_bind(self):
        """
        This method adds the moving bind (LMB click and release) to the canvas.
        """
        self.bind("<Button-1>", self.click_to_move)
        self.bind("<ButtonRelease-1>", self.release_to_move)

    def add_deleting_bind(self):
        """
        This method adds the deleting bind (LMB click) to the canvas.
        """
        self.bind("<Button-1>", self.click_to_delete)

    def add_selecting_bind(self):
        """
        This method adds the selecting bind (LMB click) to the canvas.
        """
        self.bind("<Button-1>", self.click_to_select)

    def click_to_move(self, event):
        """
        This method is triggered after receiving moving bind (LMB click) event.
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
        This method is triggered after receiving moving bind (LMB release) event.
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
        This method is triggered after receiving deleting bind (LMB click) event.
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
        """
        This method is triggered after receiving selecting bind (LMB click) event.
        """
        canvas = event.widget
        handle = canvas.find_withtag("current")
        tag = canvas.gettags("current")
        if not handle or "background" in tag:
            self.view.controller.click_to_select(False, False)
            return
        coordinates = canvas.coords(handle)
        endpoints = (coordinates[0:2], coordinates[2:4])
        self.view.controller.click_to_select(endpoints, OFFSET)
