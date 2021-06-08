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
            self.sets = self.generate_possible_sets()
            #self.generate_sets()

    def generate_tiles(self):
        tiles = defaultdict(list)
        colorkey = {1:'red', 2:'yellow', 3:'blue', 4:'black'}
        for tile_set in range(1, self.tile_sets+1): #for every tile set
            for number in range(1, self.numbers+1): #for every number in the tile set
                for color in range(1, self.colors+1): #for every color in colors
                    tiles[f'{colorkey[color]}_{tile_set}'].append(number) #add every number to the corresponding key
        for joker in range(1, self.jokers+1):
            tiles['jokers'].append(joker) #add the jokers
        return tiles

    def generate_valid_groups(self):
        #generate valid groups
        groups = [tuple([i for j in range(j)]) for i in range(1, self.numbers+1) for j in range(3, self.colors+1)]
        return groups

    def generate_valid_runs(self):
        #generate valid runs
        runs = defaultdict(list) #generate a default dict with lists as values
        for key, value in self.tiles.items(): #for every color and tile value
            for i in range(3, 14): #for the run lengths 3-14
                for item in itertools.combinations(value, i): #for every combination of tiles with length i
                    all_1_diff = True #check if the values in the combination have a difference of one with their neighbours
                    for j in range(1, len(item)):
                        if item[j] - item[j-1] != 1:
                            all_1_diff = False
                    if all_1_diff: #if all values have a difference of 1, append them as a valid run
                        runs[key[0]].append(item)
        return runs


    def generate_possible_sets(self):
        #combine runs and groups to form a list of possible sets
        sets = defaultdict(list)
        sets['runs'].append(self.generate_valid_runs())
        sets['groups'].append(self.generate_valid_groups())
        return sets