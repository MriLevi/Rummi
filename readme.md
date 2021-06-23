Welcome to Rummi!

I programmed this as a proof-of-concept for a rummikub solver. To use, download this program and simply run rummi.py. 

Prerequisites:

termcolor, numpy

This program basically executes a search tree on all available tiles and then calculates what the best scoring solution would be, keeping into account which tiles were already on the board.

Right now, it will probably work well during the first few turns, but after too many tiles are in play, it slows down considerably. There is still some optimization I have to do, but I believe it is very possible to make this algorithm work in near real time.

Have fun!