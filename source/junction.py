"""
This module implements some common-type junctions.
"""

import numpy as np

class Junction(object):
    """
    This class of methods instantiates a junction object on which wave
    propagation methods are performed.
    """

    def __init__(self, widths):
        self.__junction_type = 1
        self.__left = None
        self.__straight = None
        self.__right = None
        if "left" in widths:
            self.__left = widths["left"]
            self.__junction_type += 1
        if "straight" in widths:
            self.__straight = widths["straight"]
            self.__junction_type += 1
        if "right" in widths:
            self.__right = widths["right"]
            self.__junction_type += 1

    def compute(self):
        """
        This is the main method which constructs and returns an appropriate
        function based on the type of a junction and its street widths.
        """
        FC = lambda theta, entry, exiting: max(
            1-exiting/entry*math.tan(theta), 0)
        FT = lambda theta, entry, exiting: 0.5*min(
            exiting/entry*math.tan(theta), 1)
        if self.__junction_type == 2:
            return self.__bend()
        elif self.__junction_type == 3:
            if self.__left is not None and self.__right is not None:
                return self.__t_junction()
            else:
                return self.__side_street()
        elif self.__junction_type == 4:
            return self.__simple_crossroads()

    def __simple_crossroads(self):
        """
        This private method constructs function for a simple crossroads, where
        simple means that opposite streets are of the same width.
        """
        return (lambda theta: theta,[0,1,2])

    def __bend(self):
        """
        This private method constructs function for a right-angle bend.
        """
        return (lambda theta: theta,[0,1,2])

    def __t_junction(self):
        """
        This private method constructs function for a t-junction (TODO:opposite
        streets same length?)
        """
        return (lambda theta: theta,[0,1,2])

    def __side_street(self):
        """
        This private method constructs function for side-street junction.
        """
        return (lambda theta: theta,[0,1,2])
