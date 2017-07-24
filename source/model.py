"""
This module performs probabilistic model on some network of streets given by
the modified adjacency matrix (with dictionary of length, width, alpha,
orientation).
"""
#from collections import defaultdict
import numpy as np
import scipy.integrate as integrate
import networkx as nx

from source.junction import Junction

class Model(object):
    """docstring for Model."""
    def __init__(self):
        self.__modified_adjacency = None
        self.__nodes = None
        self.__graph = None
        self.__source = None
        self.__receiver = None
        self.__threshold = None

    def set_adjacency(self, modified_adjacency):
        self.__modified_adjacency = modified_adjacency
        self.__nodes = len(modified_adjacency)
        self.__graph = nx.from_numpy_matrix(self.__create_adjacency())

    def set_source(self, source1, source2):
        """
        This setter method sets source node.
        """
        try:
            source1 = int(source1)
            source2 = int(source2)
        except ValueError:
            raise ValueError("Source nodes must be integers.")
        if source1 < 0 or source1 > self.__nodes:
            raise ValueError("First source node not in range.")
        if source2 < 0 or source2 > self.__nodes:
            raise ValueError("Second source node not in range.")
        if source2 not in self.__graph.neighbors(source1):
            raise ValueError("Sources are not neighbours.")
        self.__source = (source1, source2)

    def set_receiver(self, receiver1, receiver2):
        """
        This setter method sets receiver node.
        """
        try:
            receiver1 = int(receiver1)
            receiver2 = int(receiver2)
        except ValueError:
            raise ValueError("Receiver nodes must be integers.")
        if receiver1 < 0 or receiver1 > self.__nodes:
            raise ValueError("First receiver node not in range.")
        if receiver2 < 0 or receiver2 > self.__nodes:
            raise ValueError("Second receiver node not in range.")
        if receiver2 not in self.__graph.neighbors(receiver1):
            raise ValueError("Receivers are not neighbours.")
        self.__receiver = (receiver1, receiver2)

    def set_threshold(self, threshold):
        try:
            threshold = int(threshold)
        except ValueError:
            raise ValueError("Threshold must be an integer.")
        if threshold < 0:
            raise ValueError("Threshold must be a positive number.")
        self.__threshold = threshold

    def get_source(self):
        if self.__source is not None:
            return self.__source
        else:
            raise ValueError("Source not set.")

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

    def solve(self):
        """
        This method is the main method of the class and it solves the wave
        propagation problem. Treshold specifies length additional to the
        shortest path length.
        """
        assert self.__source is not None and self.__receiver is not None and self.__threshold is not None
        paths = self.__compute_paths() # obtain all connecting paths
        power = 0
        error = 0
        for path in paths:
            integrand = self.__walk(path) # obtain functions and breaking points
            (part_power, part_error) = self.__integrate(integrand)
            power += part_power
            error += part_error
        print("==========================================")
        print("Resulting power from node {0} to node {1} is {2} (error {3})".format(
            self.__source, self.__receiver, power, error))
        return (power, error) # resulting power flow

    def __compute_paths(self):
        """
        This private method computes all paths between source and receiver.
        """
        lengths = []
        paths = []
        # Find lengths of all four combinations
        for source in self.__source:
            for receiver in self.__receiver:
                lengths.append(nx.shortest_path_length(self.__graph, source, receiver))
        # Find minimal length and compute cutoff
        shortest_length = min(lengths)
        cutoff = shortest_length + self.__threshold

        # Find all paths of lengths up to cutoff of all four combinations
        for source in self.__source:
            for receiver in self.__receiver:
                paths.extend(self.__find_paths(source, receiver, cutoff+1))
        return paths


    def __find_paths(self, element, receiver, n, distances=False):
        """
        This private method implements an algorithm for finding all paths
        between source and receiver of specified length.
        """
        # Compute distances dictionary only the first time
        if not distances:
            distances = nx.all_pairs_dijkstra_path_length(self.__graph)[receiver]
        paths = []
        # Recursive algorithm
        if n > 0:
            for neighbor in self.__graph.neighbors(element):
                for path in self.__find_paths(neighbor, receiver, n-1, distances):
                    if distances[element] < n:
                        paths.append([element]+path)
        # Only append path if the last element is the receiver node
        if element == receiver:
            paths.append([element])
        return paths

    def __walk(self, path):
        """
        This private method iterates through the path and fills the functions
        and breaking_points arrays at each step.
        """
        # Prepend "apparent" source
        if path[0] == self.__source[0]:
            path.insert(0, self.__source[1])
            lengths = [self.__modified_adjacency[path[0]][path[1]]["length"]/2]
        else:
            path.insert(0, self.__source[0])
            lengths = [self.__modified_adjacency[path[0]][path[1]]["length"]/2]

        # Fill width, alpha and rotation of the first street
        widths = [self.__modified_adjacency[path[0]][path[1]]["width"]]
        alphas = [self.__modified_adjacency[path[0]][path[1]]["alpha"]]
        rotations = [0]

        # Append "apparent" receiver
        if path[-1] == self.__receiver[0]:
            path.append(self.__receiver[1])
        else:
            path.append(self.__receiver[0])

        # Set empty array of functions and breaking points
        functions = []
        breaking_points = set()

        # Iterate through the rest of the path
        for i in range(1, len(path)-1):
            previous, current, following = path[i-1], path[i], path[i+1]

            # Get widths of appropriately rotated junction
            rotated_widths = self.__rotate(previous, current, following)
            junction = Junction(rotated_widths, current)
            functions.append(junction.compute_function())
            breaking_points.add(junction.compute_breaking_point())

            # Add length, alpha and rotation of the following street
            lengths.append(self.__modified_adjacency[current][following]["length"])
            widths.append(self.__modified_adjacency[current][following]["width"])
            alphas.append(self.__modified_adjacency[current][following]["alpha"])
            rotations.append((rotations[-1]+junction.correct_orientation())%2)

        # Last length is only half
        lengths[-1] = lengths[-1]/2

        return {"path": path,
                "functions": functions,
                "breaks": breaking_points,
                "rotations": rotations,
                "lengths": lengths,
                "widths": widths,
                "alphas": alphas
                }

    def __rotate(self, previous, current, following):
        """
        This private method figures out an orientation of the junction and
        provides information on street widths and exiting street.
        """
        orientation = self.__modified_adjacency[current][previous]["orientation"]
        backward = orientation
        right = (orientation+1)%4
        forward = (orientation+2)%4
        left = (orientation+3)%4
        rotated = {}
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
        path = integrand["path"]
        functions = integrand["functions"]
        breaking_points = integrand["breaks"]
        rotations = integrand["rotations"]
        lengths = integrand["lengths"]
        widths = integrand["widths"]
        alphas = integrand["alphas"]

        def compose_function(theta):
            # Scalar coefficient and first street element
            complete = 1/np.pi * (1-alphas[0])**(lengths[0]/widths[0]*np.tan(theta))
            # Junctions functions and street elements
            for i in range(1, len(path)-1):
                if rotations[i] == 1:
                    angle = np.pi/2 - theta
                else:
                    angle = theta
                complete = complete * (1-alphas[i])**(lengths[i]/widths[i]*np.tan(theta)) \
                    *functions[i-1](theta)
            return complete

        (integral, error) = integrate.quad(compose_function, 0, np.pi/2)
        print("Contribution from path {0}: {1} (error {2})".format(path, integral, error))
        return (integral, error)
