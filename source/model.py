"""
This module performs probabilistic model on some network of streets given by
the modified adjacency matrix (with dictionary of length, width, alpha, beta,
orientation).
"""
import numpy as np
import scipy.integrate as integrate
from collections import defaultdict

from source.junction import Junction

class Model(object):
    """
    This class of methods is the core part of the Probabilistic ray model of
    energy propagation.
    """
    def __init__(self):
        self.__modified_adjacency = None
        self.__nodes = None
        self.__graph = None
        self.__source = None
        self.__receiver = None
        self.__threshold = None
        self.__height = False

    def set_adjacency(self, modified_adjacency):
        """
        This setter method sets the adjacency matrix of the network.
        """
        self.__modified_adjacency = modified_adjacency
        self.__nodes = len(modified_adjacency)
        self.__set_graph(modified_adjacency)

    def __set_graph(self, modified_adjacency):
        """
        This method returns normal adjacency matrix from modified adjacency
        matrix.
        """
        graph = defaultdict(set)
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if modified_adjacency[i][j] != 0:
                    graph[i].add(j)
        self.__graph = graph

    def set_source(self, source1, source2):
        """
        This setter method sets the source node.
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
        if source2 not in self.__graph[source1]:
            raise ValueError("Sources are not neighbours.")
        self.__source = (source1, source2)

    def set_receiver(self, receiver1, receiver2):
        """
        This setter method sets the receiver node.
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
        if receiver2 not in self.__graph[receiver1]:
            raise ValueError("Receivers are not neighbours.")
        self.__receiver = (receiver1, receiver2)

    def set_threshold(self, threshold):
        """
        This setter method sets the threshold of the computation.
        """
        try:
            threshold = int(threshold)
        except ValueError:
            raise ValueError("Threshold must be an integer.")
        if threshold < 0:
            raise ValueError("Threshold must be a positive number.")
        self.__threshold = threshold

    def set_height(self, height):
        try:
            height = int(height)
        except ValueError:
            raise ValueError("Height must be an floating point number.")
        if height < 0:
            raise ValueError("Height must be a positive number.")
        if height == 0:
            self.__height = False
        else:
            self.__height = height

    def solve(self):
        """
        This method is the main method of the class and solves the wave
        propagation problem.
        """
        assert self.__source is not None and self.__receiver is not None and self.__threshold is not None
        paths = self.__compute_paths() # obtain all connecting paths
        print("Number of paths is {}".format(len(paths)))
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
        return (power, error, paths) # resulting power flow

    def __compute_paths(self):
        """
        This private method computes all paths between source and receiver.
        """
        lengths = []
        paths = []
        # Find lengths of all four combinations
        for source in self.__source:
            for receiver in self.__receiver:
                lengths.append(self.__dijkstra(source)[receiver])
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
            distances = self.__dijkstra(receiver)
        paths = []
        # Recursive algorithm
        if n > 0:
            for neighbor in self.__graph[element]:
                for path in self.__find_paths(neighbor, receiver, n-1, distances):
                    if distances[element] < n:
                        paths.append([element]+path)
        # Only append path if the last element is the receiver node
        if element == receiver:
            paths.append([element])
        return paths

    def __dijkstra(self, source):
        distances = {source: 0}    # Shortest lengths dictionary
        nodes = set(self.__graph)    # Set of graph nodes
        while nodes:
            min_node = None
            for node in nodes:
                if node in distances:
                    if min_node is None:
                        min_node = node
                    elif distances[node] < distances[min_node]:
                        min_node = node
            if min_node is None:
                break
            nodes.remove(min_node)
            current_length = distances[min_node]
            for edge in self.__graph[min_node]:
                length = current_length + 1
                if edge not in distances or length < distances[edge]:
                    distances[edge] = length
        return distances

    def __walk(self, path):
        """
        This private method iterates through the path and fills the functions
        and other street values at each step.
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
        betas = [self.__modified_adjacency[path[0]][path[1]]["beta"]]
        rotations = [0]

        # Append "apparent" receiver
        if path[-1] == self.__receiver[0]:
            path.append(self.__receiver[1])
        else:
            path.append(self.__receiver[0])

        # Set empty array of functions and breaking points
        functions = []

        # Iterate through the rest of the path
        for i in range(1, len(path)-1):
            previous, current, following = path[i-1], path[i], path[i+1]

            # Get widths of appropriately rotated junction
            rotated_widths = self.__rotate(previous, current, following)
            junction = Junction(rotated_widths, current)
            functions.append(junction.compute_function())

            # Add length, alpha and rotation of the following street
            lengths.append(self.__modified_adjacency[current][following]["length"])
            widths.append(self.__modified_adjacency[current][following]["width"])
            alphas.append(self.__modified_adjacency[current][following]["alpha"])
            betas.append(self.__modified_adjacency[current][following]["beta"])
            rotations.append((rotations[-1]+junction.correct_orientation())%2)

        # Last length is only half
        lengths[-1] = lengths[-1]/2

        return {"path": path,
                "functions": functions,
                "rotations": rotations,
                "lengths": lengths,
                "widths": widths,
                "alphas": alphas,
                "betas": betas
                }

    def __rotate(self, previous, current, following):
        """
        This private method determines the orientation of the junction and
        provides information on street widths and exiting street.
        """
        orientation = self.__modified_adjacency[current][previous]["orientation"]
        backward = orientation
        right = (orientation+1)%4
        forward = (orientation+2)%4
        left = (orientation+3)%4
        rotated = {}
        for neighbor in self.__graph[current]:
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
        This private method integrates functions.
        """
        path = integrand["path"]
        functions = integrand["functions"]
        rotations = integrand["rotations"]
        lengths = integrand["lengths"]
        widths = integrand["widths"]
        alphas = integrand["alphas"]
        betas = integrand["betas"]

        def compose_f(theta):
            f = 2*self.__height/np.pi if self.__height else 1/np.pi
            for i in range(len(rotations)):
                angle = np.pi/2-theta if rotations[i]==1 else theta # angle rotation
                A = (1-alphas[i])**(lengths[i]/widths[i]*np.tan(angle)) # wall absorption
                B = np.exp(-betas[i]*lengths[i]/np.cos(angle)) # air absorption
                f *= A*B/np.cos(angle)

            for i in range(len(functions)):
                angle = np.pi/2-theta if rotations[i]==1 else theta # angle rotation
                f *= functions[i](angle) # Junction probability distribution function
            return f

        def compose_L(theta):
            L = 1
            for i in range(len(rotations)):
                angle = np.pi/2-theta if rotations[i]==1 else theta # angle rotation
                L += lengths[i]/np.cos(angle)
            return L

        if not self.__height: # 2D
            (energy, error) = integrate.quad(compose_f, 0, np.pi/2)
        else: # 3D
            integrand = lambda theta: compose_f(theta)/compose_L(theta)
            (energy, error) = integrate.quad(integrand, 0, np.pi/2)
        print("Contribution from path {0}: {1} (error {2})".format(
            path, energy, error))
        return (energy, error)

    def solve_all(self, positions):
        """
        This method performs computations of the wave propagation problem from
        the source to all possible receivers and returns the result as X and Y
        coordinates of the receivers along with the percentage of the power
        flow.
        """
        receivers = self.__get_receivers()
        powers = []
        for receiver in receivers:
            self.set_receiver(*receiver) # * unpacks tuple
            powers.append(self.solve())

        receiver_positions = self.__get_positions(receivers, positions)
        source_position = self.__get_positions([self.__source], positions)

        X = [element[0] for element in receiver_positions]
        Y = [element[1] for element in receiver_positions]
        Z = [element[0] for element in powers]

        X.append(source_position[0][0])
        Y.append(source_position[0][1])
        Z.append(1)

        return (X, Y, Z)

    def __get_receivers(self):
        """
        This private method returns a list of tuples of all possible receivers.
        """
        receivers = []
        for j in range(len(self.__modified_adjacency)):
            for i in range(j):
                if self.__modified_adjacency[i][j] != 0:
                    if self.__source != (i,j) and self.__source != (j,i):
                        receivers.append((i,j))
        return receivers

    def __get_positions(self, streets, positions):
        """
        This private method returns a list of tuples of (X, Y) coordinates of
        middles of the given streets based on the input positions matrix.
        """
        center_positions = []
        for street in streets:
            x1, y1 = positions[street[0]][0], positions[street[0]][1]
            x2, y2 = positions[street[1]][0], positions[street[1]][1]
            if x1 == x2:
                center_positions.append((x1, (y1+y2)/2))
            elif y1 == y2:
                center_positions.append(((x1+x2)/2, y1))
        return center_positions
