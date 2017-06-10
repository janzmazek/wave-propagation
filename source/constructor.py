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
        self.horizontals = horizontals
        self.verticals = verticals
        self.nodes = horizontals*verticals
        self.adjacency = self.create_adjacency()
        self.modified_adjacency = None
        self.positions = self.create_positions(length)

    def create_adjacency(self):
        """
        This method returns initial adjacency matrix.
        """
        adjacency = np.zeros((self.nodes, self.nodes), dtype=np.int)
        # Normal adjacency matrix for grid network
        for i in range(self.nodes):
            for j in range(self.nodes):
                if (j == i+1 and j%self.verticals != 0) or \
                   (j == i-1 and i%self.verticals != 0) or \
                    j == i+self.verticals or \
                    j == i-self.verticals:
                    adjacency[i][j] = 1
        return adjacency

    def create_positions(self, length):
        """
        This method returns initial positions matrix.
        """
        positions = np.zeros((self.nodes, 2))
        for i in range(self.nodes):
            positions[i][0] = i%self.horizontals*length
            positions[i][1] = i//self.horizontals*length
        return positions

    def move_horizontal_line(self, i, length):
        """
        This method moves the horizontal line i.
        """
        if i in range(self.horizontals):
            for node in range(self.nodes):
                if node//self.horizontals == i:
                    self.positions[node][1] += length
        else:
            raise ValueError("No such horizontal line.")

    def move_vertical_line(self, j, length):
        """
        This method moves the vertical line j.
        """
        if j in range(self.verticals):
            for node in range(self.nodes):
                if node%self.horizontals == j:
                    self.positions[node][0] += length
        else:
            raise ValueError("No such vertical line.")

    def delete_connection(self, i, j):
        """
        This method deletes the street (i, j).
        """
        # TODO: don't allow border to be deleted...
        if i in range(self.nodes) and j in range(self.nodes):
            if self.adjacency[i][j] != 0:
                self.adjacency[i][j] = 0
                self.adjacency[j][i] = 0
                to_delete = []
                if sum(self.adjacency[i]) == 2:
                    connections = []
                    for k in range(self.nodes):
                        if self.adjacency[i][k] == 1:
                            connections.append(k)
                    if (self.positions[i][0] == self.positions[connections[0]][0] and \
                        self.positions[i][0] == self.positions[connections[1]][0]) or \
                       (self.positions[i][1] == self.positions[connections[0]][1] and \
                        self.positions[i][1] == self.positions[connections[1]][1]):
                        self.adjacency[connections[0]][connections[1]] = 1
                        self.adjacency[connections[1]][connections[0]] = 1
                        to_delete.append(i)
                if sum(self.adjacency[j]) == 2:
                    connections = []
                    for k in range(self.nodes):
                        if self.adjacency[j][k] == 1:
                            connections.append(k)
                    if (self.positions[j][0] == self.positions[connections[0]][0] and \
                        self.positions[j][0] == self.positions[connections[1]][0]) or \
                       (self.positions[j][1] == self.positions[connections[0]][1] and \
                        self.positions[j][1] == self.positions[connections[1]][1]):
                        self.adjacency[connections[0]][connections[1]] = 1
                        self.adjacency[connections[1]][connections[0]] = 1
                        to_delete.append(j)
                if len(to_delete) != 0:
                    self.adjacency = np.delete(self.adjacency, to_delete, axis=0)
                    self.adjacency = np.delete(self.adjacency, to_delete, axis=1)
                    self.positions = np.delete(self.positions, to_delete, axis=0)

                    self.nodes = int(self.nodes - len(to_delete))
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range.")

    def modify_adjacency(self, width=10, alpha=0.5):
        """
        This method creates new adjacency matrix with dictionaries of keys
        (alpha, street width, street length, orientation) instead of 1s.
        """
        self.modified_adjacency = self.adjacency.tolist() # To python structure
        for i in range(self.nodes):
            for j in range(i):
                if self.adjacency[i][j] == 1:
                    if self.positions[i][1] == self.positions[j][1]:
                        length = abs(self.positions[i][0] - self.positions[j][0])
                        if self.positions[i][0] < self.positions[j][0]:
                            orientation = 0
                        elif self.positions[i][0] > self.positions[j][0]:
                            orientation = 2
                        else:
                            raise ValueError("Points are at the same position.")
                    elif self.positions[i][0] == self.positions[j][0]:
                        length = abs(self.positions[i][1] - self.positions[j][1])
                        if self.positions[i][1] < self.positions[j][1]:
                            orientation = 1
                        elif self.positions[i][1] > self.positions[j][1]:
                            orientation = 3
                        else:
                            raise ValueError("Points are at the same position.")

                    else:
                        raise ValueError("Points are not colinear.")

                    self.modified_adjacency[i][j] = {
                        "alpha": alpha,
                        "width": width,
                        "length": length,
                        "orientation": orientation}
                    self.modified_adjacency[j][i] = {
                        "alpha": alpha,
                        "width": width,
                        "length": length,
                        "orientation": (orientation+2)%4}

    def change_width(self, i, j, width):
        """
        This method changes the street width of street (i, j).
        """
        assert width>0
        if i in range(self.nodes) and j in range(self.nodes):
            if self.modified_adjacency[i][j] is not 0:
                self.modified_adjacency[i][j]["width"] = width
                self.modified_adjacency[j][i]["width"] = width
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range")

    def change_alpha(self, i, j, alpha):
        """
        This method changes the absorption coefficient of street (i, j).
        """
        assert alpha>=0 and alpha<=1
        if i in range(self.nodes) and j in range(self.nodes):
            if self.modified_adjacency[i][j] != 0:
                self.modified_adjacency[i][j]["alpha"] = alpha
                self.modified_adjacency[j][i]["alpha"] = alpha
            else:
                raise ValueError("Junctions are not neighbours.")
        else:
            raise ValueError("Nodes out of range.")

    def get_modified_adjacency(self):
        """
        This getter method returns the modified adjacency matrix.
        """
        return self.modified_adjacency


    def output_network(self):
        """
        This method outputs file "output.html" with svg drawing of network.
        """
        with open("output.html", "w") as file:
            file.write("<html><head><title>Network representation</title></head><body>")
            file.write("<svg width='{0}' height='{1}'>\n".format(
                self.positions[self.nodes-1][0], self.positions[self.nodes-1][1]))
            for i in range(self.nodes):
                for j in range(i):
                    if self.modified_adjacency[i][j] is not 0:
                        [xi, yi] = self.positions[i]
                        [xj, yj] = self.positions[j]
                        alpha = self.modified_adjacency[i][j]["alpha"]
                        width = self.modified_adjacency[i][j]["width"]/10
                        file.write(
                            "<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' \
                            style='stroke: rgb({4}, 0, {5}); stroke-width:{6}'/>\n".format(
                                xi, yi, xj, yj, int(alpha*255), int((1-alpha)*255), width))
            file.write("</svg></body></html>")
