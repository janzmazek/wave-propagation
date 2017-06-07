from source.constructor import Constructor
import matplotlib.pyplot as plt
import networkx as nx

network = Constructor(4,4)
network.delete_connection(5,6)
network.delete_connection(6,7)
network.modify_adjacency()
network.change_width(0, 1, 30)
network.change_width(0, 4, 50)
network.change_alpha(9, 13, 1)
network.change_alpha(12, 13, 0)
network.output_network()
