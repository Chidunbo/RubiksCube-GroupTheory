
#Project Overview

This repository is part of a discrete mathematics project focusing on the Rubik's Cube. It contains two Python files: cube.py and cube_looper.py. These scripts provide different ways to interact with and visualize the state space of a Rubik's Cube using concepts from graph theory, particularly Cayley's graph.

#Dependencies
Python 3.x
pygame library for rendering graphics
rubik-cube library for Rubik's Cube model and operations
Installation
Before running the scripts, ensure you have Python 3 installed on your machine. Then, install the required Python packages using the following commands:

```
pip install pygame
pip install rubiks-cube
```
##cube.py
cube.py is an interactive model of the Rubik's Cube. It allows users to explore the cube's state space through an interactable Cayley's graph. The program visualizes both the graph and an animated Rubik's Cube, letting users interact with the cube by clicking on nodes representing standard Rubik's Cube moves.

##Features of cube.py
Visualization of the Rubik's Cube's state space as an interactive Cayley's graph.
Animated display of the Rubik's Cube corresponding to the current state in the graph.
Interactive exploration of cube states through mouse clicks on graph nodes.
Usage
Run cube.py:
```
python cube.py
```
Interact with the program's graphical interface to explore different states of the Rubik's Cube and understand their relationships through the Cayley's graph.
<img src="pics/1.JPG" width="800" height="1000" />
##cube_looper.py
cube_looper.py generates and visualizes a graph based on a series of moves on the Rubik's Cube using standard Rubik's Cube notation. It uses similar principles as cube.py but focuses on creating a graph for a predefined series of moves.

##Features of cube_looper.py
Automatic generation of the state space graph for a specific series of Rubik's Cube moves.
Graphical visualization of the transitions between different cube states.
Customizable move sequences to explore various aspects of the cube's state space.
Usage
Run cube_looper.py:

```
python cube_looper.py
```
The script does not accept command-line arguments. Modify the moves list inside cube_looper.py to explore different move sequences.
Here is the graph for all possible 2-combination moves using standard rubik's cube notation, starting from the solved state, until the solved state is reached again:
<img src="pics/dorito.JPG" width="800" height="1000" />

