import json

class Controller(object):
    """docstring for Controller."""
    def __init__(self, constructor, model, view):
        self.constructor = constructor
        self.model = model
        self.view = view

        self.view.register(self) # Give "view" object access to controller

        # canvas bind variables
        self.click_endpoints = False
        self.release_point = False
        self.modified = False
        self.selected = False
        self.numbered = False

    def done_creating(self, horizontals, verticals, length):
        try:
            self.constructor.set_grid(horizontals, verticals, length)
        except ValueError as e:
            self.view.show_message("Error", e)
            return
        self.view.switch_tools("MovingTools")
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified
                                 )

    def click_to_move(self, endpoints, offset):
        if not endpoints:
            self.click_endpoints = False
            print("You misclicked.")
            return
        self.click_endpoints = (endpoints, offset)

    def release_to_move(self, endpoint):
        if not endpoint:
            self.click_endpoints = False
            self.release_point = False
            return
        self.release_point = endpoint
        if self.click_endpoints:
            self.move()

    def move(self):
        start_line = self.__find_line_properties(*self.click_endpoints)
        (end_x, end_y) = self.release_point
        start_index = start_line["line_index"]
        start = start_line["start"]
        if start_line["orientation"] == "horizontal":
            end = end_y
            delta = end - start
            self.constructor.move_horizontal_line(start_index, delta)
        else:
            end = end_x
            delta = end - start
            self.constructor.move_vertical_line(start_index, delta)
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=False
                                 )


    def __find_line_properties(self, endpoints, offset):
        (node1, node2) = self.__find_nodes(endpoints, offset)
        verticals = self.constructor.get_verticals()
        positions = self.constructor.get_positions()
        if positions[node1][0] == positions[node2][0]:
            orientation = "vertical"
            start = positions[node1][0]
            line_index = node1%verticals
        elif positions[node1][1] == positions[node2][1]:
            orientation = "horizontal"
            start = positions[node1][1]
            line_index = node1//verticals
        start = start + offset

        return {"orientation": orientation,
                "start": start,
                "line_index": line_index
                }

    def __find_nodes(self, endpoints, offset):
        node1, node2 = None, None
        (point1, point2) = endpoints
        counter = 0
        positions = self.constructor.get_positions()
        for position in positions:
            if position[0]+offset == point1[0] and \
               position[1]+offset == point1[1]:
                node1 = counter
            elif position[0]+offset == point2[0] and \
                 position[1]+offset == point2[1]:
                node2 = counter
            counter += 1
        return (node1, node2)


    def done_moving(self):
        self.view.switch_tools("DeletingTools")
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified
                                 )

    def click_to_delete(self, endpoints, offset):
        if not endpoints:
            print("You misclicked")
            return
        nodes = self.__find_nodes(endpoints, offset)
        self.constructor.delete_connection(*nodes)
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified
                                 )

    def done_deleting(self):
        self.view.switch_tools("ModifyingTools")
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified
                                 )
        self.view.remove_binds()

    def done_modifying(self, width, alpha):
        try:
            self.constructor.modify_adjacency(width, alpha)
        except ValueError as e:
            self.view.show_message("Error", e)
            return
        self.view.switch_tools("CustomisingTools")
        self.modified = True
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified
                                 )

    def click_to_select(self, endpoints, offset):
        if not endpoints:
            self.selected = False
        else:
            self.selected = self.__find_nodes(endpoints, offset)
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified,
                                 selected=self.selected
                                 )

    def customise_click(self, width, alpha):
        if not self.selected:
            self.view.show_message("Error", "Nothing selected.")
            return
        try:
            self.constructor.change_width(*self.selected, width)
            self.constructor.change_alpha(*self.selected, alpha)
        except ValueError as e:
            self.view.show_message("Error", e)
            return
        self.selected = False
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified,
                                 selected=self.selected
                                 )
    def done_customising(self):
        self.view.switch_tools("ModelTools")
        self.selected = False
        self.numbered = True
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=self.modified,
                                 selected=self.selected,
                                 numbered=self.numbered
                                 )

    def compute_click(self, starting_1, starting_2, ending_1, ending_2, threshold):
        self.model.set_adjacency(self.constructor.get_modified_adjacency())
        try:
            self.model.set_source(starting_1, starting_2)
            self.model.set_receiver(ending_1, ending_2)
            self.model.set_threshold(threshold)
            (power, error) = self.model.solve()
        except ValueError as e:
            self.view.show_message("Error", e)
            return
        power = format(power*100, '.3f')
        error = format(error*100, '.3f')
        self.view.show_message("Result", "Power: {0} % ± {1} %".format(power, error))

    def compute_all_click(self, starting_1, starting_2, threshold):
        self.model.set_adjacency(self.constructor.get_modified_adjacency())
        try:
            self.model.set_source(starting_1, starting_2)
            self.model.set_threshold(threshold)
        except ValueError as e:
            self.view.show_message("Error", e)
            return
        results = self.model.solve_all(self.constructor.get_positions())
        filename = self.view.save_as(".html")
        if filename is None:
            return
        self.constructor.draw_network(filename, results)

    def file_click(self, option):
        if option in ["export_network", "draw_network"] and self.constructor.get_stage() == 0:
            return
        if option == "import_network":
            filename = self.view.open()
            if filename is None:
                return
            self.__import_network(filename)

        elif option == "export_network":
            filename = self.view.save_as(".json")
            if filename is None:
                return
            self.constructor.export_network(filename)

        elif option == "draw_network":
            filename = self.view.save_as(".html")
            if filename is None:
                return
            self.constructor.draw_network(filename)

        elif option == "set_background":
            filename = self.view.open()
            if filename is None:
                return
            self.view.canvas.set_background(filename)

        elif option == "remove_background":
            self.view.canvas.remove_background()

        if self.modified:
            adjacency = self.constructor.get_modified_adjacency()
        else:
            adjacency = self.constructor.get_adjacency()
        self.view.refresh_canvas(adjacency,
                                 self.constructor.get_positions(),
                                 modified=self.modified,
                                 selected=self.selected,
                                 numbered=self.numbered
                                 )

    def __import_network(self, filename):
        with open(filename, "r") as file:
            invalues = json.load(file)
        modified_adjacency = invalues["modified_adjacency"]
        self.constructor.import_network(invalues)
        if modified_adjacency is None:
            self.view.switch_tools("ModifyingTools")
            self.modified = False
            self.view.remove_binds()
        else:
            self.view.switch_tools("ModelTools")
            self.modified = True
            self.numbered = True
            self.view.remove_binds()

    def window_click(self, option):
        self.view.resize_window(option)

    def tools_click(self, option):
        if self.constructor.get_stage() == 0:
            return
        if option in ["CreationTools", "MovingTools", "DeletingTools", "ModifyingTools"]:
            self.constructor.unmodify_adjacency()
            self.modified, self.numbered = False, False
            if option == "CreationTools":
                self.constructor.unset_grid()
            elif option == "MovingTools":
                self.constructor.set_grid(self.constructor.get_horizontals(),
                                          self.constructor.get_verticals(),
                                          100
                                          )
            self.view.switch_tools(option)
        elif option == "CustomisingTools":
            if self.constructor.get_modified_adjacency() == None:
                self.modified = False
                self.view.switch_tools("ModifyingTools")
            else:
                self.modified = True
                self.view.switch_tools(option)
        if self.modified:
            adjacency = self.constructor.get_modified_adjacency()
        else:
            adjacency = self.constructor.get_adjacency()
        positions = self.constructor.get_positions()
        self.view.refresh_canvas(adjacency, positions, self.modified)

    def about_click(self):
        self.view.show_message("About", "Hello")
        return
