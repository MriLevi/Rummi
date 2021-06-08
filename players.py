import itertools
import numpy as np
from collections import defaultdict
import set_generator

class Players:
    def human_player(self, rack):
        self.rack = rack
        print('human player')
    def dumb_bot(self, rack):
        self.rack = rack
        print('dumb bot')
    def algorithm_bot(self, rack):
        self.rack = rack


