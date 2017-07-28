"""
This module constructs network of streets.
"""

import numpy as np
import json


OFFSET = 50
LEGEND_WIDTH = 100
STROKE_COLOUR = "black"
GRID_WIDTH = 3
WIDTH_SCALE = 0.5
JUNCTION_WIDTH = 20
JUNCTION_COLOUR = "gray"
MAX_RADIUS = 25
RESULT_COLOUR = "green"
INITIAL_DECIBELS = 120


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

    def set_grid(self, horizontals, verticals, length=100):
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
            print("To delete:")
            print(to_delete)
            self.__adjacency = np.delete(self.__adjacency, to_delete, axis=0)
            self.__adjacency = np.delete(self.__adjacency, to_delete, axis=1)
            self.__positions = np.delete(self.__positions, to_delete, axis=0)

            self.__nodes = int(self.__nodes - len(to_delete))


    def modify_adjacency(self, width=10, alpha=0.5):
        """
        This method creates new adjacency matrix with dictionaries of keys
        (alpha, street width, street length, orientation) instead of 1s.
        """
        if self.__stage == 1 or self.__stage == 2:
            self.__stage = 3
        try:
            width = float(width)
            alpha = float(alpha)
        except ValueError:
            raise ValueError("Width and absorption must be floating point numbers.")
        if width < 0:
            raise ValueError("Width must be a positive number.")
        if alpha < 0 or alpha > 1:
            raise ValueError("Absorption must be a number between 0 and 1.")
        assert self.__stage == 3
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
                        "width": width,
                        "length": length,
                        "orientation": orientation}
                    self.__modified_adjacency[j][i] = {
                        "alpha": alpha,
                        "width": width,
                        "length": length,
                        "orientation": (orientation+2)%4}

    def unmodify_adjacency(self):
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
        if width < 0:
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
        This method changes the absorption coefficient of street (i, j).
        """
        assert self.__stage == 3
        try:
            alpha = float(alpha)
        except ValueError:
            raise ValueError("Absorption must be a floating point number.")
        if alpha < 0 or alpha > 1:
            raise ValueError("Absorption must be a number between 0 and 1")
        if i in range(self.__nodes) and j in range(self.__nodes):
            if self.__modified_adjacency[i][j] != 0:
                self.__modified_adjacency[i][j]["alpha"] = alpha
                self.__modified_adjacency[j][i]["alpha"] = alpha
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range.")

    def get_horizontals(self):
        return self.__horizontals

    def get_verticals(self):
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
        return self.__stage

    def import_network(self, invalues):
        self.__horizontals = invalues["horizontals"]
        self.__verticals = invalues["verticals"]
        self.__nodes = invalues["nodes"]
        self.__adjacency = np.array(invalues["adjacency"])
        self.__modified_adjacency = invalues["modified_adjacency"]
        self.__positions = np.array(invalues["positions"])
        self.__stage = invalues["stage"]

    def export_network(self, filename):
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
        This method outputs file "output.html" with svg drawing of network.
        """
        positions = self.__positions
        if self.__stage == 3:
            adjacency = self.__modified_adjacency
            modified = True
        else:
            adjacency = self.__adjacency
            modified = False
        with open(filename, "w") as file:
            file.write(
                "<html><head><title>Network representation</title></head><body>")
            file.write("<svg width='{0}' height='{1}'>\n".format(
                positions[self.__nodes-1][0]+2*OFFSET+LEGEND_WIDTH,
                positions[self.__nodes-1][1]+2*OFFSET
                ))
            for i in range(self.__nodes):
                for j in range(i):
                    if adjacency[i][j] != 0:
                        [xi, yi] = positions[i]
                        [xj, yj] = positions[j]
                        if modified:
                            alpha = adjacency[i][j]["alpha"]
                            width = adjacency[i][j]["width"]
                            file.write(
                                "<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' \
style='stroke: rgb({4}, 0, {5}); stroke-width:{6}'/>\n".format(
                                xi+OFFSET, yi+OFFSET, xj+OFFSET, yj+OFFSET,
                                int(alpha*255), int((1-alpha)*255),
                                width*WIDTH_SCALE
                                ))
                        else:
                            file.write("<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' \
style='stroke: {4}; stroke-width: {5}'/>\n".format(
                                xi+OFFSET, yi+OFFSET, xj+OFFSET, yj+OFFSET,
                                STROKE_COLOUR, GRID_WIDTH
                                ))
            if modified:
                # Draw junctions (rectangles with numbers)
                counter = 0
                for position in positions:
                    file.write("<rect x='{0}' y='{1}' width='{2}' height='{2}' \
stroke='{3}' stroke-width='{4}' fill='{5}'/>".format(
                        position[0]-JUNCTION_WIDTH/2+OFFSET,
                        position[1]-JUNCTION_WIDTH/2+OFFSET,
                        JUNCTION_WIDTH, STROKE_COLOUR, GRID_WIDTH, JUNCTION_COLOUR
                        ))
                    file.write("<text x='{0}' y='{1}' fill='{2}', \
text-anchor='middle'>{3}</text>".format(
                        position[0]+OFFSET,
                        position[1]+OFFSET+JUNCTION_WIDTH/4,
                        STROKE_COLOUR, counter
                        ))
                    counter += 1

            if results:
                (X, Y, Z) = results
                for i in range(len(Z)):
                    radius = 20*np.log10(Z[i]*10**(INITIAL_DECIBELS/20))
                    # scale radius:
                    radius = radius/INITIAL_DECIBELS*MAX_RADIUS
                    file.write("<circle cx='{0}' cy='{1}' r='{2}' stroke='{3}' \
stroke-width='{4}' fill='rgb({5}, {6}, 0)'/>".format(
                        X[i]+OFFSET, Y[i]+OFFSET,
                        radius,
                        STROKE_COLOUR, GRID_WIDTH,
                        int(radius/MAX_RADIUS*255), 255-int(radius/MAX_RADIUS*255)
                        ))
                    counter += 1

            file.write("</svg></body></html>")
