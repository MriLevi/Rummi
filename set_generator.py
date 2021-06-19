import itertools
import numpy as np
from collections import defaultdict

class SetGenerator:

    def __init__(self, numbers=13, colors=4, jokers=2, combi_len=3, tile_sets=2, minimal_startscore=30):
            self.numbers = numbers
            self.colors = colors
            self.jokers = jokers
            self.combi_len = combi_len
            self.tile_sets = tile_sets
            self.tiles = self.generate_tiles()
            self.tilecount = (colors*numbers)+jokers
            self.minimal_startscore = minimal_startscore

            #self.generate_sets()

    def generate_tiles(self):
        tiles = []
        for tileset in range(1, self.tile_sets+1):
            for color in range(1, self.colors+1):
                for tilenumber in range(1, self.numbers+1):
                    tiles.append((color, tilenumber))
        for joker in range(1, self.jokers+1):
            tiles.append((5, f'j{joker}'))
        return tiles