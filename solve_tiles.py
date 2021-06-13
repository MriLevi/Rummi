import itertools
from set_generator import SetGenerator
from collections import defaultdict


class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']


    def sort_defaultdict(self, dict):
        for key, value in dict.items():
            newvalue=sorted(value)
            dict[key] = newvalue
        return dict

    def solve_tiles(self, board, rack):
        sg = SetGenerator()
        runs = defaultdict(list)  # generate a default dict with lists as values
        sorted_rack = self.sort_defaultdict(rack)
        print(f'sorted rack: {sorted_rack}')
        runs = sg.generate_valid_runs(rack)
        groups = sg.generate_valid_groups(rack)
        print(f'found runs: {runs}')
        print(f'found groups: {groups}')
        return runs, rack, board

    def points(self, possiblesolution):
        points = 0
        for tile in possiblesolution:
            points += tile[0]
        print(points)
        return points
