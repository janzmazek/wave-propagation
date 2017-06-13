from source.constructor import Constructor
from source.model import Model
import yaml
#import matplotlib.pyplot as plt
#import networkx as nx

network = Constructor(5,5)

network.move_vertical_line(2,25)
network.move_vertical_line(3,50)
network.move_horizontal_line(2,25)
network.move_horizontal_line(3,50)


network.delete_connection(5,6)
network.delete_connection(5,6)
network.delete_connection(5,6)
network.delete_connection(7,8)
network.delete_connection(7,8)
network.delete_connection(10,11)
network.delete_connection(3,5)
network.delete_connection(2,6)
network.delete_connection(1,8)

network.modify_adjacency(alpha=0)

network.change_width(2,3,30)
network.change_width(4,5,60)
network.change_width(7,8,90)
network.change_width(2,5,90)
network.change_width(4,8,60)
network.change_width(7,12,30)
network.change_width(5,6,60)
network.change_width(8,9,90)
network.change_width(9,10,90)
network.change_width(5,9,90)
network.change_width(9,14,90)
network.change_width(8,13,60)

network.change_alpha(5,9,0.8)
network.change_alpha(8,9,0.8)
network.change_alpha(5,6,0.2)
network.change_alpha(8,13,0.2)

network.output_network()

modified_adjacency = network.get_modified_adjacency()
model = Model(modified_adjacency)
model.set_source(0)
model.set_receiver(1)
model.solve(0)
