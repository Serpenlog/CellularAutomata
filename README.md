# CellularAutomata
Cellular Automata Simulator

This is a simple Cellular automata simulator in order to test simple CA patterns with the ability to import premade patterns and save user-made patterns as well.
There are two main programs.
1. PygameGameOfLife is the simulator which opens up an interface with two options to select patterns or edit rules (editing rules through interface is not yet enabled, please edit rules through GameOfLife.py variables)
You can either choose to select patterns which will give you a list of different patterns to pick from and simulate or click on the X at the top right and use an empty board. You may change the grid_size by editing the initiated simulator rows and columns.
Any selected pattern will be centered on the simulator.

2. PatternDesigner is a simple grid that allows you to toggle cells on/off, when you press enter it will output the set of toggled cells, this can then be added into Patterns.py to save your own patterns.
   PatternDesigner centers the pattern at the top left of the grid at [0,0], so if you want the pattern to be centered correctly build from the top left going down and right.
