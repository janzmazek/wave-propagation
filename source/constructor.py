"""
This module constructs network of streets.
"""

import numpy as np
import json

# Adobe flat UI colour scheme
DARK_BLUE = "#2C3E50"
MEDIUM_BLUE = "#2980B9"
LIGHT_BLUE = "#3498DB"
RED = "#E74C3C"
WHITE = "#ECF0F1"

# Colour parameters
STROKE_COLOUR = DARK_BLUE
STREET_COLOUR = DARK_BLUE
JUNCTION_COLOUR = MEDIUM_BLUE
JUNCTION_TEXT = DARK_BLUE
RESULTS_COLOUR = RED
RESULTS_TEXT = DARK_BLUE

# Dimensions
OFFSET = 50
STREET_WIDTH = 8
STROKE_WIDTH = 2
JUNCTION_WIDTH = 20
MAX_RADIUS = 25
INITIAL_DECIBELS = 120

# Max absorption
MAX_ABSORPTION = 0.1

# Don't plot absorption coefficients (option)
ABSORPTION = False


class Constructor(object):
    """
    This class of methods initialises a network object of specified dimensions,
    modifies the network using modifying methods, outputs the adjacency matrix
    of the network and outputs the visualisation in the svg format.
    """
    def __init__(self):
        self.__horizontals = None
        self.__verticals = None
        self.__nodes = None
        self.__adjacency = None
        self.__modified_adjacency = None
        self.__positions = None
        self.__stage = 0

    def set_grid(self, horizontals, verticals, length):
        """
        This setter method sets stage 1 (setting and moving) of the construction.
        """
        try:
            horizontals = int(horizontals)
            verticals = int(verticals)
        except ValueError:
            raise ValueError("Horizontals and verticals must be integers.")
        try:
            length = float(length)
        except ValueError:
            raise ValueError("Length must be a floating point number.")
        for quantity in [horizontals, verticals, length]:
            if quantity < 0:
                raise ValueError(
                    "Horizontals, verticals and length must be positive numbers.")
        self.__horizontals = horizontals
        self.__verticals = verticals
        self.__nodes = horizontals*verticals
        self.__adjacency = self.__create_adjacency()
        self.__modified_adjacency = None
        self.__positions = self.__create_positions(length)
        self.__stage = 1

    def unset_grid(self):
        """
        This method is used to set the network to the stage 0 (instantiation) of
        the construction.
        """
        self.__horizontals = None
        self.__verticals = None
        self.__nodes = None
        self.__adjacency = None
        self.__modified_adjacency = None
        self.__positions = None
        self.__stage = 0


    def __create_adjacency(self):
        """
        This private method returns initial adjacency matrix.
        """
        adjacency = np.zeros((self.__nodes, self.__nodes), dtype=np.int)
        # Normal adjacency matrix for grid network
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if (j == i+1 and j%self.__verticals != 0) or \
                   (j == i-1 and i%self.__verticals != 0) or \
                    j == i+self.__verticals or \
                    j == i-self.__verticals:
                    adjacency[i][j] = 1
        return adjacency

    def __create_positions(self, length):
        """
        This private method returns initial positions matrix.
        """
        positions = np.zeros((self.__nodes, 2))
        for i in range(self.__nodes):
            positions[i][0] = i%self.__verticals*length
            positions[i][1] = i//self.__verticals*length
        return positions

    def move_horizontal_line(self, i, length):
        """
        This method moves the horizontal line i.
        """
        assert self.__stage == 1
        if i in range(self.__horizontals):
            for node in range(self.__nodes):
                if node//self.__verticals == i:
                    self.__positions[node][1] += length
        else:
            raise ValueError("No such horizontal line.")

    def move_vertical_line(self, j, length):
        """
        This method moves the vertical line j.
        """
        assert self.__stage == 1
        if j in range(self.__verticals):
            for node in range(self.__nodes):
                if node%self.__verticals == j:
                    self.__positions[node][0] += length
        else:
            raise ValueError("No such vertical line.")

    def delete_connection(self, i, j):
        """
        This method deletes the street (i, j).
        """
        if self.__stage == 1:
            self.__stage = 2 # set stage to 1 so lines cannot be moved
        assert self.__stage == 2
        if i not in range(self.__nodes) or j not in range(self.__nodes):
            raise ValueError("Nodes out of range.")
        if self.__adjacency[i][j] == 0:
            raise ValueError("Junctions are not neighbours.")
        self.__adjacency[i][j] = 0
        self.__adjacency[j][i] = 0
        to_delete = []
        if sum(self.__adjacency[i]) == 2:
            connections = []
            for k in range(self.__nodes):
                if self.__adjacency[i][k] == 1:
                    connections.append(k)
            if (self.__positions[i][0] == self.__positions[connections[0]][0] and \
                self.__positions[i][0] == self.__positions[connections[1]][0]) or \
               (self.__positions[i][1] == self.__positions[connections[0]][1] and \
                self.__positions[i][1] == self.__positions[connections[1]][1]):
                self.__adjacency[connections[0]][connections[1]] = 1
                self.__adjacency[connections[1]][connections[0]] = 1
                to_delete.append(i)
        elif sum(self.__adjacency[i]) == 0:
            to_delete.append(i)
        if sum(self.__adjacency[j]) == 2:
            connections = []
            for k in range(self.__nodes):
                if self.__adjacency[j][k] == 1:
                    connections.append(k)
            if (self.__positions[j][0] == self.__positions[connections[0]][0] and \
                self.__positions[j][0] == self.__positions[connections[1]][0]) or \
               (self.__positions[j][1] == self.__positions[connections[0]][1] and \
                self.__positions[j][1] == self.__positions[connections[1]][1]):
                self.__adjacency[connections[0]][connections[1]] = 1
                self.__adjacency[connections[1]][connections[0]] = 1
                to_delete.append(j)
        elif sum(self.__adjacency[j]) == 0:
            to_delete.append(j)
        if len(to_delete) != 0:
            self.__adjacency = np.delete(self.__adjacency, to_delete, axis=0)
            self.__adjacency = np.delete(self.__adjacency, to_delete, axis=1)
            self.__positions = np.delete(self.__positions, to_delete, axis=0)

            self.__nodes = int(self.__nodes - len(to_delete))


    def modify_adjacency(self, width, alpha, beta):
        """
        This method creates new adjacency matrix with dictionaries of keys
        (alpha, beta, street width, street length, orientation) instead of 1s.
        """
        if self.__stage == 1 or self.__stage == 2:
            self.__stage = 3
        assert self.__stage == 3
        try:
            width = float(width)
            alpha = float(alpha)
            beta = float(beta)
        except ValueError:
            raise ValueError("Width and absorption must be floating point numbers.")
        if width <= 0:
            raise ValueError("Width must be a positive number.")
        if alpha < 0 or alpha > 1 or beta < 0 or beta > 1:
            raise ValueError("Absorption must be a number between 0 and 1.")
        self.__modified_adjacency = self.__adjacency.tolist() # To python structure
        positions = self.__positions
        for i in range(self.__nodes):
            for j in range(i):
                if self.__adjacency[i][j] == 1:
                    if positions[i][1] == positions[j][1]:
                        length = abs(positions[i][0] - positions[j][0]).tolist()
                        if positions[i][0] < positions[j][0]:
                            orientation = 0
                        elif positions[i][0] > positions[j][0]:
                            orientation = 2
                        else:
                            raise ValueError("Points are at the same position.")
                    elif positions[i][0] == positions[j][0]:
                        length = abs(positions[i][1] - positions[j][1]).tolist()
                        if positions[i][1] < positions[j][1]:
                            orientation = 1
                        elif positions[i][1] > positions[j][1]:
                            orientation = 3
                        else:
                            raise ValueError("Points are at the same position.")

                    else:
                        raise ValueError("Points are not colinear.")

                    self.__modified_adjacency[i][j] = {
                        "alpha": alpha,
                        "beta": beta,
                        "width": width,
                        "length": length,
                        "orientation": orientation}
                    self.__modified_adjacency[j][i] = {
                        "alpha": alpha,
                        "beta": beta,
                        "width": width,
                        "length": length,
                        "orientation": (orientation+2)%4}

    def unmodify_adjacency(self):
        """
        This method is used to set the stage to stage 2 (deleting) of the
        construction.
        """
        self.__stage = 2
        self.__modified_adjacency = None

    def change_width(self, i, j, width):
        """
        This method changes the street width of street (i, j).
        """
        assert self.__stage == 3
        try:
            width = float(width)
        except ValueError:
            raise ValueError("Width must be a floating point number.")
        if width <= 0:
            raise ValueError("Width must be a positive number.")
        if i in range(self.__nodes) and j in range(self.__nodes):
            if self.__modified_adjacency[i][j] is not 0:
                self.__modified_adjacency[i][j]["width"] = width
                self.__modified_adjacency[j][i]["width"] = width
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range")

    def change_alpha(self, i, j, alpha):
        """
        This method changes the wall absorption of street (i, j).
        """
        assert self.__stage == 3
        try:
            alpha = float(alpha)
        except ValueError:
            raise ValueError("Absorption must be a floating point number.")
        if alpha < 0 or alpha > 1:
            raise ValueError("Absorption must be a number between 0 and 1")
        if i not in range(self.__nodes) or j not in range(self.__nodes):
            raise ValueError("Nodes out of range.")
        if self.__modified_adjacency[i][j] == 0:
            raise ValueError("Junctions are not neighbours.")
        self.__modified_adjacency[i][j]["alpha"] = alpha
        self.__modified_adjacency[j][i]["alpha"] = alpha

    def change_beta(self, i, j, beta):
        """
        This method changes the air absorption of street (i, j).
        """
        assert self.__stage == 3
        try:
            beta = float(beta)
        except ValueError:
            raise ValueError("Absorption must be a floating point number.")
        if beta < 0 or beta > 1:
            raise ValueError("Absorption must be a number between 0 and 1")
        if i not in range(self.__nodes) or j not in range(self.__nodes):
            raise ValueError("Nodes out of range.")
        if self.__modified_adjacency[i][j] == 0:
            raise ValueError("Junctions are not neighbours.")
        self.__modified_adjacency[i][j]["beta"] = beta
        self.__modified_adjacency[j][i]["beta"] = beta

    def get_horizontals(self):
        """
        This getter method returns the number of horizontal streets.
        """
        return self.__horizontals

    def get_verticals(self):
        """
        This getter method returns the number of vertical streets.
        """
        return self.__verticals

    def get_adjacency(self):
        """
        This getter method returns the normal adjacency matrix.
        """
        return self.__adjacency

    def get_modified_adjacency(self):
        """
        This getter method returns the modified adjacency matrix.
        """
        return self.__modified_adjacency

    def get_positions(self):
        """
        This getter method returns the positions matrix.
        """
        return self.__positions

    def get_stage(self):
        """
        This getter method returns current stage index.
        """
        return self.__stage

    def import_network(self, invalues):
        """
        This method is used to import existing network from the invalues
        dictionary.
        """
        self.__horizontals = invalues["horizontals"]
        self.__verticals = invalues["verticals"]
        self.__nodes = invalues["nodes"]
        self.__adjacency = np.array(invalues["adjacency"])
        self.__modified_adjacency = invalues["modified_adjacency"]
        self.__positions = np.array(invalues["positions"])
        self.__stage = invalues["stage"]

    def export_network(self, filename):
        """
        This method is used to export currently constructed network to json
        format to some file.
        """
        data = {
                "horizontals": self.__horizontals,
                "verticals": self.__verticals,
                "nodes": self.__nodes,
                "adjacency": self.__adjacency.tolist(),
                "modified_adjacency": self.__modified_adjacency,
                "positions": self.__positions.tolist(),
                "stage": self.__stage
                }
        with open(filename, "w") as file:
            json.dump(data, file)

    def draw_network(self, filename, results=False):
        """
        This method outputs file "output.html" with svg drawing of network and
        optinally plots the results.
        """
        def get_hex_fill(coefficient, max_absorption):
            red = hex(int(coefficient/max_absorption*255))
            red = red[-2:] if len(red)==4 else "0{0}".format(red[-1])
            blue = hex(int((1-coefficient/max_absorption)*255))
            blue = blue[-2:] if len(blue)==4 else "0{0}".format(blue[-1])
            fill = "#{0}00{1}".format(red, blue)
            return fill

        def svg_header(width, height):
            return "<svg width='{0}' height='{1}'>\n".format(width, height)

        def svg_line(x1, y1, x2, y2, fill=STREET_COLOUR, width=STREET_WIDTH):
            return "<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' \
style='stroke: {4}; stroke-width: {5}'/>\n".format(x1+OFFSET, y1+OFFSET,
                                                  x2+OFFSET, y2+OFFSET,
                                                  fill, width)

        def svg_square(x, y):
            return "<rect x='{0}' y='{1}' width='{2}' height='{2}' \
style='stroke: {3}; stroke-width: {4}; fill: {5}'/>\n".format(x-JUNCTION_WIDTH/2+OFFSET,
                                                       y-JUNCTION_WIDTH/2+OFFSET,
                                                       JUNCTION_WIDTH,
                                                       STROKE_COLOUR,
                                                       STROKE_WIDTH,
                                                       JUNCTION_COLOUR
                                                       )

        def svg_circle(x, y, r, fill):
            return "<circle cx='{0}' cy='{1}' r='{2}' style='stroke: {3}; \
stroke-width: {4}; fill: {5}'/>\n".format(x+OFFSET,
                                           y+OFFSET,
                                           r,
                                           STROKE_COLOUR,
                                           STROKE_WIDTH,
                                           fill
                                           )

        def svg_text(x, y, colour, size, text):
            move = (size-15)/4 # adjust text position
            return "<text text-anchor='middle' x='{0}' y='{1}' \
style='fill: {2}; font-size: {3}'>{4}</text>\n".format(x+OFFSET,
                                y+OFFSET+JUNCTION_WIDTH/4 + move,
                                colour,
                                size,
                                text
                                )

        positions = self.__positions
        if self.__stage == 3:
            adjacency = self.__modified_adjacency
            modified = True
        else:
            adjacency = self.__adjacency
            modified = False

        with open(filename, "w") as file:
            width = positions[self.__nodes-1][0]+2*OFFSET
            height = positions[self.__nodes-1][1]+2*OFFSET
            file.write(svg_header(width, height))
            # Draw walls if modified (with absorption)
            if modified and ABSORPTION:
                for i in range(self.__nodes):
                    for j in range(i):
                        if adjacency[i][j] != 0:
                            [xi, yi] = positions[i]
                            [xj, yj] = positions[j]
                            alpha = adjacency[i][j]["alpha"]
                            alpha_fill = get_hex_fill(alpha, MAX_ABSORPTION)
                            width = adjacency[i][j]["width"]
                            translation = width/2
                            if xi == xj:
                                file.write(svg_line(xi-translation, yi,
                                                    xj-translation, yj,
                                                    alpha_fill, width
                                                    ))
                                file.write(svg_line(xi+translation, yi,
                                                    xj+translation, yj,
                                                    alpha_fill, width
                                                    ))
                            elif yi == yj:
                                file.write(svg_line(xi, yi-translation,
                                                    xj, yj-translation,
                                                    alpha_fill, width
                                                    ))
                                file.write(svg_line(xi, yi+translation,
                                                    xj, yj+translation,
                                                    alpha_fill, width
                                                    ))


            # Draw streets (with absorption if modified)
            for i in range(self.__nodes):
                for j in range(i):
                    if adjacency[i][j] != 0:
                        [xi, yi] = positions[i]
                        [xj, yj] = positions[j]
                        if not modified or not ABSORPTION:
                            file.write(svg_line(xi, yi, xj, yj))
                        else:
                            beta = adjacency[i][j]["beta"]
                            beta_fill = get_hex_fill(beta, MAX_ABSORPTION)
                            width = adjacency[i][j]["width"]
                            file.write(svg_line(xi, yi, xj, yj,
                                                beta_fill, width
                                                ))

            # Draw junctions (rectangles with numbers)
            counter = 0
            for position in positions:
                file.write(svg_square(position[0], position[1]))
                file.write(svg_text(position[0], position[1], JUNCTION_TEXT, 15, counter))
                counter += 1

            # Draw results
            if results:
                (X, Y, Z) = results
                for i in range(len(Z)):
                    decibels = 20*np.log10(Z[i]*10**(INITIAL_DECIBELS/20))
                    if decibels < 0:
                        continue
                    # Radius
                    radius = (decibels/INITIAL_DECIBELS)*MAX_RADIUS
                    file.write(svg_circle(X[i], Y[i], radius, RESULTS_COLOUR))
                    if decibels > 20:
                        file.write(svg_text(X[i], Y[i], RESULTS_TEXT, radius, int(round(decibels))))

            file.write("</svg>")
