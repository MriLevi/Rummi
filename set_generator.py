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
            self.runs = self.generate_valid_runs(self.tiles)
            self.groups = self.generate_valid_groups(self.tiles)
            self.sets = self.generate_possible_sets()

            #self.generate_sets()

    def generate_tiles(self):
        tiles = defaultdict(list)
        colorkey = {1:'red', 2:'yellow', 3:'cyan', 4:'black'}
        for tile_set in range(1, self.tile_sets+1): #for every tile set
            for number in range(1, self.numbers+1): #for every number in the tile set
                for color in range(1, self.colors+1): #for every color in colors
                    tiles[f'{colorkey[color]}'].append(number) #add every number to the corresponding key
        for joker in range(1, self.jokers+1):
            tiles['jokers'].append(f'j{joker}') #add the jokers
        return tiles

    def generate_valid_groups(self, tiles):
        #generate valid groups
        tempgroups = defaultdict(list)
        groups = defaultdict(list)
        for key, value in tiles.items():
            for tile in value:
                if [key, tile] not in tempgroups[tile]:
                    tempgroups[tile].append([key, tile])
                for i in range(3,5):
                    for item in itertools.combinations(tempgroups[tile], i):
                        if item not in groups[item[0][1]]:
                            groups[item[0][1]].append(item)
        return groups

    def generate_valid_runs(self, tiles):
        # generate valid runs
        runs = defaultdict(list)  # generate a default dict with lists as values
        joker = len(tiles['jokers'])
        for key, value in tiles.items():  # for every color and tile value
            for i in range(2, 14):  # for the run lengths 3-14
                for item in itertools.combinations(value[:13], i):  # for every combination of tiles with length i
                    sum = 0
                    save_index = None
                    save_index_2 = None
                    two_gap_index = None
                    for j in reversed(range(1, len(item))):
                        try:
                            currentcalculation = item[j] - item[j - 1]
                        except TypeError: #skip the combination of 2 jokers...
                            continue
                        sum += currentcalculation
                        if currentcalculation == 2:
                            if save_index == None:
                                save_index = j
                            else:
                                save_index_2 = j
                        if currentcalculation == 3:
                            two_gap_index = j

                    if sum == len(item) - 1 and len(item) > 2:  # no jokers needed
                        tempitem = list(item)
                        if len(set(tempitem)) == len(tempitem): #check if all elements are unique
                            if tempitem not in runs[key]:
                                runs[key].append(tempitem)
                    if sum == len(item) and joker >= 1:
                        tempitem = list(item)
                        if len(set(tempitem)) == len(tempitem):
                            tempitem.insert(save_index, tiles['jokers'][0])
                            if tempitem not in runs[key]:
                                runs[key].append(tempitem)
                    if sum == len(item) + 1 and joker == 2:
                        tempitem = list(item)
                        if len(set(tempitem)) == len(tempitem):
                            if two_gap_index == None:
                                tempitem.insert(save_index, tiles['jokers'][0])
                                tempitem.insert(save_index_2, tiles['jokers'][1])
                            else:
                                tempitem.insert(two_gap_index, tiles['jokers'][1])
                                tempitem.insert(two_gap_index, tiles['jokers'][0])
                            if tempitem not in runs[key]:
                                runs[key].append(tempitem)
        return runs


    def generate_possible_sets(self):
        #combine runs and groups to form a list of possible sets
        sets = defaultdict(list)
        sets['runs'].append(self.runs)
        sets['groups'].append(self.groups)
        print(sets)
        return sets
sg = SetGenerator()