OFFSET = 20

class NetworkCanvas(object):
    """docstring for Canvas."""
    def __init__(self, canvas, constructor):
        self.canvas = canvas
        self.constructor = constructor

        self.modified = False

        self.movement = None
        self.selected = False

    def add_moving_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_move)
        self.canvas.bind("<ButtonRelease-1>", self.release_to_move)

    def add_deleting_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_delete)

    def add_selecting_bind(self):
        self.canvas.bind("<Button-1>", self.click_to_select)

    def delete_binds(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")

    def draw_network(self):
        """
        This method draws network of streets on canvas.
        """
        if self.modified:
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
                    if self.modified:
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
        if self.selected:
            index1 = self.selected[0]
            index2 = self.selected[1]
            x0 = positions[index1][0]
            y0 = positions[index1][1]
            x1 = positions[index2][0]
            y1 = positions[index2][1]
            self.canvas.create_line(x0+OFFSET, y0+OFFSET, x1+OFFSET, y1+OFFSET, fill="green", width=10)

    def clear_network(self):
        self.canvas.delete("all")

    def refresh_network(self):
        self.clear_network()
        if self.constructor.get_modified_adjacency() is None:
            self.modified = False
        else:
            self.modified = True
        self.draw_network()

    def modify_network(self, width, alpha):
        self.modified = True
        self.constructor.modify_adjacency(width, alpha)


    def customise_network(self, width, alpha):
        if width:
            self.constructor.change_width(self.selected[0], self.selected[1], width)
        if alpha:
            self.constructor.change_alpha(self.selected[0], self.selected[1], alpha)
        self.refresh_network()

    def draw_nodes(self):
        def circle(canvas, x, y, r, **kwargs):
            canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        positions = self.constructor.get_positions()
        node = 0
        for position in positions:
            circle(self.canvas,
                   position[0]+OFFSET,
                   position[1]+OFFSET,
                   10,
                   outline="gray",
                   fill="gray",
                   width=2)
            self.canvas.create_text(position[0]+OFFSET,
                                    position[1]+OFFSET,
                                    text="{0}".format(node))
            node += 1

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
        if not line and self.movement["move"]:
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

            self.refresh_network()
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

            self.refresh_network()

    def click_to_select(self, event):
        canvas = event.widget
        line = canvas.find_withtag("current")
        if not line:
            self.selected = False
            print("You misclicked!")
        else:
            self.selected = self.find_nodes(canvas)
        self.refresh_network()

    def get_modified_adjacency(self):
        return self.constructor.get_modified_adjacency()
