from unittest import TestCase
from source.model import Model
import json

with open("source/tests/fixtures.json", "r") as file:
    invalues = json.load(file)

ALPHA = invalues[0] # Alpha values set to 0
BETA = invalues[1] # Beta values set to 0
WIDTH = invalues[2] # width values set to 1e0-10

class TestModel(TestCase):
    def test_setters(self):
        model = Model()
        model.set_adjacency(ALPHA)
        with self.assertRaises(ValueError):
            model.set_source(-1, 0) # nodes out of range
        with self.assertRaises(ValueError):
            model.set_source(5, 6) # nodes out of range
        with self.assertRaises(ValueError):
            model.set_source(0, 2) # nodes not neighbours
        with self.assertRaises(ValueError):
            model.set_receiver(-1, 0) # nodes out of range
        with self.assertRaises(ValueError):
            model.set_receiver(5, 6) # nodes out of range
        with self.assertRaises(ValueError):
            model.set_receiver(0, 2) # nodes not neighbours
        with self.assertRaises(ValueError):
            model.set_threshold(-1)

    def test_zero_power(self):
        model = Model()
        model.set_adjacency(ALPHA)
        model.set_source(0, 1)
        model.set_receiver(4, 5)
        model.set_threshold(0)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

        model.set_threshold(2)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

        model.set_adjacency(BETA)
        model.set_source(0, 1)
        model.set_receiver(4, 5)
        model.set_threshold(0)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

        model.set_threshold(2)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

        model.set_adjacency(WIDTH)
        model.set_source(0, 1)
        model.set_receiver(4, 5)
        model.set_threshold(0)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

        model.set_threshold(2)

        (power, error, paths) = model.solve()
        self.assertAlmostEqual(power, 0)
        self.assertAlmostEqual(error, 0)

    def test_shortest_paths(self):
        model = Model()
        model.set_adjacency(ALPHA)
        model.set_threshold(0)

        model.set_source(0, 1)
        model.set_receiver(4, 5)

        (power, error, paths) = model.solve()
        self.assertEqual(len(paths), 1)

        model.set_source(0, 3)
        model.set_receiver(2, 5)

        (power, error, paths) = model.solve()
        self.assertEqual(len(paths), 2)
