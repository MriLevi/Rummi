import numpy as np
from itertools import combinations
from collections import defaultdict

class SetGenerator:

    def __init__(self, numbers=13, colors=4, jokers=2, combi_len=3, tile_sets=2):
            self.numbers = numbers
            self.colors = colors
            self.jokers = jokers
            self.combi_len = combi_len
            self.tile_sets = tile_sets
            self.tiles = self.generate_tiles()
            self.runs = set()
            self.groups = set()
            self.sets = set()
            #self.generate_sets()

    def generate_tiles(self):
        tiles = defaultdict(list)
        for tile_set in range(1, self.tile_sets+1):
            for number in range(1, self.numbers+1):
                for color in range(1, self.colors+1):
                    tiles[color].append(number)
        for joker in range(1, self.jokers+1):
            tiles['jokers'].append(joker)
        print(tiles)



sg = SetGenerator()