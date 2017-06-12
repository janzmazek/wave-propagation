"""
This module constructs network of streets.
"""

import numpy as np


class Constructor(object):
    """
    This class of methods initialises a network object of specified dimensions,
    modifies the network using modifying methods, outputs the adjacency matrix
    of the network and outputs the visualisation in the svg format.
    """
    def __init__(self, horizontals, verticals, length=100):
        self.__horizontals = horizontals
        self.__verticals = verticals
        self.__nodes = horizontals*verticals
        self.__adjacency = self.__create_adjacency()
        self.__modified_adjacency = None
        self.__positions = self.__create_positions(length)
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
            positions[i][0] = i%self.__horizontals*length
            positions[i][1] = i//self.__horizontals*length
        return positions

    def move_horizontal_line(self, i, length):
        """
        This method moves the horizontal line i.
        """
        assert self.__stage == 0
        if i in range(self.__horizontals):
            for node in range(self.__nodes):
                if node//self.__horizontals == i:
                    self.__positions[node][1] += length
        else:
            raise ValueError("No such horizontal line.")

    def move_vertical_line(self, j, length):
        """
        This method moves the vertical line j.
        """
        assert self.__stage == 0
        if j in range(self.__verticals):
            for node in range(self.__nodes):
                if node%self.__horizontals == j:
                    self.__positions[node][0] += length
        else:
            raise ValueError("No such vertical line.")

    def delete_connection(self, i, j):
        """
        This method deletes the street (i, j).
        """
        # TODO: don't allow border to be deleted...
        if self.__stage == 0:
            self.__stage = 1 # set stage to 1 so lines cannot be moved
        assert self.__stage == 1
        if i in range(self.__nodes) and j in range(self.__nodes):
            if self.__adjacency[i][j] != 0:
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
                if len(to_delete) != 0:
                    self.__adjacency = np.delete(self.__adjacency, to_delete, axis=0)
                    self.__adjacency = np.delete(self.__adjacency, to_delete, axis=1)
                    self.__positions = np.delete(self.__positions, to_delete, axis=0)

                    self.__nodes = int(self.__nodes - len(to_delete))
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range.")

    def modify_adjacency(self, width=10, alpha=0.5):
        """
        This method creates new adjacency matrix with dictionaries of keys
        (alpha, street width, street length, orientation) instead of 1s.
        """
        if self.__stage == 0 or self.__stage == 1:
            self.__stage = 2
        assert self.__stage == 2
        self.__modified_adjacency = self.__adjacency.tolist() # To python structure
        for i in range(self.__nodes):
            for j in range(i):
                if self.__adjacency[i][j] == 1:
                    if self.__positions[i][1] == self.__positions[j][1]:
                        length = abs(self.__positions[i][0] - self.__positions[j][0])
                        if self.__positions[i][0] < self.__positions[j][0]:
                            orientation = 0
                        elif self.__positions[i][0] > self.__positions[j][0]:
                            orientation = 2
                        else:
                            raise ValueError("Points are at the same position.")
                    elif self.__positions[i][0] == self.__positions[j][0]:
                        length = abs(self.__positions[i][1] - self.__positions[j][1])
                        if self.__positions[i][1] < self.__positions[j][1]:
                            orientation = 1
                        elif self.__positions[i][1] > self.__positions[j][1]:
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

    def change_width(self, i, j, width):
        """
        This method changes the street width of street (i, j).
        """
        assert self.__stage == 2
        assert width > 0
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
        assert self.__stage == 2
        assert alpha >= 0 and alpha <= 1
        if i in range(self.__nodes) and j in range(self.__nodes):
            if self.__modified_adjacency[i][j] != 0:
                self.__modified_adjacency[i][j]["alpha"] = alpha
                self.__modified_adjacency[j][i]["alpha"] = alpha
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range.")

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

    def output_network(self):
        """
        This method outputs file "output.html" with svg drawing of network.
        """
        with open("output.html", "w") as file:
            file.write("<html><head><title>Network representation</title></head><body>")
            file.write("<svg width='{0}' height='{1}'>\n".format(
                self.__positions[self.__nodes-1][0], self.__positions[self.__nodes-1][1]))
            for i in range(self.__nodes):
                for j in range(i):
                    if self.__modified_adjacency[i][j] is not 0:
                        [xi, yi] = self.__positions[i]
                        [xj, yj] = self.__positions[j]
                        alpha = self.__modified_adjacency[i][j]["alpha"]
                        width = self.__modified_adjacency[i][j]["width"]/10
                        file.write(
                            "<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' \
                            style='stroke: rgb({4}, 0, {5}); stroke-width:{6}'/>\n".format(
                                xi, yi, xj, yj, int(alpha*255), int((1-alpha)*255), width))
            file.write("</svg></body></html>")
