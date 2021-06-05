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
            self.runs = self.generate_valid_runs()
            self.groups = self.generate_valid_groups()
            self.sets = set()
            #self.generate_sets()

    def generate_tiles(self):
        tiles = defaultdict(list)
        for tile_set in range(1, self.tile_sets+1):
            for number in range(1, self.numbers+1):
                for color in range(1, self.colors+1):
                    tiles[f'{color}_{tile_set}'].append(number)
        for joker in range(1, self.jokers+1):
            tiles['jokers'].append(joker)
        return tiles

    def generate_valid_groups(self):
        groups = []
        for i in range(1,14):
            groups.append((i,i,i))
            groups.append((i,i,i,i))
        return groups

    def generate_valid_runs(self):
        runs = []
        for value in self.tiles.values():
            for i in range(3, 14):
                for item in itertools.combinations(value, i):
                    all_1_diff = True
                    for j in range(1, len(item)):
                        if item[j] - item[j-1] != 1:
                            all_1_diff = False
                    if all_1_diff:
                        runs.append(item)
        return runs


    def generate_possible_sets(self):
        print('hoi')




sg = SetGenerator()
runs = sg.generate_valid_groups()
groups = sg.generate_valid_runs()

print(runs)
print(groups)