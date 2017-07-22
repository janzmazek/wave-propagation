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
        self.selected = False

    def done_creating(self, horizontals, verticals, length):
        self.constructor.set_grid(horizontals, verticals, length)
        self.view.switch_tools("MovingTools")
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=False
                                 )

    def click_to_move(self, endpoints, offset):
        if not endpoints:
            self.click_endpoints = False
            print("You misclicked")
            return
        self.click_endpoints = (endpoints, offset)

    def release_to_move(self, endpoint):
        if not endpoint:
            self.click_endpoints = False
            self.release_point = False
            return
        self.release_point = endpoint
        self.move()

    def move(self):
        start_line = self.find_line_properties(*self.click_endpoints)
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


    def find_line_properties(self, endpoints, offset):
        (node1, node2) = self.find_nodes(endpoints, offset)
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

    def find_nodes(self, endpoints, offset):
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
                                 modified=False
                                 )

    def click_to_delete(self, endpoints, offset):
        if not endpoints:
            print("You misclicked")
            return
        nodes = self.find_nodes(endpoints, offset)
        self.constructor.delete_connection(*nodes)
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=False
                                 )

    def done_deleting(self):
        self.view.switch_tools("ModifyingTools")
        self.view.refresh_canvas(self.constructor.get_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=False
                                 )
        self.view.remove_binds()

    def done_modifying(self, width, alpha):
        self.view.switch_tools("CustomisingTools")
        self.constructor.modify_adjacency(width, alpha)
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=True
                                 )

    def click_to_select(self, endpoints, offset):
        if not endpoints:
            self.selected = False
        else:
            self.selected = self.find_nodes(endpoints, offset)
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=True,
                                 selected=self.selected
                                 )

    def customise_click(self, width, alpha):
        if not self.selected:
            self.view.show_message("Error", "Nothing selected.")
            return
        if width is not False and width < 0:
            self.view.show_message("Error", "Width must be a positive number.")
            raise ValueError("Width must be a positive number.")
        if alpha is not False and (alpha < 0 or alpha > 1):
            self.view.show_message("Error",
                "Absorption coefficient must be between 0 and 1")
            raise ValueError("Absorption coefficient must be between 0 and 1")
        self.constructor.change_width(*self.selected, width)
        self.constructor.change_alpha(*self.selected, alpha)
        self.selected = False
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=True,
                                 selected=self.selected
                                 )
    def done_customising(self):
        self.view.switch_tools("ModelTools")
        self.selected = False
        self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                 self.constructor.get_positions(),
                                 modified=True,
                                 selected=self.selected,
                                 numbered=True
                                 )

    def compute_click(self, starting_1, starting_2, ending_1, ending_2, threshold):
        self.model.set_source(starting_1, starting_2)
        self.model.set_receiver(ending_1, ending_2)
        self.model.set_threshold(threshold)
        self.model.set_adjacency(self.constructor.get_modified_adjacency())
        power = self.model.solve()
        self.view.show_message("Result", "Power percentage: {0}".format(power))

    def compute_all_click(self, starting_1, starting_2, threshold):
        self.model.set_source(starting_1, starting_2)
        self.model.set_threshold(threshold)
        plotter = Plotter(self.constructor, self.model)
        plotter.plot("result.png")


    def import_network(self, filename):
        with open(filename, "r") as file:
            invalues = json.load(file)
        modified_adjacency = invalues["modified_adjacency"]
        self.constructor.import_network(invalues)
        if modified_adjacency is None:
            self.view.switch_tools("ModifyingTools")
            self.view.refresh_canvas(self.constructor.get_adjacency(),
                                     self.constructor.get_positions(),
                                     modified=False
                                     )
            self.view.remove_binds()
            self.view.add_bind("ModifyingTools")
        else:
            self.view.switch_tools("ModelTools")
            self.view.refresh_canvas(self.constructor.get_modified_adjacency(),
                                     self.constructor.get_positions(),
                                     modified=True,
                                     selected=self.selected,
                                     numbered=True
                                     )
            self.view.remove_binds()

    def export_network(self, filename):
        outvalues = self.constructor.export_network()
        with open(filename, 'w') as file:
            json.dump(outvalues, file)


    def file_click(self, option):
        if option in ["export", "svg"] and self.constructor.get_stage() == 0:
            return
        self.view.show_filedialog(option)

    def window_click(self, option):
        self.view.resize_window(option)

    def tools_click(self, option):
        if self.constructor.get_stage() == 0:
            return
        if option in ["CreationTools", "MovingTools", "DeletingTools", "ModifyingTools"]:
            self.constructor.unmodify_adjacency()
            self.view.switch_tools(option)
            modified = False
        elif option == "CustomisingTools":
            if self.constructor.get_modified_adjacency() == None:
                modified = False
                self.view.switch_tools("ModifyingTools")
            else:
                self.view.switch_tools(option)
                modified = True
        if modified:
            adjacency = self.constructor.get_modified_adjacency()
        else:
            adjacency = self.constructor.get_adjacency()
        positions = self.constructor.get_positions()
        self.view.refresh_canvas(adjacency, positions, modified)

    def about_click(self):
        self.view.show_message("About", "Hello")
