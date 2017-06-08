from unittest import TestCase
import numpy as np
from source.constructor import Constructor

class TestConstructor(TestCase):
    def test_create_adjacency(self):
        # Test normal usage
        network = Constructor(4,4)
        self.assertEqual(len(network.adjacency),16)

    def test_create_positions(self):
        # Test normal usage
        network = Constructor(5,5)
        self.assertEqual(len(network.positions),25)
        self.assertEqual(len(network.positions[0]),2)

    def test_move_horizontal_line(self):
        # Test normal usage
        network1 = Constructor(4,4)
        network1.move_horizontal_line(2,50)
        for i in range(2*network1.verticals, 3*network1.verticals):
            self.assertEqual(network1.positions[i][1],250)
        network2 = Constructor(5,5)
        network2.move_horizontal_line(0,-10)
        for i in range(0, network2.verticals):
            self.assertEqual(network2.positions[i][1],-10)
        # Test wrong usage
        with self.assertRaises(ValueError): # no such horizontal line
            network1.move_horizontal_line(-1,0)
        with self.assertRaises(ValueError): # no such horizontal line
            network2.move_horizontal_line(5,0)

    def test_move_vertical_line(self):
        # Test normal usage
        network1 = Constructor(4,4)
        network1.move_vertical_line(3,30)
        for i in range(3, network1.nodes, network1.verticals):
            self.assertEqual(network1.positions[i][0],330)
        network2 = Constructor(2,2)
        network2.move_vertical_line(1,100)
        for i in range(1, network2.nodes, network2.verticals):
            self.assertEqual(network2.positions[i][0],200)
        # Test wrong usage
        with self.assertRaises(ValueError):
            network1.move_vertical_line(-1,0) # no such vertical line
        with self.assertRaises(ValueError):
            network2.move_vertical_line(2,0) # no such vertical line

    def test_delete_connection(self):
        # Test normal usage
        network1 = Constructor(5,5)
        network1.delete_connection(6,7)
        self.assertEqual(network1.nodes,25)
        network1.delete_connection(7,8)
        self.assertEqual(network1.nodes,24)
        network1.delete_connection(2,11)
        network1.delete_connection(2,6)
        self.assertEqual(network1.nodes,22)
        self.assertEqual(len(network1.adjacency),22)
        self.assertEqual(len(network1.positions),22)
        network1.modify_adjacency()
        network1.output_network()

    def test_modify_adjacency(self):
        # Test normal usage
        network1 = Constructor(5,5)
        network1.modify_adjacency()
        self.assertEqual(len(network1.modified_adjacency),25)
        for i in range(network1.nodes):
            for j in range(network1.nodes):
                if network1.adjacency[i][j]==0:
                    self.assertTrue(network1.modified_adjacency[i][j]==0)
                else:
                    self.assertFalse(network1.modified_adjacency[i][j]==0)

    def test_change_width(self):
        # Test normal usage
        network1 = Constructor(5,5)
        network1.modify_adjacency(width=20)
        network1.change_width(0,1,50)
        self.assertEqual(network1.modified_adjacency[0][1]["width"],50)
        self.assertEqual(network1.modified_adjacency[1][0]["width"],50)
        for i in range(1, network1.nodes):
            for j in range(1, network1.nodes):
                if network1.adjacency[i][j]==1:
                    self.assertEqual(network1.modified_adjacency[i][j]["width"],20)
        # Test wrong usage
        with self.assertRaises(AssertionError): # width=0
            network1.change_width(0,1,0)
        with self.assertRaises(AssertionError): # width<0
            network1.change_width(0,1,-10)
        with self.assertRaises(ValueError): # nodes not neighbours
            network1.change_width(0,2,50)
        with self.assertRaises(ValueError): #nodes out of range
            network1.change_width(0,25,20)

    def test_change_alpha(self):
        # Test normal usage
        network1 = Constructor(5,5)
        network1.modify_adjacency(alpha=0.8)
        network1.change_alpha(0,1,0.5)
        self.assertEqual(network1.modified_adjacency[0][1]["alpha"],0.5)
        self.assertEqual(network1.modified_adjacency[1][0]["alpha"],0.5)
        for i in range(1, network1.nodes):
            for j in range(1, network1.nodes):
                if network1.adjacency[i][j]==1:
                    self.assertEqual(network1.modified_adjacency[i][j]["alpha"],0.8)
        # Test wrong usage
        with self.assertRaises(AssertionError): # alpha>1
            network1.change_alpha(0,1,2)
        with self.assertRaises(AssertionError): # alpha<0
            network1.change_alpha(0,1,-1)
        with self.assertRaises(ValueError): # nodes not neighbours
            network1.change_alpha(0,2,0.5)
        with self.assertRaises(ValueError): # nodes out of range
            network1.change_alpha(0,25,0.5)
