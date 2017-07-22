import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

class Plotter(object):
    """docstring for Plotter."""
    def __init__(self, constructor, model):
        self.__constructor = constructor
        self.__model = model
        self.__receivers = None

    def __get_receivers(self):
        receivers = []
        adjacency = self.__constructor.get_adjacency()
        for j in range(len(adjacency)):
            for i in range(i):
                if (i,j) is not self.__model.get_source() and adjacency[i] == 1 and adjacency[j] == 1:
                    receivers.append((i, j))
        return receivers

    def plot(self, filename):
        print(filename)
        return
        powers = []
        for receiver in self.__receivers:
            self.__model.set_receiver(*receiver) # * unpacks tuple
            powers.append(self.__model.solve())
        self.__draw(powers, filename)

    def __draw(self, solution, filename):
        positions = self.__constructor.get_positions()
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X = [element[0] for element in positions]
        Y = [element[1] for element in positions]

        # Plot the surface.
        surf = ax.plot_surface(X, Y, solution, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
