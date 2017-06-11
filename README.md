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
```python
from source.constructor import Constructor
from source.model import Model
network = Constructor(4,4)
network.move_horizontal_line(2,10)
network.move_vertical_line(1,40)
network.delete_connection(5,6)
network.modify_adjacency()
network.change_width(0,1,20)
network.change_alpha(0,1,0,1)
```
