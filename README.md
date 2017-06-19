# Wave propagation
Implementation of the wave propagation model in an urban streets environment.

# Installation

To install this package using pip please run commands in the command line:
```bash
pip install git+git://github.com/janzmazek/wave-propagation.git
```
or if you want a local copy of the repository
```bash
git clone https://github.com/janzmazek/bad-boids.git
python setup.py install
```
# Example usage
Constructor class creates street network and arbitrarily modifies streets:
```python
from source.constructor import Constructor
network = Constructor(4,5) # 4x5 network
network.move_horizontal_line(2,10) # moves third horizontal line by 10 (right)
network.move_vertical_line(1,-30) # moves second vertical line by 30 (left)
network.delete_connection(5,6) # deletes street (5,6)
network.modify_adjacency() # this step is mandatory. After this, moving and deleting is no longer possible
network.change_width(0,1,20) # changes width of street (0,1) to 20
network.change_alpha(0,1,0.1) # changes absorption of street (0,1) to 0.1
```
Model class performs the algorithm on the network:
```python
from source.model import Model
model = Model(constructor.get_adjacency_matrix())
model.set_source(0) # sets source to 0
model.set_receiver(1) # sets receiver to 1
power = model.solve(2) # computes power percentage with threshold 2
```
