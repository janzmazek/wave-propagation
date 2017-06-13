import numpy as np

class Crossroads(object):
    def __init__(self, widths, current):
        self.__backward = widths["entry"]
        self.__forward = widths["forward"] if "forward" in widths else 0
        self.__left = widths["left"] if "left" in widths else 0
        self.__right = widths["right"] if "right" in widths else 0
        self.__next = widths["next"]
        self.__exiting = widths[widths["next"]]
        self.__type = self.__define_junction()

    def __define_junction(self):
        if (self.__backward < self.__left < self.__forward < self.__right) or \
           (self.__backward < self.__left < self.__right < self.__forward) or \
           (self.__backward < self.__forward < self.__left < self.__right) or \
           (self.__left < self.__backward < self.__forward < self.__right) or \
           (self.__left < self.__backward < self.__right < self.__forward) or \
           (self.__left < self.__right < self.__backward < self.__forward):
                return ("a", False)
        elif (self.__backward < self.__right < self.__forward < self.__left) or \
             (self.__backward < self.__right < self.__left < self.__forward) or \
             (self.__backward < self.__forward < self.__right < self.__left) or \
             (self.__right < self.__backward < self.__forward < self.__left) or \
             (self.__right < self.__backward < self.__left < self.__forward) or \
             (self.__right < self.__left < self.__backward < self.__forward):
                return ("b", True)
        elif (self.__forward < self.__backward < self.__left < self.__right) or \
             (self.__forward < self.__left < self.__backward < self.__right) or \
             (self.__left < self.__forward < self.__backward < self.__right) or \
             (self.__left < self.__right < self.__forward < self.__backward) or \
             (self.__left < self.__forward < self.__right < self.__backward) or \
             (self.__forward < self.__left < self.__right < self.__backward):
                return ("b", False)

        elif (self.__forward < self.__backward < self.__right < self.__left) or \
             (self.__forward < self.__right < self.__backward < self.__left) or \
             (self.__right < self.__forward < self.__backward < self.__left) or \
             (self.__right < self.__left < self.__forward < self.__backward) or \
             (self.__right < self.__forward < self.__left < self.__backward) or \
             (self.__forward < self.__right < self.__left < self.__backward):
                return ("b", True)

    def compute_function(self):
        pass

    def compute_breaking_points(self):
        pass

    def __type_a(self, inverted):
        if inverted:
            self.__right, self.__left = self.__left, self.__right
        t1 = self.__right-self.__left/self.__forward+self.__backward
        t2 = self.__right-self.__left/self.staight-self.__backward
        t3 = self.__right+self.__left/self.__forward+self.__backward
        t4 = 2*self.__right/self.__forward+self.__backward
        t5 = self.__right+self.__left/self.__forward-self.__backward
        t6 = 2*self.__right/self.__forward-self.__backward
        t7 = 2*self.__right/self.__backward-self.__forward
        t8 = -2*self.__right/self.__backward+self.__forward

    def __type_b(self, inverted):
        if inverted:
            self.__right, self.__left = self.__left, self.__right
