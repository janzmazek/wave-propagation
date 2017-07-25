class Plotter(object):
    """docstring for Plotter."""
    def __init__(self):
        self.__constructor = None
        self.__model = None
        self.__source = None
        self.__receivers = None

    def set_model(self, constructor, model):
        self.__constructor = constructor
        self.__model = model
        self.__source = self.__model.get_source()
        self.__receivers = self.__get_receivers()

    def __get_receivers(self):
        receivers = []
        adjacency = self.__constructor.get_adjacency()
        for j in range(len(adjacency)):
            for i in range(j):
                if (i,j) is not self.__source and adjacency[i][j] == 1:
                    receivers.append((i, j))
        return receivers

    def plot(self):
        if self.__constructor is None or self.__model is None:
            raise ValueError("Plotter not initialised.")
        powers = []
        for receiver in self.__receivers:
            self.__model.set_receiver(*receiver) # * unpacks tuple
            powers.append(self.__model.solve())
        self.__draw(powers, filename)

        receiver_positions = self.__get_receiver_positions()

        X = [element[0] for element in receiver_positions]
        Y = [element[1] for element in receiver_positions]
        Z = powers
        

    def __get_receiver_positions(self):
        receiver_positions = []
        positions = self.__constructor.get_positions()
        for receiver in self.__receivers:
            x1, y1 = positions[receiver[0]][0], positions[receiver[0]][1]
            x2, y2 = positions[receiver[1]][0], positions[receiver[1]][1]
            if x1 == x2:
                receiver_positions.append((x1, (y1+y2)/2))
            elif y1 == y2:
                receiver_positions.append(((x1+x2)/2, y1))
        return receiver_positions
