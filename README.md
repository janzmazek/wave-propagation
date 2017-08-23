# Wave propagation
Implementation of the wave propagation model in an urban streets environment.

# Installation

To clone and run this application, run commands
```bash
git clone https://github.com/janzmazek/wave-propagation.git
python wave-propagation
```
The application must be run using Python 3 with Numpy and Scipy installed.

# Testing
To run unit tests, run command
```bash
python -m unittest
```
inside package's main directory.

# Usage examples
Package modules Constructor and Model may be used separately.
```python
from source.constructor import Constructor
network = Constructor() # initialises constructor object
network.set_grid(4,5,100) # sets number of horizontal streets to 4, vertical streets to 5 and street length to 100
network.move_horizontal_line(2,10) # moves third horizontal line by 10 (right)
network.move_vertical_line(1,-30) # moves second vertical line by 30 (left)
network.delete_connection(6,11) # deletes street (5,6)
network.modify_adjacency(5,0.04,0.001) # sets width to 5, wall absorption to 0.04 and air absorption to 0.001 to all streets
network.change_width(1,6,20) # changes width of street (0,1) to 20
network.change_alpha(0,1,0.1) # changes wall absorption of street (0,1) to 0.1
network.change_beta(0, 1, 0.005) # changes air absorption of street (0,1) to 0.005
```
Model class performs the algorithm on the constructed network:
```python
from source.model import Model
model = Model() # initialises model object
model.set_adjacency(network.get_modified_adjacency()) # sets adjacency
model.set_source(0, 1) # sets source between junctions 0 and 1
model.set_receiver(18, 19) # sets receiver between junctions 18 and 19
model.set_threshold(2) # sets threshold to 2
power = model.solve() # computes power percentage
print("Power percentage is {0}".format(power[0]))
```
Output solutions of all possible receivers along with their coordinates:
```python
(X, Y, Z) = model.solve_all(network.get_positions())
```
Plot results:
```python
network.draw_network("solution.svg", (X,Y,Z))
```
![](images/solution.png?raw=true)
