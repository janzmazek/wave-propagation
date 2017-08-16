from unittest import TestCase
from source.constructor import Constructor

class TestConstructor(TestCase):
    def test_setters(self):
        network = Constructor()
        with self.assertRaises(ValueError):
            network.set_grid(-1, 1, 100)
        with self.assertRaises(ValueError):
            network.set_grid(1, -1, 100)
        with self.assertRaises(ValueError):
            network.set_grid(2, 2, -10)

    def test_create_adjacency(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(4,4,100)
        adjacency = network.get_adjacency()
        self.assertEqual(len(adjacency),16)

    def test_create_positions(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        positions = network.get_positions()
        self.assertEqual(len(positions),25)
        self.assertEqual(len(positions[0]),2)

    def test_move_horizontal_line(self):
        # Test normal usage
        network1 = Constructor()
        network1.set_grid(4,4,100)
        network1.move_horizontal_line(2,50)
        positions1 = network1.get_positions()
        for i in range(2*4, 3*4):
            self.assertEqual(positions1[i][1],250)
        network2 = Constructor()
        network2.set_grid(5,5,100)
        network2.move_horizontal_line(0,-10)
        positions2 = network2.get_positions()
        for i in range(0, 5):
            self.assertEqual(positions2[i][1],-10)
        # Test wrong usage
        with self.assertRaises(ValueError): # no such horizontal line
            network1.move_horizontal_line(-1,0)
        with self.assertRaises(ValueError): # no such horizontal line
            network2.move_horizontal_line(5,0)

    def test_move_vertical_line(self):
        # Test normal usage
        network1 = Constructor()
        network1.set_grid(4,4,100)
        network1.move_vertical_line(3,30)
        positions1 = network1.get_positions()
        for i in range(3, 16, 4):
            self.assertEqual(positions1[i][0],330)
        network2 = Constructor()
        network2.set_grid(2,2,100)
        network2.move_vertical_line(1,100)
        positions2 = network2.get_positions()
        for i in range(1, 4, 2):
            self.assertEqual(positions2[i][0],200)
        # Test wrong usage
        with self.assertRaises(ValueError):
            network1.move_vertical_line(-1,0) # no such vertical line
        with self.assertRaises(ValueError):
            network2.move_vertical_line(2,0) # no such vertical line

    def test_delete_connection(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        network.delete_connection(6,7)
        network.delete_connection(7,8)
        network.delete_connection(2,11)
        network.delete_connection(2,6)
        adjacency = network.get_adjacency()
        positions = network.get_positions()
        self.assertEqual(len(adjacency),22)
        self.assertEqual(len(positions),22)
        network.modify_adjacency(10, 0.5, 0.5)

    def test_modify_adjacency(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        network.modify_adjacency(10, 0.1, 0.1)
        adjacency = network.get_adjacency()
        modified_adjacency = network.get_modified_adjacency()
        self.assertEqual(len(modified_adjacency),25)
        for i in range(25):
            for j in range(25):
                if adjacency[i][j]==0:
                    self.assertTrue(modified_adjacency[i][j]==0)
                else:
                    self.assertFalse(modified_adjacency[i][j]==0)

        with self.assertRaises(ValueError): # width=0
            network.modify_adjacency(0, 0.1, 0.1)


    def test_change_width(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        network.modify_adjacency(20, 0.1, 0.1)
        network.change_width(0,1,50)
        adjacency = network.get_adjacency()
        modified_adjacency = network.get_modified_adjacency()
        self.assertEqual(modified_adjacency[0][1]["width"],50)
        self.assertEqual(modified_adjacency[1][0]["width"],50)
        for i in range(1, 25):
            for j in range(1, 25):
                if adjacency[i][j]==1:
                    self.assertEqual(modified_adjacency[i][j]["width"],20)
        # Test wrong usage
        with self.assertRaises(ValueError): # width=0
            network.change_width(0,1,0)
        with self.assertRaises(ValueError): # width<0
            network.change_width(0,1,-10)
        with self.assertRaises(ValueError): # nodes not neighbours
            network.change_width(0,2,50)
        with self.assertRaises(ValueError): #nodes out of range
            network.change_width(0,25,20)

    def test_change_alpha(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        network.modify_adjacency(10, 0.8, 0.1)
        network.change_alpha(0,1,0.5)
        adjacency = network.get_adjacency()
        modified_adjacency = network.get_modified_adjacency()
        self.assertEqual(modified_adjacency[0][1]["alpha"],0.5)
        self.assertEqual(modified_adjacency[1][0]["alpha"],0.5)
        for i in range(1, 25):
            for j in range(1, 25):
                if adjacency[i][j]==1:
                    self.assertEqual(modified_adjacency[i][j]["alpha"],0.8)
        # Test wrong usage
        with self.assertRaises(ValueError): # alpha>1
            network.change_alpha(0,1,2)
        with self.assertRaises(ValueError): # alpha<0
            network.change_alpha(0,1,-1)
        with self.assertRaises(ValueError): # nodes not neighbours
            network.change_alpha(0,2,0.5)
        with self.assertRaises(ValueError): # nodes out of range
            network.change_alpha(0,25,0.5)

    def test_change_beta(self):
        # Test normal usage
        network = Constructor()
        network.set_grid(5,5,100)
        network.modify_adjacency(10, 0.1, 0.8)
        network.change_beta(0,1,0.5)
        adjacency = network.get_adjacency()
        modified_adjacency = network.get_modified_adjacency()
        self.assertEqual(modified_adjacency[0][1]["beta"],0.5)
        self.assertEqual(modified_adjacency[1][0]["beta"],0.5)
        for i in range(1, 25):
            for j in range(1, 25):
                if adjacency[i][j]==1:
                    self.assertEqual(modified_adjacency[i][j]["beta"],0.8)
        # Test wrong usage
        with self.assertRaises(ValueError): # alpha>1
            network.change_beta(0,1,2)
        with self.assertRaises(ValueError): # alpha<0
            network.change_beta(0,1,-1)
        with self.assertRaises(ValueError): # nodes not neighbours
            network.change_beta(0,2,0.5)
        with self.assertRaises(ValueError): # nodes out of range
            network.change_beta(0,25,0.5)

    def test_staging(self):
        network = Constructor()
        network.set_grid(5,5,100)
        network.delete_connection(0,1)
        with self.assertRaises(AssertionError): # no moving after deleting street
            network.move_horizontal_line(0,10)
        with self.assertRaises(AssertionError):
            network.move_vertical_line(0,10)

        network.modify_adjacency(10, 0.5, 0.5)
        with self.assertRaises(AssertionError): # no moving after modifying
            network.move_vertical_line(0,10)
        with self.assertRaises(AssertionError):
            network.move_horizontal_line(0,10)
        with self.assertRaises(AssertionError): # no deleting after modifying
            network.delete_connection(0,1)
