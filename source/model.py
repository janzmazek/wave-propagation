"""
This module performs probabilistic model on some network of streets given by the
modified adjacency matrix (with dictionary of length, width, alpha, orientation).
"""
from collections import defaultdict
import numpy as np
import networkx as nx

from source.junction import Junction

class Model(object):
    """docstring for Model."""
    def __init__(self, modified_adjacency):
        self.__modified_adjacency = modified_adjacency
        self.__nodes = len(modified_adjacency)
        self.__graph = nx.from_numpy_matrix(self.__create_adjacency())
        self.__source = None
        self.__receiver = None

    def __create_adjacency(self):
        """
        This method returns normal adjacency matrix from modified adjacency
        matrix.
        """
        adjacency = np.zeros((self.__nodes, self.__nodes))
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if self.__modified_adjacency[i][j] != 0:
                    adjacency[i][j] = 1
        return adjacency

    def set_source(self, source):
        """
        This setter method sets source node.
        TODO: input coordinates, find closest node, set node
        """
        self.__source = source

    def set_receiver(self, receiver):
        """
        This setter method sets receiver node.
        TODO: input coordinates, find closest node, set node
        """
        self.__receiver = receiver

    def solve(self, treshold):
        """
        This method is the main method of the class and it solves the wave
        propagation problem. Treshold specifies length additional to the shortest
        path length.
        """
        assert self.__source is not None and self.__receiver is not None
        all_paths = self.__compute_paths(treshold) # obtain all connecting paths
        power = 0
        for length, paths in all_paths.items(): # iterate through defaultdict
            for path in paths:
                integrand = self.__walk(length, path) # obtain functions and breaking points
                power += self.__integrate(integrand) # sum up all path contributions
        return power # resulting power flow

    def __compute_paths(self, treshold):
        """
        This private method computes paths between source and receiver and sorts
        them by the length (in a dictionary).
        """
        shortest_length = nx.shortest_path_length(
            self.__graph, self.__source, self.__receiver)
        paths = defaultdict(list)
        cutoff = shortest_length + treshold
        # all_simple_paths = nx.all_simple_paths(
        #    self.__graph, self.__source, self.__receiver, cutoff)
        distances_dictionary = nx.all_pairs_dijkstra_path_length(
            self.__graph)[self.__receiver]
        all_paths = self.__find_paths(
            distances_dictionary, self.__source, cutoff+1)

        for path in all_paths:
            paths[len(path)].append(path) # sort paths by the length (defaultdict)
        return paths


    def __find_paths(self, distances_dictionary, element, n):
        """
        This private method implements an algorithm for finding all paths
        between source and receiver of specified length.
        """
        if element==self.__receiver or n<=0:
            return [[element]]
        paths = []
        for neighbor in self.__graph.neighbors(element):
            for path in self.__find_paths(distances_dictionary, neighbor, n-1):
                if distances_dictionary[element] < n:
                    paths.append([element]+path)
        return paths

    def __walk(self, length, path):
        """
        This private method iterates through the path and fills the functions
        and breaking_points arrays at each step.
        """
        functions = []
        breaking_points = set()
        if length > 2:
            # Fill length of first street
            lengths = [self.__modified_adjacency[path[0]][path[1]]["length"]]
            # Fill alpha of first street
            alphas = [self.__modified_adjacency[path[0]][path[1]]["alpha"]]

            for i in range(1, length-1):
                previous = path[i-1]
                current = path[i]
                following = path[i+1]

                widths = self.__rotate(previous, current, following)
                junction = Junction(widths, current)
                functions.append(junction.compute_function())
                breaking_points.add(junction.compute_breaking_point())

                # add length and alpha
                lengths.append(self.__modified_adjacency[previous][current]["length"])
                alphas.append(self.__modified_adjacency[previous][current]["alpha"])

            # Fill length of last street
            lengths.append(self.__modified_adjacency[path[length-2]][path[length-1]]["length"])
            # Fill alpha of last street
            alphas.append(self.__modified_adjacency[path[length-2]][path[length-1]]["alpha"])

            return {
                "path": path,
                "functions": functions,
                "breaks": breaking_points,
                "lengths": lengths,
                "alphas": alphas}
        else:
            raise ValueError("Path too short.")

    def __rotate(self, previous, current, following):
        """
        This private method figures out an orientation of the junction
        """
        orientation = self.__modified_adjacency[current][previous]["orientation"]
        backward = orientation
        right = (orientation+1)%4
        forward = (orientation+2)%4
        left = (orientation+3)%4
        rotated = {"entry": self.__modified_adjacency[current][previous]["width"]}
        for neighbor in self.__graph.neighbors(current):
            if self.__modified_adjacency[current][neighbor]["orientation"] == left:
                rotated["left"] = self.__modified_adjacency[current][neighbor]["width"]
                if following == neighbor:
                    rotated["next"] = "left"
            elif self.__modified_adjacency[current][neighbor]["orientation"] == forward:
                rotated["forward"] = self.__modified_adjacency[current][neighbor]["width"]
                if following == neighbor:
                    rotated["next"] = "forward"
            elif self.__modified_adjacency[current][neighbor]["orientation"] == right:
                rotated["right"] = self.__modified_adjacency[current][neighbor]["width"]
                if following == neighbor:
                    rotated["next"] = "right"
            elif self.__modified_adjacency[current][neighbor]["orientation"] == backward:
                rotated["backward"] = self.__modified_adjacency[current][neighbor]["width"]
                if following == neighbor:
                    rotated["next"] = "backward"
        return rotated

    def __integrate(self, integrand):
        """
        This private method integrates functions with respect to the breaking
        points.
        """
        # TODO: implement integrator
        return 1
